"""
test_verse_split.py — Parser edge-case regression guards for split_verses_in_text
and the lowercase-start verse recovery pipeline.
"""
from __future__ import annotations

import json


# ── split_verses_in_text: uppercase boundary splits ──────────────────────────

def test_uppercase_split_basic(osb_extract):
    """Standard uppercase-start boundary splits at the verse number."""
    results = osb_extract.split_verses_in_text(
        "And God said let there be light. 14 He dwelt in the land",
        current_chapter=1, book_code="TST", start_verse=13
    )
    nums = [v for (_, _, v, _) in results]
    assert 14 in nums


def test_opening_punct_fused(osb_extract):
    """Case 2: opening punctuation fused with digit — 14(He dwelt."""
    results = osb_extract.split_verses_in_text(
        "And God said. 14(He dwelt in the land",
        current_chapter=1, book_code="TST", start_verse=13
    )
    nums = [v for (_, _, v, _) in results]
    assert 14 in nums


# ── Lowercase-start verse recovery (_recover_lc_splits) ─────────────────────

def test_lc_opener_and(osb_extract):
    """lc opener 'and' with terminal-punct signal recovers the verse."""
    results = osb_extract.split_verses_in_text(
        "He came to the end. 18 and he said unto them",
        current_chapter=1, book_code="TST", start_verse=17
    )
    nums = [v for (_, _, v, _) in results]
    assert 18 in nums


def test_lc_opener_if(osb_extract):
    """lc opener 'if' with comma+sequential signal recovers the verse."""
    results = osb_extract.split_verses_in_text(
        "he went to bed, 19 if the man rises",
        current_chapter=1, book_code="TST", start_verse=18
    )
    nums = [v for (_, _, v, _) in results]
    assert 19 in nums


def test_fused_digit_word(osb_extract):
    """Fused digit-word '2that' triggers lc recovery."""
    results = osb_extract.split_verses_in_text(
        "the Lord said. 2that they should go",
        current_chapter=1, book_code="TST", start_verse=1
    )
    nums = [v for (_, _, v, _) in results]
    assert 2 in nums


# ── _lc_boundary_valid signal tests ──────────────────────────────────────────

def test_signal1_terminal_punct(osb_extract):
    """Signal 1: terminal punctuation → always accept."""
    assert osb_extract._lc_boundary_valid("the end.", 5, 4) is True


def test_signal1b_comma_sequential(osb_extract):
    """Signal 1b: comma/semicolon + sequential → accept."""
    assert osb_extract._lc_boundary_valid("a word,", 5, 4) is True


def test_signal2_reject_inline_ctx(osb_extract):
    """Signal 2: preceding word in _INLINE_NUM_CTX → reject."""
    assert osb_extract._lc_boundary_valid("lived years", 5, 4) is False


def test_signal3_sequential(osb_extract):
    """Signal 3: sequential +1 with no rejection signal → accept."""
    assert osb_extract._lc_boundary_valid("some word", 5, 4) is True


# ── Single-part branch lc recovery ──────────────────────────────────────────

def test_single_part_lc_recovery(osb_extract):
    """When no uppercase split fires, lc recovery still runs on the single part."""
    # No uppercase letter after digit, so RE_VERSE_SPLIT won't split.
    # But lc recovery should find "2 and".
    results = osb_extract.split_verses_in_text(
        "the Lord spoke. 2 and he said unto them",
        current_chapter=1, book_code="TST", start_verse=1
    )
    nums = [v for (_, _, v, _) in results]
    assert 2 in nums
    assert len(results) == 2


# ── Negative tests (guard against false expansion) ──────────────────────────

def test_preserving_not_in_openers(osb_extract):
    """'preserving' is not an lc opener — no false lc match."""
    results = osb_extract.split_verses_in_text(
        "abounding in mercy and true, 7preserving righteousness",
        current_chapter=34, book_code="TST", start_verse=6
    )
    nums = [v for (_, _, v, _) in results]
    assert 7 not in nums


def test_except_not_in_openers(osb_extract):
    """'except' is not an lc opener — documents known miss."""
    results = osb_extract.split_verses_in_text(
        "the Lord said. 24except those things which",
        current_chapter=1, book_code="TST", start_verse=23
    )
    nums = [v for (_, _, v, _) in results]
    assert 24 not in nums


def test_boundary_marker_trace_attaches_to_preceding_verse(osb_extract):
    """Boundary-trailing marker stays on the preceding verse with trace metadata."""
    results = osb_extract.split_verses_in_text(
        "He finished the word. † 2 And he continued",
        current_chapter=1, book_code="TST", start_verse=1
    )
    markers = results[0][3]
    assert len(results) == 2
    assert markers[0]["marker"] == "†"
    assert markers[0]["ownership"] == "boundary_trailing"
    assert "And he continued" in markers[0]["normalized_excerpt"]


def test_inline_marker_trace_contains_provenance_fields(osb_extract):
    """Inline markers emit structured trace records even without page provenance."""
    results = osb_extract.split_verses_in_text(
        "He† finished the word.",
        current_chapter=1, book_code="TST", start_verse=1
    )
    marker = results[0][3][0]
    assert marker["marker"] == "†"
    assert marker["ownership"] == "inline_body"
    assert marker["element_index"] is None
    assert marker["page"] is None
    assert marker["raw_excerpt"]
    assert marker["normalized_excerpt"]


