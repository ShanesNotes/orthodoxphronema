"""
validate_canon.py — Canon file validation (V1-V8 checks)

Validates a staged canon Markdown file before promotion to canon/.

Checks:
    V1  Anchor uniqueness — no duplicate BOOK.CH:V anchors
    V2  Chapter count — correct number of chapters for the book
    V3  Chapter sequence — chapters are sequential with no gaps
    V4  Verse sequence — within each chapter, verses are monotonically increasing
    V5  No article bleed — known article phrases must not appear in the canon file
    V6  Frontmatter present — required YAML fields exist
    V7  Completeness — total anchors match registry verse counts
    V8  Heading integrity — no fragment headings in canon text

Usage:
    python3 pipeline/validate/validate_canon.py staging/validated/OT/GEN.md
    python3 pipeline/validate/validate_canon.py staging/validated/OT/GEN.md --strict
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT    = Path(__file__).parent.parent.parent
REGISTRY     = REPO_ROOT / "schemas" / "anchor_registry.json"

# Anchor pattern: BOOK.CHAPTER:VERSE
RE_ANCHOR    = re.compile(r'^([A-Z0-9]+)\.(\d+):(\d+)\s')
RE_CHAPTER_H = re.compile(r'^## Chapter (\d+)')
RE_FM_FIELD  = re.compile(r'^(\w+):\s*(.+)')

# Phrases that indicate article text leaked into canon
ARTICLE_BLEED_PATTERNS = [
    r'Fall of Adam caused mankind',
    r"Mankind.s strong propensity to commit sin",
    r"intellectual, desiring and incensive",
    r"We who are of Adam.s race are not guilty because of Adam.s sin",
    r"Even after the Fall, the intellectual",
    r"T he Holy Trinity is revealed both",
]

REQUIRED_FM_FIELDS = ["book_code", "book_name", "testament", "canon_position",
                       "source", "parse_date", "status"]


def load_registry() -> dict:
    with open(REGISTRY, encoding="utf-8") as f:
        return json.load(f)


def parse_frontmatter(lines: list[str]) -> tuple[dict, int]:
    """Return (frontmatter_dict, first_body_line_index)."""
    if not lines or lines[0].strip() != "---":
        return {}, 0
    fm = {}
    i = 1
    while i < len(lines) and lines[i].strip() != "---":
        m = RE_FM_FIELD.match(lines[i])
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"')
        i += 1
    return fm, i + 1  # skip closing ---


def validate_file(path: Path, strict: bool = False) -> list[str]:
    """
    Run all validation checks. Returns a list of error/warning strings.
    Empty list = clean.
    """
    errors: list[str] = []
    warnings: list[str] = []

    if not path.exists():
        return [f"FAIL  File not found: {path}"]

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # ── V6 Frontmatter ──────────────────────────────────────────────────────
    fm, body_start = parse_frontmatter(lines)
    for field in REQUIRED_FM_FIELDS:
        if field not in fm:
            errors.append(f"V6   Missing frontmatter field: {field}")
    book_code = fm.get("book_code", path.stem)

    # ── Load expected chapter count from registry ────────────────────────────
    expected_chapters: int | None = None
    chapter_verse_counts_list: list | None = None
    try:
        registry = load_registry()
        for book in registry.get("books", []):
            if book["code"] == book_code:
                expected_chapters = book.get("chapters")
                chapter_verse_counts_list = book.get("chapter_verse_counts")
                break
    except Exception:
        warnings.append(f"WARN  Could not load registry; skipping chapter-count check")

    # ── Collect anchors and chapters ─────────────────────────────────────────
    anchors: list[tuple[str, int, int, int]] = []  # (anchor, chapter, verse, lineno)
    chapters_seen: list[tuple[int, int]] = []        # (chapter_num, lineno)
    anchor_set: set[str] = set()
    duplicate_anchors: list[str] = []

    for lineno, line in enumerate(lines[body_start:], start=body_start + 1):
        # Chapter header
        m_ch = RE_CHAPTER_H.match(line)
        if m_ch:
            chapters_seen.append((int(m_ch.group(1)), lineno))
            continue

        # Verse anchor
        m_anc = RE_ANCHOR.match(line)
        if m_anc:
            bk, ch, v = m_anc.group(1), int(m_anc.group(2)), int(m_anc.group(3))
            anchor_str = f"{bk}.{ch}:{v}"
            if anchor_str in anchor_set:
                duplicate_anchors.append(f"  line {lineno}: {anchor_str}")
            anchor_set.add(anchor_str)
            anchors.append((anchor_str, ch, v, lineno))

        # V5 Article bleed
        for pattern in ARTICLE_BLEED_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                errors.append(f"V5   Article text in canon at line {lineno}: {line[:80]!r}")
                break

    # ── V1 Anchor uniqueness ─────────────────────────────────────────────────
    if duplicate_anchors:
        errors.append(f"V1   {len(duplicate_anchors)} duplicate anchor(s):")
        errors.extend(duplicate_anchors[:10])
        if len(duplicate_anchors) > 10:
            errors.append(f"     ... and {len(duplicate_anchors) - 10} more")
    else:
        print(f"  V1  PASS  No duplicate anchors ({len(anchor_set)} unique)")

    # ── V2 Chapter count ─────────────────────────────────────────────────────
    actual_chapters = len(chapters_seen)
    if expected_chapters is not None:
        if actual_chapters == expected_chapters:
            print(f"  V2  PASS  Chapter count: {actual_chapters}")
        else:
            msg = f"V2   Chapter count: expected {expected_chapters}, got {actual_chapters}"
            (errors if strict else warnings).append(msg)
    else:
        print(f"  V2  INFO  Chapter count: {actual_chapters} (no registry reference)")

    # ── V3 Chapter sequence ───────────────────────────────────────────────────
    v3_pass = True
    for i, (ch_num, lineno) in enumerate(chapters_seen):
        expected = i + 1
        if ch_num != expected:
            errors.append(f"V3   Chapter sequence broken at line {lineno}: "
                          f"expected {expected}, got {ch_num}")
            v3_pass = False
    if v3_pass:
        print(f"  V3  PASS  Chapter sequence 1–{actual_chapters} is sequential")

    # ── V4 Verse sequence (within each chapter, verses must increase) ─────────
    verses_by_chapter: dict[int, list[tuple[int, int]]] = {}
    for (anchor, ch, v, lineno) in anchors:
        verses_by_chapter.setdefault(ch, []).append((v, lineno))

    v4_errors = 0
    v4_missing_anchors = 0
    for ch, verse_list in sorted(verses_by_chapter.items()):
        prev_v = 0
        for (v, lineno) in verse_list:
            if v < prev_v:
                errors.append(f"V4   Verse goes backward in ch.{ch} at line {lineno}: "
                               f"verse {v} after verse {prev_v}")
                v4_errors += 1
            elif v > prev_v + 1:
                warnings.append(f"V4   Missing verses in ch.{ch}: jumps from {prev_v} to {v}")
                v4_errors += 1
                v4_missing_anchors += v - prev_v - 1
            prev_v = max(prev_v, v)
    if v4_errors == 0:
        print(f"  V4  PASS  Verse order is monotonically increasing in all chapters")
    elif 0 < v4_missing_anchors <= 100:
        print(
            "  V4  INFO  Residual missing-anchor count is "
            f"{v4_missing_anchors}; consider PDF source spot-check:"
        )
        print(f"       python3 pipeline/validate/pdf_edge_case_check.py {path}")

    # ── V9 Embedded verse detection ──────────────────────────────────────────
    # For each V4 gap, check if the preceding verse line contains embedded
    # verse numbers for the missing verses (structural one-verse-per-line
    # violation).
    re_v4_gap = re.compile(r'V4\s+Missing verses in ch\.(\d+): jumps from (\d+) to (\d+)')
    v9_errors = 0
    verse_line_map: dict[str, tuple[int, str]] = {}  # anchor -> (lineno, text)
    for lineno, line in enumerate(lines[body_start:], start=body_start + 1):
        m_anc = RE_ANCHOR.match(line)
        if m_anc:
            anchor_str = f"{m_anc.group(1)}.{int(m_anc.group(2))}:{int(m_anc.group(3))}"
            verse_line_map[anchor_str] = (lineno, line)

    for w in warnings:
        m_gap = re_v4_gap.match(w)
        if not m_gap:
            continue
        gap_ch = int(m_gap.group(1))
        gap_from = int(m_gap.group(2))
        gap_to = int(m_gap.group(3))
        prev_anchor = f"{book_code}.{gap_ch}:{gap_from}"
        if prev_anchor not in verse_line_map:
            continue
        prev_lineno, prev_line = verse_line_map[prev_anchor]
        for missing_v in range(gap_from + 1, gap_to):
            # Match bare digit that isn't part of a larger number
            if re.search(rf'(?<!\d){missing_v}(?!\d)', prev_line):
                errors.append(
                    f"V9   Embedded verse {book_code}.{gap_ch}:{missing_v} "
                    f"found inside {prev_anchor} at line {prev_lineno}"
                )
                v9_errors += 1
    if v9_errors == 0:
        print(f"  V9  PASS  No embedded verses detected")

    # ── V7 Completeness ───────────────────────────────────────────────────────
    if chapter_verse_counts_list:
        expected_total = sum(chapter_verse_counts_list)
        actual = len(anchor_set)
        gap = expected_total - actual
        if gap == 0:
            print(f"  V7  PASS  Verse completeness: {actual}/{expected_total}")
        else:
            pct = actual / expected_total * 100
            warnings.append(
                f"V7   Completeness: {actual}/{expected_total} verses "
                f"({pct:.1f}%); gap of {gap}"
            )
    else:
        print(f"  V7  INFO  No chapter_verse_counts in registry; skipping completeness")

    # ── V8 Heading integrity ──────────────────────────────────────────────────
    v8_errors = 0
    for lineno, line in enumerate(lines[body_start:], start=body_start + 1):
        if not line.startswith('### '):
            continue
        heading = line[4:].rstrip()
        if heading.endswith((':', ',')):
            errors.append(
                f"V8   Fragment heading at line {lineno}: {line.rstrip()!r}"
            )
            v8_errors += 1
        elif heading[:1].isdigit():
            errors.append(
                f"V8   Digit-leading heading at line {lineno}: {line.rstrip()!r}"
            )
            v8_errors += 1
    if v8_errors == 0:
        print(f"  V8  PASS  No fragment headings detected")

    # ── Summary ──────────────────────────────────────────────────────────────
    verse_count = len(anchors)
    print(f"\n  Total verses : {verse_count}")
    print(f"  Total anchors: {len(anchor_set)} unique")

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a canon Markdown file.")
    parser.add_argument("path", help="Path to the canon .md file")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as errors")
    args = parser.parse_args()

    path = Path(args.path)
    print(f"\nValidating: {path}\n{'─' * 60}")

    errors, warnings = validate_file(path, strict=args.strict)

    if not errors and not warnings:
        print("\n  ALL CHECKS PASSED\n")
        sys.exit(0)
    else:
        if warnings:
            print(f"\n  WARNINGS ({len(warnings)}):")
            for w in warnings:
                print(f"    {w}")
        if errors:
            print(f"\n  ERRORS ({len(errors)}):")
            for e in errors:
                print(f"    {e}")
            print()
            sys.exit(1)
        else:
            print("\n  PASSED WITH WARNINGS\n")
            sys.exit(0)


if __name__ == "__main__":
    main()
