"""
generate_book_status_dashboard.py — Build a durable book-status dashboard.

The dashboard summarizes live staged/promoted state for each canonical book using
existing repo artifacts:
  - reports/BOOK_promotion_dossier.json
  - staging/validated/{OT,NT}/BOOK_editorial_candidates.json
  - staging/validated/{OT,NT}/BOOK_residuals.json
  - canon/{OT,NT}/BOOK.md

Status ladder:
  extracting -> structurally_passable -> editorially_clean
  -> promotion_ready -> promoted
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import sys as _sys; from pathlib import Path as _Path
_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists(): _R = _R.parent
if str(_R) not in _sys.path: _sys.path.insert(0, str(_R))
import pipeline.common.paths as _paths
from pipeline.common.paths import canon_filepath
import pipeline.common.registry as _reg
from pipeline.common.text import sha256_hex

# Module-level path constants — tests may override these
REPO_ROOT = _paths.REPO_ROOT
REGISTRY = _paths.REGISTRY_PATH
RESIDUAL_CLASSES = _paths.RESIDUAL_CLASSES_PATH
REPORTS_ROOT = _paths.REPORTS_ROOT
STAGING_ROOT = _paths.STAGING_ROOT
CANON_ROOT = _paths.CANON_ROOT

PASSISH_VALIDATION_KEYS = ("V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9")
HARD_STRUCTURAL_KEYS = ("V1", "V2", "V3", "V9")
EDITORIAL_VALIDATION_KEYS = ("V11", "V12")
DISPLAY_VALIDATION_KEYS = PASSISH_VALIDATION_KEYS + EDITORIAL_VALIDATION_KEYS
STRUCTURAL_RESIDUAL_HINTS = (
    "absorbed",
    "appears within",
    "instead of as a separate verse",
    "embedded",
    "fused into",
)


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_registry() -> dict:
    return _reg.load_registry(REGISTRY)


def ratification_required_classes() -> set[str]:
    return _reg.classifications_requiring_entry_ratification(RESIDUAL_CLASSES)


def is_pass_or_warn(value: str | None) -> bool:
    return value in {"PASS", "WARN"}


def validation_map(dossier: dict | None) -> dict:
    return (dossier or {}).get("validation", {})


def staged_body_checksum(path: Path) -> str | None:
    from pipeline.common.frontmatter import split_frontmatter
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    _, body = split_frontmatter(text)
    return sha256_hex(body)


def dossier_freshness_status(
    dossier: dict | None,
    staged_path: Path,
    staged_checksum: str | None,
) -> str:
    if dossier is None:
        return "NO_DOSSIER"
    if not staged_path.exists():
        return "NO_STAGED_FILE"
    dossier_checksum = dossier.get("body_checksum")
    if not dossier_checksum:
        return "NO_CHECKSUM"
    if staged_checksum is None:
        return "NO_STAGED_CHECKSUM"
    if staged_checksum == dossier_checksum:
        return "FRESH"
    return "STALE"


def dossier_refresh_priority(freshness_status: str, status: str, decision: str | None) -> str:
    if freshness_status != "STALE":
        return "none"
    if status in {"promotion_ready", "editorially_clean"} or decision == "dry-run":
        return "high"
    if status == "structurally_passable":
        return "medium"
    return "low"


def residual_summary(sidecar: dict | list | None) -> dict:
    if isinstance(sidecar, list):
        residuals = sidecar
    else:
        residuals = (sidecar or {}).get("residuals", [])
    required_classes = ratification_required_classes()
    blocking = [r for r in residuals if r.get("blocking")]
    unratified = [r for r in residuals if not r.get("ratified", False)]
    needs_entry_ratification = [
        r for r in residuals
        if r.get("classification", "") in required_classes and not r.get("ratified", False)
    ]
    structural_hints = [
        r for r in residuals
        if any(hint in (r.get("description", "")).lower() for hint in STRUCTURAL_RESIDUAL_HINTS)
    ]
    schema_mismatch = [
        r for r in residuals
        if "class" in r and "classification" not in r
    ]
    return {
        "count": len(residuals),
        "blocking_count": len(blocking),
        "ratified_by": (sidecar or {}).get("ratified_by") if isinstance(sidecar, dict) else None,
        "ratified_date": (sidecar or {}).get("ratified_date") if isinstance(sidecar, dict) else None,
        "unratified_count": len(unratified),
        "per_entry_pending_count": len(needs_entry_ratification),
        "structural_hint_count": len(structural_hints),
        "schema_mismatch_count": len(schema_mismatch),
    }


def editorial_summary(editorial: dict | None) -> dict:
    editorial = editorial or {}
    return {
        "total_candidates": editorial.get("total_candidates", 0),
        "by_category": editorial.get("by_category", {}),
    }


def editorial_reason(summary: dict | None) -> str:
    summary = summary or {}
    total = int(summary.get("total_candidates", 0) or 0)
    if total == 0:
        return "editorial candidates clear"

    by_category = summary.get("by_category", {}) or {}
    if not by_category:
        return f"{total} editorial candidate(s) remain"

    ordered = sorted(by_category.items(), key=lambda item: (-item[1], item[0]))
    category_text = ", ".join(f"{name}={count}" for name, count in ordered[:3])
    return f"{total} editorial candidate(s) remain: {category_text}"


def determine_status(
    dossier: dict | None,
    editorial: dict | None,
    residuals: dict | None,
    promoted_exists: bool,
    staged_matches_dossier: bool,
) -> tuple[str, list[str]]:
    reasons: list[str] = []

    if promoted_exists:
        reasons.append("canon artifact exists")
        return "promoted", reasons

    validation = validation_map(dossier)
    if not validation:
        reasons.append("no promotion dossier")
        return "extracting", reasons

    hard_failures = [
        key for key in HARD_STRUCTURAL_KEYS
        if validation.get(key, {}).get("status") != "PASS"
    ]
    if hard_failures:
        reasons.append("hard validation failures: " + ", ".join(hard_failures))
        return "extracting", reasons

    soft_failures = [
        key for key in PASSISH_VALIDATION_KEYS
        if not is_pass_or_warn(validation.get(key, {}).get("status"))
    ]
    if soft_failures:
        reasons.append("validation failures: " + ", ".join(soft_failures))
        return "extracting", reasons

    reasons.append("validation is structurally passable")
    status = "structurally_passable"

    editorial_info = editorial_summary(editorial)
    editorial_count = editorial_info["total_candidates"]
    if editorial_count:
        reasons.append(editorial_reason(editorial_info))
        return status, reasons

    reasons.append(editorial_reason(editorial_info))
    status = "editorially_clean"

    editorial_validation_failures = [
        key for key in EDITORIAL_VALIDATION_KEYS
        if validation.get(key, {}).get("status") not in {None, "PASS"}
    ]
    if editorial_validation_failures:
        reasons.append(
            "validation still reports editorial issues: "
            + ", ".join(editorial_validation_failures)
        )
        return "structurally_passable", reasons

    summary = residual_summary(residuals)
    if not staged_matches_dossier and dossier is not None:
        reasons.append("promotion dossier checksum does not match current staged file")
        return status, reasons

    if summary["blocking_count"]:
        reasons.append(f"{summary['blocking_count']} blocking residual(s) remain")
        return status, reasons
    if validation.get("V4", {}).get("status") == "WARN":
        reasons.append("live V4 warning still present")
        return status, reasons
    if summary["structural_hint_count"]:
        reasons.append(
            f"{summary['structural_hint_count']} residual(s) still describe embedded or absorbed verse content"
        )
        return status, reasons
    if summary["schema_mismatch_count"]:
        reasons.append(
            f"{summary['schema_mismatch_count']} residual entry uses non-standard class field"
        )
        return status, reasons
    if summary["count"] and summary["ratified_by"] != "human":
        reasons.append("residual exceptions are not yet human-ratified")
        return status, reasons
    if summary["per_entry_pending_count"]:
        reasons.append(
            f"{summary['per_entry_pending_count']} residual(s) still need per-entry ratification"
        )
        return status, reasons

    if summary["count"] and summary["ratified_date"] is None:
        reasons.append("residual sidecar not yet ratified")
        return status, reasons

    reasons.append("promotion gate conditions are satisfied")
    return "promotion_ready", reasons


def build_book_entry(book: dict) -> dict:
    code = book["code"]
    testament = book["testament"]
    dossier = load_json(REPORTS_ROOT / f"{code}_promotion_dossier.json")
    editorial = load_json(STAGING_ROOT / testament / f"{code}_editorial_candidates.json")
    residuals = load_json(STAGING_ROOT / testament / f"{code}_residuals.json")
    try:
        promoted_exists = canon_filepath(testament, code).exists()
    except ValueError:
        promoted_exists = False
    staged_path = STAGING_ROOT / testament / f"{code}.md"
    checksum = staged_body_checksum(staged_path)
    freshness_status = dossier_freshness_status(dossier, staged_path, checksum)
    dossier_checksum = (dossier or {}).get("body_checksum")
    staged_matches_dossier = freshness_status != "STALE"

    status, reasons = determine_status(
        dossier, editorial, residuals, promoted_exists, staged_matches_dossier
    )
    validation = validation_map(dossier)
    decision = (dossier or {}).get("decision")

    return {
        "book_code": code,
        "testament": testament,
        "status": status,
        "status_reasons": reasons,
        "decision": decision,
        "body_checksum": dossier_checksum,
        "staged_matches_dossier": staged_matches_dossier,
        "dossier_freshness": {
            "status": freshness_status,
            "refresh_priority": dossier_refresh_priority(freshness_status, status, decision),
            "staged_body_checksum": checksum,
        },
        "validation": {
            key: validation.get(key, {}).get("status", "MISSING")
            for key in DISPLAY_VALIDATION_KEYS
        },
        "editorial": editorial_summary(editorial),
        "residuals": residual_summary(residuals),
    }


def build_dashboard() -> dict:
    registry = load_registry()
    books = [build_book_entry(book) for book in registry.get("books", [])]
    counts: dict[str, int] = {}
    for book in books:
        counts[book["status"]] = counts.get(book["status"], 0) + 1

    return {
        "generated": str(date.today()),
        "registry_version": registry.get("registry_version"),
        "status_ladder": [
            "extracting",
            "structurally_passable",
            "editorially_clean",
            "promotion_ready",
            "promoted",
        ],
        "counts_by_status": counts,
        "books": books,
    }


def write_dashboard(dashboard: dict) -> Path:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    path = REPORTS_ROOT / "book_status_dashboard.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dashboard, f, indent=2)
    print(path)
    return path


def main() -> None:
    write_dashboard(build_dashboard())


if __name__ == "__main__":
    main()
