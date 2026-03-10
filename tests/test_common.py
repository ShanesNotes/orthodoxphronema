"""Tests for pipeline.common — shared utilities."""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# paths
# ---------------------------------------------------------------------------

def test_repo_root_points_to_project():
    from pipeline.common.paths import REPO_ROOT
    assert (REPO_ROOT / "schemas" / "anchor_registry.json").exists()


def test_all_path_constants_are_path_objects():
    from pipeline.common import paths
    for name in dir(paths):
        obj = getattr(paths, name)
        if name.isupper() and not name.startswith("_"):
            assert isinstance(obj, Path), f"{name} should be Path"


# ---------------------------------------------------------------------------
# registry
# ---------------------------------------------------------------------------

def test_load_registry_returns_dict():
    from pipeline.common.registry import load_registry
    reg = load_registry()
    assert isinstance(reg, dict)
    assert "books" in reg


def test_book_meta_found():
    from pipeline.common.registry import load_registry, book_meta
    reg = load_registry()
    meta = book_meta(reg, "GEN")
    assert meta["code"] == "GEN"
    assert "testament" in meta


def test_book_meta_not_found():
    from pipeline.common.registry import load_registry, book_meta
    reg = load_registry()
    with pytest.raises(ValueError, match="ZZZZ"):
        book_meta(reg, "ZZZZ")


def test_book_testament():
    from pipeline.common.registry import load_registry, book_testament
    reg = load_registry()
    assert book_testament(reg, "GEN") == "OT"


def test_chapter_verse_counts_returns_dict_or_none():
    from pipeline.common.registry import load_registry, chapter_verse_counts
    reg = load_registry()
    cvc = chapter_verse_counts(reg, "GEN")
    if cvc is not None:
        assert isinstance(cvc, dict)
        assert 1 in cvc  # 1-indexed


def test_page_ranges():
    from pipeline.common.registry import load_registry, page_ranges
    reg = load_registry()
    text_range, fn_range = page_ranges(reg, "GEN")
    assert len(text_range) == 2
    assert len(fn_range) == 2
    assert text_range[0] < text_range[1]


def test_load_residual_classes():
    from pipeline.common.registry import load_residual_classes
    data = load_residual_classes()
    assert "classes" in data


def test_classifications_requiring_entry_ratification():
    from pipeline.common.registry import classifications_requiring_entry_ratification
    result = classifications_requiring_entry_ratification()
    assert isinstance(result, set)


# ---------------------------------------------------------------------------
# frontmatter
# ---------------------------------------------------------------------------

def test_parse_frontmatter_basic():
    from pipeline.common.frontmatter import parse_frontmatter
    lines = [
        "---",
        'book_code: GEN',
        'testament: OT',
        "---",
        "GEN.1:1 In the beginning",
    ]
    fm, body_start = parse_frontmatter(lines)
    assert fm["book_code"] == "GEN"
    assert fm["testament"] == "OT"
    assert body_start == 4


def test_parse_frontmatter_no_delimiters():
    from pipeline.common.frontmatter import parse_frontmatter
    lines = ["GEN.1:1 In the beginning"]
    fm, body_start = parse_frontmatter(lines)
    assert fm == {}
    assert body_start == 0


def test_parse_frontmatter_strips_quotes():
    from pipeline.common.frontmatter import parse_frontmatter
    lines = ["---", 'book_name: "Genesis"', "---"]
    fm, _ = parse_frontmatter(lines)
    assert fm["book_name"] == "Genesis"


def test_split_frontmatter_basic():
    from pipeline.common.frontmatter import split_frontmatter
    text = "---\nbook_code: GEN\n---\nGEN.1:1 In the beginning\n"
    fm_block, body = split_frontmatter(text)
    assert fm_block.startswith("---")
    assert fm_block.endswith("---\n")
    assert "GEN.1:1" in body


def test_split_frontmatter_no_fm():
    from pipeline.common.frontmatter import split_frontmatter
    text = "GEN.1:1 In the beginning\n"
    fm_block, body = split_frontmatter(text)
    assert fm_block == ""
    assert body == text


def test_update_frontmatter():
    from pipeline.common.frontmatter import update_frontmatter
    fm_block = '---\npromote_date: ""\nstatus: staged\nchecksum: ""\n---\n'
    result = update_frontmatter(fm_block, "2026-03-10", "abc123")
    assert '"2026-03-10"' in result
    assert "promoted" in result
    assert '"abc123"' in result


# ---------------------------------------------------------------------------
# patterns
# ---------------------------------------------------------------------------

def test_re_anchor_matches():
    from pipeline.common.patterns import RE_ANCHOR
    m = RE_ANCHOR.match("GEN.1:1 In the beginning")
    assert m is not None
    assert m.group(1) == "GEN"
    assert m.group(2) == "1"
    assert m.group(3) == "1"


def test_re_anchor_full_captures_text():
    from pipeline.common.patterns import RE_ANCHOR_FULL
    m = RE_ANCHOR_FULL.match("GEN.1:1 In the beginning")
    assert m.group(4) == "In the beginning"


def test_re_anchor_parts_anchor_only():
    from pipeline.common.patterns import RE_ANCHOR_PARTS
    assert RE_ANCHOR_PARTS.match("GEN.1:1") is not None
    assert RE_ANCHOR_PARTS.match("GEN.1:1 text") is None


def test_re_chapter_hdr():
    from pipeline.common.patterns import RE_CHAPTER_HDR
    m = RE_CHAPTER_HDR.match("## Chapter 42")
    assert m.group(1) == "42"


