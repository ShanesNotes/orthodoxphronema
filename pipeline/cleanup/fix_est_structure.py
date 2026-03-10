#!/usr/bin/env python3
"""
EST structural reconstruction.

The OSB Esther integrates Greek additions (A-F) at their narrative positions
using sub-verse notation (1a, 1b, 13b, etc.). The extraction produced chapters
0-7 instead of the correct 1-10 structure, with chapters 8-10 collapsed into
chapter 7.

This script:
1. Merges chapter 0 (Addition A) into chapter 1, renumbering sequentially
2. Fixes V9 embedded verse splits in ch1 (1:10→1:11), ch2 (2:5→2:6),
   ch9 (9:8→9:9, 9:22→9:23/9:24)
3. Renumbers duplicate verse anchors in ch3 (3:14/3:15 appear twice)
4. Splits collapsed ch7 into chapters 7-10 based on backward verse jumps
5. Renumbers all verse anchors in ch8-10 sequentially
"""

import re
import sys

INPUT = "staging/validated/OT/EST.md"
OUTPUT = INPUT  # overwrite


def parse_file(path):
    """Parse EST.md into a list of (line_type, data) tuples.
    line_type: 'frontmatter', 'chapter', 'heading', 'verse', 'blank'
    """
    lines = []
    with open(path, "r", encoding="utf-8") as f:
        raw = f.readlines()

    in_frontmatter = False
    fm_lines = []
    for line in raw:
        stripped = line.rstrip("\n")

        if stripped == "---":
            if not in_frontmatter and not fm_lines:
                in_frontmatter = True
                fm_lines.append(stripped)
                continue
            elif in_frontmatter:
                in_frontmatter = False
                fm_lines.append(stripped)
                lines.append(("frontmatter", fm_lines))
                continue

        if in_frontmatter:
            fm_lines.append(stripped)
            continue

        if stripped.startswith("## Chapter "):
            ch_num = int(stripped.split()[-1])
            lines.append(("chapter", ch_num))
        elif stripped.startswith("### "):
            lines.append(("heading", stripped))
        elif re.match(r"^EST\.\d+:\d+\s", stripped):
            m = re.match(r"^EST\.(\d+):(\d+)\s(.*)", stripped)
            ch = int(m.group(1))
            v = int(m.group(2))
            text = m.group(3)
            lines.append(("verse", (ch, v, text)))
        elif stripped == "":
            lines.append(("blank", None))
        else:
            # Shouldn't happen, but preserve
            lines.append(("other", stripped))

    return lines


def v9_split_verse(text, current_v):
    """Split embedded verse numbers from text. Returns list of (vnum, text)."""
    # Pattern: text ending, then a bare number starting a new verse
    # Look for patterns like "Artaxerxes11 to bring" or "Vajezatha9 the ten"
    # or "them: 23 how Haman" or "them; 24 how he"

    results = [(current_v, text)]

    # Pattern 1: number fused with preceding word (e.g., "Artaxerxes11", "Vajezatha9")
    # Pattern 2: number after punctuation/space (e.g., ": 23 how", "; 24 how")
    next_v = current_v + 1

    # Try fused pattern first
    fused = re.match(
        r"^(.*?\S)(" + str(next_v) + r")\s+(.*)$", text
    )
    if fused:
        pre = fused.group(1)
        vnum = int(fused.group(2))
        post = fused.group(3)
        return [(current_v, pre), (vnum, post)]

    # Try space-separated pattern for sequential verse numbers
    parts = [(current_v, text)]
    remaining = text
    curr = current_v

    # Look for multiple embedded verses (e.g., "... 23 how ... 24 how ...")
    splits_found = []
    for next_candidate in range(current_v + 1, current_v + 10):
        # Pattern: punctuation or end of clause, then number, then text
        pat = re.compile(
            r"^(.*?(?:[;:,.]\s*|\s))(" + str(next_candidate) + r")\s+([a-z].*)",
            re.DOTALL,
        )
        m = pat.match(remaining)
        if m:
            splits_found.append((next_candidate, m.start(2), m.end(2)))

    if splits_found:
        result = []
        pos = 0
        current_vnum = current_v
        for vnum, start, end in splits_found:
            # Text before this split point
            pre_text = remaining[pos:start].rstrip(": ;,\t ")
            if pre_text:
                result.append((current_vnum, pre_text))
            current_vnum = vnum
            pos = end
            # Skip leading space after verse number
            while pos < len(remaining) and remaining[pos] == " ":
                pos += 1
        # Remaining text
        if pos < len(remaining):
            result.append((current_vnum, remaining[pos:]))
        if len(result) > 1:
            return result

    return [(current_v, text)]


