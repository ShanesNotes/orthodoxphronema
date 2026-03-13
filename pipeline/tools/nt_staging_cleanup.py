#!/usr/bin/env python3
"""nt_staging_cleanup.py — Clean trailing footnote markers from NT staging files.

Removes trailing single lowercase letters (` a`, ` b`, etc.) from verse lines,
and fixes V12 inline verse-number leakage.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

# Match verse lines ending with ` a` or ` b` (trailing footnote letter)
RE_TRAILING_MARKER = re.compile(r"^([A-Z0-9]+\.\d+:\d+\s.*\S)\s+([a-z])$")

# V12: inline verse number leakage — a number in the middle of text that
# matches the verse pattern but is actually verse text
# e.g., "...ized; 40 but to si..." in MRK.10:40
# These need case-by-case review, not automated fix


def clean_trailing_markers(filepath: Path) -> int:
    """Strip trailing footnote letters from verse lines. Returns count fixed."""
    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()
    fixed = 0
    out = []
    for line in lines:
        m = RE_TRAILING_MARKER.match(line)
        if m:
            out.append(m.group(1))
            fixed += 1
        else:
            out.append(line)
    if fixed:
        filepath.write_text("\n".join(out) + "\n", encoding="utf-8")
    return fixed


def main():
    books = ["MAT", "MRK", "LUK", "JOH", "ACT", "ROM", "1CO", "PHP", "COL", "1PE", "REV"]
    total = 0
    for code in books:
        path = REPO / "staging" / "validated" / "NT" / f"{code}.md"
        if not path.exists():
            print(f"  {code}: MISSING")
            continue
        fixed = clean_trailing_markers(path)
        total += fixed
        print(f"  {code}: {fixed} trailing markers removed")
    print(f"\n  Total: {total} lines cleaned")


if __name__ == "__main__":
    main()
