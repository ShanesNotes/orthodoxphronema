"""
normalize_reference_text.py — Shared normalization utilities for Brenton ↔ OSB comparison.

COMPARISON ONLY — these functions never modify canon text.
"""

from __future__ import annotations

import difflib
import json
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Quote/dash normalization map (curly → straight)
# ---------------------------------------------------------------------------
_QUOTE_MAP = str.maketrans({
    '\u2018': "'",   # left single quotation mark
    '\u2019': "'",   # right single quotation mark
    '\u201c': '"',   # left double quotation mark
    '\u201d': '"',   # right double quotation mark
    '\u2013': '-',   # en dash
    '\u2014': '-',   # em dash
})

RE_ANCHOR_PREFIX = re.compile(r'^[A-Z0-9]+\.\d+:\d+\s+')


def strip_anchor(line: str) -> str:
    """Strip 'GEN.1:1 ' prefix from an OSB verse line."""
    return RE_ANCHOR_PREFIX.sub('', line)


def normalize_for_compare(text: str) -> str:
    """
    Normalize text for comparison only — never mutates canon.

    Steps:
      1. Translate curly quotes/dashes to straight equivalents
      2. Lowercase
      3. Collapse all whitespace runs to single space
      4. Strip leading/trailing non-alphabetic chars
    """
    text = text.translate(_QUOTE_MAP)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'^[^a-z]+', '', text)
    text = re.sub(r'[^a-z]+$', '', text)
    return text


def token_similarity(a: str, b: str) -> float:
    """SequenceMatcher ratio on two (already normalized) strings. Returns 0.0–1.0."""
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def tokenize(text: str) -> list[str]:
    """Split normalized text into lowercase word tokens (alpha only)."""
    return re.findall(r"[a-z']+", text.lower())


# ---------------------------------------------------------------------------
# Brenton index helpers
# ---------------------------------------------------------------------------

def load_brenton_index(book_code: str, brenton_dir: Path) -> dict | None:
    """
    Load staging/reference/brenton/BOOK.json.
    Returns None if the file does not exist.
    """
    path = brenton_dir / f"{book_code}.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_brenton_verse(index: dict, chapter: int, verse: int) -> str | None:
    """
    Retrieve a single Brenton verse.
    chapter and verse are 1-based. Returns None if out of range or missing.
    """
    ch_data = index.get("chapters", {}).get(str(chapter))
    if ch_data is None:
        return None
    verses = ch_data.get("verses", [])
    idx = verse - 1
    if idx < 0 or idx >= len(verses):
        return None
    return verses[idx]
