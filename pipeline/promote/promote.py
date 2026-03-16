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

from pipeline.common.registry import classifications_requiring_entry_ratification
from pipeline.promote.gates import (
    gate_absorbed_content,
    gate_completeness,
    gate_editorial,
    gate_errors,
    gate_freshness,
    gate_ratification,
    gate_sidecar_fields,
    gate_v4_coverage,
)

REPO_ROOT    = Path(__file__).parent.parent.parent
REGISTRY     = REPO_ROOT / "schemas" / "anchor_registry.json"
RESIDUAL_CLASSES = REPO_ROOT / "schemas" / "residual_classes.json"
STAGING_ROOT = REPO_ROOT / "staging" / "validated"
CANON_ROOT   = REPO_ROOT / "canon"

from pipeline.common.paths import canon_filepath
REPORTS_ROOT = REPO_ROOT / "reports"


def load_validate_module():
    """Dynamically import pipeline/validate/validate_canon.py."""
    validate_path = REPO_ROOT / "pipeline" / "validate" / "validate_canon.py"
    spec = importlib.util.spec_from_file_location("validate_canon", validate_path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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
    Replace or inject promote_date, status, and checksum fields in the frontmatter block.
    """
    fm = fm_block

    def _inject_before_closing(block: str, field_line: str) -> str:
        """Insert a field line just before the closing --- delimiter."""
        lines = block.splitlines(keepends=True)
        # Find the last --- line
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip() == "---":
                lines.insert(i, field_line + "\n")
                return "".join(lines)
        # Fallback: append
        return block.rstrip("\n") + "\n" + field_line + "\n"

    # promote_date
    if re.search(r'^promote_date:', fm, re.MULTILINE):
        fm = re.sub(r'^(promote_date:\s*).*$', rf'\g<1>"{promote_date}"', fm, flags=re.MULTILINE)
    else:
        fm = _inject_before_closing(fm, f'promote_date: "{promote_date}"')

    # checksum
    if re.search(r'^checksum:', fm, re.MULTILINE):
        fm = re.sub(r'^(checksum:\s*).*$', rf'\g<1>"{checksum}"', fm, flags=re.MULTILINE)
    else:
        fm = _inject_before_closing(fm, f'checksum: "{checksum}"')

    # status (should always exist, but inject if missing)
    if re.search(r'^status:', fm, re.MULTILINE):
        fm = re.sub(r'^(status:\s*).*$', r'\g<1>promoted', fm, flags=re.MULTILINE)
    else:
        fm = _inject_before_closing(fm, 'status: promoted')

    return fm


# ── Dossier ──────────────────────────────────────────────────────────────────

def generate_dossier(book_code: str, testament: str,
                     errors: list[str], warnings: list[str],
                     sidecar: dict | None, body_checksum: str,
                     registry_version: str, decision: str,
                     allow_incomplete: bool = False,
                     staged_path: Path | None = None,
                     residuals_path: Path | None = None,
                     editorial_candidates_path: Path | None = None,
                     validation_result=None) -> dict:
    """Build promotion dossier dict."""
    validation: dict[str, dict[str, object]] = {}

    if validation_result is not None:
        for check in validation_result.checks:
            if check.name.startswith("V") and check.name[1:].isdigit():
                validation[check.name] = {
                    "status": check.status,
                    "messages": check.messages,
                }
    else:
        all_msgs = [(m, "error") for m in errors] + [(m, "warning") for m in warnings]

        def _is_check_msg(msg: str, check_name: str) -> bool:
            return msg.startswith(f"{check_name} ")

        for cn in [f"V{i}" for i in range(1, 14)]:
            msgs = [m for m, _ in all_msgs if _is_check_msg(m, cn)]
            has_err = any(t == "error" for m, t in all_msgs if _is_check_msg(m, cn))
            has_warn = any(t == "warning" for m, t in all_msgs if _is_check_msg(m, cn))
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
        "allow_incomplete": allow_incomplete,
        "staged_path": str(staged_path) if staged_path else None,
        "residuals_path": str(residuals_path) if residuals_path else None,
        "editorial_candidates_path": (
            str(editorial_candidates_path) if editorial_candidates_path else None
        ),
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
    canon_path  = canon_filepath(testament, book_code)
    dossier_path = REPORTS_ROOT / f"{book_code}_promotion_dossier.json"
    residuals_path = STAGING_ROOT / testament / f"{book_code}_residuals.json"
    editorial_candidates_path = (
        STAGING_ROOT / testament / f"{book_code}_editorial_candidates.json"
    )

    if not staged_path.exists():
        print(f"ERROR: Staged file not found: {staged_path}", file=sys.stderr)
        sys.exit(1)

    # ── Validate ──────────────────────────────────────────────────────────────
    print(f"\nValidating: {staged_path}\n{'─' * 60}")
    validate_mod = load_validate_module()
    validation_result = validate_mod.run_validation(staged_path, strict=False)
    errors = validation_result.errors
    warnings = validation_result.warnings

    if warnings:
        print(f"\n  WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"    {w}")

    # ── Compute checksum early (needed by dossier at all exit points) ─────────
    text        = staged_path.read_text(encoding="utf-8")
    fm_block, body = split_frontmatter(text)
    body_checksum = sha256_hex(body) if fm_block else ""

    # ── Load sidecar ──────────────────────────────────────────────────────────
    sidecar: dict | None = None
    if residuals_path.exists():
        with open(residuals_path, encoding="utf-8") as f:
            sidecar = json.load(f)
        # Normalize legacy bare-list sidecars into canonical dict form
        if isinstance(sidecar, list):
            sidecar = {"residuals": sidecar}

    ratified_classes = classifications_requiring_entry_ratification(
        Path(RESIDUAL_CLASSES)
    )

    def _exit_with_dossier(decision: str, exit_code: int) -> None:
        dossier = generate_dossier(
            book_code, testament, errors, warnings, sidecar,
            body_checksum, registry_version, decision,
            allow_incomplete=allow_incomplete,
            staged_path=staged_path,
            residuals_path=residuals_path if residuals_path.exists() else None,
            editorial_candidates_path=(
                editorial_candidates_path if editorial_candidates_path.exists() else None
            ),
            validation_result=validation_result,
        )
        write_dossier(dossier)
        sys.exit(exit_code)

    gate_sequence = [
        gate_errors(errors),
        gate_editorial(editorial_candidates_path),
        gate_freshness(dossier_path, body_checksum, dry_run),
        gate_sidecar_fields(sidecar),
        gate_v4_coverage(validation_result.check("V4"), sidecar, book_code),
        gate_absorbed_content(sidecar),
        gate_ratification(sidecar, ratified_classes),
        gate_completeness(validation_result.check("V7"), allow_incomplete),
    ]
    for gate_result in gate_sequence:
        if gate_result.passed:
            continue
        for message in gate_result.messages:
            print(message)
        _exit_with_dossier("blocked", gate_result.exit_code)

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
        body_checksum, registry_version, decision,
        allow_incomplete=allow_incomplete,
        staged_path=staged_path,
        residuals_path=residuals_path if residuals_path.exists() else None,
        editorial_candidates_path=(
            editorial_candidates_path if editorial_candidates_path.exists() else None
        ),
        validation_result=validation_result,
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
