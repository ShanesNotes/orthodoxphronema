#!/usr/bin/env python3
"""
proofread.py — Thin wrapper delegating to text-cleaner/scripts/clean.py.

This script preserves backward compatibility for existing callers while
the canonical implementation now lives in the text-cleaner skill.

All P1-P8 detection logic is handled by clean.py with --profile canon.

Usage (same interface as before):
    python3 proofread.py --file canon/OT/01_GEN.md --dry-run
    python3 proofread.py --scope all --dry-run --report-dir reports/proofread/
    python3 proofread.py --scope all --apply --report-dir reports/proofread/
    python3 proofread.py --scope all --include-staging --dry-run
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_THIS = Path(__file__).resolve().parent
_REPO = _THIS
while _REPO != _REPO.parent and not (_REPO / "pipeline" / "__init__.py").exists():
    _REPO = _REPO.parent

CLEAN_PY = _REPO / "skills" / "text-cleaner" / "scripts" / "clean.py"

# Scope translation: proofread.py scopes → clean.py scopes
SCOPE_MAP = {
    "all": "canon",
    "canon": "canon",
    "staging": "staging",
}


def main():
    parser = argparse.ArgumentParser(
        description="Multi-pass proofreader (delegates to text-cleaner/clean.py)."
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--file", type=Path, help="Single file to proofread")
    target.add_argument("--scope", choices=["all", "canon", "staging"],
                        help="Scope: all, canon, or staging")

    parser.add_argument("--include-staging", action="store_true",
                        help="Include staging files (with --scope all)")
    parser.add_argument("--pass", dest="passes", action="append",
                        choices=["regex", "spell", "all"],
                        help="Which passes to run (default: all)")
    parser.add_argument("--apply", action="store_true",
                        help="Apply auto-fixable corrections in place")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Report only, no file changes (default)")
    parser.add_argument("--report-dir", type=Path,
                        default=_REPO / "reports" / "proofread",
                        help="Directory for JSON reports")
    parser.add_argument("--memo", action="store_true",
                        help="Also write an Ezra audit memo")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")

    args = parser.parse_args()

    # Build clean.py command
    cmd = [sys.executable, str(CLEAN_PY), "--profile", "canon"]

    if args.file:
        cmd.extend(["--file", str(args.file)])
    elif args.scope:
        mapped = SCOPE_MAP.get(args.scope, args.scope)
        cmd.extend(["--scope", mapped])

    if args.passes:
        for p in args.passes:
            cmd.extend(["--pass", p])

    if args.apply:
        cmd.append("--apply")

    if args.json:
        cmd.append("--json")

    cmd.extend(["--report-dir", str(args.report_dir)])

    print(f"Delegating to text-cleaner: {' '.join(cmd[1:])}", file=sys.stderr)
    result = subprocess.run(cmd, check=False)

    # Handle --include-staging: run a second pass on staging
    if args.include_staging and args.scope in ("all", None):
        staging_cmd = [
            sys.executable, str(CLEAN_PY),
            "--profile", "staging",
            "--scope", "staging",
            "--report-dir", str(args.report_dir),
        ]
        if args.passes:
            for p in args.passes:
                staging_cmd.extend(["--pass", p])
        if args.apply:
            staging_cmd.append("--apply")
        if args.json:
            staging_cmd.append("--json")

        print(f"\nDelegating staging pass: {' '.join(staging_cmd[1:])}",
              file=sys.stderr)
        staging_result = subprocess.run(staging_cmd, check=False)
        # Use worst exit code
        result.returncode = max(result.returncode, staging_result.returncode)

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
