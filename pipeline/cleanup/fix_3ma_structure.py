#!/usr/bin/env python3
"""fix_3ma_structure.py — Reconstruct 3MA chapters 3-7 from collapsed ch2.

This script can be run on either:
- The original extraction (all ch3-7 collapsed into ch2)
- A previously-reconstructed file (to re-apply with corrected boundaries)

It works by flattening all verse text after ch2:33, then re-applying
chapter boundaries using unique content signatures.

Registry CVC: [29, 33, 30, 21, 51, 41, 23] = 228 total
Expected output: 28+33+30+21+51+41+23 = 227 verse lines (ch1:28, CVC=29 mismatch)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FILE = Path("staging/validated/OT/3MA.md")
RE_VERSE = re.compile(r'^3MA\.(\d+):(\d+) (.+)$')

# Content signatures for the first verse of each chapter after ch2.
# IMPORTANT: Each signature must be unique across the entire file.
# Ch7 uses extended signature to avoid matching ch3:12's "King Ptolemy" letter.
CH_SIGNATURES = [
    (3, "When the ungodly king heard this"),
    (4, "Wherever this decree arrived"),
    (5, "Then the king, filled with wrath"),
    (6, "Now there was acertain man, Eleazar"),
    (7, "'King Ptolemy Philopator, to the commanders in Egypt and to all those"),
]

# Section headers that repeat on every page — Docling page-layout artifacts.
DUPLICATE_HEADERS = {
    "### The Traitors Are Punished",
    "### Death Threat",
    "### The Jews Are Delivered",
    "### Ptolemy's Change of Heart",
    "### God Delivers His People",
    "### Ptolemy Assaults the Jews",
    "### Deportation to Alexandria",
    "### The Ambivalent King",
    "### A Letter of Support from the King",
}


def find_chapter_start(text: str) -> int | None:
    """Check if verse text matches a chapter-start signature."""
    for ch, sig in CH_SIGNATURES:
        if text.startswith(sig):
            return ch
    return None


def split_v9_verses(ch: int, verse_num: int, text: str) -> list[tuple[int, str]]:
    """Split V9 embedded verses. Returns list of (verse_num, text) pairs."""
    # Ch5:6 — contains inline "7" and "8"
    if ch == 5 and ", 7 called out" in text:
        parts = text.split(", 7 ", 1)
        if len(parts) == 2:
            v6_text = parts[0] + ","
            remainder = parts[1]
            parts2 = remainder.rsplit(" 8 ", 1)
            if len(parts2) == 2:
                v7_text = parts2[0]
                v8_text = parts2[1]
                return [
                    (verse_num, v6_text),
                    (verse_num + 1, v7_text),
                    (verse_num + 2, v8_text),
                ]
    # Ch6:2 — contains inline "3"
    if ch == 6 and "in mercy, 3 look upon" in text:
        parts = text.split(", 3 ", 1)
        if len(parts) == 2:
            return [
                (verse_num, parts[0] + ","),
                (verse_num + 1, parts[1]),
            ]
    return [(verse_num, text)]


def main():
    if not FILE.exists():
        print(f"File not found: {FILE}", file=sys.stderr)
        sys.exit(1)

    content = FILE.read_text(encoding="utf-8")
    lines = content.splitlines()

    # Phase 1: Separate frontmatter, ch1, ch2, and collapsed content
    # Strategy: collect all verse texts in order, ignoring current chapter labels
    frontmatter_lines = []
    ch1_header_seen = False
    ch1_verses = []  # (text,) tuples
    ch1_section_headers = {}  # position -> header text
    ch2_header_seen = False
    ch2_verses = []
    post_ch2_verse_texts = []  # flat list of verse texts after ch2

    in_frontmatter = True
    in_ch1 = False
    in_ch2 = False
    past_ch2 = False
    ch2_verse_count = 0

    for line in lines:
        stripped = line.strip()

        # Track frontmatter
        if in_frontmatter:
            frontmatter_lines.append(line)
            if stripped == "---" and len(frontmatter_lines) > 1:
                in_frontmatter = False
            continue

        # Skip duplicate section headers everywhere
        if stripped in DUPLICATE_HEADERS:
            continue

        # Skip chapter headers (we'll re-create them)
        if stripped.startswith("## Chapter"):
            ch_num = int(stripped.split()[-1])
            if ch_num == 1:
                in_ch1 = True
                in_ch2 = False
                past_ch2 = False
            elif ch_num == 2:
                in_ch1 = False
                in_ch2 = True
                past_ch2 = False
            else:
                # Any other chapter header from previous bad reconstruction
                in_ch1 = False
                in_ch2 = False
                past_ch2 = True
            continue

        # Skip blank lines (we'll add them back structurally)
        if stripped == "":
            continue

        # Check for verse lines
        m = RE_VERSE.match(line)
        if m:
            verse_text = m.group(3)
            ch = int(m.group(1))
            v = int(m.group(2))

            if in_ch1 or ch == 1:
                ch1_verses.append(verse_text)
                in_ch1 = True
            elif (in_ch2 or ch == 2) and not past_ch2:
                ch2_verses.append(verse_text)
                ch2_verse_count += 1
                in_ch2 = True
                # After 33 real ch2 verses, everything else goes to collapsed
                if ch2_verse_count == 33:
                    in_ch2 = False
                    past_ch2 = True
            else:
                post_ch2_verse_texts.append(verse_text)
                past_ch2 = True
            continue

        # Section headers (non-duplicate ones, like ch1's unique headers)
        if stripped.startswith("###"):
            if in_ch1:
                ch1_section_headers[len(ch1_verses)] = stripped
            continue

        # Any other line — keep track
        # (shouldn't happen but be safe)

    print(f"Parsed: ch1={len(ch1_verses)}, ch2={len(ch2_verses)}, collapsed={len(post_ch2_verse_texts)}")

    # Phase 2: Apply chapter boundaries to collapsed verse texts
    chapters = {}  # ch_num -> list of verse texts
    current_ch = None

    for text in post_ch2_verse_texts:
        new_ch = find_chapter_start(text)
        if new_ch is not None:
            current_ch = new_ch
            chapters[current_ch] = [text]
        elif current_ch is not None:
            chapters[current_ch].append(text)
        else:
            print(f"WARNING: verse before any chapter boundary: {text[:60]}", file=sys.stderr)

    # Phase 3: Apply V9 splits within chapters
    for ch, verses in chapters.items():
        expanded = []
        for text in verses:
            verse_num = len(expanded) + 1
            splits = split_v9_verses(ch, verse_num, text)
            for _, t in splits:
                expanded.append(t)
        chapters[ch] = expanded

    # Phase 4: Build output
    output = []

    # Frontmatter
    output.extend(frontmatter_lines)
    output.append("")

    # Chapter 1
    output.append("## Chapter 1")
    output.append("")
    for i, text in enumerate(ch1_verses):
        v = i + 1
        # Insert section headers at their recorded positions
        if i in ch1_section_headers:
            output.append("")
            output.append(ch1_section_headers[i])
            output.append("")
        output.append(f"3MA.1:{v} {text}")

    # Chapter 2
    output.append("")
    output.append("## Chapter 2")
    output.append("")
    for i, text in enumerate(ch2_verses):
        v = i + 1
        output.append(f"3MA.2:{v} {text}")

    # Chapters 3-7
    for ch in sorted(chapters):
        output.append("")
        output.append(f"## Chapter {ch}")
        output.append("")
        for i, text in enumerate(chapters[ch]):
            v = i + 1
            output.append(f"3MA.{ch}:{v} {text}")

    FILE.write_text("\n".join(output) + "\n", encoding="utf-8")

    # Phase 5: Report stats
    total = len(ch1_verses) + len(ch2_verses)
    cvc = [29, 33, 30, 21, 51, 41, 23]

    print(f"\nReconstructed 3MA: {2 + len(chapters)} chapters")
    ch_all = {1: len(ch1_verses), 2: len(ch2_verses)}
    ch_all.update({ch: len(vs) for ch, vs in chapters.items()})
    total = sum(ch_all.values())

    for ch in sorted(ch_all):
        expected = cvc[ch - 1] if ch <= len(cvc) else "?"
        count = ch_all[ch]
        status = "✓" if count == expected else f"(CVC={expected})"
        print(f"  Ch{ch}: {count} verses {status}")
    print(f"  Total: {total} verse lines")


if __name__ == "__main__":
    main()
