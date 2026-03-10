"""Tests for ChapterTracker — threshold logic with crafted CVC dicts."""

from __future__ import annotations

from pipeline.parse.chapter_tracker import ChapterTracker


def test_advance_no_cvc():
    """With no CVC data, any candidate == current + 1 should advance."""
    ct = ChapterTracker()
    ct.current_chapter = 1
    ct.current_verse = 5
    assert ct.should_advance(2) is True


def test_advance_at_80_pct():
    """Advance when current_verse >= 80% of max_verse."""
    ct = ChapterTracker({1: 20})
    ct.current_chapter = 1
    ct.current_verse = 16  # 80%
    assert ct.should_advance(2) is True


def test_no_advance_below_60_pct():
    """Don't advance when below 60% (no threshold met)."""
    ct = ChapterTracker({1: 20})
    ct.current_chapter = 1
    ct.current_verse = 10  # 50%, candidate 2 < 10 but 10 < 12 (60% threshold)
    assert ct.should_advance(2) is False


def test_backward_signal_at_60_pct():
    """Advance via backward signal when verse > candidate and verse >= 60%."""
    ct = ChapterTracker({11: 20})
    ct.current_chapter = 11
    ct.current_verse = 14  # 70%, candidate 12 < 14 → backward signal
    assert ct.should_advance(12) is True


def test_no_advance_wrong_candidate():
    """Candidate != current + 1 should never advance."""
    ct = ChapterTracker()
    ct.current_chapter = 1
    ct.current_verse = 30
    assert ct.should_advance(3) is False


def test_advance_resets_verse():
    """After advance, current_verse should be 0."""
    ct = ChapterTracker()
    ct.current_chapter = 1
    ct.current_verse = 15
    ct.advance(2)
    assert ct.current_chapter == 2
    assert ct.current_verse == 0


def test_max_verse():
    """max_verse returns expected count or 0 if unknown."""
    ct = ChapterTracker({1: 31, 2: 25})
    assert ct.max_verse(1) == 31
    assert ct.max_verse(2) == 25
    assert ct.max_verse(3) == 0


def test_false_advance_verse_equals_chapter():
    """GEN.11:12 should NOT trigger ch12 advance when only at verse 12/32."""
    ct = ChapterTracker({11: 32})
    ct.current_chapter = 11
    ct.current_verse = 12  # 37.5% — well below 80%
    # candidate 12 == current_chapter + 1 but threshold not met
    assert ct.should_advance(12) is False
