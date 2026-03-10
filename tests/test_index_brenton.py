"""
test_index_brenton.py — Tests for Brenton Septuagint indexing logic.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

from pipeline.reference.index_brenton import (
    BOOK_CODE_ALIASES,
    RE_FILENAME,
    parse_chapter_file,
    summarize,
    write_book_json,
)


class TestFilenameRegex:
    """Verify the Brenton filename regex matches expected patterns."""

    def test_standard_filename(self):
        """Standard Brenton filename should match with position, code, chapter."""
        m = RE_FILENAME.match("eng-Brenton_001_GEN_01_read.txt")
        assert m is not None
        assert m.group(1) == "001"
        assert m.group(2) == "GEN"
        assert m.group(3) == "01"

    def test_three_digit_chapter(self):
        """Three-digit chapter numbers should be accepted."""
        m = RE_FILENAME.match("eng-Brenton_019_PSA_150_read.txt")
        assert m is not None
        assert m.group(3) == "150"

    def test_non_matching_filename(self):
        """Non-Brenton filenames should not match."""
        m = RE_FILENAME.match("some_random_file.txt")
        assert m is None

    def test_metadata_file_code_000(self):
        """Metadata file (code 000) should still match regex (filtered later)."""
        m = RE_FILENAME.match("eng-Brenton_000_000_00_read.txt")
        assert m is not None


class TestAliasMapping:
    """Verify Brenton code aliases map to correct registry codes."""

    def test_dag_to_dan(self):
        """DAG (Daniel Greek/LXX) should map to DAN."""
        assert BOOK_CODE_ALIASES["DAG"] == "DAN"

    def test_esg_to_est(self):
        """ESG (Esther Greek) should map to EST."""
        assert BOOK_CODE_ALIASES["ESG"] == "EST"

    def test_nam_to_nah(self):
        """NAM (Nahum filename code) should map to NAH."""
        assert BOOK_CODE_ALIASES["NAM"] == "NAH"

    def test_alias_passthrough_for_unknown(self):
        """Non-aliased codes should return themselves via dict.get."""
        assert BOOK_CODE_ALIASES.get("GEN", "GEN") == "GEN"
        assert BOOK_CODE_ALIASES.get("EXO", "EXO") == "EXO"


class TestParseChapterFile:
    """Verify chapter file parsing extracts verse texts correctly."""

    def test_basic_chapter_file(self, tmp_path):
        """Standard chapter file should yield verse texts after skipping 2 header lines."""
        chapter_file = tmp_path / "eng-Brenton_001_GEN_01_read.txt"
        chapter_file.write_text(
            "Genesis.\n"
            "Chapter 1.\n"
            "In the beginning God made the heaven and the earth.\n"
            "But the earth was unsightly and unfurnished.\n"
            "And God said, Let there be light, and there was light.\n",
            encoding="utf-8",
        )
        verses = parse_chapter_file(chapter_file)
        assert len(verses) == 3
        assert verses[0].startswith("In the beginning")
        assert verses[1].startswith("But the earth")
        assert verses[2].startswith("And God said")

    def test_empty_lines_skipped(self, tmp_path):
        """Empty lines between verses should be skipped."""
        chapter_file = tmp_path / "eng-Brenton_001_GEN_02_read.txt"
        chapter_file.write_text(
            "Genesis.\n"
            "Chapter 2.\n"
            "And the heavens and the earth were finished.\n"
            "\n"
            "And God finished on the sixth day.\n"
            "\n"
            "\n"
            "And God blessed the seventh day.\n",
            encoding="utf-8",
        )
        verses = parse_chapter_file(chapter_file)
        assert len(verses) == 3

    def test_empty_chapter(self, tmp_path):
        """Chapter file with only header lines should yield an empty list."""
        chapter_file = tmp_path / "eng-Brenton_001_GEN_03_read.txt"
        chapter_file.write_text(
            "Genesis.\n"
            "Chapter 3.\n",
            encoding="utf-8",
        )
        verses = parse_chapter_file(chapter_file)
        assert verses == []

    def test_whitespace_stripping(self, tmp_path):
        """Trailing whitespace should be stripped from verse texts."""
        chapter_file = tmp_path / "eng-Brenton_001_GEN_04_read.txt"
        chapter_file.write_text(
            "Genesis.\n"
            "Chapter 4.\n"
            "And Adam knew Eve his wife.   \n"
            "And she conceived and bore Cain.  \n",
            encoding="utf-8",
        )
        verses = parse_chapter_file(chapter_file)
        assert len(verses) == 2
        assert not verses[0].endswith(" ")
        assert not verses[1].endswith(" ")


class TestSummarize:
    """Verify the summary line format."""

    def test_summary_format_basic(self):
        """Summary should include book code, chapter count, and verse count."""
        data = {
            "chapters": {
                "1": {"verses": ["v1", "v2", "v3"], "line_count": 3},
                "2": {"verses": ["v1", "v2"], "line_count": 2},
            },
            "warnings": [],
        }
        result = summarize("GEN", data)
        assert "GEN" in result
        assert "2 chapters" in result
        assert "5 verses" in result

    def test_summary_with_warnings(self):
        """Summary should note warning count when present."""
        data = {
            "chapters": {
                "1": {"verses": ["v1"], "line_count": 1},
            },
            "warnings": ["some warning"],
        }
        result = summarize("TST", data)
        assert "1 warning(s)" in result


class TestWriteBookJson:
    """Verify JSON output structure."""

    def test_output_structure(self, tmp_path, monkeypatch):
        """Written JSON should have expected top-level keys."""
        import pipeline.reference.index_brenton as mod
        monkeypatch.setattr(mod, "OUTPUT_DIR", tmp_path)

        data = {
            "chapters": {
                "1": {"verses": ["In the beginning"], "line_count": 1},
            },
            "warnings": [],
        }
        out_path = write_book_json("TST", data)
        assert out_path.exists()

        import json
        with open(out_path, encoding="utf-8") as f:
            payload = json.load(f)

        assert payload["book_code"] == "TST"
        assert "source" in payload
        assert "chapters" in payload
        assert "1" in payload["chapters"]
        assert payload["chapters"]["1"]["verses"] == ["In the beginning"]