def reconstruct(parsed):
    """Apply all structural fixes and return list of output lines."""
    output = []

    # ---- Phase 1: Collect all verses by their ORIGINAL chapter ----
    orig_chapters = {}  # ch_num -> list of items (type, data)
    current_ch = None
    frontmatter = None

    for item_type, data in parsed:
        if item_type == "frontmatter":
            frontmatter = data
        elif item_type == "chapter":
            current_ch = data
            if current_ch not in orig_chapters:
                orig_chapters[current_ch] = []
        elif current_ch is not None:
            orig_chapters[current_ch].append((item_type, data))

    # ---- Phase 2: Build new chapter structure ----
    new_chapters = {}

    # --- Chapter 1: merge ch0 (Addition A) + ch1 (Hebrew) ---
    ch1_items = []
    verse_counter = 0

    # Addition A from ch0
    for item_type, data in orig_chapters.get(0, []):
        if item_type == "verse":
            _, _, text = data
            # Strip leading "1 " from first verse (artifact of verse number in text)
            if verse_counter == 0 and text.startswith("1 "):
                text = text[2:]
            verse_counter += 1
            ch1_items.append(("verse", (1, verse_counter, text)))
        elif item_type == "heading":
            # "King Artaxerxes' Banquet" heading: defer to after Addition A
            if "Banquet" in data:
                continue  # Will be re-inserted at correct position
            ch1_items.append((item_type, data))
        else:
            ch1_items.append((item_type, data))

    # Insert heading before Hebrew content
    ch1_items.append(("blank", None))
    ch1_items.append(("heading", "### King Artaxerxes' Banquet"))
    ch1_items.append(("blank", None))

    # Hebrew ch1
    for item_type, data in orig_chapters.get(1, []):
        if item_type == "verse":
            _, v, text = data
            verse_counter += 1
            # V9 split at old 1:10 (embedded "11")
            if v == 10 and "Artaxerxes11" in text:
                parts = text.split("Artaxerxes11", 1)
                ch1_items.append(
                    ("verse", (1, verse_counter, parts[0] + "Artaxerxes"))
                )
                verse_counter += 1
                ch1_items.append(
                    ("verse", (1, verse_counter, parts[1].lstrip()))
                )
            else:
                ch1_items.append(("verse", (1, verse_counter, text)))
        else:
            ch1_items.append((item_type, data))

    new_chapters[1] = ch1_items

    # --- Chapter 2: V9 split at 2:5 (embedded "6") ---
    ch2_items = []
    for item_type, data in orig_chapters.get(2, []):
        if item_type == "verse":
            _, v, text = data
            if v == 5 and ", 6 " in text:
                # Split at ", 6 "
                idx = text.index(", 6 ")
                pre = text[: idx + 1]  # Keep the comma
                post = text[idx + 4 :]  # After "6 "
                ch2_items.append(("verse", (2, 5, pre)))
                ch2_items.append(("verse", (2, 6, post)))
            else:
                ch2_items.append(("verse", (2, v, text)))
        else:
            ch2_items.append((item_type, data))
    new_chapters[2] = ch2_items

    # --- Chapter 3: renumber duplicate 3:14/3:15 ---
    ch3_items = []
    seen_14 = False
    seen_15 = False
    for item_type, data in orig_chapters.get(3, []):
        if item_type == "verse":
            _, v, text = data
            if v == 14:
                if not seen_14:
                    seen_14 = True
                    ch3_items.append(("verse", (3, 14, text)))
                else:
                    ch3_items.append(("verse", (3, 16, text)))
            elif v == 15:
                if not seen_15:
                    seen_15 = True
                    ch3_items.append(("verse", (3, 15, text)))
                else:
                    ch3_items.append(("verse", (3, 17, text)))
            else:
                ch3_items.append(("verse", (3, v, text)))
        else:
            ch3_items.append((item_type, data))
    new_chapters[3] = ch3_items

    # --- Chapters 4, 5, 6: keep as-is ---
    for ch in [4, 5, 6]:
        if ch in orig_chapters:
            new_chapters[ch] = orig_chapters[ch]

    # --- Split chapter 7 into 7, 8, 9, 10 ---
    ch7_verses = []
    ch7_other = []  # Non-verse items with their position
    verse_idx = 0
    for item_type, data in orig_chapters.get(7, []):
        if item_type == "verse":
            ch7_verses.append((verse_idx, item_type, data))
            verse_idx += 1
        else:
            ch7_other.append((verse_idx, item_type, data))

    # Identify chapter boundaries by content matching against Brenton
    # Ch7: first 10 verses (7:1-10, sequential, no backward jumps)
    # Ch8 starts: "On that day, King Artaxerxes gave Esther everything"
    # Ch9 starts: "Now in the twelfth month, on the thirteenth day"
    # Ch10 starts: "And the king levied tribute upon his kingdom"

    ch8_start_text = "On that day, King Artaxerxes gave Esther"
    ch9_start_text = "Now in the twelfth month, on the thirteenth day"
    ch10_start_text = "And the king levied tribute"

    ch8_idx = ch9_idx = ch10_idx = None
    for i, (_, _, (_, _, text)) in enumerate(ch7_verses):
        if ch8_idx is None and ch8_start_text in text:
            ch8_idx = i
        elif ch9_idx is None and ch9_start_text in text:
            ch9_idx = i
        elif ch10_idx is None and ch10_start_text in text:
            ch10_idx = i

    if not all([ch8_idx, ch9_idx, ch10_idx]):
        print(f"ERROR: Could not find chapter boundaries: ch8={ch8_idx}, ch9={ch9_idx}, ch10={ch10_idx}")
        sys.exit(1)

    print(f"Chapter boundaries in ch7: ch8 at verse idx {ch8_idx}, ch9 at {ch9_idx}, ch10 at {ch10_idx}")

    # Helper to collect non-verse items for a verse range
    def get_other_before(verse_start_idx, verse_end_idx):
        return [
            (t, d)
            for idx, t, d in ch7_other
            if verse_start_idx <= idx < verse_end_idx
        ]

    # Build ch7 (first 10 verses)
    ch7_items = []
    for pos, _, (_, _, text) in ch7_verses[:ch8_idx]:
        others = [(t, d) for idx, t, d in ch7_other if idx == pos]
        for t, d in others:
            ch7_items.append((t, d))
        ch7_items.append(("verse", (7, pos + 1, text)))
    # Add any trailing non-verse items
    for idx, t, d in ch7_other:
        if ch8_idx > 0 and idx >= ch7_verses[ch8_idx - 1][0] and idx < ch7_verses[ch8_idx][0]:
            ch7_items.append((t, d))
    new_chapters[7] = ch7_items

    # Build ch8
    ch8_items = []
    v_num = 0
    for pos, _, (_, _, text) in ch7_verses[ch8_idx:ch9_idx]:
        # Include headings that precede this verse
        for idx, t, d in ch7_other:
            if idx == ch7_verses[ch8_idx + v_num][0]:
                ch8_items.append((t, d))
        v_num += 1
        ch8_items.append(("verse", (8, v_num, text)))
    new_chapters[8] = ch8_items

    # Build ch9 (with V9 splits)
    ch9_items = []
    v_num = 0
    for pos, _, (_, _, text) in ch7_verses[ch9_idx:ch10_idx]:
        # Include headings
        for idx, t, d in ch7_other:
            if idx == ch7_verses[ch9_idx + v_num][0]:
                ch9_items.append((t, d))
        v_num += 1

        # V9 split: "Vajezatha9" (verse 8→9)
        if "Vajezatha9" in text:
            parts = text.split("9 ", 1)
            # "Parmashta, Arisai, Aridai, and Vajezatha" + "the ten sons..."
            pre = parts[0].replace("Vajezatha9", "Vajezatha,")
            post = parts[1] if len(parts) > 1 else ""
            # Actually, split more carefully
            idx_v = text.index("Vajezatha9")
            pre_text = text[:idx_v] + "Vajezatha,"
            post_text = text[idx_v + len("Vajezatha9"):].lstrip()
            ch9_items.append(("verse", (9, v_num, pre_text)))
            v_num += 1
            ch9_items.append(("verse", (9, v_num, post_text)))
            continue

        # V9 split: "23 how Haman" and "24 how he had gone"
        if v_num > 1 and ": 23 how" in text:
            # Split at ": 23 " and "; 24 "
            splits = v9_split_verse(text, v_num)
            if len(splits) > 1:
                for sv, st in splits:
                    ch9_items.append(("verse", (9, v_num if sv == splits[0][0] else v_num + (sv - splits[0][0]), st)))
                v_num += len(splits) - 1
                continue

        ch9_items.append(("verse", (9, v_num, text)))
    new_chapters[9] = ch9_items

    # Build ch10
    ch10_items = []
    v_num = 0
    for pos, _, (_, _, text) in ch7_verses[ch10_idx:]:
        for idx, t, d in ch7_other:
            if idx == ch7_verses[ch10_idx + v_num][0]:
                ch10_items.append((t, d))
        v_num += 1
        ch10_items.append(("verse", (10, v_num, text)))
    new_chapters[10] = ch10_items

    # ---- Phase 3: Generate output ----
    # Frontmatter (update checksum will happen at promotion)
    output = []
    if frontmatter:
        for fl in frontmatter:
            output.append(fl)
    output.append("")

    for ch_num in sorted(new_chapters.keys()):
        output.append(f"## Chapter {ch_num}")
        output.append("")

        for item_type, data in new_chapters[ch_num]:
            if item_type == "verse":
                ch, v, text = data
                output.append(f"EST.{ch}:{v} {text}")
            elif item_type == "heading":
                output.append("")
                output.append(data)
                output.append("")
            elif item_type == "blank":
                # Avoid double blanks
                if output and output[-1] != "":
                    output.append("")

    # Remove trailing blank lines
    while output and output[-1] == "":
        output.pop()
    output.append("")  # Final newline

    return output


