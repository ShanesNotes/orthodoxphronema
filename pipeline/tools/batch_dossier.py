"""
batch_dossier.py — Run promote.py --dry-run --allow-incomplete for all staged books.

Refreshes promotion dossiers and prints a summary table.

Usage:
    python3 pipeline/tools/batch_dossier.py
    python3 pipeline/tools/batch_dossier.py --book GEN EXO LEV
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import sys as _sys; from pathlib import Path as _Path
_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists(): _R = _R.parent
if str(_R) not in _sys.path: _sys.path.insert(0, str(_R))
from pipeline.common.paths import REPO_ROOT, STAGING_ROOT, REPORTS_ROOT
from pipeline.common.text import discover_staged_books

PROMOTE_SCRIPT = REPO_ROOT / "pipeline" / "promote" / "promote.py"


def run_dossier(code: str) -> dict:
    """Run promote.py --dry-run --allow-incomplete for a book, return result."""
    result = subprocess.run(
        [sys.executable, str(PROMOTE_SCRIPT),
         "--book", code, "--dry-run", "--allow-incomplete"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )

    dossier_path = REPORTS_ROOT / f"{code}_promotion_dossier.json"
    dossier = None
    if dossier_path.exists():
        with open(dossier_path, encoding="utf-8") as f:
            dossier = json.load(f)

    return {
        "code": code,
        "exit_code": result.returncode,
        "dossier": dossier,
        "stderr": result.stderr.strip() if result.stderr else None,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Batch refresh promotion dossiers for all staged books."
    )
    parser.add_argument(
        "--book", nargs="*", metavar="CODE",
        help="Book code(s) to process. Default: all."
    )
    args = parser.parse_args()

    all_codes = discover_staged_books()
    if args.book:
        book_filter = {b.upper() for b in args.book}
        codes = [c for c in all_codes if c in book_filter]
    else:
        codes = all_codes

    if not codes:
        print("No staged books found.")
        sys.exit(0)

    results = []
    for code in codes:
        print(f"  Processing {code}...", end=" ", flush=True)
        r = run_dossier(code)
        results.append(r)
        decision = r["dossier"]["decision"] if r["dossier"] else "ERROR"
        print(decision)

    # Print summary table
    header = f"{'BOOK':4s} | {'Decision':12s} | {'V7%':>7s} | Blockers"
    print(f"\nBatch Dossier Summary ({len(results)} books)")
    print("=" * 70)
    print(header)
    print("-" * 70)

    for r in results:
        d = r["dossier"]
        if not d:
            print(f"{r['code']:4s} | {'ERROR':12s} | {'?':>7s} | promote.py failed (exit {r['exit_code']})")
            continue

        decision = d.get("decision", "?")
        v7_info = d.get("validation", {}).get("V7", {})
        v7_msgs = v7_info.get("messages", [])
        v7_pct = "100.0%"
        for m in v7_msgs:
            import re
            pct_m = re.search(r'\((\d+\.\d+)%\)', m)
            if pct_m:
                v7_pct = pct_m.group(1) + "%"
                break

        # Collect blockers (FAIL checks)
        blockers = []
        for check, info in d.get("validation", {}).items():
            if info.get("status") == "FAIL":
                blockers.append(check)

        blocker_str = ", ".join(blockers) if blockers else "-"
        print(f"{r['code']:4s} | {decision:12s} | {v7_pct:>7s} | {blocker_str}")

    print("=" * 70)
    sys.exit(0)


if __name__ == "__main__":
    main()
