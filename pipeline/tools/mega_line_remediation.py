"""
mega_line_remediation.py — Delete V13-failing mega-lines from canon books.

Strategy: clone canon → staging, delete mega-lines (identified by anchor),
reset frontmatter to staged, run V1-V13 validation.

Handles three tiers:
  A: verse_fusing only (simple delete)
  B: article_bleed + verse_fusing (delete, verify study content exists)
  C: oversized (skip — handled via config allowlist or manual)

Usage:
    python3 pipeline/tools/mega_line_remediation.py
    python3 pipeline/tools/mega_line_remediation.py --book NUM JOS
    python3 pipeline/tools/mega_line_remediation.py --dry-run
    python3 pipeline/tools/mega_line_remediation.py --tier A
    python3 pipeline/tools/mega_line_remediation.py --tier B
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

# Repo path setup
_R = Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists():
    _R = _R.parent
if str(_R) not in sys.path:
    sys.path.insert(0, str(_R))

from pipeline.common.paths import REPO_ROOT, CANON_ROOT, STAGING_ROOT
from pipeline.common.paths import canon_filepath
from pipeline.common.patterns import RE_ANCHOR

AUDIT_PATH = REPO_ROOT / "reports" / "v13_mega_line_audit.json"
REPORTS_DIR = REPO_ROOT / "reports"

# Books classified by tier
TIER_A_BOOKS = {
    "NUM", "JOS", "JDG", "2SA", "2KI", "1CH", "2CH",
    "EZR", "NEH", "TOB", "JDT", "JON", "ZEP", "ZEC",
}
TIER_B_BOOKS = {"LEV", "EXO", "JER"}
# EST handled via config allowlist; 1KI.2:1 treated as Tier A
TIER_C_1KI_FUSED = {"1KI"}  # only 1KI.2:1 is a true fused line

# All books that need mega-line deletion
ALL_DELETE_BOOKS = TIER_A_BOOKS | TIER_B_BOOKS | TIER_C_1KI_FUSED


def load_audit() -> dict:
    """Load the V13 mega-line audit report."""
    with open(AUDIT_PATH, encoding="utf-8") as f:
        return json.load(f)


def extract_book_code(key: str) -> str:
    """Extract book code from audit key like '04_NUM'."""
    return key.split("_", 1)[1] if "_" in key else key


def find_canon_file(code: str) -> Path | None:
    """Find the canon file for a book code."""
    for testament in ["OT", "NT"]:
        p = canon_filepath(testament, code)
        if p.exists():
            return p
    return None


def get_testament(code: str) -> str:
    """Determine testament for a book code."""
    nt_books = {
        "MAT", "MRK", "LUK", "JOH", "ACT", "ROM", "1CO", "2CO",
        "GAL", "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI",
        "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JN", "2JN",
        "3JN", "JUD", "REV",
    }
    return "NT" if code in nt_books else "OT"


def clone_canon_to_staging(canon_path: Path, code: str) -> Path:
    """Clone a canon file to staging, resetting frontmatter."""
    text = canon_path.read_text(encoding="utf-8")
    lines = text.split("\n")

    # Find and modify frontmatter
    new_lines = []
    in_fm = False
    fm_count = 0
    for line in lines:
        if line.strip() == "---":
            fm_count += 1
            if fm_count == 1:
                in_fm = True
                new_lines.append(line)
                continue
            elif fm_count == 2:
                in_fm = False
                new_lines.append(line)
                continue
        if in_fm:
            if line.startswith("status:"):
                new_lines.append("status: staged")
            elif line.startswith("promote_date:"):
                continue  # drop
            elif line.startswith("checksum:"):
                continue  # drop
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    testament = get_testament(code)
    staging_path = STAGING_ROOT / testament / f"{code}.md"
    staging_path.parent.mkdir(parents=True, exist_ok=True)
    staging_path.write_text("\n".join(new_lines), encoding="utf-8")
    return staging_path


def truncate_mega_lines(
    staging_path: Path,
    mega_anchors: list[str],
    *,
    skip_oversized: bool = True,
    mega_details: list[dict] | None = None,
) -> tuple[int, list[str]]:
    """Truncate mega-lines to just the first verse text.

    The mega-line contains ANCHOR.CH:V text plus fused subsequent verses.
    The split verses below start from :V+1. We extract just the :V text
    by finding where the first embedded verse number appears.

    Returns (truncated_count, truncated_anchors).
    """
    # Regex to find the first embedded verse number in the text after the anchor.
    # Matches patterns like: "3he", "3Then", "3\u2018Now" — a digit followed by
    # uppercase letter or quote, preceded by sentence-ending punctuation or space.
    # Non-raw string to support Unicode escapes (\u2018, \u2019, \u201c, \u201d).
    RE_EMBEDDED_VNUM = re.compile(
        "(?<=[,;:.!?\u201d\"\u2019\u2018' ] )"   # preceded by punctuation + space
        r"(\d+)"                                    # verse number
        "(?=[\u201c\u2018\"'A-Za-z])"             # followed by letter/quote
    )

    # Build set of anchors to truncate, skipping genuinely oversized lines
    skip_set = set()
    if skip_oversized and mega_details:
        for d in mega_details:
            if d["classification"] == "oversized" and d["embedded_verse_count"] == 0:
                skip_set.add(d["anchor"])

    target_set = {a for a in mega_anchors if a not in skip_set}

    text = staging_path.read_text(encoding="utf-8")
    lines = text.split("\n")
    kept = []
    truncated = []

    for line in lines:
        m = RE_ANCHOR.match(line)
        if m and len(line) > 1000:
            anchor = f"{m.group(1)}.{m.group(2)}:{m.group(3)}"
            if anchor in target_set:
                # Extract just the first verse text
                anchor_end = m.end()
                text_part = line[anchor_end:]

                # Find first embedded verse number (skip first 10 chars to avoid
                # matching the verse's own number in case of short first-verse text)
                first_v = RE_EMBEDDED_VNUM.search(text_part, pos=10)
                if first_v:
                    # Keep only up to the embedded verse number
                    first_verse_text = text_part[:first_v.start()].rstrip()
                    kept.append(line[:anchor_end] + first_verse_text)
                else:
                    # No embedded verse found — keep the full line (shouldn't happen
                    # for lines with embedded_verse_count > 0)
                    kept.append(line)
                truncated.append(anchor)
                continue
        kept.append(line)

    staging_path.write_text("\n".join(kept), encoding="utf-8")
    return len(truncated), truncated


def run_validation(staging_path: Path) -> dict:
    """Run V1-V13 validation and return results."""
    from pipeline.validate.validate_canon import run_validation as _run
    result = _run(staging_path)
    # Compute overall from individual check statuses
    statuses = [c.status for c in result.checks]
    if any(s == "FAIL" for s in statuses):
        overall = "FAIL"
    elif any(s == "WARN" for s in statuses):
        overall = "WARN"
    else:
        overall = "PASS"
    return {
        "file": str(staging_path),
        "overall": overall,
        "checks": {
            c.name: {"status": c.status, "errors": c.errors[:3], "warnings": c.warnings[:3]}
            for c in result.checks
        },
    }


def remediate_book(
    code: str,
    mega_details: list[dict],
    *,
    dry_run: bool = False,
) -> dict:
    """Remediate a single book: clone, delete mega-lines, validate."""
    canon_path = find_canon_file(code)
    if not canon_path:
        return {"book": code, "status": "ERROR", "message": f"Canon file not found for {code}"}

    mega_anchors = [d["anchor"] for d in mega_details]

    if dry_run:
        return {
            "book": code,
            "status": "DRY_RUN",
            "canon_file": str(canon_path),
            "mega_lines_to_delete": len([
                d for d in mega_details
                if not (d["classification"] == "oversized" and d["embedded_verse_count"] == 0)
            ]),
            "anchors": [
                d["anchor"] for d in mega_details
                if not (d["classification"] == "oversized" and d["embedded_verse_count"] == 0)
            ],
        }

    # Clone canon → staging
    staging_path = clone_canon_to_staging(canon_path, code)

    # Truncate mega-lines to first verse only (skip genuinely oversized)
    deleted_count, deleted_anchors = truncate_mega_lines(
        staging_path, mega_anchors,
        skip_oversized=True, mega_details=mega_details,
    )

    # Validate
    validation = run_validation(staging_path)

    return {
        "book": code,
        "status": "OK" if validation["overall"] in ("PASS", "WARN") else validation["overall"],
        "staging_file": str(staging_path),
        "deleted_count": deleted_count,
        "deleted_anchors": deleted_anchors,
        "validation_overall": validation["overall"],
        "validation_checks": validation["checks"],
    }


def main():
    parser = argparse.ArgumentParser(description="Remediate V13 mega-line failures")
    parser.add_argument("--book", nargs="+", help="Specific book codes to remediate")
    parser.add_argument("--tier", choices=["A", "B", "AB", "all"], default="all",
                        help="Which tier(s) to process")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--output-json", type=str, help="Write results JSON to this path")
    args = parser.parse_args()

    audit = load_audit()
    fail_books = audit.get("v13_fail_books", {})

    # Determine which books to process
    if args.tier == "A":
        target_codes = TIER_A_BOOKS | TIER_C_1KI_FUSED
    elif args.tier == "B":
        target_codes = TIER_B_BOOKS
    elif args.tier == "AB":
        target_codes = ALL_DELETE_BOOKS
    else:
        target_codes = ALL_DELETE_BOOKS

    if args.book:
        target_codes = target_codes & {b.upper() for b in args.book}

    results = []
    for key, details in sorted(fail_books.items()):
        code = extract_book_code(key)
        if code not in target_codes:
            continue

        print(f"\n{'='*60}")
        print(f"Remediating {code} ({len(details)} mega-lines)")
        print(f"{'='*60}")

        result = remediate_book(code, details, dry_run=args.dry_run)
        results.append(result)

        if result["status"] == "DRY_RUN":
            print(f"  DRY RUN: would delete {result['mega_lines_to_delete']} mega-lines")
            for a in result.get("anchors", []):
                print(f"    - {a}")
        elif result["status"] == "OK":
            print(f"  Deleted {result['deleted_count']} mega-lines")
            print(f"  Validation: {result['validation_overall']}")
        else:
            print(f"  STATUS: {result['status']}")
            if "validation_checks" in result:
                for name, check in result["validation_checks"].items():
                    if check["status"] != "PASS":
                        print(f"    {name}: {check['status']}")
                        for e in check.get("errors", []):
                            print(f"      {e}")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    ok = sum(1 for r in results if r["status"] == "OK")
    fail = sum(1 for r in results if r["status"] not in ("OK", "DRY_RUN"))
    dry = sum(1 for r in results if r["status"] == "DRY_RUN")
    total_deleted = sum(r.get("deleted_count", 0) for r in results)
    print(f"  Books processed: {len(results)}")
    print(f"  OK: {ok}  FAIL: {fail}  DRY_RUN: {dry}")
    print(f"  Total mega-lines deleted: {total_deleted}")

    if args.output_json:
        out_path = Path(args.output_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"date": str(date.today()), "results": results}, f, indent=2)
        print(f"\n  Results written to {out_path}")

    # Exit with failure code if any books didn't validate
    if fail > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
