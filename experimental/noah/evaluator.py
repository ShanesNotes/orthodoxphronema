"""
evaluator.py — Track A grounded_reflection_score evaluator.

Deterministic, embedding-free, no GPU. Takes journal text + source text -> scorecard.

Hard gates (all must pass):
- require_valid_anchor_syntax: all [[...]] match BOOK.CH:V format
- require_all_sections: 5 required sections present
- reject_external_sources: no URLs, no external citation patterns
- minimum_grounding_score: lexical_grounding >= threshold

Score components:
- anchor_coverage (0.30): unique valid anchors cited / total pericope verses
- lexical_grounding (0.35): fraction of journal sentences with >=1 4-gram overlap to source
- section_completeness (0.20): non-empty sections present / 5
- bounded_novelty (0.15): fraction of sentences NOT verbatim from source
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

# Required journal sections
REQUIRED_SECTIONS = [
    "Literal scene",
    "Patterns",
    "Tension or surprise",
    "Interior response",
    "Question / prayer",
]

# Patterns
RE_WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
RE_ANCHOR_SYNTAX = re.compile(r"^[A-Z0-9]+\.\d+:\d+$")
RE_URL = re.compile(r"https?://\S+")
RE_EXTERNAL_CITE = re.compile(
    r"\b(?:according to|as (?:noted|stated|written) (?:in|by)|per|cf\.|see also)\b.*?"
    r"(?:[A-Z][a-z]+ \d{4}|\([^)]*\d{4}[^)]*\))",
    re.IGNORECASE,
)
RE_SECTION_HDR = re.compile(r"^##\s+(.+)$", re.MULTILINE)

# Default weights and thresholds
DEFAULT_WEIGHTS = {
    "anchor_coverage": 0.30,
    "lexical_grounding": 0.35,
    "section_completeness": 0.20,
    "bounded_novelty": 0.15,
}
DEFAULT_GROUNDING_THRESHOLD = 0.70


@dataclass
class GateResult:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class Scorecard:
    gates: list[GateResult] = field(default_factory=list)
    scores: dict[str, float] = field(default_factory=dict)
    weighted_composite: float = 0.0
    all_gates_passed: bool = False

    def to_dict(self) -> dict:
        return {
            "gates": [{"name": g.name, "passed": g.passed, "detail": g.detail} for g in self.gates],
            "scores": self.scores,
            "weighted_composite": round(self.weighted_composite, 4),
            "all_gates_passed": self.all_gates_passed,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


# ── Utility functions ────────────────────────────────────────────────────────

def _sentences(text: str) -> list[str]:
    """Split text into sentences (simple heuristic)."""
    # Remove markdown headers and blank lines
    lines = [l.strip() for l in text.splitlines() if l.strip() and not l.strip().startswith("#")]
    # Join and split on sentence boundaries
    body = " ".join(lines)
    # Split on period/question/exclamation followed by space or end
    parts = re.split(r"(?<=[.?!])\s+", body)
    return [s.strip() for s in parts if len(s.strip()) > 10]


def _ngrams(text: str, n: int = 4) -> set[tuple[str, ...]]:
    """Extract word-level n-grams from text."""
    words = re.findall(r"\w+", text.lower())
    if len(words) < n:
        return set()
    return {tuple(words[i : i + n]) for i in range(len(words) - n + 1)}


def _extract_wikilinks(text: str) -> list[str]:
    """Extract all [[...]] wikilink targets."""
    return RE_WIKILINK.findall(text)


# ── Gate checks ──────────────────────────────────────────────────────────────

def gate_valid_anchor_syntax(journal_text: str) -> GateResult:
    """All [[...]] that look like scripture refs must match BOOK.CH:V format."""
    links = _extract_wikilinks(journal_text)
    # Filter to links that contain a dot and colon (likely anchor attempts)
    anchor_attempts = [l for l in links if "." in l and ":" in l and "/" not in l]
    invalid = [a for a in anchor_attempts if not RE_ANCHOR_SYNTAX.match(a)]
    if invalid:
        return GateResult("require_valid_anchor_syntax", False, f"invalid anchors: {invalid[:5]}")
    return GateResult("require_valid_anchor_syntax", True, f"{len(anchor_attempts)} valid anchors")


def gate_all_sections(journal_text: str) -> GateResult:
    """All 5 required sections must be present as ## headers."""
    headers = [m.group(1).strip() for m in RE_SECTION_HDR.finditer(journal_text)]
    missing = [s for s in REQUIRED_SECTIONS if s not in headers]
    if missing:
        return GateResult("require_all_sections", False, f"missing: {missing}")
    return GateResult("require_all_sections", True, f"{len(REQUIRED_SECTIONS)}/{len(REQUIRED_SECTIONS)} present")


