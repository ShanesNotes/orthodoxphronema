"""
validate_canon.py — Canon file validation (V1-V12 checks)

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
    V9  Embedded verse detection
    V10 Absorbed content (Brenton cross-reference)
    V11 Split-word artifacts (Docling column-split)
    V12 Inline verse-number leakage

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

from pipeline.common.types import ValidationResult
from pipeline.common.patterns import RE_ANCHOR, RE_CHAPTER_HDR, RE_FM_FIELD
from pipeline.common.frontmatter import parse_frontmatter
from pipeline.validate.checks import (
    check_frontmatter,
    check_anchor_uniqueness,
    check_chapter_count,
    check_chapter_sequence,
    check_verse_sequence,
    check_article_bleed,
    check_completeness,
    check_heading_integrity,
    check_embedded_verses,
    check_absorbed_content,
    check_split_words,
    check_inline_leakage,
    compute_v4_gaps,
)

REPO_ROOT    = Path(__file__).parent.parent.parent
REGISTRY     = REPO_ROOT / "schemas" / "anchor_registry.json"
BRENTON_DIR  = REPO_ROOT / "staging" / "reference" / "brenton"

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


def run_validation(path: Path, strict: bool = False) -> ValidationResult:
    """Run all V1-V12 checks and return a structured ValidationResult.

    This is the primary entry point for batch_validate.py and other tools
    that need structured check results.
    """
    if not path.exists():
        from pipeline.common.types import CheckResult
        err_check = CheckResult(name="FILE", status="FAIL",
                                errors=[f"File not found: {path}"])
        return ValidationResult(book_code=path.stem, checks=[err_check])

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # ── Parse frontmatter ─────────────────────────────────────────────────
    fm, body_start = parse_frontmatter(lines)
    book_code = fm.get("book_code", path.stem)

    # ── Load registry data ────────────────────────────────────────────────
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
        pass

    # ── Collect anchors and chapters ──────────────────────────────────────
    anchors: list[tuple[str, int, int, int]] = []
    chapters_seen: list[tuple[int, int]] = []
    anchor_set: set[str] = set()

    for lineno, line in enumerate(lines[body_start:], start=body_start + 1):
        m_ch = RE_CHAPTER_HDR.match(line)
        if m_ch:
            chapters_seen.append((int(m_ch.group(1)), lineno))
            continue
        m_anc = RE_ANCHOR.match(line)
        if m_anc:
            bk, ch, v = m_anc.group(1), int(m_anc.group(2)), int(m_anc.group(3))
            anchor_str = f"{bk}.{ch}:{v}"
            anchor_set.add(anchor_str)
            anchors.append((anchor_str, ch, v, lineno))

    # ── Build verses_by_chapter ───────────────────────────────────────────
    verses_by_chapter: dict[int, list[tuple[int, int]]] = {}
    for (anchor_str, ch, v, lineno) in anchors:
        verses_by_chapter.setdefault(ch, []).append((v, lineno))

    # ── Build verse_line_map (for V9, V10) ────────────────────────────────
    verse_line_map: dict[str, tuple[int, str]] = {}
    for lineno, line in enumerate(lines[body_start:], start=body_start + 1):
        m_anc = RE_ANCHOR.match(line)
        if m_anc:
            anc = f"{m_anc.group(1)}.{int(m_anc.group(2))}:{int(m_anc.group(3))}"
            verse_line_map[anc] = (lineno, line)

    # ── Compute V4 gaps (shared by V4, V9, V10) ──────────────────────────
    gaps = compute_v4_gaps(verses_by_chapter)

    # ── Run all 12 checks ─────────────────────────────────────────────────
    checks = []
    checks.append(check_frontmatter(fm))                                          # V6
    checks.append(check_anchor_uniqueness(anchors, anchor_set))                   # V1
    checks.append(check_chapter_count(chapters_seen, expected_chapters, strict))   # V2
    checks.append(check_chapter_sequence(chapters_seen))                          # V3
    checks.append(check_verse_sequence(verses_by_chapter, book_code))             # V4
    checks.append(check_article_bleed(lines, body_start))                         # V5
    checks.append(check_completeness(anchor_set, chapter_verse_counts_list))      # V7
    checks.append(check_heading_integrity(lines, body_start, anchor_set))         # V8
    checks.append(check_embedded_verses(gaps, verse_line_map, book_code))         # V9
    brenton_path = BRENTON_DIR / f"{book_code}.json"
    checks.append(check_absorbed_content(
        gaps, verse_line_map, book_code, brenton_path))                           # V10
    checks.append(check_split_words(lines, body_start))                           # V11
    checks.append(check_inline_leakage(lines, body_start))                        # V12

    return ValidationResult(
        book_code=book_code,
        checks=checks,
        metadata={"path": str(path), "total_anchors": len(anchor_set)},
    )


def validate_file(path: Path, strict: bool = False) -> tuple[list[str], list[str]]:
    """Run all validation checks. Returns (errors, warnings) lists.

    Delegates to run_validation() for all V1-V12 checks, then formats
    output for CLI backward compatibility.
    """
    if not path.exists():
        return [f"FAIL  File not found: {path}"], []

    result = run_validation(path, strict=strict)
    total_anchors = result.metadata.get("total_anchors", 0)

    # Print per-check PASS lines for CLI output
    for check in result.checks:
        if check.status == "PASS":
            if check.name == "V1":
                print(f"  V1  PASS  No duplicate anchors ({total_anchors} unique)")
            elif check.name == "V2":
                print(f"  V2  PASS  Chapter count matches registry")
            elif check.name == "V3":
                print(f"  V3  PASS  Chapter sequence is sequential")
            elif check.name == "V4":
                print(f"  V4  PASS  Verse order is monotonically increasing in all chapters")
            elif check.name == "V7":
                pct_data = check.data.get("pct")
                if pct_data is not None:
                    print(f"  V7  PASS  Verse completeness: {check.data['actual_total']}/{check.data['expected_total']}")
                else:
                    print(f"  V7  PASS  Verse completeness")
            elif check.name == "V8":
                print(f"  V8  PASS  No fragment headings detected")
            elif check.name == "V9":
                print(f"  V9  PASS  No embedded verses detected")
        elif check.status == "INFO":
            if check.name == "V2":
                print(f"  V2  INFO  No registry reference for chapter count")
            elif check.name == "V7":
                print(f"  V7  INFO  No chapter_verse_counts in registry; skipping completeness")

    v4_check = result.check("V4")
    if v4_check and v4_check.status == "WARN":
        total_missing = v4_check.data.get("total_missing", 0)
        if 0 < total_missing <= 100:
            print(f"  V4  INFO  Residual missing-anchor count is {total_missing}; consider PDF source spot-check:")
            print(f"       python3 pipeline/validate/pdf_edge_case_check.py {path}")

    print(f"\n  Total verses : {total_anchors}")
    print(f"  Total anchors: {total_anchors} unique")

    return result.errors, result.warnings


def collect_v4_gap_anchors(warnings: list[str], book_code: str) -> list[str]:
    """Extract missing-verse anchors from V4 gap warnings."""
    re_v4_gap = re.compile(r'V4\s+Missing verses in ch\.(\d+): jumps from (\d+) to (\d+)')
    gap_anchors: list[str] = []
    for w in warnings:
        m = re_v4_gap.match(w)
        if not m:
            continue
        ch = int(m.group(1))
        gap_from = int(m.group(2))
        gap_to = int(m.group(3))
        for v in range(gap_from + 1, gap_to):
            gap_anchors.append(f"{book_code}.{ch}:{v}")
    return gap_anchors


def generate_sidecar(path: Path, warnings_or_result, book_code: str) -> Path | None:
    """Generate a draft residuals sidecar JSON from V4 gap warnings.

    Accepts either a list of warning strings or a ValidationResult.
    Returns the output path on success, or None if the file already exists
    or there are no gaps to record.
    """
    if isinstance(warnings_or_result, ValidationResult):
        # Extract missing_anchors directly from structured V4 data
        v4_check = warnings_or_result.check("V4")
        gap_anchors = v4_check.data.get("missing_anchors", []) if v4_check else []
    else:
        gap_anchors = collect_v4_gap_anchors(warnings_or_result, book_code)
    if not gap_anchors:
        print("  SIDECAR  No V4 gaps found — nothing to generate.")
        return None

    # Determine testament from path or registry
    testament = None
    path_str = str(path)
    if "/OT/" in path_str:
        testament = "OT"
    elif "/NT/" in path_str:
        testament = "NT"
    else:
        try:
            registry = load_registry()
            for book in registry.get("books", []):
                if book["code"] == book_code:
                    testament = book.get("testament")
                    break
        except Exception:
            pass
    if testament is None:
        print(f"  SIDECAR  WARN  Could not determine testament for {book_code}; defaulting to OT")
        testament = "OT"

    # Load registry version
    registry_version = "unknown"
    try:
        registry = load_registry()
        registry_version = registry.get("registry_version", "unknown")
    except Exception:
        pass

    # Build output path
    out_dir = REPO_ROOT / "staging" / "validated" / testament
    out_path = out_dir / f"{book_code}_residuals.json"

    if out_path.exists():
        print(f"  SIDECAR  WARN  Refusing to overwrite existing file: {out_path}")
        return None

    sidecar = {
        "book_code": book_code,
        "registry_version": registry_version,
        "ratified_by": None,
        "ratified_date": None,
        "residuals": [
            {
                "anchor": anchor,
                "classification": "docling_issue",
                "description": "Auto-generated \u2014 verify classification",
                "blocking": False,
            }
            for anchor in gap_anchors
        ],
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(sidecar, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
    print(f"  SIDECAR  Generated {out_path} with {len(gap_anchors)} residual(s)")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a canon Markdown file.")
    parser.add_argument("path", help="Path to the canon .md file")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as errors")
    parser.add_argument("--generate-sidecar", action="store_true",
                        help="Generate a draft residuals sidecar JSON from V4 gaps")
    args = parser.parse_args()

    path = Path(args.path)
    print(f"\nValidating: {path}\n{'─' * 60}")

    errors, warnings = validate_file(path, strict=args.strict)

    if not errors and not warnings:
        print("\n  ALL CHECKS PASSED\n")
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

    # Generate sidecar if requested (run even if there are errors)
    if args.generate_sidecar:
        book_code = Path(args.path).stem
        generate_sidecar(path, warnings, book_code)

    if errors:
        sys.exit(1)
    elif not errors and not warnings:
        sys.exit(0)
    else:
        print("\n  PASSED WITH WARNINGS\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
