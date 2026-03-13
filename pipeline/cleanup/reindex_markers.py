"""
reindex_markers.py — Regenerate footnote marker JSON from validated Markdown.

Useful when markers were missed in initial Docling extraction or when
chapter boundaries were shifted manually.

Modes:
  (default)        Scan scripture .md for dagger/omega markers
  --from-footnotes Rebuild markers from *_footnotes.md anchor lines
  --all-ot         Iterate all OT books (requires --from-footnotes)
  --all-nt         Iterate all NT books (requires --from-footnotes)
  --force          Rebuild even if marker anchors already align
  --dry-run        Report what would change without writing files
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import date

# ── Repo-root bootstrap ──────────────────────────────────────────────────────
_R = Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists():
    _R = _R.parent
if str(_R) not in sys.path:
    sys.path.insert(0, str(_R))

from pipeline.common.paths import STAGING_ROOT, REGISTRY_PATH
from pipeline.common.registry import load_registry, book_testament

# ── Regex patterns ────────────────────────────────────────────────────────────
FOOTNOTE_ANCHOR_RE = re.compile(r'\(anchor: ([A-Z0-9]+\.\d+:\d+)\)')
ANCHOR_PARTS_RE = re.compile(r'^([A-Z0-9]+)\.(\d+):(\d+)$')


def _anchor_sort_key(anchor: str) -> tuple[int, int]:
    """Return (chapter, verse) for canonical ordering."""
    m = ANCHOR_PARTS_RE.match(anchor)
    if not m:
        return (0, 0)
    return (int(m.group(2)), int(m.group(3)))


# ── Original mode: extract markers from scripture MD ──────────────────────────

def extract_markers_from_md(md_path: Path) -> list[dict]:
    content = md_path.read_text(encoding="utf-8")
    book_code = md_path.stem

    # Markers to find
    MARKERS = ["\u2020\u03c9", "\u2020", "\u03c9"]

    markers = []
    marker_seq_book = 0

    lines = content.splitlines()
    for line in lines:
        # Match verse: BOOK.CH:V Text
        m = re.match(r"^([A-Z0-9]{2,4})\.(\d+):(\d+)\s+(.*)", line)
        if m:
            b, ch, v, text = m.groups()
            anchor = f"{b}.{ch}:{v}"

            # Find markers in this verse
            # We look for all occurrences
            for marker in MARKERS:
                # We use regex to find the marker, avoiding overlaps (longest first)
                # But actually they are distinct characters.
                # Just find all occurrences of any of the marker strings
                pass

            # Simple approach: check for each marker type
            # Note: order matters if multiple markers in one verse
            # OSB usually has them at the end of phrases.

            # Find all markers in the text
            found = []
            for marker in ["\u2020\u03c9", "\u2020", "\u03c9"]:
                start = 0
                while True:
                    idx = text.find(marker, start)
                    if idx == -1: break
                    found.append((idx, marker))
                    start = idx + len(marker)

            # Sort by position in verse
            found.sort()

            for i, (idx, marker) in enumerate(found, 1):
                marker_seq_book += 1
                markers.append({
                    "marker": marker,
                    "anchor": anchor,
                    "marker_index_in_verse": i,
                    "marker_seq_book": marker_seq_book,
                    # We lose page/excerpt metadata here, but Photius can recover it if needed
                    "source": "reindexed_from_md"
                })

    return markers


# ── New mode: extract markers from footnotes MD ──────────────────────────────

def extract_anchors_from_footnotes(footnotes_path: Path) -> list[str]:
    """Extract unique anchors from a *_footnotes.md file, in canonical order."""
    content = footnotes_path.read_text(encoding="utf-8")
    raw = FOOTNOTE_ANCHOR_RE.findall(content)
    # Deduplicate while preserving first-seen order, then sort canonically
    seen = set()
    unique = []
    for a in raw:
        if a not in seen:
            seen.add(a)
            unique.append(a)
    unique.sort(key=_anchor_sort_key)
    return unique


def build_markers_from_footnotes(anchors: list[str]) -> list[dict]:
    """Build marker entries from footnote anchors."""
    markers = []
    for seq, anchor in enumerate(anchors, 1):
        markers.append({
            "marker": "unknown",
            "anchor": anchor,
            "marker_index_in_verse": 1,
            "marker_seq_book": seq,
            "source": "reindexed_from_footnotes_md"
        })
    return markers


def load_existing_markers(markers_path: Path) -> list[dict]:
    """Load existing marker list from JSON (handles both list and dict formats)."""
    if not markers_path.exists():
        return []
    with open(markers_path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    return data.get("markers", [])


def extract_marker_anchors(markers: list[dict]) -> list[str]:
    """Return unique existing anchors in canonical order."""
    anchors = {
        marker.get("anchor", "")
        for marker in markers
        if isinstance(marker, dict) and marker.get("anchor")
    }
    return sorted(anchors, key=_anchor_sort_key)


def reindex_book_from_footnotes(
    book_code: str,
    testament: str,
    dry_run: bool = False,
    force: bool = False,
) -> dict:
    """Reindex a single book's markers from its footnotes file.

    Returns a status dict with keys: action, book, marker_count, footnote_count, reason.
    """
    staging = STAGING_ROOT / testament
    markers_path = staging / f"{book_code}_footnote_markers.json"
    footnotes_path = staging / f"{book_code}_footnotes.md"

    result = {"book": book_code, "testament": testament}

    # Check footnotes file exists
    if not footnotes_path.exists():
        result.update(action="skip", reason="no_footnotes_file",
                      marker_count=0, footnote_count=0)
        return result

    # Extract counts and anchor sets
    footnote_anchors = extract_anchors_from_footnotes(footnotes_path)
    existing_markers = load_existing_markers(markers_path)
    existing_anchors = extract_marker_anchors(existing_markers)
    m_count = len(existing_markers)
    f_count = len(footnote_anchors)
    aligned = existing_anchors == footnote_anchors

    result["marker_count"] = m_count
    result["footnote_count"] = f_count
    result["marker_anchor_count"] = len(existing_anchors)
    result["aligned"] = aligned

    # Skip only when the actual anchor sets already align and force is not set.
    if aligned and not force:
        result.update(action="skip", reason="markers_adequate")
        return result

    # Without --force, skip only when markers strictly exceed footnotes and the
    # anchors are not aligned. Equal-count mismatches should still rebuild.
    if not force and f_count < m_count:
        result.update(action="skip", reason="markers_exceed_footnotes")
        return result

    if dry_run:
        result.update(
            action="would_reindex",
            delta=f_count - m_count,
            anchor_delta=len(footnote_anchors) - len(existing_anchors),
        )
        return result

    # Build new markers
    new_markers = build_markers_from_footnotes(footnote_anchors)

    # Preserve original markers as audit trail
    original_markers_snapshot = existing_markers.copy() if existing_markers else []

    data = {
        "book_code": book_code,
        "reindex_date": str(date.today()),
        "marker_count": len(new_markers),
        "markers": new_markers,
    }
    if original_markers_snapshot:
        data["original_markers"] = original_markers_snapshot

    with open(markers_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    result.update(
        action="reindexed",
        delta=f_count - m_count,
        anchor_delta=len(footnote_anchors) - len(existing_anchors),
    )
    return result


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Reindex footnote markers from MD (scripture or footnotes)")
    parser.add_argument("md_file", nargs="?", type=Path, default=None,
                        help="Path to BOOK.md (original mode)")
    parser.add_argument("--from-footnotes", action="store_true",
                        help="Rebuild markers from *_footnotes.md anchors")
    parser.add_argument("--all-ot", action="store_true",
                        help="Iterate all OT books (requires --from-footnotes)")
    parser.add_argument("--all-nt", action="store_true",
                        help="Iterate all NT books (requires --from-footnotes)")
    parser.add_argument("--book", type=str, default=None,
                        help="Single book code to reindex (with --from-footnotes)")
    parser.add_argument("--force", action="store_true",
                        help="Rebuild even if marker anchors already align")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report what would change without writing")
    args = parser.parse_args()

    # ── --from-footnotes mode ─────────────────────────────────────────────
    if args.from_footnotes:
        registry = load_registry(REGISTRY_PATH)

        if args.all_ot and args.all_nt:
            all_books = [b["code"] for b in registry["books"]]
            skip_set = {"PSA"}
            books = [c for c in all_books if c not in skip_set]
        elif args.all_ot:
            ot_books = [b["code"] for b in registry["books"]
                        if b.get("testament") == "OT"]
            skip_set = {"PSA"}
            books = [c for c in ot_books if c not in skip_set]
        elif args.all_nt:
            books = [b["code"] for b in registry["books"]
                     if b.get("testament") == "NT"]
        elif args.book:
            books = [args.book]
        else:
            parser.error("--from-footnotes requires --all-ot, --all-nt, or --book BOOK")
            return

        reindexed = []
        skipped = []
        for code in books:
            testament = book_testament(registry, code)
            if testament is None:
                skipped.append({"book": code, "action": "skip",
                                "reason": "unknown_testament"})
                continue
            result = reindex_book_from_footnotes(code, testament,
                                                 dry_run=args.dry_run,
                                                 force=args.force)
            if result["action"] in ("reindexed", "would_reindex"):
                reindexed.append(result)
            else:
                skipped.append(result)

        # Report
        tag = "[dry-run]" if args.dry_run else "[reindex]"
        if reindexed:
            print(f"{tag} {'Would reindex' if args.dry_run else 'Reindexed'} "
                  f"{len(reindexed)} book(s):")
            for r in reindexed:
                print(f"  {r['book']:4s}  markers {r['marker_count']:3d} -> "
                      f"{r['footnote_count']:3d}  (+{r['delta']})")
        else:
            print(f"{tag} No books to reindex.")

        if skipped:
            print(f"\n{tag} Skipped {len(skipped)} book(s):")
            for s in skipped:
                reason = s.get("reason", "unknown")
                m = s.get("marker_count", "?")
                f = s.get("footnote_count", "?")
                print(f"  {s['book']:4s}  markers={m} footnotes={f}  ({reason})")

        total_new = sum(r["footnote_count"] for r in reindexed)
        total_old = sum(r["marker_count"] for r in reindexed)
        print(f"\n{tag} Total: {total_old} -> {total_new} markers "
              f"across {len(reindexed)} book(s)")
        return

    # ── Original mode (positional md_file) ────────────────────────────────
    if args.md_file is None:
        parser.error("Provide md_file or use --from-footnotes")
        return

    if not args.md_file.exists():
        print(f"Error: {args.md_file} not found")
        return

    markers = extract_markers_from_md(args.md_file)

    out_path = args.md_file.parent / f"{args.md_file.stem}_footnote_markers.json"

    data = {
        "book_code": args.md_file.stem,
        "reindex_date": str(date.today()),
        "marker_count": len(markers),
        "markers": markers
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[reindex] Found {len(markers)} markers in {args.md_file.name}")
    print(f"[reindex] Updated {out_path.name}")

if __name__ == "__main__":
    main()
