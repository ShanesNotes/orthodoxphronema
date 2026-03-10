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


def discover_staged_books(staging_root: Path | None = None) -> list[str]:
    """Find all book codes with .md files in staging/validated.

    Returns sorted list of book codes (e.g. ['DEU', 'EXO', 'GEN']).
    """
    root = staging_root or STAGING_ROOT
    codes: list[str] = []
    for testament_dir in sorted(root.iterdir()):
        if not testament_dir.is_dir():
            continue
        for md_file in sorted(testament_dir.glob("*.md")):
            # Skip notes files and other sidecars
            stem = md_file.stem
            if stem.endswith("_notes") or "_" in stem:
                continue
            codes.append(stem)
    return sorted(codes)


def discover_staged_paths(staging_root: Path | None = None) -> list[Path]:
    """Find all .md book files in staging/validated. Returns sorted list of Paths."""
    root = staging_root or STAGING_ROOT
    paths: list[Path] = []
    for testament_dir in sorted(root.iterdir()):
        if not testament_dir.is_dir():
            continue
        for md_file in sorted(testament_dir.glob("*.md")):
            stem = md_file.stem
            if stem.endswith("_notes") or "_" in stem:
                continue
            paths.append(md_file)
    return sorted(paths)


def normalize_whitespace(text: str) -> str:
    """Collapse multiple spaces and normalize whitespace."""
    import re
    return re.sub(r'\s+', ' ', text).strip()
