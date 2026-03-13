"""
nt_structural_reorder.py — Fix structural verse ordering issues in NT staging.

Fixes:
- REV ch16/17 boundary shift (16:17-21 misplaced into ch17)
- REV ch21/22 boundary shift (21:22-27 misplaced into ch22)
- 1CO ch1 verse misordering (1:5 before 1:2-4)

Usage:
    python3 pipeline/cleanup/nt_structural_reorder.py --dry-run
    python3 pipeline/cleanup/nt_structural_reorder.py --in-place
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
NT_DIR = REPO_ROOT / "staging" / "validated" / "NT"

RE_ANCHOR = re.compile(r'^([A-Z0-9]{2,4})\.(\d+):(\d+)\s+(.*)')
RE_CHAPTER_HDR = re.compile(r'^## Chapter (\d+)')
RE_HEADING = re.compile(r'^###\s+(.+)')


def _find_chapter_ranges(lines: list[str]) -> dict[int, tuple[int, int]]:
    """Return {chapter_num: (start_line, end_line)} for chapter headers."""
    positions = []
    for i, line in enumerate(lines):
        m = RE_CHAPTER_HDR.match(line)
        if m:
            positions.append((int(m.group(1)), i))

    ranges = {}
    for idx, (ch, start) in enumerate(positions):
        end = positions[idx + 1][1] if idx + 1 < len(positions) else len(lines)
        ranges[ch] = (start, end)
    return ranges


def _sort_chapter(lines: list[str], book: str, ch_num: int,
                  relabel: dict[str, str] | None = None,
                  export_to_prev: dict[str, str] | None = None) -> tuple[list[str], list[str]]:
    """Sort verses within a chapter section. Returns (exported_lines, rebuilt_chapter).

    relabel: anchors to rename within the chapter {old_anchor: new_anchor}
    export_to_prev: anchors to relabel and move to previous chapter {old: new}
    """
    relabel = relabel or {}
    export_to_prev = export_to_prev or {}

    # Parse into heading+verse pairs
    pairs: list[tuple[int, str | None, str]] = []  # (sort_key, heading_or_None, verse_line)
    exported: list[tuple[int, str]] = []  # (sort_key, verse_line)
    pending_heading: str | None = None

    for line in lines:
        stripped = line.strip()
        if RE_CHAPTER_HDR.match(stripped):
            continue  # skip chapter header itself
        if stripped == "":
            continue
        if RE_HEADING.match(stripped):
            pending_heading = stripped
            continue

        m = RE_ANCHOR.match(stripped)
        if m:
            anchor = f"{m.group(1)}.{m.group(2)}:{m.group(3)}"
            body = m.group(4)

            # Export to previous chapter?
            if anchor in export_to_prev:
                new_anchor = export_to_prev[anchor]
                new_vnum = int(new_anchor.split(":")[1])
                exported.append((new_vnum, f"{new_anchor} {body}"))
                pending_heading = None  # drop heading paired with exported verse
                continue

            # Internal relabel?
            if anchor in relabel:
                anchor = relabel[anchor]

            vnum = int(anchor.split(":")[1])
            pairs.append((vnum, pending_heading, f"{anchor} {body}"))
            pending_heading = None
            continue

        # Non-verse, non-heading line — keep it as-is attached to next verse
        # (rare; skip for safety)

    # Sort by verse number
    pairs.sort(key=lambda x: x[0])
    exported.sort(key=lambda x: x[0])

    # Rebuild chapter
    rebuilt = [f"## Chapter {ch_num}", ""]
    for vnum, heading, vline in pairs:
        if heading:
            rebuilt.append("")
            rebuilt.append(heading)
            rebuilt.append("")
        rebuilt.append(vline)

    export_lines = [line for _, line in exported]
    return export_lines, rebuilt


def fix_rev(filepath: Path, dry_run: bool = False) -> int:
    """Fix REV chapter boundary shifts and verse ordering."""
    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()
    ranges = _find_chapter_ranges(lines)

    changes = 0

    # --- Fix ch16/17 boundary ---
    if 17 in ranges and 18 in ranges:
        ch17_start, ch17_end = ranges[17]
        ch17_lines = lines[ch17_start:ch17_end]

        export_lines, rebuilt_ch17 = _sort_chapter(
            ch17_lines, "REV", 17,
            export_to_prev={
                "REV.17:1": "REV.16:17",
                "REV.17:19": "REV.16:19",
                "REV.17:20": "REV.16:20",
                "REV.17:21": "REV.16:21",
            },
        )

        # Insert exported lines before ch17 header (end of ch16)
        new_lines = lines[:ch17_start]
        for eline in export_lines:
            new_lines.append(eline)
        new_lines.extend(rebuilt_ch17)
        new_lines.extend(lines[ch17_end:])
        lines = new_lines
        changes += len(export_lines) + 1  # exports + reorder
        ranges = _find_chapter_ranges(lines)  # recalculate

    # --- Fix ch21/22 boundary ---
    if 22 in ranges:
        ch22_start, ch22_end = ranges[22]
        ch22_lines = lines[ch22_start:ch22_end]

        export_lines, rebuilt_ch22 = _sort_chapter(
            ch22_lines, "REV", 22,
            export_to_prev={
                "REV.22:1": "REV.21:22",
                "REV.22:23": "REV.21:23",
                "REV.22:24": "REV.21:24",
                "REV.22:25": "REV.21:25",
                "REV.22:26": "REV.21:26",
                "REV.22:27": "REV.21:27",
            },
            relabel={
                "REV.22:22": "REV.22:1",
            },
        )

        new_lines = lines[:ch22_start]
        for eline in export_lines:
            new_lines.append(eline)
        new_lines.extend(rebuilt_ch22)
        new_lines.extend(lines[ch22_end:])
        lines = new_lines
        changes += len(export_lines) + 1

    result = "\n".join(lines) + "\n"
    if dry_run:
        print(f"  [REV] Would fix {changes} structural issues (ch16/17 + ch21/22 boundaries)")
    else:
        filepath.write_text(result, encoding="utf-8")
        print(f"  [REV] Fixed {changes} structural issues (ch16/17 + ch21/22 boundaries)")
    return changes


def fix_1co(filepath: Path, dry_run: bool = False) -> int:
    """Fix 1CO ch1 verse misordering."""
    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()
    ranges = _find_chapter_ranges(lines)

    if 1 not in ranges:
        print("  [1CO] Chapter 1 not found")
        return 0

    ch1_start, ch1_end = ranges[1]
    ch1_lines = lines[ch1_start:ch1_end]

    _, rebuilt_ch1 = _sort_chapter(ch1_lines, "1CO", 1)

    new_lines = lines[:ch1_start]
    new_lines.extend(rebuilt_ch1)
    new_lines.extend(lines[ch1_end:])

    result = "\n".join(new_lines) + "\n"
    if dry_run:
        print("  [1CO] Would reorder ch1 verses")
    else:
        filepath.write_text(result, encoding="utf-8")
        print("  [1CO] Reordered ch1 verses")
    return 1


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Fix NT structural ordering")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()

    dry_run = args.dry_run or not args.in_place

    print(f"NT Structural Reorder {'(dry-run)' if dry_run else '(in-place)'}:")

    rev_path = NT_DIR / "REV.md"
    co_path = NT_DIR / "1CO.md"

    total = 0
    if rev_path.exists():
        total += fix_rev(rev_path, dry_run=dry_run)
    if co_path.exists():
        total += fix_1co(co_path, dry_run=dry_run)

    print(f"\nTotal structural fixes: {total}")


if __name__ == "__main__":
    main()
