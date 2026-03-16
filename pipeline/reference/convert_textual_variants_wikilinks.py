#!/usr/bin/env python3
"""
convert_textual_variants_wikilinks.py

Convert bare scripture references in reference/textual-variants.md to wikilink format.

The file is structured in two major sections, both processed by book-tracking
state machines that advance on chapter resets:

  SECTION 1 (lines 17–1907): Main NT textual variants (NU-Text, M-Text,
    alternative translations) for MAT through REV.  1TH and 2TH are absent
    in this section (no variants present).

  SECTION 2 (lines 1908–end): Post-variant sections:
    - 1TH / 2TH variants (lines 1908–1939)
    - A few leftover 1CO / REV cross-reference notes
    - Per-book OT citation sections for MAT, MRK, LUK, JOH, ACT, ROM,
      1CO, 2CO, GAL, EPH, PHP, COL, HEB, JAS, 1PE, 2PE, and REV
    - Long endnote commentary blocks (not reliably wikifiable)

Wikilink format:
  [[BOOK.CH:V]]subletter rest-of-line
  e.g.  1:7a NU-Text…  →  [[MAT.1:7]]a NU-Text…

Range refs:
  7:53—8:11  →  [[JOH.7:53]]—8:11

Anchors are validated against the registry CVC.  Invalid anchors are left
as bare refs and logged.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MD_PATH = REPO / "reference" / "textual-variants.md"

sys.path.insert(0, str(REPO))
from pipeline.common.registry import load_registry


# ---------------------------------------------------------------------------
# Registry helpers
# ---------------------------------------------------------------------------

def build_cvc_map() -> dict[str, dict[int, int]]:
    reg = load_registry()
    cvc: dict[str, dict[int, int]] = {}
    for book in reg.get("books", []):
        code = book["code"]
        cvc_list = book.get("chapter_verse_counts")
        if cvc_list:
            cvc[code] = {i + 1: count for i, count in enumerate(cvc_list)}
    return cvc


def anchor_valid(book: str, ch: int, v: int, cvc_map: dict) -> bool:
    if book not in cvc_map:
        return False
    ch_map = cvc_map[book]
    return ch in ch_map and 1 <= v <= ch_map[ch]


def max_ch(book: str, cvc_map: dict) -> int:
    return len(cvc_map.get(book, {}))


# ---------------------------------------------------------------------------
# Book sequences
# ---------------------------------------------------------------------------

# Section 1: main NT variant notes.
# 1TH and 2TH are skipped because the OSB notes section has no variants for them.
# The document goes directly from COL to 1TI.
S1_BOOKS = [
    "MAT", "MRK", "LUK", "JOH", "ACT",
    "ROM", "1CO", "2CO", "GAL", "EPH", "PHP", "COL",
    "1TI", "2TI", "TIT", "PHM",
    "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV",
]

# Section 2: 1TH/2TH variants + per-book OT citation cross-reference sections.
# After 2TH, the document has stray 1CO and REV cross-ref notes, then restarts
# the full book sequence from MAT for the per-book citation sections.
# The long endnote commentary blocks at the end are handled by the "skip invalid"
# path in the state machine.
S2_BOOKS = [
    "1TH", "2TH", "1CO", "REV",           # stray cross-ref notes
    "MAT", "MRK", "LUK", "JOH", "ACT",    # per-book OT citation sections
    "ROM", "1CO", "2CO", "GAL", "EPH",
    "PHP", "COL", "HEB", "JAS",
    "1PE", "2PE", "REV",                   # last OT citation section
]

# Line on which Section 2 begins (1-indexed).
SECTION2_START = 1908


# ---------------------------------------------------------------------------
# Regex
# ---------------------------------------------------------------------------

BARE_REF_RE = re.compile(
    r"^"
    r"(\d+)"                              # chapter
    r":"
    r"(\d+)"                              # verse
    r"([a-z]?)"                           # subletter
    r"([—\-]\d+(?::\d+)?[a-z]?)?"        # range suffix
    r"(\s|$)"                             # trailing space or EOL
)


def parse_bare_ref(line: str):
    m = BARE_REF_RE.match(line)
    if m is None:
        return None
    return int(m.group(1)), int(m.group(2)), m.group(3) or "", m.group(4) or "", m


# ---------------------------------------------------------------------------
# Book-boundary state machine (shared logic)
# ---------------------------------------------------------------------------

class BookTracker:
    """Greedy chapter-reset state machine for tracking book boundaries."""

    def __init__(self, books: list[str], cvc_map: dict):
        self.books = books
        self.cvc_map = cvc_map
        self.idx = 0
        self.current_chapter = 0
        self.advances: list[tuple[int, str, str]] = []  # (lineno, from, to)

    @property
    def book(self) -> str:
        return self.books[min(self.idx, len(self.books) - 1)]

    def _fits(self, b: str, ch: int, v: int) -> bool:
        return anchor_valid(b, ch, v, self.cvc_map)

    def _advance(self, lineno: int) -> None:
        old = self.book
        self.idx = min(self.idx + 1, len(self.books) - 1)
        self.current_chapter = 0
        self.advances.append((lineno, old, self.book))

    def update(self, lineno: int, ch: int, v: int) -> None:
        # If chapter exceeds current book's chapter count, advance
        while self.idx < len(self.books) - 1 and ch > max_ch(self.book, self.cvc_map):
            self._advance(lineno)

        # Chapter reset: advance until (ch, v) fits in current book
        if ch < self.current_chapter:
            while self.idx < len(self.books) - 1 and not self._fits(self.book, ch, v):
                self._advance(lineno)
            # If the current book does accept (ch, v) but the chapter reset
            # implies a new book, try one more advance if the next book also fits
            if (
                self._fits(self.book, ch, v)
                and self.idx < len(self.books) - 1
                and ch < self.current_chapter
            ):
                self._advance(lineno)

        # Verse overflow: advance until (ch, v) fits
        while self.idx < len(self.books) - 1 and not self._fits(self.book, ch, v):
            self._advance(lineno)

        self.current_chapter = ch


# ---------------------------------------------------------------------------
# Core conversion
# ---------------------------------------------------------------------------

def wikify(book: str, ch: int, v: int, sub: str, range_sfx: str,
           trailing: str, rest: str) -> str:
    return f"[[{book}.{ch}:{v}]]{sub}{range_sfx}{trailing}{rest}"


def convert(dry_run: bool = False) -> None:
    cvc_map = build_cvc_map()

    with open(MD_PATH, encoding="utf-8") as fh:
        original_lines = fh.readlines()

    s1 = BookTracker(S1_BOOKS, cvc_map)
    s2 = BookTracker(S2_BOOKS, cvc_map)

    new_lines: list[str] = []
    s1_converted = s1_skipped = 0
    s2_converted = s2_skipped = 0
    conversion_log: list[tuple[int, str, str]] = []

    for lineno, raw_line in enumerate(original_lines, 1):
        line = raw_line.rstrip("\n")
        eol = "\n" if raw_line.endswith("\n") else ""

        # YAML frontmatter (lines 1-7)
        if lineno <= 7:
            new_lines.append(raw_line)
            continue

        # Already wikified
        if line.lstrip().startswith("[["):
            new_lines.append(raw_line)
            continue

        parsed = parse_bare_ref(line)
        if parsed is None:
            new_lines.append(raw_line)
            continue

        ch, v, sub, range_sfx, m = parsed
        trailing = m.group(5)
        rest = line[m.end():]

        if lineno < SECTION2_START:
            # Section 1
            s1.update(lineno, ch, v)
            book = s1.book
            if anchor_valid(book, ch, v, cvc_map):
                new_line = wikify(book, ch, v, sub, range_sfx, trailing, rest)
                new_lines.append(new_line + eol)
                s1_converted += 1
                conversion_log.append((lineno, line, new_line))
            else:
                new_lines.append(raw_line)
                s1_skipped += 1
        else:
            # Section 2
            s2.update(lineno, ch, v)
            book = s2.book
            if anchor_valid(book, ch, v, cvc_map):
                new_line = wikify(book, ch, v, sub, range_sfx, trailing, rest)
                new_lines.append(new_line + eol)
                s2_converted += 1
                conversion_log.append((lineno, line, new_line))
            else:
                new_lines.append(raw_line)
                s2_skipped += 1

    # Report
    print("Conversion summary:")
    print(f"  Lines processed:          {len(original_lines)}")
    print(f"  Section 1 converted:      {s1_converted}  (main NT variants)")
    print(f"  Section 1 skipped:        {s1_skipped}  (invalid anchors)")
    print(f"  Section 2 converted:      {s2_converted}  (cross-refs / 1TH-2TH)")
    print(f"  Section 2 skipped:        {s2_skipped}  (commentary blocks / invalid)")
    print(f"  Total wikilinks created:  {s1_converted + s2_converted}")

    print(f"\nSection 1 book advances ({len(s1.advances)}):")
    for ln, frm, to in s1.advances:
        print(f"  line {ln}: {frm} -> {to}")

    print(f"\nSection 2 book advances ({len(s2.advances)}):")
    for ln, frm, to in s2.advances:
        print(f"  line {ln}: {frm} -> {to}")

    print(f"\nSample conversions (first 10):")
    for ln, old, new in conversion_log[:10]:
        print(f"  line {ln}:")
        print(f"    OLD: {old[:80]}")
        print(f"    NEW: {new[:80]}")

    print(f"\nSpot-check 10 converted anchors (evenly spread):")
    step = max(1, len(conversion_log) // 10)
    for i in range(0, min(len(conversion_log), 10 * step), step):
        ln, old, new = conversion_log[i]
        m2 = re.match(r"\[\[(\w+)\.(\d+):(\d+)\]\]", new)
        if m2:
            b, c, vv = m2.group(1), int(m2.group(2)), int(m2.group(3))
            valid = anchor_valid(b, c, vv, cvc_map)
            print(f"  line {ln}: {m2.group(0)} => {'VALID' if valid else 'INVALID'}")

    if dry_run:
        print("\nDRY RUN — no file written.")
        return

    with open(MD_PATH, "w", encoding="utf-8") as fh:
        fh.writelines(new_lines)
    print(f"\nWrote {MD_PATH}")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    convert(dry_run=dry_run)
