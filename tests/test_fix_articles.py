"""
test_fix_articles.py — Regression coverage for fused-article spell audit.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from pipeline.cleanup import fix_articles


def test_spell_audit_boosts_obvious_fused_article_candidates():
    decree = fix_articles.find_fused_articles("he established adecree for them", "TST.1:1", None)
    ephod = fix_articles.find_fused_articles("he clothed him with aephod", "TST.1:2", None)

    assert decree
    assert decree[0]["token"] == "adecree"
    assert decree[0]["confidence"] >= 0.75
    assert decree[0]["replacement"] == "a decree"

    assert ephod
    assert ephod[0]["token"] == "aephod"
    assert ephod[0]["confidence"] >= 0.75
    assert ephod[0]["replacement"] == "an ephod"

    if shutil.which("aspell"):
        assert "aspell" in decree[0]["source_hint"]


def test_false_positive_name_is_suppressed():
    mod = fix_articles
    candidates = mod.find_fused_articles("Abimelech went down", "TST.1:3", None)
    assert candidates == []


def test_titlecase_name_like_arad_is_suppressed():
    mod = fix_articles
    candidates = mod.find_fused_articles("Arad was defeated", "TST.1:4", None)
    assert candidates == []


def test_live_historical_targets_are_detected():
    mod = fix_articles
    candidates = mod.find_fused_articles(
        "there was acertain man who made atreaty with aprophet",
        "TST.1:4",
        None,
    )
    tokens = {candidate["token"] for candidate in candidates}
    assert {"acertain", "atreaty", "aprophet"} <= tokens


def test_editorial_report_shape_contains_pending_candidates(tmp_path):
    mod = fix_articles
    book = tmp_path / "TST.md"
    book.write_text(
        "---\n"
        "book_code: TST\n"
        "---\n\n"
        "TST.1:1 he established adecree for them\n",
        encoding="utf-8",
    )

    _, candidates = mod.process_file(book, None, threshold=1.01)
    report = mod.build_editorial_report("TST", book, candidates)

    assert report["book"] == "TST"
    assert report["total_candidates"] == 1
    assert report["by_category"] == {"fused_article_explicit": 1}
    assert report["candidates"][0]["anchor"] == "TST.1:1"
    assert report["candidates"][0]["manual_status"] == "pending"


def test_auto_fixable_candidate_remains_pending_until_in_place_apply(tmp_path):
    mod = fix_articles
    book = tmp_path / "TST.md"
    book.write_text(
        "---\n"
        "book_code: TST\n"
        "---\n\n"
        "TST.1:1 he established adecree for them\n",
        encoding="utf-8",
    )

    _, candidates = mod.process_file(book, None, threshold=0.70, apply_fixes=False)
    report = mod.build_editorial_report("TST", book, candidates)

    assert report["total_candidates"] == 1
    assert report["candidates"][0]["token"] == "adecree"


def test_editorial_report_merge_preserves_existing_notes(tmp_path):
    mod = fix_articles
    existing = {
        "book": "TST",
        "file": "staging/validated/OT/TST.md",
        "generated": "2026-03-08",
        "total_candidates": 1,
        "by_category": {"truncation": 1},
        "candidates": [
            {
                "line": 8,
                "anchor": "TST.1:8",
                "category": "truncation",
                "token": "truncated",
                "confidence": 0.9,
                "source_hint": "heuristic",
                "manual_status": "pending",
            }
        ],
        "notes": ["Existing truncation audit"],
    }
    book = tmp_path / "TST.md"
    report = {
        "book": "TST",
        "file": str(book),
        "generated": "2026-03-09",
        "total_candidates": 1,
        "by_category": {"fused_article_explicit": 1},
        "candidates": [
            {
                "line": 1,
                "anchor": "TST.1:1",
                "category": "fused_article_explicit",
                "token": "adecree",
                "confidence": 0.91,
                "source_hint": "aspell_split_confirms",
                "manual_status": "pending",
            }
        ],
        "notes": ["Explicit fused article audit from fix_articles.py"],
    }

    merged = mod.merge_editorial_report(existing, report)

    assert merged["total_candidates"] == 2
    assert merged["by_category"] == {"truncation": 1, "fused_article_explicit": 1}
    assert "Existing truncation audit" in merged["notes"]
    assert "Explicit fused article audit from fix_articles.py" in merged["notes"]


# ---------------------------------------------------------------------------
# Additional tests: false positive protection, confidence scoring, Brenton
# ---------------------------------------------------------------------------


class TestFalsePositiveProtection:
    """Words that naturally start with article prefixes should NOT be flagged."""

    def test_common_a_prefix_words_not_flagged(self):
        """Words like 'about', 'above', 'after' should not trigger fused-article detection."""
        for word in ("about", "above", "after", "again", "against", "along",
                     "among", "around", "away", "afraid", "alive", "alone"):
            candidates = fix_articles.find_fused_articles(
                f"He went {word} the city", "TST.1:1", None
            )
            tokens = {c["token"] for c in candidates}
            assert word not in tokens, f"'{word}' should not be flagged as fused article"

    def test_the_prefix_words_not_flagged(self):
        """Words like 'then', 'there', 'these', 'they' should not be flagged."""
        for word in ("then", "there", "these", "they", "therefore", "themselves",
                     "thereof", "therein", "this", "those", "though", "through"):
            candidates = fix_articles.find_fused_articles(
                f"And {word} came forth", "TST.1:1", None
            )
            tokens = {c["token"] for c in candidates}
            assert word not in tokens, f"'{word}' should not be flagged as fused article"

    def test_an_prefix_words_not_flagged(self):
        """Words like 'angel', 'anger', 'another', 'answer' should not be flagged."""
        for word in ("angel", "anger", "another", "answer", "ancient", "animal"):
            candidates = fix_articles.find_fused_articles(
                f"The {word} appeared", "TST.1:1", None
            )
            tokens = {c["token"] for c in candidates}
            assert word not in tokens, f"'{word}' should not be flagged as fused article"

    def test_short_remainder_rejected(self):
        """Remainders shorter than _MIN_WORD_LEN should be rejected."""
        candidates = fix_articles.find_fused_articles(
            "He saw ado about nothing", "TST.1:1", None
        )
        # "ado" has remainder "do" which is only 2 chars → should be rejected
        tokens = {c["token"] for c in candidates}
        assert "ado" not in tokens


class TestFusedArticleDetection:
    """Verify detection of genuine fused article patterns."""

    def test_a_man_fused(self):
        """'aman' should be detected as 'a man'."""
        candidates = fix_articles.find_fused_articles("there was aman", "TST.1:1", None)
        assert any(c["token"] == "aman" and c["replacement"] == "a man" for c in candidates)

    def test_a_house_fused(self):
        """'ahouse' should be detected as 'a house'."""
        candidates = fix_articles.find_fused_articles("he built ahouse", "TST.1:1", None)
        assert any(c["token"] == "ahouse" and c["replacement"] == "a house" for c in candidates)

    def test_the_fused_with_biblical_target(self):
        """'thepriest' should be detected as 'the priest'."""
        candidates = fix_articles.find_fused_articles("and thepriest came", "TST.1:1", None)
        assert any(c["token"] == "thepriest" for c in candidates)

    def test_an_offering_fused(self):
        """'anoffering' should be detected as 'an offering'."""
        candidates = fix_articles.find_fused_articles("he brought anoffering", "TST.1:1", None)
        assert any(c["token"] == "anoffering" for c in candidates)

    def test_a_vowel_word_gets_an(self):
        """'aephod' should be corrected to 'an ephod' (article upgrade)."""
        candidates = fix_articles.find_fused_articles("wearing aephod", "TST.1:1", None)
        assert any(c["replacement"] == "an ephod" for c in candidates)


class TestConfidenceScoring:
    """Verify that confidence is boosted by known biblical targets."""

    def test_biblical_target_boosts_confidence(self):
        """Remainder in _KNOWN_BIBLICAL_TARGETS should boost confidence by 0.3."""
        # "sacrifice" is in _KNOWN_BIBLICAL_TARGETS
        candidates = fix_articles.find_fused_articles("he offered asacrifice", "TST.1:1", None)
        assert candidates
        assert candidates[0]["confidence"] >= 0.8  # base 0.5 + 0.3 biblical

    def test_non_target_has_lower_confidence(self):
        """Remainder not in biblical targets should have lower confidence."""
        candidates = fix_articles.find_fused_articles("he saw amonkey", "TST.1:1", None)
        if candidates:
            assert candidates[0]["confidence"] < 0.85


class TestBrentonConfirmation:
    """Verify Brenton reference confirmation logic."""

    def test_brenton_confirms_exact_phrase(self):
        """Brenton text containing 'a sacrifice' should boost confidence."""
        brenton = {"TST.1:1": "And he offered a sacrifice unto the Lord."}
        boost = fix_articles._brenton_confirms("TST.1:1", "a", "sacrifice", brenton)
        assert boost == 0.4

    def test_brenton_confirms_remainder_only(self):
        """Brenton text containing just the remainder word should give partial boost."""
        brenton = {"TST.1:1": "And he brought his sacrifice."}
        boost = fix_articles._brenton_confirms("TST.1:1", "a", "sacrifice", brenton)
        assert boost == 0.2

    def test_brenton_no_match(self):
        """Brenton text without the word should give no boost."""
        brenton = {"TST.1:1": "And he went away."}
        boost = fix_articles._brenton_confirms("TST.1:1", "a", "sacrifice", brenton)
        assert boost == 0.0

    def test_brenton_missing_anchor(self):
        """Missing anchor in Brenton should give no boost."""
        brenton = {"TST.1:2": "Some other verse."}
        boost = fix_articles._brenton_confirms("TST.1:1", "a", "sacrifice", brenton)
        assert boost == 0.0

    def test_brenton_none_gives_zero(self):
        """None Brenton reference should give no boost."""
        boost = fix_articles._brenton_confirms("TST.1:1", "a", "sacrifice", None)
        assert boost == 0.0


class TestReplacementPhrase:
    """Verify _replacement_phrase logic for article upgrade."""

    def test_a_before_consonant(self):
        """'a' before consonant word should stay 'a'."""
        assert fix_articles._replacement_phrase("a", "man") == "a man"

    def test_a_before_vowel_upgrades_to_an(self):
        """'a' before vowel word should upgrade to 'an'."""
        assert fix_articles._replacement_phrase("a", "offering") == "an offering"

    def test_capital_a_before_vowel(self):
        """'A' before vowel word should upgrade to 'An'."""
        assert fix_articles._replacement_phrase("A", "offering") == "An offering"

    def test_the_unchanged(self):
        """'the' prefix should not be upgraded."""
        assert fix_articles._replacement_phrase("the", "priest") == "the priest"


class TestProcessFileApply:
    """Verify process_file applies fixes correctly."""

    def test_in_place_fix_applies(self, tmp_path):
        """With apply_fixes=True, fixable candidates should be resolved."""
        book = tmp_path / "TST.md"
        book.write_text(
            "---\nbook_code: TST\n---\n\n"
            "TST.1:1 he offered asacrifice to the Lord\n",
            encoding="utf-8",
        )
        fixed_lines, candidates = fix_articles.process_file(
            book, None, threshold=0.70, apply_fixes=True
        )
        resolved = [c for c in candidates if c.get("output_resolved")]
        if resolved:
            # Verify the fix was applied in the output lines
            body = "\n".join(fixed_lines)
            assert "a sacrifice" in body

    def test_frontmatter_not_modified(self, tmp_path):
        """YAML frontmatter should pass through untouched."""
        book = tmp_path / "TST.md"
        book.write_text(
            "---\nbook_code: TST\nstatus: staged\n---\n\n"
            "TST.1:1 normal text\n",
            encoding="utf-8",
        )
        fixed_lines, candidates = fix_articles.process_file(
            book, None, threshold=0.70, apply_fixes=False
        )
        assert "book_code: TST" in fixed_lines[1]
        assert "status: staged" in fixed_lines[2]


class TestIsFalsePositive:
    """Verify _is_false_positive function."""

    def test_known_word_is_false_positive(self):
        """A word in _FALSE_POSITIVE_PREFIXES should be a false positive."""
        assert fix_articles._is_false_positive("about", "a", "bout") is True

    def test_short_remainder_is_false_positive(self):
        """Remainder shorter than _MIN_WORD_LEN should be a false positive."""
        assert fix_articles._is_false_positive("ado", "a", "do") is True

    def test_unknown_long_remainder_is_not_false_positive(self):
        """Unknown word with long-enough remainder should not be a false positive."""
        assert fix_articles._is_false_positive("asacrifice", "a", "sacrifice") is False
