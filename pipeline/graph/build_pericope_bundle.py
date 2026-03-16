"""
build_pericope_bundle.py — Layer 3 pericope bundle builder.

Assembles on-demand context packages from enriched backlink shards,
canon text, study footnotes, and study articles for a given pericope.

Usage:
    python3 pipeline/graph/build_pericope_bundle.py GEN.P001 [--preset devotional] [--output-dir research/bundle_pilot]
    python3 pipeline/graph/build_pericope_bundle.py GEN.P001 --all-presets --output-dir research/bundle_pilot
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path

from pipeline.common.paths import CANON_ROOT, METADATA_ROOT, STUDY_ROOT
from pipeline.graph.build_backlinks import BACKLINKS_ROOT

PERICOPE_INDEX_DIR = METADATA_ROOT / "pericope_index"
ANCHOR_RE = re.compile(r"^([A-Z0-9]+\.\d+:\d+)\s+(.*)")
FOOTNOTE_HEADING_RE = re.compile(r"^###\s+(\d+):(\d+)(?:-(\d+))?")
ARTICLE_PLACEMENT_RE = re.compile(r"\*\(after\s+([A-Z0-9]+\.\d+:\d+)\)\*")


# ── Presets ─────────────────────────────────────────────────────────────────

PRESETS = {
    "quick":      {"depth": 1, "token_budget": 1_000,  "max_cross_refs": 4},
    "devotional": {"depth": 2, "token_budget": 4_000,  "max_cross_refs": 12},
    "study":      {"depth": 3, "token_budget": 8_000,  "max_cross_refs": 24},
    "phronema":   {"depth": 4, "token_budget": 16_000, "max_cross_refs": 50},
}


# ── Data classes ────────────────────────────────────────────────────────────

@dataclass
class CrossReference:
    anchor: str
    verse_text: str
    pericope: dict | None
    topic_threads: list[str]
    source_context: str
    depth_available: int

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PericopeBundle:
    pericope_id: str
    title: str
    range: str
    preset: str
    depth: int
    canon_text: str
    footnotes: str
    article_sections: str
    cross_references: list[dict]
    token_estimate: int
    token_budget: int
    built_at: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


# ── Helpers ─────────────────────────────────────────────────────────────────

def _estimate_tokens(text: str) -> int:
    """Rough token estimate: word count * 1.3."""
    return int(len(text.split()) * 1.3)


def _parse_anchor(anchor: str) -> tuple[str, int, int]:
    book, rest = anchor.split(".", 1)
    ch, v = rest.split(":", 1)
    return book, int(ch), int(v)


def _anchor_in_range(anchor: str, start: str, end: str) -> bool:
    """Check if anchor is within [start, end] inclusive."""
    a_book, a_ch, a_v = _parse_anchor(anchor)
    s_book, s_ch, s_v = _parse_anchor(start)
    e_book, e_ch, e_v = _parse_anchor(end)
    if a_book != s_book:
        return False
    if a_ch < s_ch or a_ch > e_ch:
        return False
    if a_ch == s_ch and a_v < s_v:
        return False
    if a_ch == e_ch and a_v > e_v:
        return False
    return True


# ── Canon text extraction ───────────────────────────────────────────────────

def extract_canon_text(book_code: str, start: str, end: str) -> str:
    """Extract canon text for a verse range, one verse per line."""
    lines: list[str] = []
    for canon_file in sorted(CANON_ROOT.glob(f"*/*_{book_code}.md")) or sorted(CANON_ROOT.glob(f"*/{book_code}.md")):
        for line in canon_file.read_text(encoding="utf-8").splitlines():
            m = ANCHOR_RE.match(line)
            if m and _anchor_in_range(m.group(1), start, end):
                lines.append(line)
    return "\n".join(lines)


# ── Footnote extraction ────────────────────────────────────────────────────

def extract_footnotes(book_code: str, start: str, end: str) -> str:
    """Extract footnote sections for verses in the given range."""
    testament = _find_testament(book_code)
    fn_path = STUDY_ROOT / "footnotes" / testament / f"{book_code}_footnotes.md"
    if not fn_path.exists():
        return ""

    text = fn_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    sections: list[str] = []
    capturing = False
    current_section: list[str] = []
    current_chapter = 0

    for line in lines:
        # Track chapter headings
        ch_match = re.match(r"^##\s+Chapter\s+(\d+)", line)
        if ch_match:
            current_chapter = int(ch_match.group(1))

        heading_match = FOOTNOTE_HEADING_RE.match(line)
        if heading_match:
            # Flush previous section if capturing
            if capturing and current_section:
                sections.append("\n".join(current_section))
                current_section = []

            ch = int(heading_match.group(1))
            v_start = int(heading_match.group(2))
            v_end = int(heading_match.group(3)) if heading_match.group(3) else v_start

            # Check if any verse in this footnote range overlaps the target range
            capturing = False
            for v in range(v_start, v_end + 1):
                test_anchor = f"{book_code}.{ch}:{v}"
                if _anchor_in_range(test_anchor, start, end):
                    capturing = True
                    break

            if capturing:
                current_section = [line]
        elif capturing:
            current_section.append(line)

    if capturing and current_section:
        sections.append("\n".join(current_section))

    return "\n\n".join(sections)


# ── Article extraction ──────────────────────────────────────────────────────

def extract_articles(book_code: str, start: str, end: str) -> str:
    """Extract article sections relevant to the verse range."""
    testament = _find_testament(book_code)
    art_path = STUDY_ROOT / "articles" / testament / f"{book_code}_articles.md"
    if not art_path.exists():
        return ""

    text = art_path.read_text(encoding="utf-8")
    if "(No study articles extracted" in text:
        return ""

    lines = text.splitlines()
    sections: list[str] = []
    current_section: list[str] = []
    section_anchor: str | None = None
    in_section = False

    for line in lines:
        # New article section
        if line.startswith("### "):
            # Flush previous
            if in_section and section_anchor and current_section:
                if _anchor_in_range(section_anchor, start, end):
                    sections.append("\n".join(current_section))
            current_section = [line]
            section_anchor = None
            in_section = True
            continue

        if in_section:
            current_section.append(line)
            # Check for placement marker
            pm = ARTICLE_PLACEMENT_RE.search(line)
            if pm and section_anchor is None:
                section_anchor = pm.group(1)

    # Flush last section
    if in_section and section_anchor and current_section:
        if _anchor_in_range(section_anchor, start, end):
            sections.append("\n".join(current_section))

    return "\n\n".join(sections)


# ── Cross-reference resolution ──────────────────────────────────────────────

def resolve_cross_references(
    book_code: str,
    start: str,
    end: str,
    max_refs: int,
    depth: int,
) -> list[CrossReference]:
    """Find enriched backlink shards for anchors in the range, collect unique cross-refs."""
    # Collect all wikilinks FROM the footnotes/articles in the range
    # by scanning the backlink shards for anchors IN the range
    seen_targets: set[str] = set()
    cross_refs: list[CrossReference] = []

    # Strategy: load shards for anchors in this pericope's range,
    # then look at what they link FROM (source files reference them).
    # But we actually want outgoing links from this pericope — the wikilinks
    # that appear in footnotes/articles for these verses.
    #
    # Better approach: scan enriched shards across the domain to find those
    # whose links[] contain source references from our book's footnotes/articles
    # pointing to anchors OUTSIDE our range.
    #
    # Most efficient: scan the book's footnotes/articles for wikilinks,
    # then look up the target shards for enriched data.

    testament = _find_testament(book_code)
    wikilink_re = re.compile(r"\[\[([A-Z0-9]+\.\d+:\d+)\]\]")

    # Collect outgoing wikilinks from footnotes in range
    targets: list[tuple[str, str]] = []  # (anchor_id, source_context)
    fn_text = extract_footnotes(book_code, start, end)
    for line in fn_text.splitlines():
        for m in wikilink_re.finditer(line):
            target = m.group(1)
            if not _anchor_in_range(target, start, end):
                context_snippet = line.strip()[:120]
                targets.append((target, f"footnote: {context_snippet}"))

    # Also from articles
    art_text = extract_articles(book_code, start, end)
    for line in art_text.splitlines():
        for m in wikilink_re.finditer(line):
            target = m.group(1)
            if not _anchor_in_range(target, start, end):
                context_snippet = line.strip()[:120]
                targets.append((target, f"article: {context_snippet}"))

    # Deduplicate and resolve from enriched shards
    for target_anchor, source_ctx in targets:
        if target_anchor in seen_targets:
            continue
        if len(cross_refs) >= max_refs:
            break
        seen_targets.add(target_anchor)

        # Look up enriched shard
        t_book, t_ch, t_v = _parse_anchor(target_anchor)
        shard_name = f"{t_book}.{t_ch}-{t_v}.json"
        shard_path = BACKLINKS_ROOT / "study" / shard_name
        if shard_path.exists():
            shard = json.loads(shard_path.read_text(encoding="utf-8"))
            cr = CrossReference(
                anchor=target_anchor,
                verse_text=shard.get("verse_text", ""),
                pericope=shard.get("pericope"),
                topic_threads=shard.get("topic_threads", []),
                source_context=source_ctx,
                depth_available=shard.get("depth_available", 1),
            )
        else:
            # No shard — still resolve verse text from canon if possible
            cr = CrossReference(
                anchor=target_anchor,
                verse_text=_resolve_verse_text(target_anchor),
                pericope=None,
                topic_threads=[],
                source_context=source_ctx,
                depth_available=1,
            )
        cross_refs.append(cr)

    return cross_refs


def _resolve_verse_text(anchor: str) -> str:
    """Fallback verse text resolution from canon files."""
    book, ch, v = _parse_anchor(anchor)
    testament = _find_testament(book)
    for canon_file in sorted(CANON_ROOT.glob(f"{testament}/*_{book}.md")) or sorted(CANON_ROOT.glob(f"{testament}/{book}.md")):
        for line in canon_file.read_text(encoding="utf-8").splitlines():
            m = ANCHOR_RE.match(line)
            if m and m.group(1) == anchor:
                return m.group(2)
    return ""


def _find_testament(book_code: str) -> str:
    """Determine testament from canon file location."""
    for testament in ("OT", "NT"):
        matches = list(CANON_ROOT.glob(f"{testament}/*_{book_code}.md"))
        if matches:
            return testament
        matches = list(CANON_ROOT.glob(f"{testament}/{book_code}.md"))
        if matches:
            return testament
    return "OT"  # fallback


# ── Pericope lookup ─────────────────────────────────────────────────────────

def lookup_pericope(pericope_id: str) -> dict | None:
    """Look up a pericope by synthetic ID (e.g. GEN.P001)."""
    book_code = pericope_id.split(".")[0]
    idx_path = PERICOPE_INDEX_DIR / f"{book_code}.json"
    if not idx_path.exists():
        return None

    data = json.loads(idx_path.read_text(encoding="utf-8"))
    # Parse index from ID: BOOK.PNNN -> NNN (1-indexed)
    m = re.match(r"[A-Z0-9]+\.P(\d{3})$", pericope_id)
    if not m:
        return None
    idx = int(m.group(1)) - 1
    pericopes = data.get("pericopes", [])
    if idx < 0 or idx >= len(pericopes):
        return None

    peri = pericopes[idx]
    return {
        "book_code": book_code,
        "title": peri["title"],
        "start_anchor": peri["start_anchor"],
        "end_anchor": peri["end_anchor"],
        "verse_count": peri.get("verse_count", 0),
    }


# ── Bundle builder ──────────────────────────────────────────────────────────

def build_bundle(pericope_id: str, preset: str = "devotional") -> PericopeBundle:
    """Build a complete pericope context bundle."""
    if preset not in PRESETS:
        raise ValueError(f"Unknown preset: {preset!r}. Options: {list(PRESETS)}")

    config = PRESETS[preset]
    depth = config["depth"]
    token_budget = config["token_budget"]
    max_cross_refs = config["max_cross_refs"]

    # 1. Look up pericope
    peri = lookup_pericope(pericope_id)
    if peri is None:
        raise ValueError(f"Pericope {pericope_id!r} not found in index")

    book_code = peri["book_code"]
    start = peri["start_anchor"]
    end = peri["end_anchor"]
    title = peri["title"]
    prange = f"{start}-{end.split('.', 1)[1]}" if start.split('.')[0] == end.split('.')[0] else f"{start}-{end}"

    # 2. Extract canon text (always included)
    canon_text = extract_canon_text(book_code, start, end)

    # 3. Extract footnotes + articles (depth >= 2)
    footnotes = ""
    article_sections = ""
    if depth >= 2:
        footnotes = extract_footnotes(book_code, start, end)
        article_sections = extract_articles(book_code, start, end)

    # 4. Resolve cross-references (depth >= 1 for refs, but content varies by depth)
    cross_refs: list[CrossReference] = []
    if depth >= 1:
        cross_refs = resolve_cross_references(book_code, start, end, max_cross_refs, depth)

    # 5. Apply token budget truncation
    total_text = canon_text
    if depth >= 2:
        total_text += "\n" + footnotes + "\n" + article_sections

    running_tokens = _estimate_tokens(total_text)
    included_refs: list[dict] = []

    for cr in cross_refs:
        ref_dict = cr.to_dict()
        # At depth 1, include only verse text
        if depth == 1:
            ref_dict.pop("pericope", None)
            ref_dict.pop("topic_threads", None)

        ref_tokens = _estimate_tokens(json.dumps(ref_dict))
        if running_tokens + ref_tokens > token_budget:
            break
        running_tokens += ref_tokens
        included_refs.append(ref_dict)

    return PericopeBundle(
        pericope_id=pericope_id,
        title=title,
        range=prange,
        preset=preset,
        depth=depth,
        canon_text=canon_text,
        footnotes=footnotes,
        article_sections=article_sections,
        cross_references=included_refs,
        token_estimate=running_tokens,
        token_budget=token_budget,
        built_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


# ── CLI ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Build a pericope context bundle.")
    parser.add_argument("pericope_id", help="Pericope ID (e.g. GEN.P001)")
    parser.add_argument("--preset", default="devotional", choices=list(PRESETS), help="Phronema preset")
    parser.add_argument("--all-presets", action="store_true", help="Build bundles for all 4 presets")
    parser.add_argument("--output-dir", type=Path, help="Output directory (prints to stdout if omitted)")
    args = parser.parse_args()

    presets_to_run = list(PRESETS) if args.all_presets else [args.preset]
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)

    for preset in presets_to_run:
        print(f"Building {args.pericope_id} @ {preset}...", file=sys.stderr)
        bundle = build_bundle(args.pericope_id, preset=preset)
        bundle_json = json.dumps(bundle.to_dict(), indent=2, ensure_ascii=False)

        if args.output_dir:
            safe_id = args.pericope_id.replace(".", "_")
            out_path = args.output_dir / f"{safe_id}_{preset}.json"
            out_path.write_text(bundle_json + "\n", encoding="utf-8")
            print(f"  Written: {out_path} ({bundle.token_estimate} tokens)", file=sys.stderr)
        else:
            print(bundle_json)

        print(f"  {preset}: {bundle.token_estimate}/{bundle.token_budget} tokens, "
              f"{len(bundle.cross_references)} cross-refs", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
