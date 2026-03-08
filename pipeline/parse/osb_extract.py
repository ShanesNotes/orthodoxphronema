"""
docling_parse.py — OSB Scripture extraction (one book at a time)

Reads the OSB PDF for a single book's text page range, classifies every
Docling element through a two-state machine (VERSE_MODE / ARTICLE_MODE),
and emits:

  staging/validated/OT|NT/<BOOK>.md           — pure Scripture (one verse per line)
  staging/validated/OT|NT/<BOOK>_notes.md     — study articles (interleaved content)
  staging/validated/OT|NT/<BOOK>_footnote_markers.json  — inline footnote anchor index

Usage:
    python3 pipeline/parse/docling_parse.py --book GEN
    python3 pipeline/parse/docling_parse.py --book GEN --start 102 --end 188
    python3 pipeline/parse/docling_parse.py --book GEN --dry-run

The page range is read from schemas/anchor_registry.json unless overridden
with --start / --end.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Generator

# ──────────────────────────────────────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────────────────────────────────────

REPO_ROOT    = Path(__file__).parent.parent.parent
PDF_PATH     = REPO_ROOT / "src.texts" / "the_orthodox_study_bible.pdf"
REGISTRY     = REPO_ROOT / "schemas" / "anchor_registry.json"
STAGING_ROOT = REPO_ROOT / "staging" / "validated"

# ──────────────────────────────────────────────────────────────────────────────
# Regex constants
# ──────────────────────────────────────────────────────────────────────────────

# Spaced-caps study article header: "T H E  H O L Y  T R I N I T Y"
# Allow optional comma after a letter (e.g. "T H E P R I E S T H O O D, H E B R E W...")
RE_SPACED_CAPS = re.compile(r'^([A-Z][,]? ){2,}[A-Z]$')

# Navigation artefacts to discard
RE_NAV_STRING = re.compile(
    r'^[\d,\s]+(Back to|Home|Next|Introduction|Previous)',
    re.IGNORECASE
)
RE_COMMA_INTS = re.compile(r'^[\d,\s]+$')

# Verse-split boundary within a TextItem:
# optional footnote markers, then a digit sequence, then space+capital/quote
RE_VERSE_SPLIT = re.compile(r'([†ω]*)\s*(\d+)\s+(?=[A-Z\'"\u201c\u2018])')

# Chapter-leading TextItem: starts with a number (the chapter number) followed
# by space and then an uppercase letter — no preceding footnote marker.
RE_CHAPTER_LEAD = re.compile(r'^(\d+)\s+([A-Z\'"\u201c\u2018])')

# Inline footnote markers (to strip from verse body)
RE_FOOTNOTE_MARKERS = re.compile(r'[†ω]+')

# Split-word artifact from PDF column justification: "y ou" "wiv es"
# Only fix when a lowercase letter precedes space precedes 2+ lowercase letters
# that look like they should be joined (conservative).
RE_SPLIT_WORD = re.compile(r'(?<=[a-z]) (?=[a-z]{2,}(?:\s|[,;.!?]|$))')

# Lowercase verse-opener words that start OSB/LXX verse sentences.
# Kept narrow: conjunctions + temporal adverbs only. Pronouns/articles excluded
# (too many false-positive inline uses).
_LC_OPENERS = (
    r'and|then|for|now|so|but|thus|also|when|after|because|therefore|yet|before'
)
_LC_VERSE_PAT = re.compile(
    r'(?<!\w)(\d+)\s+(' + _LC_OPENERS + r')(?=\s)'
)

# Words that, when immediately preceding a digit, indicate the digit is an
# inline numeral (age, measurement, count) rather than a verse number.
_INLINE_NUM_CTX = frozenset({
    # units of time
    'year', 'years', 'day', 'days', 'month', 'months', 'night', 'nights',
    'week', 'weeks', 'hour', 'hours',
    # units of measure / weight
    'cubit', 'cubits', 'shekel', 'shekels', 'talent', 'talents',
    'hin', 'hins', 'ephah', 'mina', 'minas', 'bath', 'baths',
    'span', 'spans', 'handbreadth', 'handbreadths',
    # spelled-out round numbers that may precede inline digit sequences
    'hundred', 'thousand',
    # prepositions / articles
    'of', 'with', 'from', 'in', 'at', 'to', 'about', 'over', 'upon',
    'unto', 'into', 'by', 'a', 'an', 'the',
    # common verbs preceding counts or ages
    'was', 'were', 'is', 'are', 'am', 'had', 'has', 'have',
    'lived', 'live', 'begat', 'bore', 'born',
    'took', 'take', 'gave', 'give', 'brought', 'bring',
    'made', 'make', 'set', 'put', 'sent', 'send',
    'numbered', 'number', 'counted', 'count',
    # nouns commonly followed by a count
    'son', 'sons', 'daughter', 'daughters', 'man', 'men', 'woman', 'women',
    'person', 'persons', 'people', 'tribe', 'tribes',
    'lamb', 'lambs', 'goat', 'goats', 'ox', 'oxen', 'bull', 'bulls',
    'ram', 'rams', 'cow', 'cows', 'bird', 'birds', 'pigeon', 'pigeons',
    'animal', 'animals', 'beast', 'beasts', 'cattle',
    'stone', 'stones', 'board', 'boards', 'pillar', 'pillars',
    'curtain', 'curtains', 'hook', 'hooks', 'ring', 'rings',
    'city', 'cities', 'town', 'towns', 'village', 'villages',
    'old', 'young', 'age', 'or', 'than', 'more', 'less', 'some', 'each',
})

# ──────────────────────────────────────────────────────────────────────────────
# Registry helpers
# ──────────────────────────────────────────────────────────────────────────────

def load_registry() -> dict:
    with open(REGISTRY, encoding="utf-8") as f:
        return json.load(f)


def book_meta(registry: dict, book_code: str) -> dict:
    """Return book entry from registry books list."""
    for b in registry["books"]:
        if b["code"] == book_code:
            return b
    raise ValueError(f"Book code {book_code!r} not found in registry")


def page_ranges(registry: dict, book_code: str) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return ((text_start, text_end), (fn_start, fn_end)) for book."""
    pr = registry["page_ranges"][book_code]
    return tuple(pr["text"]), tuple(pr["footnotes"])


