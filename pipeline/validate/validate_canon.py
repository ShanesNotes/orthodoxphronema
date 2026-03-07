"""
validate_canon.py — Canon file validation (V1-V6 checks from memo 03)

Validates a staged canon Markdown file before promotion to canon/.

Checks:
    V1  Anchor uniqueness — no duplicate BOOK.CH:V anchors
    V2  Chapter count — correct number of chapters for the book
    V3  Chapter sequence — chapters are sequential with no gaps
    V4  Verse sequence — within each chapter, verses are monotonically increasing
    V5  No article bleed — known article phrases must not appear in the canon file
    V6  Frontmatter present — required YAML fields exist

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
    try:
        registry = load_registry()
        for book in registry.get("books", []):
            if book["code"] == book_code:
                expected_chapters = book.get("chapters")
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
    for ch, verse_list in sorted(verses_by_chapter.items()):
        prev_v = 0
        for (v, lineno) in verse_list:
            if v < prev_v:
                warnings.append(f"V4   Verse goes backward in ch.{ch} at line {lineno}: "
                                 f"verse {v} after verse {prev_v}")
                v4_errors += 1
            prev_v = max(prev_v, v)
    if v4_errors == 0:
        print(f"  V4  PASS  Verse order is monotonically increasing in all chapters")

    # ── Summary ──────────────────────────────────────────────────────────────
    verse_count = len(anchors)
    print(f"\n  Total verses : {verse_count}")
    print(f"  Total anchors: {len(anchor_set)} unique")

    all_issues = errors + warnings
    return all_issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a canon Markdown file.")
    parser.add_argument("path", help="Path to the canon .md file")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as errors")
    args = parser.parse_args()

    path = Path(args.path)
    print(f"\nValidating: {path}\n{'─' * 60}")

    issues = validate_file(path, strict=args.strict)

    if not issues:
        print("\n  ALL CHECKS PASSED\n")
        sys.exit(0)
    else:
        errors   = [i for i in issues if i.startswith(("FAIL", "V1", "V2", "V3", "V4", "V5", "V6"))]
        warnings = [i for i in issues if i.startswith("WARN")]
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
