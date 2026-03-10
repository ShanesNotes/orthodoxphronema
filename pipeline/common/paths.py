"""
paths.py — Single source of truth for all repo-relative paths.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
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
