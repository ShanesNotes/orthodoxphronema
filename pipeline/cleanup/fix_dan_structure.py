#!/usr/bin/env python3
"""Fix DAN.md structural issues from OSB extraction.

Issues:
1. Susanna (ch.13 in LXX/OSB) was placed as ch.1 vv.1-64, then real ch.1
   follows with duplicate anchors. Fix: relabel Susanna as ch.13, keep real ch.1.
2. Bel and the Dragon (ch.14 in LXX/OSB) was appended after ch.12:13 with
   duplicate DAN.12:1-42 anchors. Fix: relabel as ch.14.
3. Embedded verses (V9): inline verse numbers not split into separate lines.
   e.g. "...text, 23 these three men..." -> split at boundary.
4. Split-word artifacts in the poetic Song of the Three Young Men (ch.3).
"""
import re
import sys
from pathlib import Path

DAN_PATH = Path(__file__).resolve().parents[2] / "staging" / "validated" / "OT" / "DAN.md"

def fix_dan():
    text = DAN_PATH.read_text(encoding="utf-8")
    lines = text.split("\n")

    # ── Phase 1: Identify structural boundaries ──
    # Find where Susanna ends and real Daniel 1 begins
    # Susanna = DAN.1:1 through DAN.1:64 (first occurrence)
    # Real Daniel 1 = second DAN.1:1 occurrence

    # Find all DAN.1:1 lines
    dan_1_1_indices = [i for i, l in enumerate(lines) if l.startswith("DAN.1:1 ")]
    assert len(dan_1_1_indices) == 2, f"Expected 2 DAN.1:1 lines, found {len(dan_1_1_indices)}"

    susanna_start_line = dan_1_1_indices[0]  # First DAN.1:1 = Susanna verse 1
    real_ch1_start_line = dan_1_1_indices[1]  # Second DAN.1:1 = real Daniel 1:1

    # Find where Bel/Dragon starts (second occurrence of DAN.12:1)
    dan_12_1_indices = [i for i, l in enumerate(lines) if l.startswith("DAN.12:1 ")]
    assert len(dan_12_1_indices) == 2, f"Expected 2 DAN.12:1 lines, found {len(dan_12_1_indices)}"

    bel_start_line = dan_12_1_indices[1]  # Second DAN.12:1 = Bel verse 1

    # ── Phase 2: Relabel Susanna as chapter 13 ──
    # Susanna runs from first DAN.1:1 to one line before second DAN.1:1
    # We need to find all DAN.1:N anchors in that range and relabel to DAN.13:N
    # Also need to change "## Chapter 1" to "## Chapter 13"

    # Find the "## Chapter 1" header before Susanna
    ch1_header_idx = None
    for i in range(susanna_start_line - 1, -1, -1):
        if lines[i].strip() == "## Chapter 1":
            ch1_header_idx = i
            break
    assert ch1_header_idx is not None, "Could not find ## Chapter 1 header"

    # Relabel Susanna anchors (DAN.1:N -> DAN.13:N) in the Susanna section
    re_anchor = re.compile(r"^DAN\.1:(\d+) ")
    for i in range(susanna_start_line, real_ch1_start_line):
        m = re_anchor.match(lines[i])
        if m:
            vnum = m.group(1)
            lines[i] = f"DAN.13:{vnum} " + lines[i][m.end():]

    # Change Chapter 1 header to Chapter 13 (for Susanna)
    lines[ch1_header_idx] = "## Chapter 13"

    # Insert a proper "## Chapter 1" header before the real ch.1 content
    # Find the heading or blank line just before real_ch1_start_line
    # Look backwards from real_ch1_start_line to find where to insert
    insert_ch1_idx = real_ch1_start_line
    # Check if there's a narrative heading before real ch1
    for i in range(real_ch1_start_line - 1, real_ch1_start_line - 4, -1):
        if i >= 0 and lines[i].startswith("### "):
            insert_ch1_idx = i  # Insert before the heading
            break

    # Actually, let's look at what's between Susanna's last verse and real ch1
    # There's already a "### Daniel and His Companions Obey God" heading
    # and DAN.1:64 (Susanna's last verse, now DAN.13:64)
    # We need to insert ## Chapter 1 before the heading
    # Let's find the blank line after Susanna ends
    for i in range(real_ch1_start_line - 1, susanna_start_line, -1):
        if lines[i].strip() == "":
            # Check if the line before is a heading
            if i > 0 and lines[i-1].startswith("### "):
                # Insert chapter header before the heading
                # Find the blank line before the heading
                for j in range(i - 1, susanna_start_line, -1):
                    if lines[j].strip() == "":
                        insert_ch1_idx = j + 1
                        break
                break
            else:
                insert_ch1_idx = i + 1
                break

    # Insert ## Chapter 1 header
    lines.insert(insert_ch1_idx, "")
    lines.insert(insert_ch1_idx + 1, "## Chapter 1")
    lines.insert(insert_ch1_idx + 2, "")

    # Recalculate indices after insertion (shifted by 3)
    # Need to re-find bel_start_line
    bel_start_line = None
    dan_12_1_count = 0
    for i, l in enumerate(lines):
        if l.startswith("DAN.12:1 "):
            dan_12_1_count += 1
            if dan_12_1_count == 2:
                bel_start_line = i
                break
    assert bel_start_line is not None, "Lost Bel start line after Susanna fix"

    # ── Phase 3: Relabel Bel and the Dragon as chapter 14 ──
    # Bel runs from second DAN.12:1 to end of file
    # Relabel DAN.12:N -> DAN.14:N for the Bel section
    re_anchor12 = re.compile(r"^DAN\.12:(\d+) ")

    # Find the heading "### Bel Is Deposed" or similar before the Bel section
    # We need to insert "## Chapter 14" before the Bel content
    bel_insert_idx = bel_start_line
    for i in range(bel_start_line - 1, bel_start_line - 4, -1):
        if i >= 0 and lines[i].startswith("### "):
            bel_insert_idx = i
            break
        elif i >= 0 and lines[i].strip() == "":
            continue

    # Find the blank line before the heading
    for i in range(bel_insert_idx - 1, -1, -1):
        if lines[i].strip() == "":
            bel_insert_idx = i + 1
            break

    # Insert chapter 14 header
    lines.insert(bel_insert_idx, "")
    lines.insert(bel_insert_idx + 1, "## Chapter 14")
    lines.insert(bel_insert_idx + 2, "")

    # Now relabel all DAN.12:N anchors after the chapter 14 header to DAN.14:N
    ch14_header_idx = bel_insert_idx + 1
    for i in range(ch14_header_idx, len(lines)):
        m = re_anchor12.match(lines[i])
        if m:
            vnum = m.group(1)
            lines[i] = f"DAN.14:{vnum} " + lines[i][m.end():]

    # ── Phase 4: Fix embedded verses (V9) ──
    # Pattern: "text, N next verse text" where N is the next verse number
    # Known cases from validation:
    # DAN.3:22 contains "23" -> split
    # DAN.4:21 contains "22" -> split
    # DAN.4:23 contains "24" -> split
    # DAN.7:21 contains "22" -> split
    # DAN.8:10 contains "11" -> split
    # DAN.9:20 contains "21" -> split

    embedded_fixes = [
        # (chapter, verse_with_embedded, embedded_vnum, split_pattern)
        (3, 22, 23, r"(.*?),?\s+23\s+"),
        (4, 21, 22, r"(.*?)-?\s+22\s+"),
        (4, 23, 24, r"(.*?)-?\s+24\s+"),
        (7, 21, 22, r"(.*?),?\s+22\s+"),
        (8, 10, 11, r"(.*?)\s+11\s+"),
        (9, 20, 21, r"(.*?),?\s+21\s+"),
    ]

    new_lines = []
    for line in lines:
        handled = False
        for ch, vnum, embedded_vnum, pattern in embedded_fixes:
            anchor = f"DAN.{ch}:{vnum} "
            if line.startswith(anchor):
                # Find the embedded verse number in the text
                verse_text = line[len(anchor):]
                # Search for the embedded verse number boundary
                # Pattern: text ending with punctuation/word, then space + number + space + next text
                embed_re = re.compile(rf"^(.*?)\s+{embedded_vnum}\s+(.+)$")
                m = embed_re.match(verse_text)
                if m:
                    part1 = m.group(1).rstrip()
                    part2 = m.group(2)
                    new_lines.append(f"DAN.{ch}:{vnum} {part1}")
                    new_lines.append(f"DAN.{ch}:{embedded_vnum} {part2}")
                    handled = True
                    break
        if not handled:
            new_lines.append(line)
    lines = new_lines

    # ── Phase 5: Fix DAN.4:7/4:8 duplicate ──
    # Line 297 has "...interpretation to me, 8 until at last Daniel..."
    # then line 298 has a separate DAN.4:8
    # The "8" in line 297 is an embedded verse that was not caught because
    # DAN.4:8 already exists as a separate line. We need to split 4:7 and
    # remove the duplicate 4:8 or merge them.
    # Actually looking more carefully: line 297 has DAN.4:7 text + "8 until..."
    # and line 298 has DAN.4:8 with different text. The "8" in line 297 is
    # the verse continuation. Let's split 4:7 at "8" and check if 4:8 is duplicate.

    new_lines2 = []
    skip_next_4_8 = False
    for i, line in enumerate(lines):
        if skip_next_4_8:
            if line.startswith("DAN.4:8 "):
                # This is the separate DAN.4:8 "Then I told the dream..."
                # Keep it - it's the correct verse 8, not a duplicate
                # Actually, looking at the text: the "8" in verse 7 is part of
                # "...not make known its interpretation to me, 8 until at last Daniel..."
                # This "8" IS the verse 8 boundary. The standalone DAN.4:8 at line 298
                # starts "Then I told the dream before him" which seems like a continuation.
                # In OSB Daniel (LXX), 4:7-8 may have been restructured.
                # Let's keep both for now - the standalone 4:8 has different text.
                skip_next_4_8 = False
                new_lines2.append(line)
            else:
                skip_next_4_8 = False
                new_lines2.append(line)
        elif line.startswith("DAN.4:7 "):
            # Check for embedded "8"
            text = line[len("DAN.4:7 "):]
            m = re.match(r"(.*?),?\s+8\s+(until\s+.+)$", text)
            if m:
                new_lines2.append(f"DAN.4:7 {m.group(1).rstrip()}")
                new_lines2.append(f"DAN.4:8 {m.group(2)}")
                skip_next_4_8 = True  # Check if next line is duplicate 4:8
            else:
                new_lines2.append(line)
        else:
            new_lines2.append(line)
    lines = new_lines2

    # ── Phase 6: Fix split-word artifacts in poetic sections (ch.3) ──
    # Common pattern: "heav en" -> "heaven", "serv ant" -> "servant", etc.
    split_word_fixes = [
        (r"\bdeliv er", "deliver"),
        (r"\bserv ant", "servant"),
        (r"\bcov enant", "covenant"),
        (r"\blov ed", "loved"),
        (r"\bheav en", "heaven"),
        (r"\bhav e", "have"),
        (r"\bov er", "over"),
        (r"\bev ery", "every"),
        (r"\bev il", "evil"),
        (r"\bEv ery", "Every"),
        (r"\bbey ond", "beyond"),
        (r"\baby mn", "abymn"),  # "ahy mn" -> needs special handling
        (r"\bhy mn", "hymn"),
        (r"\briv ers", "rivers"),
        (r"\bmov es", "moves"),
        (r"\bforev er", "forever"),
        (r"\bgiv e", "give"),
        (r"\bGiv e", "Give"),
        (r"\bsay ing", "saying"),
        (r"\bserv ants", "servants"),
        (r"\babov e", "above"),
    ]

    fixed_lines = []
    for line in lines:
        for pattern, replacement in split_word_fixes:
            line = re.sub(pattern, replacement, line)
        # Fix "ahy mn" -> "a hymn" (article merged with split word)
        line = line.replace("abymn", "a hymn")
        fixed_lines.append(line)
    lines = fixed_lines

    # ── Phase 7: Reorder chapters ──
    # Currently the file has: ch.13 (Susanna), ch.1, ch.2, ..., ch.12, ch.14 (Bel)
    # Canonical order should be: ch.1-12, ch.13 (Susanna), ch.14 (Bel)
    # Parse into sections by chapter headers

    # Split into frontmatter + chapters
    frontmatter_end = 0
    for i, l in enumerate(lines):
        if l.startswith("## Chapter "):
            frontmatter_end = i
            break

    frontmatter = lines[:frontmatter_end]
    body = lines[frontmatter_end:]

    # Parse chapters
    chapters = {}
    current_ch = None
    current_lines = []
    for line in body:
        m = re.match(r"^## Chapter (\d+)", line)
        if m:
            if current_ch is not None:
                # Strip trailing blank lines
                while current_lines and current_lines[-1].strip() == "":
                    current_lines.pop()
                chapters[current_ch] = current_lines
            current_ch = int(m.group(1))
            current_lines = [line]
        else:
            current_lines.append(line)
    if current_ch is not None:
        while current_lines and current_lines[-1].strip() == "":
            current_lines.pop()
        chapters[current_ch] = current_lines

    # Reassemble in order 1-14
    result = frontmatter[:]
    for ch_num in sorted(chapters.keys()):
        result.extend(chapters[ch_num])
        result.append("")  # blank line between chapters

    # Strip trailing whitespace
    while result and result[-1].strip() == "":
        result.pop()
    result.append("")  # single trailing newline

    DAN_PATH.write_text("\n".join(result), encoding="utf-8")
    print(f"[fix_dan] Written fixed DAN.md to {DAN_PATH}")
    print(f"[fix_dan] Chapters found: {sorted(chapters.keys())}")
    print(f"[fix_dan] Total lines: {len(result)}")


if __name__ == "__main__":
    fix_dan()
