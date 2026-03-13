"""
paths.py — Single source of truth for all repo-relative paths.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
METADATA_ROOT = REPO_ROOT / "metadata"
REGISTRY_PATH = REPO_ROOT / "schemas" / "anchor_registry.json"
STAGING_ROOT = REPO_ROOT / "staging" / "validated"
CANON_ROOT = REPO_ROOT / "canon"
REPORTS_ROOT = REPO_ROOT / "reports"
BRENTON_DIR = REPO_ROOT / "staging" / "reference" / "brenton"
MEMOS_DIR = REPO_ROOT / "memos"
SCHEMAS_DIR = REPO_ROOT / "schemas"
PDF_PATH = REPO_ROOT / "src.texts" / "the_orthodox_study_bible.pdf"
BRENTON_SOURCE_DIR = REPO_ROOT / "src.texts" / "Brenton-Septuagint.txt"
GREEK_SOURCE_DIR = REPO_ROOT / "src.texts" / "greektext-antoniades"
RESIDUAL_CLASSES_PATH = SCHEMAS_DIR / "residual_classes.json"


# ── Canon file path helper ───────────────────────────────────────────────────

_POSITION_CACHE: dict[str, int] | None = None


def _load_positions() -> dict[str, int]:
    """Load book_code → position mapping from the registry."""
    global _POSITION_CACHE
    if _POSITION_CACHE is None:
        with open(REGISTRY_PATH, encoding="utf-8") as f:
            reg = json.load(f)
        _POSITION_CACHE = {b["code"]: b["position"] for b in reg["books"]}
    return _POSITION_CACHE


def canon_filepath(testament: str, code: str) -> Path:
    """Return the canonical-order filepath for a book: canon/OT/01_GEN.md"""
    pos = _load_positions().get(code)
    if pos is None:
        return CANON_ROOT / testament / f"{code}.md"
    return CANON_ROOT / testament / f"{pos:02d}_{code}.md"
