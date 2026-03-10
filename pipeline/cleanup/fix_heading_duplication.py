"""
fix_heading_duplication.py — Remove duplicated page-header headings from staged books.

Docling sometimes extracts OSB running page headers as section headings,
causing the same heading to appear 5-14 times per book. This script keeps
only the first occurrence of each heading text and removes all subsequent
duplicates.

Usage:
    python3 pipeline/cleanup/fix_heading_duplication.py staging/validated/OT/NEH.md
    python3 pipeline/cleanup/fix_heading_duplication.py staging/validated/OT/NEH.md --dry-run
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path

_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists():
    _R = _R.parent
if str(_R) not in _sys.path:
    _sys.path.insert(0, str(_R))

from pipeline.common.frontmatter import split_frontmatter

RE_HEADING = re.compile(r"^### (.+)$")


def deduplicate_headings(text: str) -> tuple[str, list[str]]:
    """Remove duplicate ### headings, keeping the first occurrence of each.

    Returns (cleaned_text, list_of_removed_headings).
    Preserves frontmatter and ## Chapter headings untouched.
    """
    fm_text, body = split_frontmatter(text)
    lines = body.split("\n")

    seen: set[str] = set()
    removed: list[str] = []
    out_lines: list[str] = []
    skip_blank_after = False

    for line in lines:
        m = RE_HEADING.match(line)
        if m:
            heading_text = m.group(1).strip()
            if heading_text in seen:
                removed.append(heading_text)
                skip_blank_after = True
                continue
            seen.add(heading_text)
            skip_blank_after = False
            out_lines.append(line)
        elif skip_blank_after and line.strip() == "":
            # Skip the blank line that followed a removed heading
            skip_blank_after = False
            continue
        else:
            skip_blank_after = False
            out_lines.append(line)

    cleaned_body = "\n".join(out_lines)
    return fm_text + cleaned_body, removed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remove duplicated page-header headings from staged books."
    )
    parser.add_argument("file", type=Path, help="Path to staged .md file")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without modifying the file",
    )
    args = parser.parse_args()

    if not args.file.exists():
        print(f"File not found: {args.file}")
        raise SystemExit(1)

    text = args.file.read_text(encoding="utf-8")
    cleaned, removed = deduplicate_headings(text)

    if not removed:
        print(f"No duplicate headings found in {args.file.name}")
        return

    from collections import Counter

    counts = Counter(removed)
    print(f"\n{args.file.name}: {len(removed)} duplicate heading(s) removed")
    for title, count in counts.most_common():
        print(f"  {title!r} — {count} duplicate(s)")

    if args.dry_run:
        print("\n(dry-run — no changes written)")
    else:
        args.file.write_text(cleaned, encoding="utf-8")
        print(f"\nWritten: {args.file}")


if __name__ == "__main__":
    main()