def test_lc_split_relabels_marker_ownership(osb_extract):
    """Markers retained on lc-split first segments are explicitly labeled."""
    results = osb_extract.split_verses_in_text(
        "He† finished the word. 2 and he continued",
        current_chapter=1, book_code="TST", start_verse=1
    )
    assert len(results) == 2
    marker = results[0][3][0]
    assert marker["ownership"] == "lc_split_first_segment"


def test_write_outputs_emits_structured_footnote_marker_sidecar(
    osb_extract, tmp_path, monkeypatch
):
    """Footnote sidecar includes top-level metadata and stable marker sequencing."""
    monkeypatch.setattr(osb_extract, "STAGING_ROOT", tmp_path / "staging" / "validated")

    from pipeline.common.types import VerseRecord
    state = osb_extract.ExtractionState("TST")
    state.verses = [
        VerseRecord(anchor="TST.1:1", chapter=1, verse=1, text="Verse one."),
        VerseRecord(anchor="TST.1:2", chapter=1, verse=2, text="Verse two."),
    ]
    state.footnote_markers = [
        {
            "anchor": "TST.1:1",
            "marker": "†",
            "ownership": "inline_body",
            "element_index": 4,
            "page": 111,
            "raw_excerpt": "Verse† one",
            "normalized_excerpt": "Verse† one",
        },
        {
            "anchor": "TST.1:2",
            "marker": "ω",
            "ownership": "boundary_trailing",
            "element_index": 5,
            "page": 111,
            "raw_excerpt": "ω 2 Verse two",
            "normalized_excerpt": "ω 2 Verse two",
        },
    ]

    meta = {
        "name": "Test Book",
        "testament": "OT",
        "position": 1,
        "deuterocanonical": False,
    }
    osb_extract.write_outputs(state, meta, "OT", dry_run=False)

    markers_path = tmp_path / "staging" / "validated" / "OT" / "TST_footnote_markers.json"
    data = json.loads(markers_path.read_text(encoding="utf-8"))
    assert data["book_code"] == "TST"
    assert data["marker_count"] == 2
    assert data["source_text_pages"] == [111]
    assert data["markers"][0]["marker_seq_book"] == 1
    assert data["markers"][1]["marker_seq_book"] == 2
    assert data["markers"][0]["marker_index_in_verse"] == 1


def test_process_element_article_mode_entry_and_exit(osb_extract):
    """Section header enters article mode; later verse text exits cleanly."""
    from pipeline.common.types import VerseRecord

    state = osb_extract.ExtractionState("TST", chapter_verse_counts={1: 10})
    state.verses = [VerseRecord(anchor="TST.1:5", chapter=1, verse=5, text="Verse five.")]
    state.current_chapter = 1
    state.current_verse = 5
    state.verse_started = True

    state.process_element("SectionHeaderItem", "T H E  A R T I C L E", "T H E  A R T I C L E")
    state.process_element("TextItem", "1 First point", "1 First point")
    state.process_element("TextItem", "2 Second point", "2 Second point")
    state.process_element("TextItem", "6 Verse six resumes.", "6 Verse six resumes.")

    assert len(state.articles) == 1
    assert state.articles[0].title == "The Article"
    assert "First point" in state.articles[0].body[0]
    assert "Second point" in state.articles[0].body[1]
    assert state.verses[-1].anchor == "TST.1:6"
    assert state.mode == osb_extract.VERSE_MODE


def test_process_element_text_chapter_advance(osb_extract):
    """TextItem chapter lead delegates to ChapterTracker and emits chapter 2 verse 1."""
    from pipeline.common.types import VerseRecord

    state = osb_extract.ExtractionState("TST", chapter_verse_counts={1: 10, 2: 10})
    state.verses = [VerseRecord(anchor="TST.1:8", chapter=1, verse=8, text="Verse eight.")]
    state.current_chapter = 1
    state.current_verse = 8
    state.verse_started = True

    state.process_element("TextItem", "2 Verse one of chapter two.", "2 Verse one of chapter two.")

    assert state.current_chapter == 2
    assert state.verses[-1].anchor == "TST.2:1"


def test_process_element_column_split_resplits_previous_verse(osb_extract):
    """Incomplete prior verse merges with prose and re-splits when a later verse appears."""
    from pipeline.common.types import VerseRecord

    state = osb_extract.ExtractionState("TST")
    state.verses = [VerseRecord(anchor="TST.1:1", chapter=1, verse=1, text="He said and")]
    state.current_chapter = 1
    state.current_verse = 1
    state.verse_started = True
    state.last_verse_text_incomplete = True

    state.process_element("TextItem", "then continued. 2 And spoke again.", "then continued. 2 And spoke again.")

    assert [verse.anchor for verse in state.verses] == ["TST.1:1", "TST.1:2"]
    assert "then continued" in state.verses[0].text
    assert "And spoke again" in state.verses[1].text


def test_process_element_section_header_emits_heading(osb_extract):
    """Title-case SectionHeaderItem in verse mode becomes a narrative heading."""
    from pipeline.common.types import VerseRecord

    state = osb_extract.ExtractionState("TST")
    state.verses = [VerseRecord(anchor="TST.1:1", chapter=1, verse=1, text="Verse one.")]
    state.current_chapter = 1
    state.current_verse = 1
    state.verse_started = True

    state.process_element("SectionHeaderItem", "The Heading", "The Heading")

    assert len(state.headings) == 1
    assert state.headings[0].after_anchor == "TST.1:1"
    assert state.headings[0].heading == "The Heading"