# ──────────────────────────────────────────────────────────────────────────────
# Text normalisation
# ──────────────────────────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    """Tab-strip + collapse runs of whitespace + deterministic artifact fixes."""
    t = re.sub(r'\s+', ' ', text.replace('\t', ' ')).strip()
    # R2: fused possessives — "'s" directly touching next lowercase word
    # e.g. "God'simage" -> "God's image" (zero false-positive risk)
    t = re.sub(r"('s)([a-z])", r"\1 \2", t)
    # R5: trailing space before punctuation / possessive 's
    t = re.sub(r" ([.,;:!?])", r"\1", t)
    t = re.sub(r" ('s)\b", r"\1", t)
    return t


def fix_split_words(text: str) -> str:
    """
    Conservatively re-join PDF column-justification word splits.
    "y ou" → "you",  "wiv es" → "wives"
    Only triggers on patterns where a lone letter or very short prefix is
    immediately followed by the remainder — heuristic, not exhaustive.
    """
    # Pattern: single lowercase char + space + 2+ lowercase chars that look
    # like a word continuation (followed by non-alpha or end)
    return re.sub(r'\b([a-z]) ([a-z]{2,})\b', r'\1\2', text)


def is_nav_noise(text: str) -> bool:
    """True if this TextItem is pure navigation / index noise."""
    t = text.strip()
    if RE_NAV_STRING.search(t):
        return True
    if RE_COMMA_INTS.match(t):
        return True
    return False


def is_spaced_caps(text: str) -> bool:
    """True if text is a spaced-letter ALL CAPS header like 'T H E  H O L Y  T R I N I T Y'."""
    t = normalize(text)
    return bool(RE_SPACED_CAPS.match(t))


def is_fragment_heading(text: str) -> bool:
    """True if a SectionHeaderItem looks like a speech-attribution fragment, not a heading."""
    t = text.rstrip()
    if t.endswith((':', ',')):
        return True
    if text[:1].isdigit():   # e.g. "26 He also said,"
        return True
    return False


def normalize_spaced_title(text: str) -> str:
    """'T H E  H O L Y  T R I N I T Y' → 'The Holy Trinity'"""
    raw_words = re.split(r'\s{2,}', text.strip())
    merged_words = ["".join(w.split()) for w in raw_words]
    return " ".join(merged_words).title()


# ──────────────────────────────────────────────────────────────────────────────
# Docling element stream
# ──────────────────────────────────────────────────────────────────────────────

def iter_elements(doc) -> Generator[tuple[str, str, str], None, None]:
    """
    Yield (elem_type, raw_text, normalized_text) for each element in the Docling document.
    raw_text is the unmodified Docling text (preserves double-space word boundaries needed
    by normalize_spaced_title for spaced-caps headers).
    normalized_text has tabs stripped and whitespace collapsed.
    Skips PictureItem and empty text.
    """
    for item in doc.iterate_items():
        elem = item[0] if isinstance(item, tuple) else item
        etype = type(elem).__name__
        if etype == "PictureItem":
            continue
        text = getattr(elem, "text", None)
        if callable(text):
            text = None
        if not text or not text.strip():
            continue
        normalized = normalize(text)
        if not normalized:
            continue
        yield etype, text, normalized


