"""
enrich_backlink_shards.py — Enrich v1 backlink shards with verse text,
pericope context, topic threads, and depth metadata to produce v2 shards.

Usage:
    python3 pipeline/graph/enrich_backlink_shards.py [--domain study] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from pipeline.common.paths import CANON_ROOT, METADATA_ROOT, STUDY_ROOT
from pipeline.graph.build_backlinks import BACKLINKS_ROOT

PERICOPE_INDEX_DIR = METADATA_ROOT / "pericope_index"
ANCHOR_RE = re.compile(r"^([A-Z0-9]+\.\d+:\d+)\s+(.*)")


# ── Canon verse loader ──────────────────────────────────────────────────────

def load_canon_verses() -> dict[str, str]:
    """Parse all canon files into {anchor_id: verse_text}."""
    verses: dict[str, str] = {}
    for testament_dir in sorted(CANON_ROOT.iterdir()):
        if not testament_dir.is_dir():
            continue
        for canon_file in sorted(testament_dir.glob("*.md")):
            for line in canon_file.read_text(encoding="utf-8").splitlines():
                m = ANCHOR_RE.match(line)
                if m:
                    verses[m.group(1)] = m.group(2)
    return verses


# ── Pericope index loader ───────────────────────────────────────────────────

def _parse_anchor_parts(anchor: str) -> tuple[str, int, int]:
    """Parse 'GEN.1:1' into ('GEN', 1, 1)."""
    book, rest = anchor.split(".", 1)
    ch, v = rest.split(":", 1)
    return book, int(ch), int(v)


def _anchor_key(anchor: str) -> tuple[str, int, int]:
    return _parse_anchor_parts(anchor)


class PericopeInfo:
    __slots__ = ("id", "title", "range", "liturgical_use")

    def __init__(self, pid: str, title: str, prange: str, liturgical_use: list[str]):
        self.id = pid
        self.title = title
        self.range = prange
        self.liturgical_use = liturgical_use

    def to_dict(self) -> dict:
        result: dict = {"id": self.id, "title": self.title, "range": self.range}
        if self.liturgical_use:
            result["liturgical_use"] = self.liturgical_use
        else:
            result["liturgical_use"] = []
        return result


def load_pericope_reverse_map() -> dict[str, PericopeInfo]:
    """Build anchor_id → PericopeInfo reverse map from all pericope index files."""
    reverse: dict[str, PericopeInfo] = {}
    if not PERICOPE_INDEX_DIR.exists():
        return reverse

    for idx_file in sorted(PERICOPE_INDEX_DIR.glob("*.json")):
        data = json.loads(idx_file.read_text(encoding="utf-8"))
        book_code = data.get("book_code", idx_file.stem)
        pericopes = data.get("pericopes", [])
        for i, peri in enumerate(pericopes, start=1):
            pid = f"{book_code}.P{i:03d}"
            start = peri["start_anchor"]
            end = peri["end_anchor"]
            title = peri.get("title", "")
            liturgical = peri.get("liturgical_context") or []
            if isinstance(liturgical, str):
                liturgical = [liturgical] if liturgical else []
            prange = f"{start}-{end.split('.', 1)[1]}" if start.split('.')[0] == end.split('.')[0] else f"{start}-{end}"
            info = PericopeInfo(pid, title, prange, liturgical)

            # Map all anchors in range to this pericope
            start_book, start_ch, start_v = _parse_anchor_parts(start)
            end_book, end_ch, end_v = _parse_anchor_parts(end)
            # Only handle same-book pericopes (all ours are)
            if start_book != end_book:
                continue
            for ch in range(start_ch, end_ch + 1):
                v_start = start_v if ch == start_ch else 1
                v_end = end_v if ch == end_ch else 200  # generous upper bound
                for v in range(v_start, v_end + 1):
                    aid = f"{start_book}.{ch}:{v}"
                    if aid not in reverse:
                        reverse[aid] = info
    return reverse


# ── Depth computation ───────────────────────────────────────────────────────

def _study_footnote_files() -> set[str]:
    """Return set of book codes that have non-empty footnote files."""
    codes: set[str] = set()
    for testament in ("OT", "NT"):
        fn_dir = STUDY_ROOT / "footnotes" / testament
        if not fn_dir.exists():
            continue
        for f in fn_dir.glob("*_footnotes.md"):
            code = f.stem.replace("_footnotes", "")
            # Check non-empty (more than frontmatter)
            text = f.read_text(encoding="utf-8")
            content_lines = [l for l in text.splitlines()
                             if l.strip() and not l.startswith("---")
                             and not l.startswith("book_code:")
                             and not l.startswith("canon_anchors")]
            if len(content_lines) > 5:
                codes.add(code)
    return codes


def _study_article_files() -> set[str]:
    """Return set of book codes that have non-placeholder article files."""
    codes: set[str] = set()
    for testament in ("OT", "NT"):
        art_dir = STUDY_ROOT / "articles" / testament
        if not art_dir.exists():
            continue
        for f in art_dir.glob("*_articles.md"):
            code = f.stem.replace("_articles", "")
            text = f.read_text(encoding="utf-8")
            if "(No study articles extracted" not in text:
                codes.add(code)
    return codes


def compute_depth(anchor_id: str, footnote_books: set[str], article_books: set[str]) -> int:
    """Compute depth_available for an anchor.

    1 = verse text only
    2 = + footnote/article available
    3 = + graph neighborhood (always true for shards — they have links)
    4 = + patristic (not yet populated)
    """
    book = anchor_id.split(".", 1)[0]
    has_study = book in footnote_books or book in article_books
    # All shards by definition have links (that's why they exist), so if study
    # material exists, depth is at least 3 (verse + study + graph neighborhood).
    # Depth 4 (patristic) is not yet available.
    if has_study:
        return 3
    return 1  # verse text only, but shard has links → still just depth 1 for study content


# ── Enrichment engine ───────────────────────────────────────────────────────

def enrich_shard(
    shard: dict,
    verses: dict[str, str],
    pericope_map: dict[str, PericopeInfo],
    footnote_books: set[str],
    article_books: set[str],
) -> dict:
    """Enrich a v1 shard to v2 format. Returns a new dict."""
    anchor_id = shard["anchor_id"]
    enriched = {
        "anchor_id": anchor_id,
        "canon_uri": shard["canon_uri"],
        "text_tradition": shard.get("text_tradition", "LXX"),
        "generated_at": shard["generated_at"],
        "generator_version": shard["generator_version"],
        "schema_version": "v2",
        "verse_text": verses.get(anchor_id, ""),
        "pericope": None,
        "topic_threads": [],
        "depth_available": compute_depth(anchor_id, footnote_books, article_books),
        "links": shard["links"],
    }
    peri = pericope_map.get(anchor_id)
    if peri:
        enriched["pericope"] = peri.to_dict()
    return enriched


def enrich_domain(
    domain: str,
    backlinks_root: Path,
    verses: dict[str, str],
    pericope_map: dict[str, PericopeInfo],
    footnote_books: set[str],
    article_books: set[str],
    dry_run: bool = False,
) -> tuple[int, int, int]:
    """Enrich all shards in a domain. Returns (total, enriched, skipped)."""
    domain_dir = backlinks_root / domain
    if not domain_dir.exists():
        return 0, 0, 0

    shard_files = sorted(domain_dir.glob("*.json"))
    total = len(shard_files)
    enriched_count = 0
    skipped = 0

    for shard_path in shard_files:
        shard = json.loads(shard_path.read_text(encoding="utf-8"))

        # Skip already-enriched shards (idempotent)
        if shard.get("schema_version") == "v2":
            skipped += 1
            continue

        enriched = enrich_shard(shard, verses, pericope_map, footnote_books, article_books)

        if not dry_run:
            shard_path.write_text(json.dumps(enriched, indent=2) + "\n", encoding="utf-8")

        enriched_count += 1

    return total, enriched_count, skipped


# ── CLI ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Enrich v1 backlink shards to v2 with verse text, pericope, and depth metadata."
    )
    parser.add_argument(
        "--domain",
        default="study",
        help="Domain to enrich (default: study)",
    )
    parser.add_argument(
        "--backlinks-root",
        type=Path,
        default=BACKLINKS_ROOT,
    )
    parser.add_argument("--dry-run", action="store_true", help="Report what would be enriched without writing")
    args = parser.parse_args()

    print("Loading canon verses...", file=sys.stderr)
    verses = load_canon_verses()
    print(f"  {len(verses):,} verses loaded", file=sys.stderr)

    print("Loading pericope index...", file=sys.stderr)
    pericope_map = load_pericope_reverse_map()
    print(f"  {len(pericope_map):,} anchors mapped to pericopes", file=sys.stderr)

    print("Scanning study layer...", file=sys.stderr)
    footnote_books = _study_footnote_files()
    article_books = _study_article_files()
    print(f"  {len(footnote_books)} books with footnotes, {len(article_books)} books with articles", file=sys.stderr)

    prefix = "[dry-run] " if args.dry_run else ""
    print(f"\n{prefix}Enriching domain: {args.domain}", file=sys.stderr)

    total, enriched, skipped = enrich_domain(
        args.domain,
        args.backlinks_root,
        verses,
        pericope_map,
        footnote_books,
        article_books,
        dry_run=args.dry_run,
    )

    print(f"\n{prefix}Results:", file=sys.stderr)
    print(f"  Total shards:    {total:,}", file=sys.stderr)
    print(f"  Enriched:        {enriched:,}", file=sys.stderr)
    print(f"  Already v2:      {skipped:,}", file=sys.stderr)

    # Spot-check output
    if not args.dry_run and enriched > 0:
        spot_anchors = ["GEN.1:1", "PSA.50:1", "JOH.1:1", "ROM.5:12", "REV.1:1"]
        print(f"\nSpot-check ({len(spot_anchors)} anchors):", file=sys.stderr)
        domain_dir = args.backlinks_root / args.domain
        for anchor in spot_anchors:
            book, rest = anchor.split(".", 1)
            ch, v = rest.split(":", 1)
            fname = f"{book}.{ch}-{v}.json"
            fpath = domain_dir / fname
            if fpath.exists():
                s = json.loads(fpath.read_text(encoding="utf-8"))
                vt = s.get("verse_text", "")[:80]
                peri = s.get("pericope", {})
                pid = peri.get("id", "none") if peri else "none"
                depth = s.get("depth_available", "?")
                sv = s.get("schema_version", "?")
                print(f"  {anchor}: sv={sv} depth={depth} peri={pid} text={vt!r}...", file=sys.stderr)
            else:
                print(f"  {anchor}: no shard in {args.domain} domain", file=sys.stderr)

    # Summary JSON to stdout
    summary = {
        "domain": args.domain,
        "dry_run": args.dry_run,
        "total_shards": total,
        "enriched": enriched,
        "already_v2": skipped,
        "canon_verses_loaded": len(verses),
        "pericope_anchors_mapped": len(pericope_map),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
