"""Tests for pipeline/validate/checks.py — individual V-check functions."""

from __future__ import annotations

from pathlib import Path

from pipeline.validate.checks import (
    check_anchor_uniqueness,
    check_article_bleed,
    check_chapter_count,
    check_chapter_sequence,
    check_completeness,
    check_embedded_verses,
    check_frontmatter,
    check_heading_integrity,
    check_inline_leakage,
    check_split_words,
    check_verse_sequence,
    compute_v4_gaps,
)


# ── V6 Frontmatter ──────────────────────────────────────────────────────────

def test_frontmatter_pass():
    fm = {
        "book_code": "TST", "book_name": "Test", "testament": "OT",
        "canon_position": 1, "source": "test", "parse_date": "2026-01-01",
        "status": "staged",
    }
    r = check_frontmatter(fm)
    assert r.status == "PASS"
    assert r.errors == []


def test_frontmatter_missing_field():
    fm = {"book_code": "TST"}
    r = check_frontmatter(fm)
    assert r.status == "FAIL"
    assert any("book_name" in e for e in r.errors)


# ── V1 Anchor uniqueness ────────────────────────────────────────────────────

def test_anchor_uniqueness_pass():
    anchors = [("TST.1:1", 1, 1, 5), ("TST.1:2", 1, 2, 6)]
    r = check_anchor_uniqueness(anchors, {"TST.1:1", "TST.1:2"})
    assert r.status == "PASS"


def test_anchor_uniqueness_duplicate():
    anchors = [("TST.1:1", 1, 1, 5), ("TST.1:1", 1, 1, 6)]
    r = check_anchor_uniqueness(anchors, {"TST.1:1"})
    assert r.status == "FAIL"
    assert any("duplicate" in e.lower() for e in r.errors)


# ── V2 Chapter count ────────────────────────────────────────────────────────

def test_chapter_count_pass():
    r = check_chapter_count([(1, 5), (2, 20)], expected_chapters=2)
    assert r.status == "PASS"


def test_chapter_count_mismatch_warning():
    r = check_chapter_count([(1, 5)], expected_chapters=2)
    assert r.status == "WARN"


def test_chapter_count_mismatch_strict():
    r = check_chapter_count([(1, 5)], expected_chapters=2, strict=True)
    assert r.status == "FAIL"


def test_chapter_count_no_registry():
    r = check_chapter_count([(1, 5)], expected_chapters=None)
    assert r.status == "INFO"


# ── V3 Chapter sequence ─────────────────────────────────────────────────────

def test_chapter_sequence_pass():
    r = check_chapter_sequence([(1, 5), (2, 20), (3, 40)])
    assert r.status == "PASS"


def test_chapter_sequence_broken():
    r = check_chapter_sequence([(1, 5), (3, 20)])
    assert r.status == "FAIL"


# ── V4 Verse sequence ───────────────────────────────────────────────────────

def test_verse_sequence_pass():
    r = check_verse_sequence({1: [(1, 5), (2, 6), (3, 7)]})
    assert r.status == "PASS"


def test_verse_sequence_gap():
    r = check_verse_sequence({1: [(1, 5), (3, 7)]}, book_code="TST")
    assert r.status == "WARN"
    assert any("Missing" in w for w in r.warnings)
    assert r.data["missing_anchors"] == ["TST.1:2"]
    assert r.data["total_missing"] == 1


def test_verse_sequence_backward():
    r = check_verse_sequence({1: [(2, 5), (1, 6)]})
    assert r.status == "FAIL"


# ── V5 Article bleed ────────────────────────────────────────────────────────

def test_article_bleed_pass():
    lines = ["---", "book_code: TST", "---", "TST.1:1 Normal text"]
    r = check_article_bleed(lines, body_start=3)
    assert r.status == "PASS"


def test_article_bleed_detected():
    lines = ["---", "book_code: TST", "---",
             "TST.1:1 Fall of Adam caused mankind to suffer"]
    r = check_article_bleed(lines, body_start=3)
    assert r.status == "FAIL"


# ── V7 Completeness ─────────────────────────────────────────────────────────

def test_completeness_pass():
    r = check_completeness({"TST.1:1", "TST.1:2", "TST.1:3"}, [3])
    assert r.status == "PASS"


def test_completeness_gap():
    r = check_completeness({"TST.1:1", "TST.1:2"}, [3])
    assert r.status == "WARN"
    assert r.data["gap"] == 1
    assert r.data["pct"] == (2 / 3) * 100


def test_completeness_no_cvc():
    r = check_completeness({"TST.1:1"}, None)
    assert r.status == "INFO"
    assert r.data["pct"] is None


# ── V8 Heading integrity ────────────────────────────────────────────────────

def test_heading_integrity_pass():
    lines = [
        "## Chapter 1",
        "### The Beginning",
        "TST.1:1 In the beginning",
        "TST.1:2 And the earth",
    ]
    r = check_heading_integrity(lines, 0, {"TST.1:1", "TST.1:2"})
    assert r.status == "PASS"


def test_heading_fragment_detected():
    lines = [
        "## Chapter 1",
        "### Fragment:",
        "TST.1:1 text",
    ]
    r = check_heading_integrity(lines, 0, {"TST.1:1"})
    assert r.status == "FAIL"
    assert any("Fragment" in e for e in r.errors)


# ── V9 Embedded verses ──────────────────────────────────────────────────────

def test_embedded_verses_pass():
    gaps = [(1, 2, 4)]  # missing v3
    verse_map = {"TST.1:2": (5, "TST.1:2 no numbers here")}
    r = check_embedded_verses(gaps, verse_map, "TST")
    assert r.status == "PASS"


def test_embedded_verses_detected():
    gaps = [(1, 2, 4)]  # missing v3
    verse_map = {"TST.1:2": (5, "TST.1:2 text with 3 inside it")}
    r = check_embedded_verses(gaps, verse_map, "TST")
    assert r.status == "FAIL"
    assert any("Embedded" in e for e in r.errors)


# ── V11 Split words ─────────────────────────────────────────────────────────

def test_split_words_pass():
    lines = ["TST.1:1 Normal text without splits"]
    r = check_split_words(lines, 0)
    assert r.status == "PASS"


# ── V12 Inline leakage ──────────────────────────────────────────────────────

def test_inline_leakage_pass():
    lines = ["TST.1:5 Normal verse text"]
    r = check_inline_leakage(lines, 0)
    assert r.status == "PASS"


# ── compute_v4_gaps ──────────────────────────────────────────────────────────

def test_compute_v4_gaps():
    verses = {1: [(1, 5), (3, 7)]}
    gaps = compute_v4_gaps(verses)
    assert gaps == [(1, 1, 3)]


def test_compute_v4_gaps_no_gaps():
    verses = {1: [(1, 5), (2, 6), (3, 7)]}
    gaps = compute_v4_gaps(verses)
    assert gaps == []