def gate_no_external_sources(journal_text: str) -> GateResult:
    """No URLs or external citation patterns."""
    urls = RE_URL.findall(journal_text)
    if urls:
        return GateResult("reject_external_sources", False, f"URLs found: {urls[:3]}")
    cites = RE_EXTERNAL_CITE.findall(journal_text)
    if cites:
        return GateResult("reject_external_sources", False, f"external citations: {cites[:3]}")
    return GateResult("reject_external_sources", True)


def gate_minimum_grounding(journal_text: str, source_text: str, threshold: float) -> GateResult:
    """Lexical grounding must meet threshold."""
    score = score_lexical_grounding(journal_text, source_text)
    passed = score >= threshold
    return GateResult(
        "minimum_grounding_score",
        passed,
        f"grounding={score:.3f}, threshold={threshold}",
    )


# ── Score components ─────────────────────────────────────────────────────────

def score_anchor_coverage(journal_text: str, verse_count: int) -> float:
    """Unique valid anchors cited / total pericope verses. Capped at 1.0."""
    if verse_count <= 0:
        return 0.0
    links = _extract_wikilinks(journal_text)
    valid_anchors = {l for l in links if RE_ANCHOR_SYNTAX.match(l)}
    return min(len(valid_anchors) / verse_count, 1.0)


def score_lexical_grounding(journal_text: str, source_text: str) -> float:
    """Fraction of journal sentences with >=1 4-gram overlap to source."""
    source_ngrams = _ngrams(source_text)
    if not source_ngrams:
        return 0.0
    journal_sents = _sentences(journal_text)
    if not journal_sents:
        return 0.0
    grounded = 0
    for sent in journal_sents:
        sent_ngrams = _ngrams(sent)
        if sent_ngrams & source_ngrams:
            grounded += 1
    return grounded / len(journal_sents)


def score_section_completeness(journal_text: str) -> float:
    """Non-empty sections present / 5."""
    sections = re.split(r"^##\s+", journal_text, flags=re.MULTILINE)
    non_empty = 0
    for section in sections[1:]:  # skip content before first ##
        header_line = section.split("\n", 1)[0].strip()
        body = section.split("\n", 1)[1].strip() if "\n" in section else ""
        if header_line in REQUIRED_SECTIONS and len(body) > 20:
            non_empty += 1
    return min(non_empty / len(REQUIRED_SECTIONS), 1.0)


def score_bounded_novelty(journal_text: str, source_text: str) -> float:
    """Fraction of journal sentences NOT verbatim from source.

    A sentence is considered verbatim if >80% of its 4-grams appear in source.
    """
    source_ngrams = _ngrams(source_text)
    if not source_ngrams:
        return 1.0
    journal_sents = _sentences(journal_text)
    if not journal_sents:
        return 0.0
    novel = 0
    for sent in journal_sents:
        sent_ngrams = _ngrams(sent)
        if not sent_ngrams:
            novel += 1
            continue
        overlap = len(sent_ngrams & source_ngrams) / len(sent_ngrams)
        if overlap <= 0.80:
            novel += 1
    return novel / len(journal_sents)


# ── Main evaluator ───────────────────────────────────────────────────────────

def evaluate(
    journal_text: str,
    source_text: str,
    verse_count: int,
    weights: dict[str, float] | None = None,
    grounding_threshold: float = DEFAULT_GROUNDING_THRESHOLD,
) -> Scorecard:
    """Evaluate a journal entry against its source text. Returns a Scorecard."""
    if weights is None:
        weights = DEFAULT_WEIGHTS

    card = Scorecard()

    # Gates
    card.gates.append(gate_valid_anchor_syntax(journal_text))
    card.gates.append(gate_all_sections(journal_text))
    card.gates.append(gate_no_external_sources(journal_text))
    card.gates.append(gate_minimum_grounding(journal_text, source_text, grounding_threshold))

    card.all_gates_passed = all(g.passed for g in card.gates)

    # Scores
    card.scores["anchor_coverage"] = round(score_anchor_coverage(journal_text, verse_count), 4)
    card.scores["lexical_grounding"] = round(score_lexical_grounding(journal_text, source_text), 4)
    card.scores["section_completeness"] = round(score_section_completeness(journal_text), 4)
    card.scores["bounded_novelty"] = round(score_bounded_novelty(journal_text, source_text), 4)

    # Weighted composite
    card.weighted_composite = sum(
        weights.get(k, 0) * card.scores.get(k, 0) for k in weights
    )

    return card
