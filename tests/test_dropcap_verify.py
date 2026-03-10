"""
test_dropcap_verify.py — Tests for drop-cap detection and classification.
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from pipeline.cleanup.dropcap_verify import (
    RESIDUAL_MAP,
    _ALWAYS_AMBIGUOUS_RESIDUALS,
    _CONFIRM_THRESHOLD,
    _REJECT_THRESHOLD,
    classify_dropcap,
    apply_repairs,
)


class TestResidualMapLookups:
    """Verify that RESIDUAL_MAP entries produce correct classifications."""

    def test_ow_prefix_maps_to_now(self):
        """'ow ' residual should propose 'Now ' repair."""
        result = classify_dropcap("GEN.2:1", "ow the Lord said", 2, 1, None, None)
        assert result is not None
        assert result["proposed_repair"].startswith("Now ")
        assert result["missing_prefix"] == "N"
        # No Brenton → confirmed_auto (not ambiguous like "o ")
        assert result["classification"] == "confirmed_auto"

    def test_nthe_prefix_maps_to_in_the(self):
        """'nthe ' residual should propose 'In the ' repair with 2-char drop-cap."""
        result = classify_dropcap("GEN.1:1", "nthe beginning God created", 1, 1, None, None)
        assert result is not None
        assert result["proposed_repair"].startswith("In the ")
        assert result["missing_prefix"] == "In"

    def test_hen_prefix_is_always_ambiguous(self):
        """'hen ' residual is inherently ambiguous (Then vs When)."""
        result = classify_dropcap("GEN.3:1", "hen the serpent said", 3, 1, None, None)
        assert result is not None
        assert result["classification"] == "ambiguous_human"

    def test_he_prefix_maps_to_the(self):
        """'he ' residual should propose 'The ' repair."""
        result = classify_dropcap("GEN.4:1", "he Lord spoke", 4, 1, None, None)
        assert result is not None
        assert result["proposed_repair"].startswith("The ")
        assert result["missing_prefix"] == "T"
        assert result["classification"] == "confirmed_auto"

    def test_nd_prefix_maps_to_and(self):
        """'nd ' residual should propose 'And ' repair."""
        result = classify_dropcap("GEN.5:1", "nd God said", 5, 1, None, None)
        assert result is not None
        assert result["proposed_repair"].startswith("And ")
        assert result["missing_prefix"] == "A"

    def test_o_space_is_ambiguous_without_brenton(self):
        """'o ' is ambiguous (So vs No) without Brenton confirmation."""
        result = classify_dropcap("GEN.6:1", "o the Lord said", 6, 1, None, None)
        assert result is not None
        assert result["classification"] == "ambiguous_human"

    def test_ut_prefix_maps_to_but(self):
        """'ut ' residual should propose 'But ' repair."""
        result = classify_dropcap("GEN.7:1", "ut the people rebelled", 7, 1, None, None)
        assert result is not None
        assert result["proposed_repair"].startswith("But ")
        assert result["missing_prefix"] == "B"

    def test_fter_prefix_maps_to_after(self):
        """'fter ' residual should propose 'After ' repair."""
        result = classify_dropcap("GEN.8:1", "fter these things", 8, 1, None, None)
        assert result is not None
        assert result["proposed_repair"].startswith("After ")
        assert result["missing_prefix"] == "A"

    def test_hus_prefix_maps_to_thus(self):
        """'hus ' residual should propose 'Thus ' repair."""
        result = classify_dropcap("GEN.9:1", "hus says the Lord", 9, 1, None, None)
        assert result is not None
        assert result["proposed_repair"].startswith("Thus ")
        assert result["missing_prefix"] == "T"

    def test_n_space_prefix_maps_to_in(self):
        """'n ' residual should propose 'In ' repair."""
        result = classify_dropcap("GEN.10:1", "n those days", 10, 1, None, None)
        assert result is not None
        assert result["proposed_repair"].startswith("In ")
        assert result["missing_prefix"] == "I"

    def test_gain_prefix_maps_to_again(self):
        """'gain ' residual should propose 'Again ' repair."""
        result = classify_dropcap("GEN.11:1", "gain the Lord appeared", 11, 1, None, None)
        assert result is not None
        assert result["proposed_repair"].startswith("Again ")
        assert result["missing_prefix"] == "A"


class TestNonCandidates:
    """Verify that non-drop-cap verses return None."""

    def test_uppercase_start_returns_none(self):
        """Verse starting with uppercase should not be a drop-cap candidate."""
        result = classify_dropcap("GEN.1:1", "In the beginning", 1, 1, None, None)
        assert result is None

    def test_empty_text_returns_none(self):
        """Empty text should not be a drop-cap candidate."""
        result = classify_dropcap("GEN.1:1", "", 1, 1, None, None)
        assert result is None

    def test_digit_start_returns_none(self):
        """Text starting with a digit is not a drop-cap candidate."""
        result = classify_dropcap("GEN.1:1", "3 hundred cubits", 1, 1, None, None)
        assert result is None


class TestUnmatchedResidual:
    """Verify behavior when no residual map entry matches."""

    def test_unmatched_lowercase_start(self):
        """Lowercase start without residual match yields ambiguous_human."""
        result = classify_dropcap("GEN.12:1", "xyzzy unknown text", 12, 1, None, None)
        assert result is not None
        assert result["classification"] == "ambiguous_human"
        assert result["proposed_repair"] is None
        assert result["source"] == "residual_unmatched"


class TestResidualMapOrdering:
    """Verify that longer prefixes match before shorter ones."""

    def test_nthe_matches_before_n(self):
        """'nthe ' (2-char drop-cap) should match before 'n ' (1-char)."""
        result = classify_dropcap("GEN.1:1", "nthe beginning", 1, 1, None, None)
        assert result is not None
        assert result["missing_prefix"] == "In"
        assert result["proposed_repair"].startswith("In the ")

    def test_tcame_matches_before_general(self):
        """'tcame ' should match the 2-char 'It came' entry."""
        result = classify_dropcap("GEN.1:1", "tcame to pass", 1, 1, None, None)
        assert result is not None
        assert result["missing_prefix"] == "It"


class TestApplyRepairs:
    """Verify that confirmed repairs are applied to canon files."""

    def test_apply_confirmed_repairs(self, tmp_path):
        """Confirmed repairs should prepend missing prefix to verse text."""
        canon = tmp_path / "TST.md"
        canon.write_text(
            "---\nbook_code: TST\n---\n\n"
            "## Chapter 1\n\n"
            "TST.1:1 ow the Lord said\n"
            "TST.1:2 In the beginning\n",
            encoding="utf-8",
        )
        candidates_file = tmp_path / "TST_dropcap_candidates.json"
        candidates_data = {
            "ratified": True,
            "candidates": [
                {
                    "anchor": "TST.1:1",
                    "classification": "confirmed_auto",
                    "missing_prefix": "N",
                },
            ],
        }
        candidates_file.write_text(
            json.dumps(candidates_data), encoding="utf-8"
        )
        count = apply_repairs(canon, candidates_file)
        assert count == 1
        text = canon.read_text(encoding="utf-8")
        assert "TST.1:1 Now the Lord said" in text
        # Unaffected verse should remain unchanged
        assert "TST.1:2 In the beginning" in text

    def test_apply_skips_ambiguous(self, tmp_path):
        """Ambiguous candidates should not be applied."""
        canon = tmp_path / "TST.md"
        canon.write_text(
            "---\nbook_code: TST\n---\n\n"
            "TST.1:1 hen the serpent said\n",
            encoding="utf-8",
        )
        candidates_file = tmp_path / "TST_dropcap_candidates.json"
        candidates_data = {
            "ratified": True,
            "candidates": [
                {
                    "anchor": "TST.1:1",
                    "classification": "ambiguous_human",
                    "missing_prefix": "T",
                },
            ],
        }
        candidates_file.write_text(
            json.dumps(candidates_data), encoding="utf-8"
        )
        count = apply_repairs(canon, candidates_file)
        assert count == 0

    def test_apply_rejects_unratified(self, tmp_path):
        """Unratified candidates JSON should cause sys.exit."""
        import pytest

        canon = tmp_path / "TST.md"
        canon.write_text("---\nbook_code: TST\n---\n\nTST.1:1 ow text\n", encoding="utf-8")
        candidates_file = tmp_path / "TST_dropcap_candidates.json"
        candidates_data = {
            "ratified": False,
            "candidates": [
                {"anchor": "TST.1:1", "classification": "confirmed_auto", "missing_prefix": "N"},
            ],
        }
        candidates_file.write_text(json.dumps(candidates_data), encoding="utf-8")
        with pytest.raises(SystemExit):
            apply_repairs(canon, candidates_file)

    def test_apply_human_verified(self, tmp_path):
        """human_verified classification should also be applied."""
        canon = tmp_path / "TST.md"
        canon.write_text(
            "---\nbook_code: TST\n---\n\nTST.1:1 hen the serpent\n",
            encoding="utf-8",
        )
        candidates_file = tmp_path / "TST_dropcap_candidates.json"
        candidates_data = {
            "ratified": True,
            "candidates": [
                {
                    "anchor": "TST.1:1",
                    "classification": "human_verified",
                    "missing_prefix": "W",
                },
            ],
        }
        candidates_file.write_text(json.dumps(candidates_data), encoding="utf-8")
        count = apply_repairs(canon, candidates_file)
        assert count == 1
        text = canon.read_text(encoding="utf-8")
        assert "TST.1:1 When the serpent" in text


class TestThresholdConstants:
    """Verify threshold constants are set to expected values."""

    def test_confirm_threshold(self):
        """Confirm threshold should be 0.70."""
        assert _CONFIRM_THRESHOLD == 0.70

    def test_reject_threshold(self):
        """Reject threshold should be 0.40."""
        assert _REJECT_THRESHOLD == 0.40

    def test_hen_is_always_ambiguous(self):
        """'hen ' should be in the always-ambiguous set."""
        assert "hen " in _ALWAYS_AMBIGUOUS_RESIDUALS
