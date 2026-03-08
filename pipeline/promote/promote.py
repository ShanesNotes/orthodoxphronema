"""
promote.py — Promote a validated staged canon file to canon/

Contract:
  - Reads staging/validated/OT|NT/BOOK.md
  - Runs validate_file(); aborts on errors (including V9 embedded verses)
  - Checks residuals sidecar: V4 coverage, structural blocks, ratification
  - Checks V7 completeness (unless --allow-incomplete)
  - Computes sha256 of body text (everything after the closing ---)
  - Writes to canon/OT|NT/BOOK.md with updated frontmatter:
      promote_date: "YYYY-MM-DD"
      status: promoted
      checksum: "<sha256>"
  - Writes reports/BOOK_promotion_dossier.json on every exit path
  - --dry-run: prints the would-be output without writing
  - --allow-incomplete: allow promotion despite V7 completeness gap

Exit codes:
    0 = promoted (or dry-run success)
    1 = validation errors (V1-V9)
    2 = V7 completeness gate (re-run with --allow-incomplete)
    3 = sidecar gate failure (unratified gaps, structural blocks)

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
from datetime import date, datetime
from pathlib import Path

REPO_ROOT    = Path(__file__).parent.parent.parent
REGISTRY     = REPO_ROOT / "schemas" / "anchor_registry.json"
STAGING_ROOT = REPO_ROOT / "staging" / "validated"
CANON_ROOT   = REPO_ROOT / "canon"
REPORTS_ROOT = REPO_ROOT / "reports"

RE_V4_WARNING = re.compile(
    r'V4\s+Missing verses in ch\.(\d+): jumps from (\d+) to (\d+)'
)


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
    fm = re.sub(
        r'^(promote_date:\s*).*$',
        rf'\g<1>"{promote_date}"',
        fm, flags=re.MULTILINE
    )
    fm = re.sub(
        r'^(status:\s*).*$',
        r'\g<1>promoted',
        fm, flags=re.MULTILINE
    )
    fm = re.sub(
        r'^(checksum:\s*).*$',
        rf'\g<1>"{checksum}"',
        fm, flags=re.MULTILINE
    )
    return fm


# ── Dossier ──────────────────────────────────────────────────────────────────

def generate_dossier(book_code: str, testament: str,
                     errors: list[str], warnings: list[str],
                     sidecar: dict | None, body_checksum: str,
                     registry_version: str, decision: str) -> dict:
    """Build promotion dossier dict."""
    all_msgs = [(m, "error") for m in errors] + [(m, "warning") for m in warnings]
    validation = {}
    for cn in ("V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9"):
        msgs = [m for m, _ in all_msgs if m.startswith(cn)]
        has_err = any(t == "error" for m, t in all_msgs if m.startswith(cn))
        has_warn = any(t == "warning" for m, t in all_msgs if m.startswith(cn))
        if has_err:
            status = "FAIL"
        elif has_warn:
            status = "WARN"
        else:
            status = "PASS"
        validation[cn] = {"status": status, "messages": msgs}

    return {
        "book_code": book_code,
        "testament": testament,
        "timestamp": datetime.now().isoformat(),
        "registry_version": registry_version,
        "body_checksum": body_checksum,
        "validation": validation,
        "residuals_sidecar": sidecar,
        "decision": decision,
    }


def write_dossier(dossier: dict) -> Path:
    """Write to reports/BOOK_promotion_dossier.json."""
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    path = REPORTS_ROOT / f"{dossier['book_code']}_promotion_dossier.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dossier, f, indent=2)
    print(f"\n[dossier] Written: {path}")
    return path


# ── Promotion logic ──────────────────────────────────────────────────────────

def promote_book(book_code: str, dry_run: bool = False,
                 allow_incomplete: bool = False) -> None:
    registry  = load_registry()
    registry_version = registry.get("registry_version", "unknown")
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

    # ── Compute checksum early (needed by dossier at all exit points) ─────────
    text        = staged_path.read_text(encoding="utf-8")
    fm_block, body = split_frontmatter(text)
    body_checksum = sha256_hex(body) if fm_block else ""

    # ── Load sidecar ──────────────────────────────────────────────────────────
    sidecar_path = STAGING_ROOT / testament / f"{book_code}_residuals.json"
    sidecar: dict | None = None
    if sidecar_path.exists():
        with open(sidecar_path, encoding="utf-8") as f:
            sidecar = json.load(f)

    def _exit_with_dossier(decision: str, exit_code: int) -> None:
        dossier = generate_dossier(
            book_code, testament, errors, warnings, sidecar,
            body_checksum, registry_version, decision
        )
        write_dossier(dossier)
        sys.exit(exit_code)

    # ── Error gate (V1-V9) ────────────────────────────────────────────────────
    if errors:
        print(f"\n  ERRORS ({len(errors)}) — promotion aborted:")
        for e in errors:
            print(f"    {e}")
        _exit_with_dossier("blocked", 1)

    # ── Sidecar gate (V4 coverage + structural block + ratification) ──────────
    v4_missing: set[str] = set()
    for w in warnings:
        m = RE_V4_WARNING.match(w)
        if m:
            ch, from_v, to_v = int(m.group(1)), int(m.group(2)), int(m.group(3))
            for v in range(from_v + 1, to_v):
                v4_missing.add(f"{book_code}.{ch}:{v}")

    if v4_missing:
        if sidecar is None:
            print(f"\n  BLOCKED: {len(v4_missing)} V4 gap(s) with no residuals sidecar.")
            print("  Create a _residuals.json sidecar to document these gaps.")
            _exit_with_dossier("blocked", 3)

        sidecar_anchors = {r["anchor"] for r in sidecar.get("residuals", [])}
        uncovered = v4_missing - sidecar_anchors
        if uncovered:
            print(f"\n  BLOCKED: {len(uncovered)} V4 gap(s) not covered by residuals sidecar:")
            for a in sorted(uncovered):
                print(f"    {a}")
            _exit_with_dossier("blocked", 3)

        blocking_entries = [
            r for r in sidecar.get("residuals", [])
            if r.get("blocking") and r["anchor"] in v4_missing
        ]
        if blocking_entries:
            print(f"\n  BLOCKED: {len(blocking_entries)} structural issue(s) flagged as blocking:")
            for r in blocking_entries:
                print(f"    {r['anchor']}: {r['description']}")
            _exit_with_dossier("blocked", 3)

        if sidecar.get("ratified_date") is None:
            # Non-blocking gaps with null ratification: warn but allow
            has_blocking = any(r.get("blocking") for r in sidecar.get("residuals", []))
            if has_blocking:
                print("\n  BLOCKED: Residuals sidecar not yet ratified by human.")
                _exit_with_dossier("blocked", 3)
            else:
                print("\n  INFO: Residuals sidecar not yet ratified (all entries non-blocking; proceeding).")

        # ── Per-entry ratification for source-absence entries ──────────
        # Source-absence residuals (osb_*) are policy decisions requiring
        # individual human acknowledgment — top-level ratified_date alone
        # is not sufficient for these entries.
        if sidecar is not None:
            for r in sidecar.get("residuals", []):
                cls = r.get("classification", "")
                if cls.startswith("osb_") and not r.get("ratified"):
                    anchor = r.get("anchor", "?")
                    print(f"\n  BLOCKED: Source-absence residual {anchor} requires explicit per-entry ratification")
                    _exit_with_dossier("blocked", 3)

    # ── V7 completeness gate ──────────────────────────────────────────────────
    v7_warnings = [w for w in warnings if w.startswith("V7")]
    if v7_warnings and not allow_incomplete:
        print(f"\n  BLOCKED ({len(v7_warnings)} completeness issue(s)):")
        for w in v7_warnings:
            print(f"    {w}")
        print("\n  Re-run with --allow-incomplete to acknowledge and proceed.")
        _exit_with_dossier("blocked", 2)

    # ── Build promoted content ────────────────────────────────────────────────
    if not fm_block:
        print("ERROR: No frontmatter found in staged file.", file=sys.stderr)
        sys.exit(1)

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
        decision = "dry-run"
    else:
        canon_path.parent.mkdir(parents=True, exist_ok=True)
        canon_path.write_text(promoted_text, encoding="utf-8")
        print(f"\n[promote] Written: {canon_path}")
        print(f"[promote] Checksum: {body_checksum}")
        print("[promote] Done.")
        decision = "promoted"

    dossier = generate_dossier(
        book_code, testament, errors, warnings, sidecar,
        body_checksum, registry_version, decision
    )
    write_dossier(dossier)


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
