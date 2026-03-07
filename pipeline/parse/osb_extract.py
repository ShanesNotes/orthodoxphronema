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
RE_SPACED_CAPS = re.compile(r'^([A-Z] ){2,}[A-Z]$')

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
    """Tab-strip + collapse runs of whitespace."""
    return re.sub(r'\s+', ' ', text.replace('\t', ' ')).strip()


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


def normalize_spaced_title(text: str) -> str:
    """'T H E  H O L Y  T R I N I T Y' → 'The Holy Trinity'"""
    words = normalize(text).split()
    merged = "".join(words)
    return merged.title()


# ──────────────────────────────────────────────────────────────────────────────
# Docling element stream
# ──────────────────────────────────────────────────────────────────────────────

def iter_elements(doc) -> Generator[tuple[str, str], None, None]:
    """
    Yield (elem_type, text) for each element in the Docling document.
    elem_type is one of: 'SectionHeaderItem', 'TextItem', 'ListItem', other.
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
        if not text:
            continue
        text = normalize(text)
        if not text:
            continue
        yield etype, text


# ──────────────────────────────────────────────────────────────────────────────
# Verse splitting
# ──────────────────────────────────────────────────────────────────────────────

def extract_footnote_markers(text: str) -> tuple[str, list[str]]:
    """
    Strip inline footnote markers (†, ω, †ω) from text.
    Returns (clean_text, [marker, ...]).
    Markers are stripped before verse split boundaries only.
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
    Returns list of (anchor_str, chapter, verse, markers).

    The text may contain multiple verses delimited by inline verse numbers.
    Chapter-leading blocks: the first "verse" is verse 1 (no explicit number).

    Returns list of (verse_text, chapter, verse_num, markers_list).
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

    # First segment (before first verse-number marker) = start_verse
    first_seg = parts[0]
    clean, markers = extract_footnote_markers(first_seg)
    clean = fix_split_words(clean).strip()
    if clean:
        results.append((clean, current_chapter, start_verse, markers))

    # Remaining segments come in triples: (marker_str, verse_num_str, verse_text)
    i = 1
    while i + 2 < len(parts):
        _markers_str = parts[i]      # footnote markers before verse number (may be empty)
        verse_num_str = parts[i + 1] # digit string
        verse_text = parts[i + 2]    # text of this verse

        try:
            vnum = int(verse_num_str)
        except ValueError:
            i += 3
            continue

        clean, markers = extract_footnote_markers(verse_text)
        clean = fix_split_words(clean).strip()
        if clean:
            results.append((clean, current_chapter, vnum, markers))
        i += 3

    return results


# ──────────────────────────────────────────────────────────────────────────────
# State machine
# ──────────────────────────────────────────────────────────────────────────────

VERSE_MODE   = "VERSE_MODE"
ARTICLE_MODE = "ARTICLE_MODE"


class ExtractionState:
    def __init__(self, book_code: str, first_chapter: int = 1):
        self.book_code      = book_code
        self.mode           = VERSE_MODE
        self.current_chapter = first_chapter
        self.current_verse  = 0   # last verse number emitted
        self.last_verse_text_incomplete = False  # for column-split merging

        # Output buffers
        self.verses: list[dict] = []               # {anchor, chapter, verse, text}
        self.headings: list[dict] = []             # {after_anchor, heading}
        self.articles: list[dict] = []             # {title, after_anchor, body_paras}
        self.footnote_markers: list[dict] = []     # {anchor, marker}

        # Article accumulation
        self._article_title: str = ""
        self._article_after: str = ""              # anchor after which article appears
        self._article_body: list[str] = []

    def _anchor(self, chapter: int, verse: int) -> str:
        return f"{self.book_code}.{chapter}:{verse}"

    def _last_anchor(self) -> str:
        if self.verses:
            v = self.verses[-1]
            return self._anchor(v["chapter"], v["verse"])
        return f"{self.book_code}.{self.current_chapter}:0"

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

    def process_element(self, etype: str, text: str) -> None:
        # ── Navigation noise → always discard ──────────────────────────────
        if is_nav_noise(text):
            return

        # ── SectionHeaderItem ───────────────────────────────────────────────
        if etype in ("SectionHeaderItem",):
            if is_spaced_caps(text):
                # Start of a study article
                self._flush_article()
                self.mode = ARTICLE_MODE
                self._article_title = normalize_spaced_title(text)
                self._article_after = self._last_anchor()
                return

            # Title-case or ALL CAPS non-spaced header
            upper = text.upper()
            if text == upper:
                # ALL CAPS non-spaced sub-header (e.g. "THE HOLY TRINITY CREATED THE WORLD")
                if self.mode == ARTICLE_MODE:
                    self._article_body.append(f"\n#### {text.title()}\n")
                else:
                    # Treat as narrative heading in VERSE_MODE
                    self.headings.append({
                        "after_anchor": self._last_anchor(),
                        "heading": text.title(),
                    })
            else:
                # Title-case narrative heading
                if self.mode == VERSE_MODE:
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

        # In ARTICLE_MODE: check if this is verse text (verse resumes)
        if self.mode == ARTICLE_MODE:
            if RE_CHAPTER_LEAD.match(text) or (text[:1].isdigit() and len(text) > 2 and text[1] == ' '):
                # Verse text resuming — fall through to VERSE_MODE processing
                self._flush_article()
                self.mode = VERSE_MODE
            else:
                self._article_body.append(text)
                return

        # ── VERSE_MODE text processing ──────────────────────────────────────

        # Column-split fragment detection:
        # If text doesn't start with a digit AND previous verse was incomplete
        if self.last_verse_text_incomplete and not text[:1].isdigit():
            # Merge with last verse
            if self.verses:
                self.verses[-1]["text"] += " " + text
                # Check if now complete (ends with sentence-final punctuation)
                last = self.verses[-1]["text"]
                self.last_verse_text_incomplete = not re.search(r'[.!?\'"\u201d\u2019]\s*$', last)
            return

        # Chapter-leading block?
        m = RE_CHAPTER_LEAD.match(text)
        if m:
            chapter_num = int(m.group(1))
            # Sanity: only advance chapter if it's plausibly the next one
            if chapter_num == self.current_chapter + 1 or chapter_num == 1:
                self.current_chapter = chapter_num
            else:
                # Could be a verse number for the current chapter; treat as verse
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
            self.verses.append({
                "anchor": anchor,
                "chapter": ch,
                "verse": vnum,
                "text": vtext,
            })
            self.current_chapter = ch
            self.current_verse   = vnum
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
                 dry_run: bool = False) -> ExtractionState:
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

    state = ExtractionState(book_code, first_chapter=1)

    elem_count = 0
    for etype, text in iter_elements(doc):
        elem_count += 1
        state.process_element(etype, text)

    print(f"[parse] Elements processed : {elem_count}")
    print(f"[parse] Verses extracted   : {len(state.verses)}")
    print(f"[parse] Articles found     : {len(state.articles)}")
    print(f"[parse] Footnote markers   : {len(state.footnote_markers)}")

    return state


def write_outputs(state: ExtractionState, meta: dict, testament: str,
                  dry_run: bool = False) -> None:
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

    state = extract_book(args.book, start_page, end_page, dry_run=args.dry_run)
    write_outputs(state, meta, testament, dry_run=args.dry_run)

    print("\n[parse] Done.")


if __name__ == "__main__":
    main()
