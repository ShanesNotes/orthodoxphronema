"""
registry.py — Consolidated anchor_registry.json loading and lookup.
"""
from __future__ import annotations

import json
from pathlib import Path

from pipeline.common.paths import REGISTRY_PATH


def load_registry(path: Path | str | None = None) -> dict:
    """Load anchor_registry.json. Uses REGISTRY_PATH by default."""
    p = Path(path) if path is not None else REGISTRY_PATH
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def book_meta(registry: dict, code: str) -> dict:
    """Look up a book entry by code."""
    for b in registry.get("books", []):
        if b["code"] == code:
            return b
    raise ValueError(f"Book code {code!r} not found in registry")


def chapter_verse_counts(registry: dict, code: str) -> dict[int, int] | None:
    """Return {chapter_num: verse_count} dict for a book, or None if no CVC.

    The registry stores chapter_verse_counts as a 1-indexed list where
    index 0 is chapter 1's count.
    """
    try:
        meta = book_meta(registry, code)
    except ValueError:
        return None
    cvc_list = meta.get("chapter_verse_counts")
    if not cvc_list:
        return None
    return {i + 1: count for i, count in enumerate(cvc_list)}


def book_testament(registry: dict, code: str) -> str | None:
    """Return testament ('OT' or 'NT') for a book code."""
    try:
        meta = book_meta(registry, code)
    except ValueError:
        return None
    return meta.get("testament")


def page_ranges(registry: dict, code: str) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return ((text_start, text_end), (footnote_start, footnote_end))."""
    page_ranges_map = registry.get("page_ranges", {})
    if code not in page_ranges_map:
        raise ValueError(f"Book code {code!r} not found in page_ranges")
    entry = page_ranges_map[code]
    return tuple(entry["text"]), tuple(entry["footnotes"])


def load_residual_classes(path: Path | str | None = None) -> dict:
    """Load residual_classes.json schema."""
    from pipeline.common.paths import SCHEMAS_DIR
    p = Path(path) if path is not None else SCHEMAS_DIR / "residual_classes.json"
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def classifications_requiring_entry_ratification(residual_classes=None) -> set[str]:
    """Return set of classification names that require per-entry ratification.

    Accepts a dict (loaded JSON), a Path (will load from it), or None (default path).
    """
    if residual_classes is None:
        residual_classes = load_residual_classes()
    elif isinstance(residual_classes, Path):
        residual_classes = load_residual_classes(residual_classes)
    result = set()
    classes = residual_classes.get("classes", [])
    if isinstance(classes, dict):
        for name, spec in classes.items():
            if spec.get("per_entry_ratification") or spec.get("requires_per_entry_ratification"):
                result.add(name)
    elif isinstance(classes, list):
        for spec in classes:
            if spec.get("per_entry_ratification") or spec.get("requires_per_entry_ratification"):
                result.add(spec.get("name", ""))
    return result
