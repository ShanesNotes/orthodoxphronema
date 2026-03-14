#!/usr/bin/env python3
"""
fix_fused_markers.py — Thin wrapper delegating to text-cleaner/scripts/fix.py.

This script preserves backward compatibility for existing callers while
the canonical implementation now lives in the text-cleaner skill.

The curated replacement map (211 tokens) has been migrated to fix.py's
profile-driven replacement map system.

Usage (same interface as before):
    python3 fix_fused_markers.py --scope canon --dry-run
    python3 fix_fused_markers.py --scope canon
    python3 fix_fused_markers.py --file canon/OT/01_GEN.md --dry-run
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

FIX_PY = _REPO / "skills" / "text-cleaner" / "scripts" / "fix.py"

CANON_OT = _REPO / "canon" / "OT"
CANON_NT = _REPO / "canon" / "NT"


def main():
    parser = argparse.ArgumentParser(
        description="Fix fused footnote markers (delegates to text-cleaner/fix.py)."
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Show fixes without applying")
    parser.add_argument("--file", type=Path, help="Single file to fix")
    parser.add_argument("--scope", choices=["canon", "ot", "nt"])
    args = parser.parse_args()

    cmd = [sys.executable, str(FIX_PY), "--profile", "canon"]

    if args.file:
        cmd.extend(["--file", str(args.file)])
    elif args.scope == "ot":
        cmd.extend(["--dir", str(CANON_OT)])
    elif args.scope == "nt":
        cmd.extend(["--dir", str(CANON_NT)])
    else:
        cmd.extend(["--dir", str(_REPO / "canon")])

    if args.dry_run:
        cmd.append("--dry-run")

    print(f"Delegating to text-cleaner: {' '.join(cmd[1:])}", file=sys.stderr)
    result = subprocess.run(cmd, check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
