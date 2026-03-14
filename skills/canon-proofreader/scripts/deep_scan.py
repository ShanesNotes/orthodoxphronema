#!/usr/bin/env python3
"""
deep_scan.py — Thin wrapper delegating to text-cleaner/scripts/scan.py.

This script preserves backward compatibility for existing callers while
the canonical implementation now lives in the text-cleaner skill.

All D1-D6 detection logic is handled by scan.py with --profile canon.

Usage (same interface as before):
    python3 deep_scan.py --file canon/OT/01_GEN.md
    python3 deep_scan.py --scope canon
    python3 deep_scan.py --scope canon --json
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

SCAN_PY = _REPO / "skills" / "text-cleaner" / "scripts" / "scan.py"

CANON_OT = _REPO / "canon" / "OT"
CANON_NT = _REPO / "canon" / "NT"


def main():
    parser = argparse.ArgumentParser(
        description="Deep per-book scanner (delegates to text-cleaner/scan.py)."
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--file", type=Path, help="Single file")
    target.add_argument("--scope", choices=["canon", "ot", "nt"])
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    cmd = [sys.executable, str(SCAN_PY), "--profile", "canon"]

    if args.file:
        cmd.extend(["--file", str(args.file)])
    elif args.scope == "ot":
        cmd.extend(["--dir", str(CANON_OT)])
    elif args.scope == "nt":
        cmd.extend(["--dir", str(CANON_NT)])
    else:
        # --scope canon: scan both OT and NT
        cmd.extend(["--dir", str(_REPO / "canon")])

    if args.json:
        cmd.append("--json")

    print(f"Delegating to text-cleaner: {' '.join(cmd[1:])}", file=sys.stderr)
    result = subprocess.run(cmd, check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