# ──────────────────────────────────────────────────────────────────────────────
# Verse splitting
# ──────────────────────────────────────────────────────────────────────────────

def extract_footnote_markers(text: str) -> tuple[str, list[str]]:
    """
    Strip inline footnote markers (†, ω, †ω) from verse body text.
    Returns (clean_text, [marker, ...]).

    Only call this on the text segment belonging to a single verse; do NOT
    call it on raw boundary-captured marker strings from RE_VERSE_SPLIT group 1
    (those belong to the PRECEDING verse and are handled separately).
    """
    markers_found = []
    # Find all marker occurrences and their positions
    for m in RE_FOOTNOTE_MARKERS.finditer(text):
        markers_found.append(m.group())
    clean = RE_FOOTNOTE_MARKERS.sub('', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean, markers_found


def split_verses_in_text(text: str, current_chapter: int, book_code: str,
                          start_verse: int = 1
                          ) -> list[tuple[str, int, int, list[str]]]:
    """
    Split a TextItem into individual verse tuples.
    Returns list of (verse_text, chapter, verse_num, markers_list).

    The text may contain multiple verses delimited by inline verse numbers.
    Chapter-leading blocks: the first "verse" is verse 1 (no explicit number).

    Marker ownership model (matches OSB physical layout):
      OSB markers appear AFTER verse-terminal punctuation, trailing the verse
      they annotate, immediately before the next verse number.  Shape:
          "... sentence end. † 18 And the Lord..."
      RE_VERSE_SPLIT captures these boundary markers in group 1 (markers_str).
      They are attached to the PRECEDING verse's markers list, not the
      following verse.  Only markers found within a verse's own body text
      (via extract_footnote_markers) belong to that verse.
    """
    results = []

    # Split on verse boundaries: (markers)(verse_num)(space)(capital...)
    # We capture the split tokens so we can reconstruct verse numbers.
    parts = RE_VERSE_SPLIT.split(text)
    # RE_VERSE_SPLIT has 2 capture groups: markers and verse_num.
    # split() with groups returns: [pre, markers1, vnum1, post1, markers2, vnum2, post2, ...]

    if len(parts) == 1:
        # No split found — entire text is one verse
        clean, markers = extract_footnote_markers(parts[0])
        clean = fix_split_words(clean).strip()
        if clean:
            results.append((clean, current_chapter, start_verse, markers))
        return results

    # First segment (before first verse-number boundary) = start_verse.
    # Markers within this segment belong to start_verse.
    first_seg = parts[0]
    clean, markers = extract_footnote_markers(first_seg)
    clean = fix_split_words(clean).strip()
    if clean:
        results.append((clean, current_chapter, start_verse, markers))

    # Remaining segments come in triples: (markers_str, verse_num_str, verse_text)
    # markers_str is the boundary-captured marker that TRAILS the previous verse.
    i = 1
    while i + 2 < len(parts):
        markers_str  = parts[i]      # boundary marker — belongs to PRECEDING verse
        verse_num_str = parts[i + 1] # digit string for the verse about to start
        verse_text   = parts[i + 2]  # body text of that verse

        try:
            vnum = int(verse_num_str)
        except ValueError:
            i += 3
            continue

        # Attach boundary-captured markers to the last emitted verse (they trail it).
        if markers_str and results:
            for m in RE_FOOTNOTE_MARKERS.findall(markers_str):
                results[-1][3].append(m)

        clean, markers = extract_footnote_markers(verse_text)
        clean = fix_split_words(clean).strip()
        if clean:
            results.append((clean, current_chapter, vnum, markers))
        i += 3

    results = _recover_lc_splits(results)
    return results


# ──────────────────────────────────────────────────────────────────────────────
# Lowercase-start verse boundary recovery (second pass)
# ──────────────────────────────────────────────────────────────────────────────

def _lc_boundary_valid(text_before: str, candidate_num: int, current_vnum: int) -> bool:
    """
    Decide whether a lowercase-start verse candidate is a real verse boundary.

    Signal 1 (strongest): text before the digit ends with sentence-terminal
    punctuation (.  !  ?  "  '  curly equivalents) → always accept.

    Signal 2 (rejection): the word immediately before the digit is in
    _INLINE_NUM_CTX (age, unit, verb, preposition context) → always reject.

    Signal 3 (sequential): candidate_num is exactly current_vnum + 1 → accept.
    This catches the most common case (consecutive verse numbers) even when
    neither Signal 1 nor Signal 2 fires.

    Default: reject (conservative).
    """
    if candidate_num <= current_vnum:
        return False

    stripped = text_before.rstrip()

    # Signal 1 — terminal punctuation
    if stripped and stripped[-1] in '.!?"\'\u201d\u2019':
        return True

    # Signal 2 — inline numeral context word
    words = re.findall(r"[a-zA-Z']+", stripped)
    if words:
        last = words[-1].lower().rstrip("'s").rstrip("'")
        if last in _INLINE_NUM_CTX:
            return False

    # Signal 3 — strictly sequential
    if candidate_num == current_vnum + 1:
        return True

    return False


def _lc_split(text: str, vnum: int) -> list[tuple[str, int]]:
    """
    Scan text for embedded lowercase-start verse boundaries and split them out.

    Returns ordered list of (segment_text, verse_num).  If no valid boundary
    is found, returns [(text, vnum)] unchanged.

    The digit from the matched boundary is consumed as the verse number;
    the verse text begins at the opener word (group 2), not at the digit.
    This means neither segment contains a spurious inline verse-number prefix.
    """
    result: list[tuple[str, int]] = []
    current_text = text
    current_vnum = vnum

    while True:
        best_match = None
        best_num = None
        for m in _LC_VERSE_PAT.finditer(current_text):
            candidate_num = int(m.group(1))
            text_before = current_text[:m.start()]
            if _lc_boundary_valid(text_before, candidate_num, current_vnum):
                best_match = m
                best_num = candidate_num
                break  # first valid candidate in left-to-right order

        if best_match is None:
            result.append((current_text.strip(), current_vnum))
            break

        before = current_text[:best_match.start()].strip()
        # Start from the opener word (group 2 start), not from the digit
        after = current_text[best_match.start(2):].strip()
        if before:
            result.append((before, current_vnum))
        current_text = after
        current_vnum = best_num

    return result


def _recover_lc_splits(
    results: list[tuple[str, int, int, list[str]]]
) -> list[tuple[str, int, int, list[str]]]:
    """
    Post-process results from split_verses_in_text to recover verse boundaries
    that begin with lowercase allowlist words (missed by RE_VERSE_SPLIT).

    Marker handling: by the time this runs, boundary-captured markers (those
    that physically trail a verse in the PDF, captured by RE_VERSE_SPLIT group 1)
    have already been attached to the correct preceding verse in split_verses_in_text.
    The `markers` list in each tuple now contains only markers found within that
    verse's own body text (from extract_footnote_markers).

    When _lc_split subdivides a verse body, body markers are kept on the FIRST
    sub-segment.  This is conservative: if the marker appeared physically before
    the lc boundary it is correct; if it appeared after it is a known limitation
    (the position is lost after text stripping).  Subsequent sub-segments receive
    an empty markers list.
    """
    expanded: list[tuple[str, int, int, list[str]]] = []
    for (vtext, ch, vnum, markers) in results:
        sub = _lc_split(vtext, vnum)
        if len(sub) == 1:
            expanded.append((vtext, ch, vnum, markers))
        else:
            expanded.append((sub[0][0], ch, sub[0][1], markers))
            for seg_text, seg_vnum in sub[1:]:
                expanded.append((seg_text, ch, seg_vnum, []))
    return expanded


# ──────────────────────────────────────────────────────────────────────────────
# State machine
# ──────────────────────────────────────────────────────────────────────────────

VERSE_MODE   = "VERSE_MODE"
ARTICLE_MODE = "ARTICLE_MODE"


class ExtractionState:
    def __init__(self, book_code: str, first_chapter: int = 1,
                 chapter_verse_counts: dict | None = None):
        self.book_code      = book_code
        self.mode           = VERSE_MODE
        # Start at chapter 0 so "1 In the beginning..." triggers chapter_num==0+1==1
        self.current_chapter = 0
        self.current_verse  = 0   # last verse number emitted
        self.verse_started  = False  # True after first real verse is emitted
        self.last_verse_text_incomplete = False  # for column-split merging
        # Map of chapter_number → expected verse count (from registry, LXX counts).
        # Used to guard against false chapter advances (Bug 1).
        self.chapter_verse_counts: dict[int, int] = chapter_verse_counts or {}

        # Output buffers
        self.verses: list[dict] = []               # {anchor, chapter, verse, text}
        self.headings: list[dict] = []             # {after_anchor, heading}
        self.articles: list[dict] = []             # {title, after_anchor, body_paras}
        self.footnote_markers: list[dict] = []     # {anchor, marker}

        # Article accumulation
        self._article_title: str = ""
        self._article_after: str = ""              # anchor after which article appears
        self._article_body: list[str] = []
        # Sequential sub-point tracker: OSB study articles use numbered paragraphs
        # starting at 1 (e.g. "1 This Fall...", "2 We who...", "3 Mankind's...").
        # We track the last sub-point number seen so we can distinguish them from
        # verse resumption or chapter-advance text that happens to share a digit.
        self._article_subpoint_seq: int = 0

    def _anchor(self, chapter: int, verse: int) -> str:
        return f"{self.book_code}.{chapter}:{verse}"

    def _last_anchor(self) -> str:
        if self.verses:
            v = self.verses[-1]
            return self._anchor(v["chapter"], v["verse"])
        return f"{self.book_code}.{self.current_chapter}:0"

    def _chapter_max_verse(self, ch: int) -> int:
        """Return expected verse count for chapter ch (0 if unknown)."""
        return self.chapter_verse_counts.get(ch, 0)

    def _flush_article(self) -> None:
        if self._article_title:
            self.articles.append({
                "title": self._article_title,
                "after_anchor": self._article_after,
                "body": self._article_body,
            })
        self._article_title = ""
        self._article_after = ""
        self._article_body  = []
        self._article_subpoint_seq = 0

    def process_element(self, etype: str, raw: str, text: str) -> None:
        """
        Process one Docling element.
        raw  = unmodified Docling text (preserves double-space word boundaries).
        text = normalize(raw) — used for all pattern matching and verse logic.
        """
        # ── Navigation noise → always discard ──────────────────────────────
        if is_nav_noise(text):
            return

        # ── SectionHeaderItem ───────────────────────────────────────────────
        if etype in ("SectionHeaderItem",):
            if is_spaced_caps(text):
                # Start of a study article.
                # Use raw text for normalize_spaced_title so double-space word
                # boundaries (e.g. "T H E  H O L Y  T R I N I T Y") are preserved.
                self._flush_article()
                self.mode = ARTICLE_MODE
                self._article_title = normalize_spaced_title(raw)
                self._article_after = self._last_anchor()
                return

            # Some chapter openings are formatted as SectionHeaderItems rather than
            # TextItems in the PDF (e.g. EXO.15: "15 Now Moses and the children of
            # Israel sang this song...").  is_fragment_heading would suppress them
            # because they start with a digit.  Intercept them first: if the leading
            # number equals current_chapter+1 and the advance threshold is met, treat
            # the element as a chapter-advance block exactly like a TextItem lead.
            if self.verse_started and text[:1].isdigit():
                m_ch = RE_CHAPTER_LEAD.match(text)
                if m_ch:
                    chapter_num = int(m_ch.group(1))
                    if chapter_num == self.current_chapter + 1:
                        # No threshold for SectionHeaderItem chapter leads:
                        # these are reliable structural markers in the PDF
                        # (unlike inline verse numbers in TextItems which need
                        # the 80% guard to prevent false advances).
                        self._flush_article()
                        self.mode = VERSE_MODE
                        self.current_chapter = chapter_num
                        self.current_verse = 0
                        body = text[m_ch.end():].strip()
                        if body:
                            verse_parts = split_verses_in_text(
                                body, self.current_chapter, self.book_code,
                                start_verse=1
                            )
                            self._emit_parts(verse_parts)
                        return

            # Title-case or ALL CAPS non-spaced header (text is already normalized).
            upper = text.upper()
            if text == upper:
                # ALL CAPS non-spaced sub-header (e.g. "THE HOLY TRINITY CREATED THE WORLD")
                if self.mode == ARTICLE_MODE:
                    self._article_body.append(f"\n#### {text.title()}\n")
                else:
                    # Treat as narrative heading in VERSE_MODE
                    if not is_fragment_heading(text):
                        self.headings.append({
                            "after_anchor": self._last_anchor(),
                            "heading": text.title(),
                        })
            else:
                # Title-case narrative heading
                if self.mode == VERSE_MODE:
                    if not is_fragment_heading(text):
                        self.headings.append({
                            "after_anchor": self._last_anchor(),
                            "heading": text,
                        })
                else:
                    # Sub-heading inside article
                    self._article_body.append(f"\n#### {text}\n")
            return

        # ── TextItem / ListItem ─────────────────────────────────────────────
        if etype not in ("TextItem", "ListItem"):
            return

        # In ARTICLE_MODE: distinguish article sub-points from verse resumption.
        #
        # OSB study articles contain numbered paragraphs that begin with a digit
        # and uppercase letter — the same pattern as verse/chapter leads.  We use
        # sequential sub-point tracking to tell them apart:
        #
        #   Rule 1 — Sequential continuation: if the leading digit is exactly
        #   _article_subpoint_seq + 1, this TextItem continues the numbered list
        #   inside the article.  Keep it there.
        #
        #   Rule 2 — Verse resumption: if the digit is NOT the expected next
        #   sub-point AND it is > current_verse, the article is over and verse
        #   text is resuming.
        #
        #   Rule 3 — Chapter advance (cross-chapter article): if the digit is
        #   NOT sequential AND equals current_chapter + 1 (the next chapter
        #   number), treat as chapter-lead resumption.  This handles articles
        #   that span a chapter boundary where the next chapter's verse 1 has a
        #   digit smaller than current_verse.
        #
        # The sub-point counter (_article_subpoint_seq) is NOT reset on non-digit
        # body text, because articles can have prose paragraphs interspersed
        # between numbered points.  It IS reset when a new article begins
        # (_flush_article) or when a numbered item breaks the sequence.
        if self.mode == ARTICLE_MODE:
            m_art = RE_CHAPTER_LEAD.match(text)
            if m_art:
                num = int(m_art.group(1))

                # Rule 1 — Sequential sub-point continuation (highest priority).
                # Fires only when we are already inside a numbered list (seq ≥ 1),
                # the digit is the very next in sequence, AND it is ≤ current_verse.
                # The ≤ current_verse guard prevents Rule 1 from absorbing verse
                # resumptions that happen to follow the current sub-point count.
                if (self._article_subpoint_seq >= 1
                        and num == self._article_subpoint_seq + 1
                        and num <= self.current_verse):
                    self._article_subpoint_seq = num
                    self._article_body.append(text)
                    return

                # Rule 2 — Verse or chapter resumption → EXIT.
                is_verse_resume = (num > self.current_verse)
                is_chapter_lead = (num == self.current_chapter + 1)
                if is_verse_resume or is_chapter_lead:
                    self._flush_article()
                    self.mode = VERSE_MODE
                    # fall through to verse processing

                # Rule 3 — First numbered sub-point of this article.
                # Only fires when no numbered list has started yet (seq == 0),
                # the digit is 1 (articles always number from 1), and we have
                # emitted at least one verse (current_verse ≥ 1) — ruling out
                # the case where "1 text" is actually the first verse of the book.
                elif self._article_subpoint_seq == 0 and num == 1 and self.current_verse >= 1:
                    self._article_subpoint_seq = 1
                    self._article_body.append(text)
                    return

                else:
                    # Non-sequential number — article content (nav ref, heading, etc.)
                    self._article_subpoint_seq = 0
                    self._article_body.append(text)
                    return
            else:
                self._article_body.append(text)
                return

        # ── VERSE_MODE text processing ──────────────────────────────────────

        # Pre-verse preamble guard: discard any non-verse TextItems that appear
        # before the first verse is emitted (page spillover from prior sections).
        if not self.verse_started and not text[:1].isdigit():
            return

        # Column-split fragment detection:
        # If text doesn't start with a digit AND previous verse was incomplete
        if self.last_verse_text_incomplete and not text[:1].isdigit():
            if self.verses:
                merged = self.verses[-1]["text"] + " " + text
                # Check whether the merged text reveals additional verse boundaries.
                # Example: Element N ends mid-sentence ("and"), Element N+1 starts with
                # prose but contains "† 9 So..." through "15 I will put enmity..." —
                # all those verses would be lost without re-splitting.
                if RE_VERSE_SPLIT.search(merged):
                    popped = self.verses.pop()
                    # Also remove any footnote markers already recorded for that anchor
                    self.footnote_markers = [
                        fm for fm in self.footnote_markers
                        if fm["anchor"] != popped["anchor"]
                    ]
                    verse_parts = split_verses_in_text(
                        merged, popped["chapter"], self.book_code,
                        start_verse=popped["verse"]
                    )
                    self._emit_parts(verse_parts)
                else:
                    self.verses[-1]["text"] = merged
                    self.last_verse_text_incomplete = not re.search(
                        r'[.!?\'"\u201d\u2019]\s*$', merged
                    )
            return

        # Chapter-leading block?
        m = RE_CHAPTER_LEAD.match(text)
        if m:
            chapter_num = int(m.group(1))
            # Sanity: only advance chapter if it's the expected next one AND
            # we are close enough to the end of the current chapter (verse-count guard).
            # Without this guard, e.g. GEN.11:12 falsely triggers a ch.12 advance
            # because chapter_num == current_chapter + 1 == 12.
            # max_v == 0 means registry has no data — allow advance unconditionally.
            max_v = self._chapter_max_verse(self.current_chapter)
            # Allow chapter advance only when we are >= 80% through the current
            # chapter's expected verses.  A bare chapter_num == current_chapter + 1
            # check is fooled when an inline verse number equals the next chapter
            # number (e.g. verse 28 in ch27 triggers false ch28 advance; verse 12
            # in ch11 triggers false ch12 advance).  80% comfortably excludes all
            # known false-advance positions while tolerating up to ~20% missed verses.
            if chapter_num == self.current_chapter + 1 and (
                    max_v == 0
                    or self.current_verse >= max_v * 4 // 5):
                self.current_chapter = chapter_num
                self.current_verse = 0  # reset so next element starts at verse 1
            else:
                # Not a real chapter advance — treat leading digit as verse number
                # for the current chapter.
                self._emit_verse_block(text, self.current_chapter, self.current_verse + 1)
                return

            # Text after chapter number is verse 1
            body = text[m.end():].strip()
            if body:
                verse_parts = split_verses_in_text(
                    body, self.current_chapter, self.book_code, start_verse=1
                )
                self._emit_parts(verse_parts)
        else:
            # Mid-chapter block: split on inline verse numbers
            # Determine start_verse: next after current
            verse_parts = split_verses_in_text(
                text, self.current_chapter, self.book_code,
                start_verse=self.current_verse + 1
            )
            self._emit_parts(verse_parts)

    def _emit_verse_block(self, text: str, chapter: int, start_verse: int) -> None:
        parts = split_verses_in_text(text, chapter, self.book_code, start_verse)
        self._emit_parts(parts)

    def _emit_parts(self, parts: list[tuple]) -> None:
        for (vtext, ch, vnum, markers) in parts:
            anchor = self._anchor(ch, vnum)
            # Deduplicate consecutive same-anchor: column-split fragments in the
            # PDF sometimes restate the verse number at the start of the second
            # column (e.g. "28 Therefore..." follows an already-emitted GEN.27:28).
            # Merging them avoids a V1 duplicate while preserving all text.
            if self.verses and self.verses[-1]["anchor"] == anchor:
                self.verses[-1]["text"] += " " + vtext
            else:
                self.verses.append({
                    "anchor": anchor,
                    "chapter": ch,
                    "verse": vnum,
                    "text": vtext,
                })
            self.current_chapter = ch
            self.current_verse   = vnum
            self.verse_started   = True
            for marker in markers:
                self.footnote_markers.append({"anchor": anchor, "marker": marker})

        # Track if last verse might be incomplete (column split)
        if parts:
            last_text = parts[-1][0]
            self.last_verse_text_incomplete = not re.search(
                r'[.!?\'"\u201d\u2019]\s*$', last_text
            )
        else:
            self.last_verse_text_incomplete = False


# ──────────────────────────────────────────────────────────────────────────────
# Output generation
# ──────────────────────────────────────────────────────────────────────────────

def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_canon_md(state: ExtractionState, meta: dict, parse_date: str) -> str:
    book_code = state.book_code
    testament = meta["testament"]
    position  = meta["position"]
    name      = meta["name"]

    # Build verse body (for checksum)
    verse_lines = []
    heading_map: dict[str, str] = {}   # after_anchor → heading text
    for h in state.headings:
        heading_map[h["after_anchor"]] = h["heading"]

    chapters: dict[int, list[dict]] = {}
    for v in state.verses:
        chapters.setdefault(v["chapter"], []).append(v)

    body_parts: list[str] = []
    for ch_num in sorted(chapters.keys()):
        body_parts.append(f"## Chapter {ch_num}\n")
        ch_verses = chapters[ch_num]

        # Insert headings that appear after the last verse of previous chapter
        # (or before any verse in this chapter)
        prev_anchor = f"{book_code}.{ch_num - 1}:0" if ch_num > 1 else f"{book_code}.0:0"

        for v in ch_verses:
            anchor = v["anchor"]
            # Heading after the PREVIOUS verse (which may be prev chapter's last)
            # We look up heading_map with the verse BEFORE this one
            if anchor in heading_map:
                body_parts.append(f"\n### {heading_map[anchor]}\n")

            line = f"{anchor} {v['text']}"
            body_parts.append(line)
            verse_lines.append(line)

    body_text = "\n".join(body_parts)
    checksum  = sha256_hex(body_text)

    frontmatter = f"""---
book_code: {book_code}
book_name: "{name}"
testament: {testament}
canon_position: {position}
source: "Orthodox Study Bible (OSB), Thomas Nelson 2008"
parse_date: "{parse_date}"
promote_date: null
checksum: "{checksum}"
status: staged
deuterocanonical: {str(meta.get("deuterocanonical", False)).lower()}
has_additions: false
---"""

    return frontmatter + "\n\n" + body_text + "\n"


def build_notes_md(state: ExtractionState, meta: dict, parse_date: str) -> str:
    book_code = state.book_code
    name      = meta["name"]

    frontmatter = f"""---
book_code: {book_code}
book_name: "{name}"
content_type: study_articles
source: "Orthodox Study Bible (OSB), Thomas Nelson 2008"
parse_date: "{parse_date}"
promote_date: null
status: staged
canon_anchors_referenced: []
---"""

    if not state.articles:
        return frontmatter + "\n\n*(No study articles extracted from this page range.)*\n"

    parts = [frontmatter, "\n## Study Articles\n"]
    for art in state.articles:
        parts.append(f"\n### {art['title']}")
        parts.append(f"*(after {art['after_anchor']})*\n")
        for para in art["body"]:
            parts.append(para)
        parts.append("")

    return "\n".join(parts) + "\n"


# ──────────────────────────────────────────────────────────────────────────────
# Main extraction routine
# ──────────────────────────────────────────────────────────────────────────────

def extract_book(book_code: str, start_page: int, end_page: int,
                 dry_run: bool = False,
                 chapter_verse_counts: dict | None = None) -> ExtractionState:
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions

    print(f"[parse] Book    : {book_code}")
    print(f"[parse] Pages   : {start_page}–{end_page}")
    print(f"[parse] Source  : {PDF_PATH}")

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr             = False
    pipeline_options.do_table_structure = True

    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )

    print("[parse] Converting (this may take several minutes) ...")
    result = converter.convert(str(PDF_PATH), page_range=(start_page, end_page))
    doc    = result.document
    print(f"[parse] Conversion complete — processing elements ...")

    state = ExtractionState(book_code, first_chapter=1,
                            chapter_verse_counts=chapter_verse_counts)

    elem_count = 0
    for etype, raw, text in iter_elements(doc):
        elem_count += 1
        state.process_element(etype, raw, text)

    print(f"[parse] Elements processed : {elem_count}")
    print(f"[parse] Verses extracted   : {len(state.verses)}")
    print(f"[parse] Articles found     : {len(state.articles)}")
    print(f"[parse] Footnote markers   : {len(state.footnote_markers)}")

    return state


def write_outputs(state: ExtractionState, meta: dict, testament: str,
                  dry_run: bool = False) -> None:
    # Deduplicate footnote markers: same (anchor, marker) pair may be recorded
    # twice when the consecutive same-anchor merge fires but both fragments carry
    # the same marker symbol.
    seen_fm: set[tuple[str, str]] = set()
    deduped: list[dict] = []
    for fm in state.footnote_markers:
        key = (fm["anchor"], fm["marker"])
        if key not in seen_fm:
            seen_fm.add(key)
            deduped.append(fm)
    state.footnote_markers = deduped

    book_code  = state.book_code
    parse_date = str(date.today())
    out_dir    = STAGING_ROOT / testament

    canon_md  = build_canon_md(state, meta, parse_date)
    notes_md  = build_notes_md(state, meta, parse_date)
    markers_j = json.dumps(
        state.footnote_markers, indent=2, ensure_ascii=False
    )

    canon_path   = out_dir / f"{book_code}.md"
    notes_path   = out_dir / f"{book_code}_notes.md"
    markers_path = out_dir / f"{book_code}_footnote_markers.json"

    if dry_run:
        print(f"\n[dry-run] Would write: {canon_path}")
        print(f"[dry-run] Would write: {notes_path}")
        print(f"[dry-run] Would write: {markers_path}")
        print("\n── Canon preview (first 60 lines) ──")
        for line in canon_md.splitlines()[:60]:
            print(line)
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    canon_path.write_text(canon_md, encoding="utf-8")
    notes_path.write_text(notes_md, encoding="utf-8")
    markers_path.write_text(markers_j, encoding="utf-8")

    print(f"\n[parse] Written: {canon_path}")
    print(f"[parse] Written: {notes_path}")
    print(f"[parse] Written: {markers_path}")


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract a single OSB book's Scripture text to Markdown."
    )
    parser.add_argument(
        "--book", required=True,
        help="Book code, e.g. GEN, EXO, MAT"
    )
    parser.add_argument(
        "--start", type=int, default=None,
        help="Override page range start (else reads from anchor_registry.json)"
    )
    parser.add_argument(
        "--end", type=int, default=None,
        help="Override page range end"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Parse and print preview without writing files"
    )
    args = parser.parse_args()

    registry = load_registry()

    try:
        meta = book_meta(registry, args.book)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    text_range, _fn_range = page_ranges(registry, args.book)
    start_page = args.start if args.start is not None else text_range[0]
    end_page   = args.end   if args.end   is not None else text_range[1]

    testament = meta["testament"]

    # Build chapter_verse_counts dict (1-indexed) from registry list (0-indexed).
    cvc_list = meta.get("chapter_verse_counts", [])
    chapter_verse_counts = {i + 1: v for i, v in enumerate(cvc_list)} if cvc_list else None

    state = extract_book(args.book, start_page, end_page, dry_run=args.dry_run,
                         chapter_verse_counts=chapter_verse_counts)
    write_outputs(state, meta, testament, dry_run=args.dry_run)

    print("\n[parse] Done.")


if __name__ == "__main__":
    main()
