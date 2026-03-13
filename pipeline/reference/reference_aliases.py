"""
reference_aliases.py — Versioned alias authority for biblical and future patristic references.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import re

import yaml

from pipeline.common.paths import SCHEMAS_DIR

REFERENCE_ALIASES_PATH = SCHEMAS_DIR / "reference_aliases.yaml"
RE_WHITESPACE = re.compile(r"\s+")


def _normalize_alias_key(text: str) -> str:
    text = text.strip()
    text = text.replace(".", "")
    text = text.replace("-", " ")
    text = text.replace("_", " ")
    text = RE_WHITESPACE.sub(" ", text)
    return text.casefold()


@lru_cache(maxsize=4)
def load_reference_aliases(path: Path | str | None = None) -> dict:
    alias_path = Path(path) if path is not None else REFERENCE_ALIASES_PATH
    with open(alias_path, encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    data.setdefault("version", 1)
    data.setdefault("biblical", [])
    data.setdefault("patristic_future", [])
    return data


@lru_cache(maxsize=4)
def build_biblical_alias_map(path: Path | str | None = None) -> dict[str, str]:
    data = load_reference_aliases(path)
    alias_map: dict[str, str] = {}
    for entry in data.get("biblical", []):
        canonical = entry["canonical"]
        alias_map[_normalize_alias_key(canonical)] = canonical
        for alias in entry.get("aliases", []):
            alias_map[_normalize_alias_key(alias)] = canonical
    return alias_map


@lru_cache(maxsize=4)
def build_patristic_alias_map(path: Path | str | None = None) -> dict[str, dict]:
    data = load_reference_aliases(path)
    alias_map: dict[str, dict] = {}
    for entry in data.get("patristic_future", []):
        canonical = entry["canonical"]
        payload = {
            "canonical": canonical,
            "context_hint": entry.get("context_hint"),
        }
        alias_map[_normalize_alias_key(canonical)] = payload
        for alias in entry.get("aliases", []):
            alias_map[_normalize_alias_key(alias)] = payload
    return alias_map


def canonical_biblical_code(token: str, path: Path | str | None = None) -> str | None:
    return build_biblical_alias_map(path).get(_normalize_alias_key(token))


def canonical_patristic_entity(token: str, path: Path | str | None = None) -> dict | None:
    return build_patristic_alias_map(path).get(_normalize_alias_key(token))

