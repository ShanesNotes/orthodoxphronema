"""
text.py — Shared text utilities.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from pipeline.common.paths import STAGING_ROOT


def normalize_text(text: str) -> str:
    """Standard text normalization (tabs, whitespace, etc.)."""
    return text.replace("\t", " ").strip()


def sha256_hex(text: str) -> str:
    """SHA-256 hex digest of text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _iter_staged_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    if not root.exists():
        return paths
    for testament_dir in sorted(root.iterdir()):
        if not testament_dir.is_dir():
            continue
        for md_file in sorted(testament_dir.glob("*.md")):
            stem = md_file.stem
            if stem.endswith("_notes") or "_" in stem:
                continue
            paths.append(md_file)
    return sorted(paths)


def discover_staged_books(
    staging_root: Path | list[str] | tuple[str, ...] | set[str] | None = None
) -> list[str]:
    """Find all book codes with .md files in staging/validated.

    Returns sorted list of book codes (e.g. ['DEU', 'EXO', 'GEN']).
    """
    if isinstance(staging_root, (list, tuple, set)):
        filter_codes = {str(code).upper() for code in staging_root}
        root = STAGING_ROOT
    else:
        filter_codes = None
        root = staging_root or STAGING_ROOT
    codes = [path.stem for path in _iter_staged_paths(root)]
    if filter_codes is not None:
        codes = [code for code in codes if code in filter_codes]
    return sorted(codes)


def discover_staged_paths(
    staging_root: Path | list[str] | tuple[str, ...] | set[str] | None = None
) -> list[Path]:
    """Find all .md book files in staging/validated. Returns sorted list of Paths."""
    if isinstance(staging_root, (list, tuple, set)):
        filter_codes = {str(code).upper() for code in staging_root}
        root = STAGING_ROOT
    else:
        filter_codes = None
        root = staging_root or STAGING_ROOT
    paths = _iter_staged_paths(root)
    if filter_codes is not None:
        paths = [path for path in paths if path.stem in filter_codes]
    return sorted(paths)


def normalize_whitespace(text: str) -> str:
    """Collapse multiple spaces and normalize whitespace."""
    import re
    return re.sub(r'\s+', ' ', text).strip()
