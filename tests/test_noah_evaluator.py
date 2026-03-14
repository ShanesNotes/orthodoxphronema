"""Tests for experimental.noah.evaluator — Track A grounded_reflection_score."""
from __future__ import annotations

import sys
from pathlib import Path

# Allow import from experimental/noah/
sys.path.insert(0, str(Path(__file__).parent.parent / "experimental" / "noah"))

from evaluator import (
    evaluate,
    gate_all_sections,
    gate_minimum_grounding,
    gate_no_external_sources,
    gate_valid_anchor_syntax,
    score_anchor_coverage,
    score_bounded_novelty,
    score_lexical_grounding,
    score_section_completeness,
)

# ── Fixtures ─────────────────────────────────────────────────────────────────

SOURCE_TEXT = """\
GEN.1:1 In the beginning God made heaven and earth.
GEN.1:2 The earth was invisible and unfinished; and darkness was over the deep.
GEN.1:3 Then God said, 'Let there be light'; and there was light.
GEN.1:4 God saw the light; it was good; and God divided the light from the darkness.
GEN.1:5 God called the light Day; the darkness He called Night; and there was evening and morning, one day.
"""

GOOD_JOURNAL = """\
---
session_id: "GEN.P001"
---

# Journal: Genesis — Opening

## Literal scene
In the beginning God made heaven and earth. The earth was invisible and unfinished.
God speaks light into being and separates it from darkness. This is the first day.

## Patterns
The repeated phrase "God said" followed by "it was so" creates a rhythm of command and
fulfillment. Light and darkness are divided; the naming of Day and Night establishes
the pattern of divine ordering that persists through the rest of creation.

## Tension or surprise
The earth was invisible and unfinished — this is not the ex nihilo moment but an already
existing substrate that God shapes. The Spirit hovering suggests agency before speech.

## Interior response
The phrase "darkness was over the deep" draws me in. There is something alive about
the deep even before God speaks. I notice the careful naming — Day, Night — as acts
of authority. See [[GEN.1:1]] and [[GEN.1:3]] and [[GEN.1:5]].

## Question / prayer
Why does God call the light "good" before the darkness is named? Is darkness not good?
Lord, let me sit with the darkness over the deep and not rush to resolve it.
"""

BAD_JOURNAL_EXTERNAL = """\
## Literal scene
According to Brueggemann 2001, this passage reflects priestly theology.
See also https://example.com/genesis-commentary for more context.

## Patterns
The text shows patterns.

## Tension or surprise
Nothing surprising.

## Interior response
I felt something.

## Question / prayer
A question.
"""


# ── Gate tests ───────────────────────────────────────────────────────────────

def test_gate_valid_anchor_syntax_passes():
    result = gate_valid_anchor_syntax(GOOD_JOURNAL)
    assert result.passed


def test_gate_valid_anchor_syntax_fails_on_bad_format():
    text = "See [[GEN.1:1]] and [[badformat]] and [[GEN.xyz:1]]"
    result = gate_valid_anchor_syntax(text)
    # badformat has no dot+colon so won't be detected as anchor attempt
    # GEN.xyz:1 has dot and colon but is malformed
    assert not result.passed


def test_gate_all_sections_passes():
    result = gate_all_sections(GOOD_JOURNAL)
    assert result.passed


def test_gate_all_sections_fails_on_missing():
    text = "## Literal scene\nSome content here.\n\n## Patterns\nMore content.\n"
    result = gate_all_sections(text)
    assert not result.passed
    assert "missing" in result.detail


def test_gate_no_external_sources_passes():
    result = gate_no_external_sources(GOOD_JOURNAL)
    assert result.passed


def test_gate_no_external_sources_fails_on_url():
    result = gate_no_external_sources(BAD_JOURNAL_EXTERNAL)
    assert not result.passed


def test_gate_minimum_grounding_passes():
    result = gate_minimum_grounding(GOOD_JOURNAL, SOURCE_TEXT, 0.20)
    assert result.passed


# ── Score tests ──────────────────────────────────────────────────────────────

def test_score_anchor_coverage():
    score = score_anchor_coverage(GOOD_JOURNAL, verse_count=5)
    # GOOD_JOURNAL cites GEN.1:1, GEN.1:3, GEN.1:5 = 3 unique out of 5
    assert score == 0.6


def test_score_anchor_coverage_zero_verses():
    score = score_anchor_coverage(GOOD_JOURNAL, verse_count=0)
    assert score == 0.0


def test_score_lexical_grounding_nonzero():
    score = score_lexical_grounding(GOOD_JOURNAL, SOURCE_TEXT)
    assert score > 0.0


def test_score_section_completeness_good():
    score = score_section_completeness(GOOD_JOURNAL)
    assert score == 1.0


def test_score_section_completeness_empty():
    text = "## Literal scene\n\n## Patterns\n\n## Tension or surprise\n\n## Interior response\n\n## Question / prayer\n"
    score = score_section_completeness(text)
    assert score == 0.0


def test_score_bounded_novelty():
    score = score_bounded_novelty(GOOD_JOURNAL, SOURCE_TEXT)
    # Most journal sentences should not be verbatim from source
    assert score > 0.5


def test_score_bounded_novelty_all_verbatim():
    # If journal IS the source, novelty should be low
    score = score_bounded_novelty(SOURCE_TEXT, SOURCE_TEXT)
    assert score < 0.5


# ── Composite evaluation ────────────────────────────────────────────────────

def test_evaluate_good_journal():
    card = evaluate(GOOD_JOURNAL, SOURCE_TEXT, verse_count=5, grounding_threshold=0.20)
    assert card.all_gates_passed
    assert card.weighted_composite > 0.0
    assert "anchor_coverage" in card.scores
    assert "lexical_grounding" in card.scores


def test_evaluate_bad_journal_fails_gates():
    card = evaluate(BAD_JOURNAL_EXTERNAL, SOURCE_TEXT, verse_count=5)
    assert not card.all_gates_passed


def test_evaluate_to_json():
    card = evaluate(GOOD_JOURNAL, SOURCE_TEXT, verse_count=5, grounding_threshold=0.20)
    j = card.to_json()
    import json
    parsed = json.loads(j)
    assert "gates" in parsed
    assert "scores" in parsed
    assert "weighted_composite" in parsed
