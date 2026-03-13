#!/usr/bin/env python3
"""
unify_marker_schema.py — Convert bare-list marker JSON files to the dict format.

Dict format (target):
    {"book_code": CODE, "reindex_date": "2026-03-13",
     "marker_count": N, "markers": [...]}

Bare-list format (source):
    [{"anchor": "MAT.1:1", "marker": "†"}, ...]

Usage:
    python3 pipeline/cleanup/unify_marker_schema.py           # dry-run (default)
    python3 pipeline/cleanup/unify_marker_schema.py --dry-run # explicit dry-run
    python3 pipeline/cleanup/unify_marker_schema.py --apply   # write changes
"""
from __future__ import annotations

import argparse
import json

import sys as _sys
from pathlib import Path as _Path

_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists():
    _R = _R.parent
if str(_R) not in _sys.path:
    _sys.path.insert(0, str(_R))

from pipeline.common.paths import STAGING_ROOT

REINDEX_DATE = "2026-03-13"


def _book_code_from_filename(path: _Path) -> str:
    """Extract book code from filename stem, e.g. 'MAT_footnote_markers' -> 'MAT'."""
    return path.stem.split("_")[0]


def _convert_bare_list(markers: list[dict], book_code: str) -> dict:
    """Wrap a bare marker list into the canonical dict format."""
    anchor_counts: dict[str, int] = {}
    enriched: list[dict] = []

    for seq, m in enumerate(markers, start=1):
        anchor = m["anchor"]
        anchor_counts[anchor] = anchor_counts.get(anchor, 0) + 1

        enriched.append({
            "marker": m["marker"],
            "anchor": anchor,
            "marker_index_in_verse": anchor_counts[anchor],
            "marker_seq_book": seq,
            "source": "migrated_from_bare_list",
        })

    return {
        "book_code": book_code,
        "reindex_date": REINDEX_DATE,
        "marker_count": len(enriched),
        "markers": enriched,
    }


def process_file(path: _Path, *, apply: bool) -> str | None:
    """Process a single marker file. Returns a status message or None if skipped."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    # Already in dict format
    if isinstance(data, dict) and "markers" in data:
        return None

    if not isinstance(data, list):
        return f"  WARN  {path.name}: unexpected JSON type {type(data).__name__}, skipping"

    # Derive book_code: prefer first marker's anchor, fall back to filename
    if data and "anchor" in data[0]:
        book_code = data[0]["anchor"].split(".")[0]
    else:
        book_code = _book_code_from_filename(path)

    converted = _convert_bare_list(data, book_code)

    if apply:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(converted, f, indent=2, ensure_ascii=False)
            f.write("\n")
        return f"  WROTE {path.name}: {converted['marker_count']} markers"
    else:
        return f"  WOULD {path.name}: {converted['marker_count']} markers"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Unify footnote-marker JSON files to dict format."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry-run", action="store_true", default=True,
                       help="Report which files would change (default)")
    group.add_argument("--apply", action="store_true",
                       help="Write changes to disk")
    args = parser.parse_args()

    apply = args.apply

    marker_files = sorted(STAGING_ROOT.glob("*/*_footnote_markers.json"))

    changed = 0
    skipped = 0

    mode = "APPLY" if apply else "DRY-RUN"
    print(f"unify_marker_schema [{mode}]  scanning {len(marker_files)} files\n")

    for mf in marker_files:
        result = process_file(mf, apply=apply)
        if result is None:
            skipped += 1
        else:
            print(result)
            changed += 1

    print(f"\n  total: {changed} converted, {skipped} already in dict format")


if __name__ == "__main__":
    main()
