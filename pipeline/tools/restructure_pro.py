#!/usr/bin/env python3
"""Restructure PRO.md: Use sequential Brenton matching for ch1-23,
then OSB text-pattern anchoring for ch24-31."""

import json
import re
from collections import defaultdict

PRO_MD = "/home/ark/orthodoxphronema/staging/validated/OT/PRO.md"
BRENTON = "/home/ark/orthodoxphronema/staging/reference/brenton/PRO.json"

CVC = [33, 22, 35, 27, 23, 35, 27, 36, 18, 32, 31, 28, 25, 35, 33, 33, 28, 24, 29, 30, 31, 29, 35, 34, 28, 28, 27, 28, 27, 33, 31]

def jaccard(a, b):
    wa = set(a.lower().split())
    wb = set(b.lower().split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)

def main():
    with open(PRO_MD, "r") as f:
        raw_lines = f.readlines()
    with open(BRENTON, "r") as f:
        brenton = json.load(f)

    # Extract frontmatter
    fm_lines, body_lines = [], []
    in_fm, fm_ended = False, False
    for line in raw_lines:
        if not fm_ended:
            if line.strip() == "---":
                fm_lines.append(line)
                if in_fm: fm_ended = True
                else: in_fm = True
                continue
            if in_fm:
                fm_lines.append(line)
                continue
        body_lines.append(line)

    RE_VERSE = re.compile(r'^PRO\.(\d+):(\d+)\s+(.*)')
    RE_HEADING = re.compile(r'^###\s+(.*)')

    items = []
    for line in body_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("## Chapter"):
            continue
        hm = RE_HEADING.match(stripped)
        if hm:
            items.append({"type": "heading", "text": hm.group(1)})
            continue
        vm = RE_VERSE.match(stripped)
        if vm:
            text = vm.group(3).strip()
            if text:
                items.append({"type": "verse", "text": text})

    # Filter orphaned headings + "Outline"
    first_vi = next((i for i, it in enumerate(items) if it["type"] == "verse"), len(items))
    items = [it for i, it in enumerate(items)
             if not (i < first_vi and it["type"] == "heading")
             and not (it["type"] == "heading" and it["text"].strip() == "Outline")]

    verse_items = [it for it in items if it["type"] == "verse"]
    print(f"Total verses: {len(verse_items)}")

    # ====== PHASE 1: Sequential matching ch1-23 ======
    brenton_1_23 = []
    for ch in range(1, 24):
        ch_str = str(ch)
        if ch_str in brenton["chapters"]:
            for i, text in enumerate(brenton["chapters"][ch_str]["verses"]):
                brenton_1_23.append((ch, i + 1, text))

    bpos = 0
    phase1_end = 0

    for vi, v_item in enumerate(verse_items):
        if bpos >= len(brenton_1_23):
            phase1_end = vi
            break

        text = v_item["text"]
        best_score, best_idx = -1, -1
        start = max(0, bpos - 3)
        end = min(len(brenton_1_23), bpos + 15)

        for idx in range(start, end):
            bch, bv, btext = brenton_1_23[idx]
            score = jaccard(text, btext)
            if score > best_score:
                best_score = score
                best_idx = idx

        if best_score >= 0.10 and best_idx >= 0:
            bch, bv, _ = brenton_1_23[best_idx]
            v_item["osb_ch"] = bch
            bpos = best_idx + 1
        else:
            if bpos < len(brenton_1_23):
                bch, bv, _ = brenton_1_23[bpos]
                v_item["osb_ch"] = bch
                bpos += 1
            else:
                phase1_end = vi
                break
    else:
        phase1_end = len(verse_items)

    print(f"Phase 1: {phase1_end} verses matched to ch1-23")

    # ====== PHASE 2: Pattern-based anchoring for ch24-31 ======
    phase2_verses = verse_items[phase1_end:]
    print(f"Phase 2: {len(phase2_verses)} verses remaining for ch24-31")

    # OSB chapter start patterns (search in order)
    ch_patterns = [
        (24, re.compile(r'do not env\s*y\s*ev\s*il men|envy evil men', re.I)),
        (25, re.compile(r'instructions of Solomon.*Hezekiah|proverbs of Solomon.*Hezekiah|Solomon.*friends.*Hezekiah', re.I)),
        (26, re.compile(r'dew in harv\s*est|snow in summer', re.I)),
        (27, re.compile(r'do not boast about tomorrow|boast not.*tomorrow', re.I)),
        (28, re.compile(r'ungodly man flees|wicked flee', re.I)),
        (29, re.compile(r'reprov\s*ing man is better|often rebuked', re.I)),
        (30, re.compile(r'man says.*repent|fear my words.*repent|words of Agur', re.I)),
        (31, re.compile(r'virtuous (wife|woman)|who (shall|can) find', re.I)),
    ]

    # Find chapter boundaries
    ch_boundaries = {}  # ch -> index in phase2_verses
    for vi, v_item in enumerate(phase2_verses):
        text = v_item["text"]
        for ch, pattern in ch_patterns:
            if ch not in ch_boundaries and pattern.search(text):
                ch_boundaries[ch] = vi
                print(f"  Ch {ch} detected at phase2 idx {vi}: {text[:70]}")
                break

    # For any chapters not found by pattern, try Brenton first-verse matching
    # but only within a restricted range (not global)
    brenton_first = {}
    for ch in range(24, 32):
        ch_str = str(ch)
        if ch_str in brenton["chapters"] and brenton["chapters"][ch_str]["verses"]:
            brenton_first[ch] = brenton["chapters"][ch_str]["verses"][0]

    for ch in range(24, 32):
        if ch in ch_boundaries:
            continue
        if ch not in brenton_first:
            continue

        btext = brenton_first[ch]
        best_score, best_idx = -1, -1

        # Only search near expected position based on neighboring chapters
        for vi, v_item in enumerate(phase2_verses):
            score = jaccard(v_item["text"], btext)
            if score > best_score:
                best_score = score
                best_idx = vi

        if best_score >= 0.25:
            ch_boundaries[ch] = best_idx
            print(f"  Ch {ch} via Brenton match at phase2 idx {best_idx} (score={best_score:.3f}): {phase2_verses[best_idx]['text'][:60]}")

    # Sort boundaries by position and ensure monotonic chapter order
    sorted_bounds = sorted(ch_boundaries.items(), key=lambda x: x[1])
    print(f"\n  Raw boundaries: {sorted_bounds}")

    # Don't enforce monotonic chapter order — OSB follows LXX ordering
    # which rearranges chapters 24-31 compared to MT
    print(f"  Final boundaries: {sorted_bounds}")

    # Assign chapters to phase2 verses
    for i, (ch, start) in enumerate(sorted_bounds):
        end = sorted_bounds[i + 1][1] if i + 1 < len(sorted_bounds) else len(phase2_verses)
        for vi in range(start, end):
            phase2_verses[vi]["osb_ch"] = ch

    # Handle verses before first boundary
    if sorted_bounds and sorted_bounds[0][1] > 0:
        first_ch = sorted_bounds[0][0]
        for vi in range(sorted_bounds[0][1]):
            phase2_verses[vi]["osb_ch"] = first_ch

    # ====== NUMBER WITHIN CHAPTERS ======
    ch_groups = defaultdict(list)
    for v in verse_items:
        ch_groups[v["osb_ch"]].append(v)
    for ch, vlist in ch_groups.items():
        for i, v in enumerate(vlist):
            v["final_v"] = i + 1

    # ====== ASSIGN HEADINGS ======
    all_items = []
    heading_buf = []
    for item in items:
        if item["type"] == "heading":
            heading_buf.append(item)
        elif item["type"] == "verse":
            for h in heading_buf:
                h["osb_ch"] = item["osb_ch"]
                h["final_v"] = item["final_v"]
                all_items.append(h)
            heading_buf = []
            all_items.append(item)
    for h in heading_buf:
        if verse_items:
            h["osb_ch"] = verse_items[-1]["osb_ch"]
            h["final_v"] = verse_items[-1]["final_v"]
        all_items.append(h)

    # ====== OUTPUT ======
    ch_output = defaultdict(list)
    for item in all_items:
        ch_output[item["osb_ch"]].append(item)

    output_lines = []
    for fl in fm_lines:
        output_lines.append(fl.rstrip("\n"))

    for ch in sorted(ch_output.keys()):
        output_lines.append("")
        output_lines.append(f"## Chapter {ch}")
        output_lines.append("")
        for item in ch_output[ch]:
            if item["type"] == "heading":
                output_lines.append("")
                output_lines.append(f"### {item['text']}")
                output_lines.append("")
            elif item["type"] == "verse":
                output_lines.append(f"PRO.{item['osb_ch']}:{item['final_v']} {item['text']}")

    with open(PRO_MD, "w") as f:
        f.write("\n".join(output_lines) + "\n")

    # Stats
    print(f"\nChapter distribution:")
    total = 0
    for ch in range(1, 32):
        expected = CVC[ch - 1]
        actual = len(ch_groups.get(ch, []))
        total += actual
        delta = actual - expected
        flag = "" if delta == 0 else f" (delta {delta:+d})"
        print(f"  Ch {ch:2d}: {actual:3d} / {expected:3d}{flag}")
    print(f"\nTotal: {total} (expected 915)")

    # First verse of each chapter
    print("\nFirst verse of each chapter:")
    for ch in sorted(ch_groups.keys()):
        v = ch_groups[ch][0]
        print(f"  Ch {ch:2d}: {v['text'][:80]}")

if __name__ == "__main__":
    main()