def main():
    parsed = parse_file(INPUT)
    output = reconstruct(parsed)

    # Count verses per chapter
    cvc = {}
    for line in output:
        m = re.match(r"^EST\.(\d+):(\d+)\s", line)
        if m:
            ch = int(m.group(1))
            v = int(m.group(2))
            if ch not in cvc:
                cvc[ch] = 0
            cvc[ch] = max(cvc[ch], v)

    print("Chapter verse counts (max verse number per chapter):")
    total = 0
    for ch in sorted(cvc.keys()):
        print(f"  Ch{ch}: {cvc[ch]}")
        total += cvc[ch]
    print(f"  Total: {total}")

    # Count actual verse lines
    actual = {}
    for line in output:
        m = re.match(r"^EST\.(\d+):(\d+)\s", line)
        if m:
            ch = int(m.group(1))
            actual[ch] = actual.get(ch, 0) + 1
    print("\nActual verse lines per chapter:")
    total_actual = 0
    for ch in sorted(actual.keys()):
        gap = cvc[ch] - actual[ch]
        gap_str = f" ({gap} gaps)" if gap else ""
        print(f"  Ch{ch}: {actual[ch]}{gap_str}")
        total_actual += actual[ch]
    print(f"  Total: {total_actual}")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print(f"\nWrote {len(output)} lines to {OUTPUT}")


if __name__ == "__main__":
    main()
