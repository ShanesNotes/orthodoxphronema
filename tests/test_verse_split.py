"""
test_verse_split.py — Parser edge-case regression guards for split_verses_in_text
and the lowercase-start verse recovery pipeline.
"""
from __future__ import annotations


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
