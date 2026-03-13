#!/usr/bin/env python3
"""
split_fused_footnote_headers.py
───────────────────────────────
Splits fused section headers in OT footnote files.

Problem:  ~52% of `### CH:V` section headers are fused inline with preceding
text (not on their own line):

    ...text here. ### 1:2
    *(anchor: GEN.1:2)*

Should be:

    ...text here.

    ### 1:2
    *(anchor: GEN.1:2)*

Safety invariant: anchor count before == anchor count after.

CLI:
    --dry-run   (default) report fused header counts per file, total
    --apply     actually write changes
    --book BOOK process a single book (e.g. GEN)
"""

from __future__ import annotations

import argparse
import re
import sys as _sys
from pathlib import Path as _Path

# ── Boilerplate: find repo root and import paths ──────────────────────────
_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists():
    _R = _R.parent
if str(_R) not in _sys.path:
    _sys.path.insert(0, str(_R))

from pipeline.common.paths import STAGING_ROOT

# ── Constants ─────────────────────────────────────────────────────────────

OT_DIR = STAGING_ROOT / "OT"
NT_DIR = STAGING_ROOT / "NT"

# Regex: any non-newline character immediately before `### \d+:\d+`
# This captures the preceding char and the header so we can insert \n\n between.
FUSED_HEADER_RE = re.compile(r"([^\n])(### \d+:\d+(?:-\d+)?)")

# Anchor pattern for safety counting
ANCHOR_RE = re.compile(r"\(anchor: [A-Z0-9]+\.\d+:\d+\)")


def count_anchors(text: str) -> int:
    """Count anchor patterns in text."""
    return len(ANCHOR_RE.findall(text))


def count_fused(text: str) -> int:
    """Count fused headers in text (headers not at start of line)."""
    return len(FUSED_HEADER_RE.findall(text))


def split_fused_headers(text: str) -> str:
    """Insert \\n\\n before fused ### headers so they start on their own line."""
    return FUSED_HEADER_RE.sub(r"\1\n\n\2", text)


def split_frontmatter(text: str) -> tuple[str, str]:
    """Split YAML frontmatter from body. Returns (frontmatter_with_fences, body)."""
    if text.startswith("---"):
        # Find the closing ---
        end = text.find("---", 3)
        if end != -1:
            end += 3  # include the closing ---
            return text[:end], text[end:]
    return "", text


def process_file(path: _Path, apply: bool) -> int:
    """Process a single footnote file. Returns count of fused headers found/fixed."""
    text = path.read_text(encoding="utf-8")

    frontmatter, body = split_frontmatter(text)
    fused_count = count_fused(body)

    if fused_count == 0:
        return 0

    if not apply:
        return fused_count

    # Safety: count anchors before
    anchors_before = count_anchors(text)

    # Apply fix to body only (leave frontmatter untouched)
    fixed_body = split_fused_headers(body)
    fixed_text = frontmatter + fixed_body

    # Safety: count anchors after
    anchors_after = count_anchors(fixed_text)
    if anchors_before != anchors_after:
        print(
            f"  SAFETY ABORT {path.name}: anchors before={anchors_before} after={anchors_after}",
            file=_sys.stderr,
        )
        return -1

    path.write_text(fixed_text, encoding="utf-8")
    return fused_count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split fused section headers in OT footnote files."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Report fused header counts without modifying files (default).",
    )
    mode.add_argument(
        "--apply",
        action="store_true",
        help="Actually write changes to files.",
    )
    parser.add_argument(
        "--book",
        type=str,
        default=None,
        help="Process a single book code (e.g. GEN).",
    )
    args = parser.parse_args()
    apply = args.apply

    # ── Gather OT footnote files ──────────────────────────────────────────
    if args.book:
        ot_files = sorted(OT_DIR.glob(f"{args.book.upper()}_footnotes.md"))
        if not ot_files:
            print(f"No OT footnote file found for book: {args.book}")
            _sys.exit(1)
    else:
        ot_files = sorted(OT_DIR.glob("*_footnotes.md"))

    # ── Process OT files ──────────────────────────────────────────────────
    total_fused = 0
    files_affected = 0
    action = "Fixed" if apply else "Found"

    print(f"\n{'=' * 60}")
    print(f"  OT Footnote Fused-Header {'Fix' if apply else 'Audit'}")
    print(f"{'=' * 60}\n")

    for fp in ot_files:
        n = process_file(fp, apply=apply)
        if n < 0:
            _sys.exit(1)
        if n > 0:
            book = fp.name.replace("_footnotes.md", "")
            print(f"  {book:6s}  {action} {n:4d} fused headers")
            total_fused += n
            files_affected += 1

    print(f"\n  {'─' * 40}")
    print(f"  Total: {total_fused} fused headers in {files_affected}/{len(ot_files)} files")
    if not apply:
        print("  (dry-run — no files modified)")
    print()

    # ── NT validation (only in full-run mode) ─────────────────────────────
    if not args.book:
        nt_files = sorted(NT_DIR.glob("*_footnotes.md"))
        nt_fused = 0
        for fp in nt_files:
            text = fp.read_text(encoding="utf-8")
            _, body = split_frontmatter(text)
            nt_fused += count_fused(body)

        print(f"  NT validation: {len(nt_files)} files checked, {nt_fused} fused headers")
        if nt_fused == 0:
            print("  NT is clean — no fused headers found.")
        else:
            print(f"  WARNING: NT has {nt_fused} fused headers!", file=_sys.stderr)
        print()


if __name__ == "__main__":
    main()
