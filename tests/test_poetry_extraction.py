from __future__ import annotations

import pytest

from pipeline.common.poetry import (
    PoetryExtractionConfig,
    clean_poetry_text,
    compile_chapter_header_patterns,
    extract_poetry_lines,
    match_chapter_header,
)
from pipeline.parse.psa_extract import (
    DEFAULT_PAGE_END,
    DEFAULT_PAGE_START,
    resolve_book_defaults,
    resolve_page_range,
)


def test_clean_poetry_text_repairs_common_pdftotext_kerning():
    text = "B lessed is the m an who shall lov e wisdom ."
    assert clean_poetry_text(text) == "Blessed is the man who shall love wisdom ."


def test_match_chapter_header_supports_prefixes_and_custom_regexes():
    config = PoetryExtractionConfig(
        book_code="PRO",
        chapter_header_prefixes=("Proverbs", "Sirach"),
        chapter_header_regexes=(r"^JOB\s+(?P<chapter>\d+)\s*(?P<text>.*)$",),
    )
    patterns = compile_chapter_header_patterns(config)
    assert match_chapter_header("Proverbs 3 Wisdom begins", patterns) == (3, "Wisdom begins")
    assert match_chapter_header("JOB 12 The friends reply", patterns) == (12, "The friends reply")


def test_extract_poetry_lines_preserves_psalm_state_machine_with_config():
    config = PoetryExtractionConfig(
        book_code="PSA",
        chapter_header_prefixes=("Psalm",),
        first_chapter_bootstrap_phrases=("Blessed is the man",),
    )
    lines = [
        "B lessed is the m an who walks not in the counsel of the ungodly.",
        "2 But his will is in the law of the Lord.",
        "Psalm 2",
        "1 Why did the Gentiles rage?",
        "2 The kings of the earth were aroused.",
    ]

    rendered = extract_poetry_lines(lines, config)
    assert "## Chapter 1" in rendered
    assert "PSA.1:1 Blessed is the man who walks not in the counsel of the ungodly." in rendered
    assert "PSA.1:2 But his will is in the law of the Lord." in rendered
    assert "## Chapter 2" in rendered
    assert "PSA.2:1 Why did the Gentiles rage?" in rendered
    assert "PSA.2:2 The kings of the earth were aroused." in rendered


def test_resolve_page_range_prefers_explicit_args():
    assert resolve_page_range("PSA", 10, 20) == (10, 20)


def test_resolve_page_range_reads_registry_defaults():
    start, end = resolve_page_range("JOB", None, None)
    assert (start, end) == (1915, 2029)


def test_resolve_page_range_requires_complete_override_pair():
    with pytest.raises(ValueError, match="--page-start and --page-end"):
        resolve_page_range("PSA", 100, None)


def test_resolve_page_range_falls_back_for_unknown_books():
    assert resolve_page_range("XXX", None, None) == (DEFAULT_PAGE_START, DEFAULT_PAGE_END)


def test_resolve_book_defaults_reads_registry_metadata():
    defaults = resolve_book_defaults("PRO")
    assert defaults == {
        "book_name": "Proverbs",
        "testament": "OT",
        "canon_position": 25,
    }


def test_resolve_book_defaults_falls_back_for_unknown_books():
    defaults = resolve_book_defaults("XXX")
    assert defaults == {
        "book_name": "XXX",
        "testament": "OT",
        "canon_position": 24,
    }
