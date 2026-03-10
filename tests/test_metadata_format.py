"""
test_metadata_format.py — Pericope index generation and frontmatter schema drift.
"""
from __future__ import annotations

import json
from pathlib import Path

from pipeline.metadata import generate_pericope_index as _pericope_mod

REPO_ROOT = Path(__file__).parent.parent


def test_pericope_index_extracts_ranges(tmp_path):
    mod = _pericope_mod

    book = tmp_path / "TST.md"
    book.write_text(
        "---\n"
        "book_code: TST\n"
        "---\n\n"
        "## Chapter 1\n\n"
        "TST.1:1 one\n"
        "### First Section\n"
        "TST.1:2 two\n"
        "TST.1:3 three\n"
        "## Chapter 2\n\n"
        "TST.2:1 four\n"
        "### Second Section\n"
        "TST.2:2 five\n"
        "### Empty Tail\n",
        encoding="utf-8",
    )

    data = mod.extract_pericopes(book)
    assert data["book_code"] == "TST"
    assert len(data["pericopes"]) == 3

    first = data["pericopes"][0]
    assert first["title"] == "First Section"
    assert first["start_anchor"] == "TST.1:2"
    assert first["end_anchor"] == "TST.2:1"
    assert first["verse_count"] is None
    assert first["chapter_range"] == "1-2"

    second = data["pericopes"][1]
    assert second["title"] == "Second Section"
    assert second["start_anchor"] == "TST.2:2"
    assert second["end_anchor"] == "TST.2:2"
    assert second["verse_count"] == 1
    assert second["chapter_range"] == "2"

    third = data["pericopes"][2]
    assert third["title"] == "Empty Tail"
    assert third["start_anchor"] is None
    assert third["end_anchor"] is None
    assert third["verse_count"] == 0
    assert third["chapter_range"] is None


def test_scripture_frontmatter_schema_matches_repo_contract():
    schema = json.loads((REPO_ROOT / "schemas" / "scripture_frontmatter.json").read_text())
    props = schema["properties"]

    assert props["source"]["minLength"] == 1
    assert "staged" in props["status"]["enum"]

    promote_oneof = props["promote_date"]["oneOf"]
    assert any(option.get("type") == "null" for option in promote_oneof)

    checksum_oneof = props["checksum"]["oneOf"]
    patterns = [option.get("pattern") for option in checksum_oneof if option.get("pattern")]
    assert "^[a-f0-9]{64}$" in patterns
    assert any(option.get("type") == "null" for option in checksum_oneof)
