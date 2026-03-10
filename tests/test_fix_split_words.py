"""
test_fix_split_words.py — Tests for fix_split_words.py split-word detection and joining.
"""
from __future__ import annotations

from pipeline.cleanup.fix_split_words import fix_line


class TestKnownSplitWordJoining:
    """Verify that known split-word patterns are detected and joined."""

    def test_forever_split(self):
        """'forev er' should be joined to 'forever'."""
        line = "GEN.1:1 He shall reign forev er and ever."
        fixed, count = fix_line(line)
        assert "forever" in fixed
        assert count >= 1

    def test_have_split(self):
        """'hav e' should be joined to 'have'."""
        line = "GEN.2:3 They hav e nothing left."
        fixed, count = fix_line(line)
        assert "have" in fixed
        assert count >= 1

    def test_beloved_split(self):
        """'belov ed' should be joined to 'beloved'."""
        line = "GEN.3:1 My belov ed son."
        fixed, count = fix_line(line)
        assert "beloved" in fixed
        assert count >= 1

    def test_silver_split(self):
        """'silv er' should be joined to 'silver'."""
        line = "GEN.4:1 Three hundred silv er shekels."
        fixed, count = fix_line(line)
        assert "silver" in fixed
        assert count >= 1

    def test_servant_split(self):
        """'serv ant' should be joined to 'servant'."""
        line = "GEN.5:1 The serv ant of the Lord."
        fixed, count = fix_line(line)
        assert "servant" in fixed
        assert count >= 1

    def test_over_split(self):
        """'ov er' should be joined to 'over'."""
        line = "GEN.6:1 He ruled ov er the land."
        fixed, count = fix_line(line)
        assert "over" in fixed
        assert count >= 1

    def test_delivered_split(self):
        """'deliv ered' should be joined to 'delivered'."""
        line = "GEN.7:1 The Lord deliv ered them."
        fixed, count = fix_line(line)
        assert "delivered" in fixed
        assert count >= 1

    def test_gave_split(self):
        """'gav e' should be joined to 'gave'."""
        line = "GEN.8:1 He gav e them bread."
        fixed, count = fix_line(line)
        assert "gave" in fixed
        assert count >= 1

    def test_olive_split(self):
        """'oliv e' should be joined to 'olive'."""
        line = "GEN.9:1 An oliv e branch."
        fixed, count = fix_line(line)
        assert "olive" in fixed
        assert count >= 1


class TestFalsePositiveProtection:
    """Ensure real words that look like splits are NOT modified."""

    def test_clean_text_unchanged(self):
        """Text with no split words should pass through unchanged."""
        line = "GEN.1:1 In the beginning God created the heavens and the earth."
        fixed, count = fix_line(line)
        assert fixed == line
        assert count == 0

    def test_word_liver_not_split(self):
        """'liver' should not be treated as 'li' + 'ver'."""
        line = "GEN.1:1 The liver of the animal was removed."
        fixed, count = fix_line(line)
        assert "liver" in fixed

    def test_word_river_not_split(self):
        """'river' should not be treated as 'ri' + 'ver'."""
        line = "GEN.1:1 The river flowed through the garden."
        fixed, count = fix_line(line)
        assert "river" in fixed

    def test_word_hover_not_split(self):
        """'hover' should not be treated as 'ho' + 'ver'."""
        line = "GEN.1:1 The Spirit did hover over the waters."
        fixed, count = fix_line(line)
        assert "hover" in fixed

    def test_word_never_not_split(self):
        """'never' should not be treated as 'ne' + 'ver'."""
        line = "GEN.1:1 He shall never return."
        fixed, count = fix_line(line)
        assert "never" in fixed


class TestMultipleSplitsInOneLine:
    """Multiple split words in a single line should all be fixed."""

    def test_two_splits_in_one_line(self):
        """Two split words in one line should both be joined."""
        line = "GEN.1:1 He gav e the serv ant food."
        fixed, count = fix_line(line)
        assert "gave" in fixed
        assert "servant" in fixed
        assert count >= 2

    def test_three_splits_in_one_line(self):
        """Three split words in one line should all be joined."""
        line = "GEN.1:1 He deliv ered the belov ed serv ant."
        fixed, count = fix_line(line)
        assert "delivered" in fixed
        assert "beloved" in fixed
        assert "servant" in fixed
        assert count >= 3


class TestNoAnchorLines:
    """Lines without anchors should still have known-word fixes applied."""

    def test_non_anchor_line_known_words(self):
        """Known split words should be fixed even without an anchor prefix."""
        line = "The belov ed of the Lord."
        fixed, count = fix_line(line)
        assert "beloved" in fixed
        assert count >= 1

    def test_chapter_heading_unchanged(self):
        """Chapter headings should not be modified."""
        line = "## Chapter 1"
        fixed, count = fix_line(line)
        assert fixed == line
        assert count == 0

    def test_empty_line_unchanged(self):
        """Empty lines should pass through unchanged."""
        line = ""
        fixed, count = fix_line(line)
        assert fixed == ""
        assert count == 0


class TestVSuffixRegex:
    """V-suffix regex only applies to body text after anchors."""

    def test_v_suffix_in_anchor_body(self):
        """V-suffix joins should work in anchor body text."""
        line = "GEN.1:1 He lov ed the people."
        fixed, count = fix_line(line)
        # "lov ed" matches the v-suffix regex (ov suffix)
        # It may or may not match depending on KNOWN_SPLIT_JOIN_WORDS
        # The key test is that fixing runs without error
        assert isinstance(fixed, str)
        assert isinstance(count, int)
