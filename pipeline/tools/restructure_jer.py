#!/usr/bin/env python3
"""Restructure JER.md chapters 25-52.

The extractor assigned all ch25-52 content to chapter 25 with cycling verse numbers.
Each new chapter starts with a "verse" whose number IS the chapter number (that verse
is actually verse 1 of the new chapter), followed by verses numbered from 2 onward.

Only chapter 30 lacks an explicit marker (its boundary is at verse index 159,
detected by the verse-number drop from 8 -> 2).
"""

import re
import sys

JER_MD = "/home/ark/orthodoxphronema/staging/validated/OT/JER.md"

OSB_CVC = {
    25: 38, 26: 24, 27: 22, 28: 17, 29: 32, 30: 24, 31: 40, 32: 44,
    33: 26, 34: 22, 35: 19, 36: 32, 37: 21, 38: 28, 39: 18, 40: 16,
    41: 18, 42: 22, 43: 13, 44: 30, 45: 5, 46: 28, 47: 7, 48: 47,
    49: 39, 50: 46, 51: 64, 52: 34
}

def main():
    with open(JER_MD) as f:
        lines = f.readlines()

    # Find start of Chapter 25
    ch25_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "## Chapter 25":
            ch25_idx = i
            break
    if ch25_idx is None:
        print("ERROR: Could not find ## Chapter 25")
        sys.exit(1)

    header_lines = lines[:ch25_idx]
    blob_lines = lines[ch25_idx + 1:]

    # Parse blob into items
    RE_VERSE = re.compile(r"^(JER\.\d+:\d+)\s(.+)$")
    RE_HEADING = re.compile(r"^###\s")

    items = []
    for line in blob_lines:
        stripped = line.strip()
        if not stripped:
            continue
        m = RE_VERSE.match(stripped)
        if m:
            vn = int(m.group(1).split(":")[1])
            items.append(("verse", {"vn": vn, "text": m.group(2)}))
        elif RE_HEADING.match(stripped):
            items.append(("heading", stripped))

    # Extract verse-only items
    verse_items = [(i, item[1]) for i, item in enumerate(items) if item[0] == "verse"]
    verse_nums = [v["vn"] for _, v in verse_items]

    # Find chapter markers: vn >= 26 AND next verse is 2 or 3
    chapter_markers = {}  # verse_seq_index -> chapter_number
    for i in range(len(verse_nums) - 1):
        vn = verse_nums[i]
        next_vn = verse_nums[i + 1]
        if 26 <= vn <= 52 and next_vn in (2, 3):
            chapter_markers[i] = vn

    # Add ch30 hidden boundary: index 159 is where verse drops from 8->2
    # Verse at index 159 (vn=8) is actually ch30 verse 1
    # Confirmed by Brenton match: "Wisdom is no longer in Teman" = Brenton 30:1
    chapter_markers[159] = 30

    # Assign chapters
    # Sort markers
    sorted_markers = sorted(chapter_markers.items())

    # Build assignments: for each verse, determine (chapter, sequential_vn)
    assignments = []
    current_ch = 25
    ch_count = 0

    for vi in range(len(verse_items)):
        if vi in chapter_markers:
            current_ch = chapter_markers[vi]
            ch_count = 1
        else:
            ch_count += 1
        assignments.append((current_ch, ch_count))

    # Group into chapters
    chapters = {}
    for vi, (ch, seq_vn) in enumerate(assignments):
        item_idx, vdata = verse_items[vi]
        chapters.setdefault(ch, []).append((item_idx, vdata["text"], vi))

    # Associate headings with following verse
    heading_before = {}
    pending_headings = []
    verse_seq = 0
    for item in items:
        if item[0] == "heading":
            pending_headings.append(item[1])
        elif item[0] == "verse":
            if pending_headings:
                heading_before[verse_seq] = list(pending_headings)
                pending_headings = []
            verse_seq += 1

    # Build output
    output_lines = list(header_lines)
    total_assigned = 0

    for ch in range(25, 53):
        output_lines.append(f"## Chapter {ch}\n")
        output_lines.append("\n")
        if ch in chapters:
            for seq_idx, (item_idx, text, vi) in enumerate(chapters[ch]):
                final_vn = seq_idx + 1
                if vi in heading_before:
                    for h in heading_before[vi]:
                        output_lines.append(f"\n{h}\n")
                        output_lines.append("\n")
                output_lines.append(f"JER.{ch}:{final_vn} {text}\n")
                total_assigned += 1

    with open(JER_MD, "w") as f:
        f.writelines(output_lines)

    print(f"Restructured JER.md: {total_assigned} verses across chapters 25-52")
    total_expected = sum(OSB_CVC.values())
    print(f"Total expected: {total_expected}, total assigned: {total_assigned}")
    mismatches = 0
    for ch in range(25, 53):
        actual = len(chapters.get(ch, []))
        expected = OSB_CVC.get(ch, "?")
        status = "OK" if actual == expected else f"MISMATCH (got {actual}, expected {expected})"
        if actual != expected:
            mismatches += 1
        print(f"  Ch {ch}: {actual:3d} verses - {status}")
    print(f"\n{mismatches} chapters with mismatches, {28 - mismatches} OK")

if __name__ == "__main__":
    main()