def test_re_footnote_markers():
    from pipeline.common.patterns import RE_FOOTNOTE_MARKERS
    assert RE_FOOTNOTE_MARKERS.search("text † more")
    assert RE_FOOTNOTE_MARKERS.search("text †ω more")
    assert not RE_FOOTNOTE_MARKERS.search("plain text")


def test_re_spaced_caps():
    from pipeline.common.patterns import RE_SPACED_CAPS
    # Docling outputs single space between each letter
    assert RE_SPACED_CAPS.match("T H E H O L Y T R I N I T Y")
    assert not RE_SPACED_CAPS.match("The Holy Trinity")


def test_known_split_join_words_superset():
    from pipeline.common.patterns import KNOWN_SPLIT_JOIN_WORDS
    # Must include both validate_canon and fix_split_words words
    assert "beloved" in KNOWN_SPLIT_JOIN_WORDS
    assert "overlooked" in KNOWN_SPLIT_JOIN_WORDS  # fix_split_words addition


def test_short_prefixes():
    from pipeline.common.patterns import SHORT_PREFIXES
    assert "a" in SHORT_PREFIXES
    assert "an" in SHORT_PREFIXES
    assert len(SHORT_PREFIXES) == 10


# ---------------------------------------------------------------------------
# text
# ---------------------------------------------------------------------------

def test_sha256_hex():
    from pipeline.common.text import sha256_hex
    result = sha256_hex("hello")
    assert len(result) == 64
    assert result == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_normalize_whitespace():
    from pipeline.common.text import normalize_whitespace
    assert normalize_whitespace("  hello\t world  ") == "hello world"
    assert normalize_whitespace("a\n\nb") == "a b"


def test_discover_staged_books_returns_list():
    from pipeline.common.text import discover_staged_books
    books = discover_staged_books()
    assert isinstance(books, list)
    # We know GEN and EXO are staged
    assert "GEN" in books
    assert "EXO" in books


def test_discover_staged_books_filter():
    from pipeline.common.text import discover_staged_books
    books = discover_staged_books(["GEN", "EXO"])
    assert set(books) <= {"GEN", "EXO"}


def test_discover_staged_paths_returns_paths():
    from pipeline.common.text import discover_staged_paths
    paths = discover_staged_paths(["GEN"])
    assert all(isinstance(p, Path) for p in paths)
    if paths:
        assert paths[0].suffix == ".md"


# ---------------------------------------------------------------------------
# types
# ---------------------------------------------------------------------------

def test_verse_record_construction():
    from pipeline.common.types import VerseRecord
    v = VerseRecord(anchor="GEN.1:1", chapter=1, verse=1, text="In the beginning")
    assert v.anchor == "GEN.1:1"
    assert v.chapter == 1
    assert v.verse == 1
    assert v.text == "In the beginning"


def test_verse_record_to_dict():
    from pipeline.common.types import VerseRecord
    v = VerseRecord(anchor="GEN.1:1", chapter=1, verse=1, text="In the beginning")
    d = v.to_dict()
    assert d == {"anchor": "GEN.1:1", "chapter": 1, "verse": 1, "text": "In the beginning"}


def test_heading_record():
    from pipeline.common.types import HeadingRecord
    h = HeadingRecord(after_anchor="GEN.1:0", heading="The Creation")
    assert h.after_anchor == "GEN.1:0"
    assert h.heading == "The Creation"


def test_article_record():
    from pipeline.common.types import ArticleRecord
    a = ArticleRecord(title="Ancestral Sin", after_anchor="GEN.3:7", body=["para 1"])
    assert a.title == "Ancestral Sin"
    assert len(a.body) == 1


def test_check_result():
    from pipeline.common.types import CheckResult
    cr = CheckResult(name="V1", status="PASS")
    assert cr.errors == []
    assert cr.warnings == []
    assert cr.messages == []


def test_validation_result():
    from pipeline.common.types import ValidationResult, CheckResult
    vr = ValidationResult(
        book_code="GEN",
        checks=[
            CheckResult(name="V1", status="PASS"),
            CheckResult(name="V4", status="WARN", warnings=["V4 gap"]),
            CheckResult(name="V5", status="FAIL", errors=["V5 article bleed"]),
        ]
    )
    assert vr.book_code == "GEN"
    assert vr.errors == ["V5 article bleed"]
    assert vr.warnings == ["V4 gap"]
    assert not vr.passed


def test_validation_result_passed():
    from pipeline.common.types import ValidationResult, CheckResult
    vr = ValidationResult(book_code="GEN", checks=[
        CheckResult(name="V1", status="PASS"),
    ])
    assert vr.passed


def test_validation_result_check_and_status_map():
    from pipeline.common.types import ValidationResult, CheckResult
    vr = ValidationResult(
        book_code="GEN",
        checks=[
            CheckResult(name="V1", status="PASS"),
            CheckResult(name="V10", status="SKIP"),
        ],
    )
    assert vr.check("V10").status == "SKIP"
    assert vr.status_map["V1"] == "PASS"
    assert vr.status_map["V10"] == "SKIP"


def test_normalize_pdf_search_text():
    from pipeline.common.pdf_source import normalize_pdf_search_text
    text = "He† said wor-\nship to “God”."
    assert normalize_pdf_search_text(text) == "he said worship to god"


def test_estimate_chapter_page_range():
    from pipeline.common.pdf_source import estimate_chapter_page_range

    start, end = estimate_chapter_page_range(
        "GEN",
        2,
        page_ranges={"GEN": {"text": [100, 199]}},
        cvc={1: 50, 2: 50},
    )
    assert start == 166
    assert end == 199


def test_residual_entry_defaults():
    from pipeline.common.types import ResidualEntry
    r = ResidualEntry(anchor="GEN.1:1", classification="docling_issue", description="test")
    assert r.blocking is False
    assert r.ratified is False
