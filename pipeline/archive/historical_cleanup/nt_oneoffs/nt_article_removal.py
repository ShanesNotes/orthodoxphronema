"""
nt_article_removal.py — Remove study article leakage from NT staging files.

Removes:
- Lines where article/outline text has replaced verse content
- Navigation junk (Back to TOC, Previous Home Next, etc.)
- Spaced-caps study article headings
- Leaked non-canon headings (Outline, book title repeats)
- Cleans mixed lines (article + verse text fused together)

Usage:
    python3 pipeline/cleanup/nt_article_removal.py --dry-run
    python3 pipeline/cleanup/nt_article_removal.py --in-place
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
NT_DIR = REPO_ROOT / "staging" / "validated" / "NT"

# ── Per-book anchors to DELETE (pure article in verse slots) ────────────────
DELETE_ANCHORS: dict[str, set[str]] = {
    "EPH": {
        "EPH.2:1", "EPH.2:2", "EPH.2:3", "EPH.2:4", "EPH.2:5",
    },
    "HEB": {
        "HEB.1:2", "HEB.1:3", "HEB.1:4", "HEB.1:6", "HEB.1:7", "HEB.1:8",
    },
    "1TI": {
        "1TI.2:1", "1TI.2:2", "1TI.2:3", "1TI.2:4",
        "1TI.2:16", "1TI.2:17", "1TI.2:20", "1TI.2:21", "1TI.2:22",
    },
    "ROM": {
        "ROM.2:1", "ROM.2:2", "ROM.2:3", "ROM.2:4", "ROM.2:5", "ROM.2:6",
        "ROM.2:7",
    },
}

# ── Generic body patterns that indicate non-scripture content ───────────────
# Any anchor line whose body matches these patterns is navigation/article junk
NAV_JUNK_PATTERNS = [
    re.compile(r'Back to the New Testament', re.IGNORECASE),
    re.compile(r'Back to Table of Contents', re.IGNORECASE),
    re.compile(r'Back to Chapters in', re.IGNORECASE),
    re.compile(r'Previous Home Next', re.IGNORECASE),
    re.compile(r'Verses in \w+ Chapter \d+'),
]

ARTICLE_INTRO_PATTERNS = [
    re.compile(r'^Author\s*[-\u2013\u2014]'),
    re.compile(r'^Date\s*[-\u2013\u2014]'),
    re.compile(r'^Major Theme\s*[-\u2013\u2014]'),
    re.compile(r'^Background\s*[-\u2013\u2014]'),
]

# ── Spaced-caps heading detection ──────────────────────────────────────────
RE_SPACED_CAPS = re.compile(
    r"###\s+.*("
    r"[A-Z]\s+[A-Z]\s+[A-Z]\s+[A-Z]"  # any 4+ spaced uppercase letters
    r")"
)

# ── Leaked non-canon headings to delete ────────────────────────────────────
LEAKED_HEADING_PATTERNS = [
    re.compile(r'^###\s+Outline$'),
    re.compile(r'^###\s+The (First|Second|Third) (Book|Epistle|Letter) of'),
    re.compile(r'^###\s+Verses in \w+ Chapter'),
    re.compile(r'^###\s+The (General |Holy )?Epistle of'),
    re.compile(r'^###\s+The (Gospel|Revelation|Acts)'),
    re.compile(r'^###\s+The Prophecy of'),
]

# ── Per-book mixed-line cleaners ───────────────────────────────────────────
CLEAN_MARKERS: dict[str, str] = {
    "EPH.2:19": "Now, therefore,",
    "1CO.1:3": "Grace to you and peace",
    "PHP.1:1": "Paul and Timothy,",
    "1TH.1:5": "Paul, Silvanus, and Timothy,",
}

RE_ANCHOR = re.compile(r'^([A-Z0-9]{2,4}\.\d+:\d+)\s+(.*)')


def _is_nav_junk(body: str) -> bool:
    """Check if verse body is navigation/index junk."""
    for pat in NAV_JUNK_PATTERNS:
        if pat.search(body):
            return True
    return False


def _is_article_intro(body: str) -> bool:
    """Check if verse body is study article intro (Author/Date/Theme/Background)."""
    for pat in ARTICLE_INTRO_PATTERNS:
        if pat.search(body):
            return True
    return False


def _is_ch0_content(anchor: str) -> bool:
    """Chapter 0 is always outline/intro text."""
    m = re.match(r'[A-Z0-9]+\.0:', anchor)
    return bool(m)


def _is_leaked_heading(line: str) -> bool:
    """Check if a heading line is a leaked non-canon heading."""
    stripped = line.strip()
    if not stripped.startswith("###"):
        return False
    # Spaced-caps headings
    if RE_SPACED_CAPS.search(stripped):
        return True
    # Pattern-based leaked headings
    for pat in LEAKED_HEADING_PATTERNS:
        if pat.match(stripped):
            return True
    return False


def process_file(filepath: Path, dry_run: bool = False) -> dict:
    """Process a single NT file. Returns stats dict."""
    book_code = filepath.stem
    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()

    delete_set = DELETE_ANCHORS.get(book_code, set())
    stats = {"deleted": 0, "cleaned": 0, "headings_removed": 0}
    new_lines = []
    skip_next_blank = False

    for line in lines:
        stripped = line.strip()

        # Check leaked headings
        if stripped.startswith("###") and _is_leaked_heading(stripped):
            stats["headings_removed"] += 1
            skip_next_blank = True
            continue

        # Skip blank line after deleted heading
        if skip_next_blank and stripped == "":
            skip_next_blank = False
            continue
        skip_next_blank = False

        # Check anchor lines
        m = RE_ANCHOR.match(line)
        if m:
            anchor = m.group(1)
            body = m.group(2)

            # Delete per-book targeted anchors
            if anchor in delete_set:
                stats["deleted"] += 1
                continue

            # Delete chapter 0 content (outline/intro)
            if _is_ch0_content(anchor):
                stats["deleted"] += 1
                continue

            # Delete navigation junk
            if _is_nav_junk(body):
                stats["deleted"] += 1
                continue

            # Delete article intro lines
            if _is_article_intro(body):
                stats["deleted"] += 1
                continue

            # Clean mixed lines (extract real verse text)
            if anchor in CLEAN_MARKERS:
                marker = CLEAN_MARKERS[anchor]
                idx = line.find(marker)
                if idx > 0:
                    new_lines.append(f"{anchor} {line[idx:]}")
                    stats["cleaned"] += 1
                    continue

        new_lines.append(line)

    # HEB.1:9 special case
    if book_code == "HEB":
        new_lines, extra = _fix_heb_1_9(new_lines)
        stats["cleaned"] += extra

    total_changes = stats["deleted"] + stats["cleaned"] + stats["headings_removed"]
    if total_changes > 0:
        result = "\n".join(new_lines) + "\n"
        if dry_run:
            print(f"  [{book_code}] Would remove {stats['deleted']} article lines, "
                  f"clean {stats['cleaned']} mixed, "
                  f"remove {stats['headings_removed']} headings")
        else:
            filepath.write_text(result, encoding="utf-8")
            print(f"  [{book_code}] Removed {stats['deleted']} article lines, "
                  f"cleaned {stats['cleaned']} mixed, "
                  f"removed {stats['headings_removed']} headings")
    else:
        print(f"  [{book_code}] No article leakage found")

    return stats


def _fix_heb_1_9(lines: list[str]) -> tuple[list[str], int]:
    """Split HEB.1:9 which contains embedded heading and verse 1:10 text."""
    new_lines = []
    fixes = 0
    for line in lines:
        if line.startswith("HEB.1:9 "):
            marker = "Christ Without Beginning, Creator of All"
            idx = line.find(marker)
            if idx > 0:
                v9_body = line[len("HEB.1:9 "):idx].rstrip()
                after = line[idx + len(marker):].strip()
                new_lines.append(f"HEB.1:9 {v9_body}")
                new_lines.append("")
                new_lines.append(f"### {marker}")
                new_lines.append("")
                if after:
                    new_lines.append(f"HEB.1:10 {after}")
                fixes += 1
                continue
        new_lines.append(line)
    return new_lines, fixes


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Remove NT article leakage")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--book", nargs="*", help="Specific books (default: all NT)")
    args = parser.parse_args()

    dry_run = args.dry_run or not args.in_place

    # Process ALL NT books by default
    if args.book:
        targets = set(args.book)
    else:
        targets = {p.stem for p in NT_DIR.glob("[A-Z0-9]*.md")
                   if not p.stem.endswith("_notes") and not p.stem.endswith("_footnote_markers")
                   and not p.stem.endswith("_residuals") and not p.stem.endswith("_editorial_candidates")
                   and "_" not in p.stem}

    print(f"NT Article Removal {'(dry-run)' if dry_run else '(in-place)'}:")
    total = {"deleted": 0, "cleaned": 0, "headings_removed": 0}

    for book in sorted(targets):
        filepath = NT_DIR / f"{book}.md"
        if filepath.exists():
            stats = process_file(filepath, dry_run=dry_run)
            for k in total:
                total[k] += stats[k]

    print(f"\nTotal: {total['deleted']} deleted, {total['cleaned']} cleaned, "
          f"{total['headings_removed']} headings removed")


if __name__ == "__main__":
    main()
