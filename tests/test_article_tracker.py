"""Tests for ArticleTracker — subpoint sequencing, flush behavior."""

from __future__ import annotations

from pipeline.parse.article_tracker import ArticleTracker


def test_start_and_flush():
    """Starting an article and flushing returns an ArticleRecord."""
    at = ArticleTracker()
    at.start("The Holy Trinity", "GEN.1:26")
    at.add_body("Paragraph 1")
    at.add_body("Paragraph 2")
    record = at.flush()
    assert record is not None
    assert record.title == "The Holy Trinity"
    assert record.after_anchor == "GEN.1:26"
    assert len(record.body) == 2


def test_flush_empty():
    """Flushing when no article active returns None."""
    at = ArticleTracker()
    assert at.flush() is None


def test_active_property():
    at = ArticleTracker()
    assert not at.active
    at.start("Title", "GEN.1:1")
    assert at.active
    at.flush()
    assert not at.active


def test_subpoint_rule1_sequential():
    """Rule 1: sequential sub-point continuation."""
    at = ArticleTracker()
    at.start("Title", "GEN.1:1")
    # First sub-point via Rule 3
    assert at.is_subpoint(1, current_verse=5) is True
    # Sequential continuation via Rule 1
    assert at.is_subpoint(2, current_verse=5) is True
    assert at.is_subpoint(3, current_verse=5) is True


def test_subpoint_rule1_rejects_above_current_verse():
    """Rule 1 requires num <= current_verse."""
    at = ArticleTracker()
    at.start("Title", "GEN.1:1")
    at.is_subpoint(1, current_verse=2)  # Rule 3 enters
    # num 3 > current_verse 2 → not a sub-point
    assert at.is_subpoint(3, current_verse=2) is False


def test_subpoint_rule3_first():
    """Rule 3: first sub-point when seq == 0 and num == 1."""
    at = ArticleTracker()
    at.start("Title", "GEN.3:7")
    assert at.is_subpoint(1, current_verse=7) is True


def test_subpoint_rule3_rejects_when_no_verses():
    """Rule 3 requires current_verse >= 1."""
    at = ArticleTracker()
    at.start("Title", "GEN.0:0")
    assert at.is_subpoint(1, current_verse=0) is False


def test_exit_signal_verse_resume():
    """num > current_verse signals article exit."""
    at = ArticleTracker()
    assert at.is_exit_signal(10, current_verse=5, current_chapter=1) is True


def test_exit_signal_chapter_advance():
    """num == current_chapter + 1 signals article exit."""
    at = ArticleTracker()
    assert at.is_exit_signal(2, current_verse=30, current_chapter=1) is True


def test_exit_signal_no_exit():
    """Non-sequential number within range is NOT an exit signal."""
    at = ArticleTracker()
    assert at.is_exit_signal(3, current_verse=10, current_chapter=5) is False


def test_add_subheading():
    at = ArticleTracker()
    at.start("Title", "GEN.1:1")
    at.add_subheading("Sub Topic")
    record = at.flush()
    assert "\n#### Sub Topic\n" in record.body
