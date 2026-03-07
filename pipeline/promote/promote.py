"""
promote.py — Promote a validated staged canon file to canon/

Contract:
  - Reads staging/validated/OT|NT/BOOK.md
  - Runs validate_file(); aborts on errors OR completeness gap (unless --allow-incomplete)
  - Computes sha256 of body text (everything after the closing ---)
  - Writes to canon/OT|NT/BOOK.md with updated frontmatter:
      promote_date: "YYYY-MM-DD"
      status: promoted
      checksum: "<sha256>"
  - --dry-run: prints the would-be output without writing
  - --allow-incomplete: allow promotion despite V7 completeness gap (explicit acknowledgment required)

Usage:
    python3 pipeline/promote/promote.py --book GEN
    python3 pipeline/promote/promote.py --book GEN --dry-run
    python3 pipeline/promote/promote.py --book GEN --allow-incomplete
    python3 pipeline/promote/promote.py --book GEN --dry-run --allow-incomplete
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT    = Path(__file__).parent.parent.parent
REGISTRY     = REPO_ROOT / "schemas" / "anchor_registry.json"
STAGING_ROOT = REPO_ROOT / "staging" / "validated"
CANON_ROOT   = REPO_ROOT / "canon"


def load_validate_file():
    """Dynamically import validate_file from pipeline/validate/validate_canon.py."""
    validate_path = REPO_ROOT / "pipeline" / "validate" / "validate_canon.py"
    spec = importlib.util.spec_from_file_location("validate_canon", validate_path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.validate_file


def load_registry() -> dict:
    with open(REGISTRY, encoding="utf-8") as f:
        return json.load(f)


def book_testament(registry: dict, book_code: str) -> str:
    """Return 'OT' or 'NT' for the given book code."""
    for b in registry["books"]:
        if b["code"] == book_code:
            return b["testament"]
    raise ValueError(f"Book code {book_code!r} not found in registry")


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_frontmatter(text: str) -> tuple[str, str]:
    """
    Split a Markdown file into (frontmatter_block, body_text).
    frontmatter_block includes the opening and closing ---.
    body_text is everything after the closing ---.
    Returns ("", text) if no frontmatter delimiters found.
    """
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return "", text

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return "", text

    fm_block = "".join(lines[:end_idx + 1])
    body     = "".join(lines[end_idx + 1:])
    return fm_block, body


def update_frontmatter(fm_block: str, promote_date: str, checksum: str) -> str:
    """
    Replace promote_date, status, and checksum fields in the frontmatter block.
    """
    fm = fm_block
    # promote_date
    fm = re.sub(
        r'^(promote_date:\s*).*$',
        rf'\g<1>"{promote_date}"',
        fm, flags=re.MULTILINE
    )
    # status
    fm = re.sub(
        r'^(status:\s*).*$',
        r'\g<1>promoted',
        fm, flags=re.MULTILINE
    )
    # checksum
    fm = re.sub(
        r'^(checksum:\s*).*$',
        rf'\g<1>"{checksum}"',
        fm, flags=re.MULTILINE
    )
    return fm


def promote_book(book_code: str, dry_run: bool = False,
                 allow_incomplete: bool = False) -> None:
    registry  = load_registry()
    testament = book_testament(registry, book_code)

    staged_path = STAGING_ROOT / testament / f"{book_code}.md"
    canon_path  = CANON_ROOT / testament / f"{book_code}.md"

    if not staged_path.exists():
        print(f"ERROR: Staged file not found: {staged_path}", file=sys.stderr)
        sys.exit(1)

    # ── Validate ──────────────────────────────────────────────────────────────
    print(f"\nValidating: {staged_path}\n{'─' * 60}")
    validate_file = load_validate_file()
    errors, warnings = validate_file(staged_path, strict=False)

    if warnings:
        print(f"\n  WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"    {w}")

    if errors:
        print(f"\n  ERRORS ({len(errors)}) — promotion aborted:")
        for e in errors:
            print(f"    {e}")
        sys.exit(1)

    # ── V7 completeness gate ──────────────────────────────────────────────────
    v7_warnings = [w for w in warnings if w.startswith("V7")]
    if v7_warnings and not allow_incomplete:
        print(f"\n  BLOCKED ({len(v7_warnings)} completeness issue(s)):")
        for w in v7_warnings:
            print(f"    {w}")
        print("\n  Re-run with --allow-incomplete to acknowledge and proceed.")
        sys.exit(2)

    # ── Compute checksum and build promoted content ───────────────────────────
    text        = staged_path.read_text(encoding="utf-8")
    fm_block, body = split_frontmatter(text)

    if not fm_block:
        print("ERROR: No frontmatter found in staged file.", file=sys.stderr)
        sys.exit(1)

    body_checksum  = sha256_hex(body)
    today          = str(date.today())
    updated_fm     = update_frontmatter(fm_block, promote_date=today, checksum=body_checksum)
    promoted_text  = updated_fm + body

    # ── Write or dry-run ──────────────────────────────────────────────────────
    if dry_run:
        print(f"\n[dry-run] Would write: {canon_path}")
        print(f"[dry-run] Checksum   : {body_checksum}")
        print(f"[dry-run] Promote date: {today}")
        print("\n── Promoted content preview (first 40 lines) ──")
        for line in promoted_text.splitlines()[:40]:
            print(line)
        print("\n[dry-run] Done. No files written.")
        return

    canon_path.parent.mkdir(parents=True, exist_ok=True)
    canon_path.write_text(promoted_text, encoding="utf-8")
    print(f"\n[promote] Written: {canon_path}")
    print(f"[promote] Checksum: {body_checksum}")
    print("[promote] Done.\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Promote a validated staged canon file to canon/."
    )
    parser.add_argument("--book", required=True, help="Book code, e.g. GEN")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print would-be output without writing files"
    )
    parser.add_argument(
        "--allow-incomplete", action="store_true",
        help="Allow promotion despite V7 completeness gap (requires explicit acknowledgment)"
    )
    args = parser.parse_args()

    promote_book(args.book.upper(), dry_run=args.dry_run,
                 allow_incomplete=args.allow_incomplete)


if __name__ == "__main__":
    main()
