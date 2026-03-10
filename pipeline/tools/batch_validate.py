"""
batch_validate.py — Run structured validation on all staged books, print summary table.

Usage:
    python3 pipeline/tools/batch_validate.py
    python3 pipeline/tools/batch_validate.py --book GEN EXO LEV
    python3 pipeline/tools/batch_validate.py --strict
    python3 pipeline/tools/batch_validate.py --output-json reports/batch_validation.json
    python3 pipeline/tools/batch_validate.py --from-cvc-report reports/cvc_report.json
"""

from __future__ import annotations

import argparse
import json
import sys
import re
from pathlib import Path

import sys as _sys; from pathlib import Path as _Path
_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists(): _R = _R.parent
if str(_R) not in _sys.path: _sys.path.insert(0, str(_R))
from pipeline.common.paths import REPO_ROOT
from pipeline.common.text import discover_staged_paths


def _load_run_validation():
    """Import run_validation from validate_canon."""
    from pipeline.validate.validate_canon import run_validation
    return run_validation


def discover_staged_books(book_filter: list[str] | None = None) -> list[Path]:
    """Find all staged .md files (excluding *_notes.md)."""
    return discover_staged_paths(book_filter)


def count_verses(path: Path) -> int:
    """Count anchor lines in a staged file."""
    re_anchor = re.compile(r'^[A-Z0-9]+\.\d+:\d+\s')
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if re_anchor.match(line):
            count += 1
    return count


def extract_v7_pct(v7_result) -> str:
    """Extract V7 percentage from structured V7 data."""
    if v7_result is None:
        return "n/a"
    pct = v7_result.data.get("pct")
    if pct is None:
        return "n/a"
    return f"{pct:.1f}%"


def main():
    parser = argparse.ArgumentParser(
        description="Batch validate all staged books."
    )
    parser.add_argument(
        "--book", nargs="*", metavar="CODE",
        help="Book code(s) to validate. Default: all."
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Treat warnings as errors."
    )
    parser.add_argument(
        "--output-json", metavar="FILE",
        help="Write structured JSON report."
    )
    parser.add_argument(
        "--from-cvc-report", metavar="FILE",
        help="Read affected books from CVC report JSON."
    )
    args = parser.parse_args()

    book_filter = [b.upper() for b in args.book] if args.book else None

    # If --from-cvc-report, extract affected books
    if args.from_cvc_report:
        with open(args.from_cvc_report, encoding="utf-8") as f:
            cvc_report = json.load(f)
        affected = cvc_report.get("affected_books", [])
        if book_filter:
            book_filter = [b for b in book_filter if b in affected]
        else:
            book_filter = affected

    run_validation = _load_run_validation()
    paths = discover_staged_books(book_filter)

    if not paths:
        print("No staged books found.")
        sys.exit(0)

    results = []
    any_errors = False

    for path in paths:
        code = path.stem
        validation = run_validation(path, strict=args.strict)
        errors = validation.errors
        warnings = validation.warnings

        verses = count_verses(path)
        v7_pct = extract_v7_pct(validation.check("V7"))
        statuses = validation.status_map

        if errors:
            any_errors = True

        results.append({
            "book": code,
            "verses": verses,
            "v7_pct": v7_pct,
            "errors": len(errors),
            "warnings": len(warnings),
            "statuses": statuses,
            "error_messages": errors,
            "warning_messages": warnings,
        })

    # Print summary table
    check_cols = ["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9",
                  "V10", "V11", "V12"]
    header = f"{'BOOK':4s} | {'Verses':>6s} | {'V7%':>7s} | {'Warn':>4s} | {'Err':>3s} | " + " ".join(f"{c:4s}" for c in check_cols)
    print(f"\nBatch Validation Summary ({len(results)} books)")
    print("=" * len(header))
    print(header)
    print("-" * len(header))

    for r in results:
        status_str = " ".join(
            f"{'OK' if r['statuses'].get(c) == 'PASS' else r['statuses'].get(c, '?'):4s}"
            for c in check_cols
        )
        print(
            f"{r['book']:4s} | {r['verses']:6d} | {r['v7_pct']:>7s} | "
            f"{r['warnings']:4d} | {r['errors']:3d} | {status_str}"
        )

    print("=" * len(header))
    total_err = sum(r["errors"] for r in results)
    total_warn = sum(r["warnings"] for r in results)
    print(f"Total: {len(results)} books, {total_err} errors, {total_warn} warnings")

    if args.output_json:
        out_path = Path(args.output_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"books": results}, f, indent=2)
        print(f"\nJSON report written: {out_path}")

    sys.exit(1 if any_errors else 0)


if __name__ == "__main__":
    main()
