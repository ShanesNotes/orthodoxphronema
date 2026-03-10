#!/usr/bin/env python3
"""Fix duplicate anchors in JOB.md by reassigning duplicates to unused verse slots."""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path("/home/ark/orthodoxphronema")
JOB_MD = REPO / "staging/validated/OT/JOB.md"
BRENTON = REPO / "staging/reference/brenton/JOB.json"

CVC = [22, 18, 26, 21, 27, 30, 21, 22, 35, 22, 20, 25, 28, 22, 35, 22, 16, 21, 30, 29, 34, 30, 17, 25, 6, 14, 23, 28, 25, 31, 40, 22, 33, 37, 15, 35, 24, 41, 30, 32, 26, 22]

RE_VERSE = re.compile(r'^(JOB)\.(\d+):(\d+)\s+(.*)')
RE_CHAPTER = re.compile(r'^## Chapter (\d+)')
RE_HEADING = re.compile(r'^### ')


def jaccard(text_a: str, text_b: str) -> float:
    words_a = set(text_a.lower().split())
    words_b = set(text_b.lower().split())
    if not words_a or not words_b:
        return 0.0
    return len(words_a & words_b) / len(words_a | words_b)


def main():
    brenton = json.load(open(BRENTON))
    brenton_ref = {}
    for ch_str, ch_data in brenton["chapters"].items():
        ch = int(ch_str)
        for i, vtext in enumerate(ch_data["verses"]):
            brenton_ref[(ch, i + 1)] = vtext

    lines = JOB_MD.read_text().splitlines()

    # Parse into structured entries preserving line order
    fm_end = 0
    if lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                fm_end = i + 1
                break

    fm_lines = lines[:fm_end]

    # Parse body into entries: (type, line_idx, data)
    # For verses: data = (ch, v, text)
    entries = []
    for idx in range(fm_end, len(lines)):
        line = lines[idx]
        m_v = RE_VERSE.match(line)
        m_ch = RE_CHAPTER.match(line)
        if m_v:
            ch, v, text = int(m_v.group(2)), int(m_v.group(3)), m_v.group(4)
            entries.append(('verse', idx, (ch, v, text)))
        elif m_ch:
            entries.append(('chapter', idx, int(m_ch.group(1))))
        elif RE_HEADING.match(line):
            entries.append(('heading', idx, line))
        elif line.strip() == '':
            entries.append(('blank', idx, ''))
        else:
            entries.append(('other', idx, line))

    # Find duplicate anchors
    anchor_indices = defaultdict(list)  # (ch, v) -> [entry_indices]
    for i, (etype, line_idx, data) in enumerate(entries):
        if etype == 'verse':
            ch, v, text = data
            anchor_indices[(ch, v)].append(i)

    duplicates = {k: v for k, v in anchor_indices.items() if len(v) > 1}
    print(f"Found {len(duplicates)} duplicate anchors", file=sys.stderr)

    if not duplicates:
        print("No duplicates to fix!", file=sys.stderr)
        return

    # For each duplicate set, keep the best Brenton match, reassign others
    reassign = []  # list of entry indices that need new anchors
    for (ch, v), entry_idxs in duplicates.items():
        btext = brenton_ref.get((ch, v), "")
        best_score = -1
        best_idx = entry_idxs[0]
        for ei in entry_idxs:
            _, _, (_, _, text) = entries[ei]
            score = jaccard(text, btext) if btext else 0
            if score > best_score:
                best_score = score
                best_idx = ei
        # Keep best_idx, reassign the rest
        for ei in entry_idxs:
            if ei != best_idx:
                reassign.append(ei)

    print(f"Need to reassign {len(reassign)} verses", file=sys.stderr)

    # Collect all occupied anchors (excluding the ones we're about to reassign)
    reassign_set = set(reassign)
    occupied = set()
    for i, (etype, line_idx, data) in enumerate(entries):
        if etype == 'verse' and i not in reassign_set:
            ch, v, text = data
            occupied.add((ch, v))

    # For each verse to reassign, find best unoccupied Brenton match
    unmatched_brenton = set(brenton_ref.keys()) - occupied
    for ei in reassign:
        _, line_idx, (old_ch, old_v, text) = entries[ei]
        best_score = 0.0
        best_key = None
        for bkey in unmatched_brenton:
            score = jaccard(text, brenton_ref[bkey])
            if score > best_score:
                best_score = score
                best_key = bkey

        if best_score >= 0.15 and best_key is not None:
            new_ch, new_v = best_key
            unmatched_brenton.discard(best_key)
            occupied.add(best_key)
            entries[ei] = ('verse', line_idx, (new_ch, new_v, text))
            print(f"  Reassigned JOB.{old_ch}:{old_v} -> JOB.{new_ch}:{new_v} (score={best_score:.3f})", file=sys.stderr)
        else:
            # Find nearest unused slot in same chapter
            for try_v in range(1, CVC[old_ch - 1] + 1):
                if (old_ch, try_v) not in occupied:
                    occupied.add((old_ch, try_v))
                    entries[ei] = ('verse', line_idx, (old_ch, try_v, text))
                    print(f"  Fallback JOB.{old_ch}:{old_v} -> JOB.{old_ch}:{try_v} (no good Brenton match)", file=sys.stderr)
                    break
            else:
                # Try adjacent chapters
                for try_ch in range(max(3, old_ch - 1), min(43, old_ch + 3)):
                    for try_v in range(1, CVC[try_ch - 1] + 1):
                        if (try_ch, try_v) not in occupied:
                            occupied.add((try_ch, try_v))
                            entries[ei] = ('verse', line_idx, (try_ch, try_v, text))
                            print(f"  Overflow JOB.{old_ch}:{old_v} -> JOB.{try_ch}:{try_v}", file=sys.stderr)
                            break
                    else:
                        continue
                    break

    # Now rebuild: collect all verses, sort by (ch, v), rebuild with chapter headers
    verse_entries = []
    heading_map = {}  # maps verse entry index -> list of heading strings before it
    pending_headings = []

    for i, (etype, line_idx, data) in enumerate(entries):
        if etype == 'heading':
            pending_headings.append(data)
        elif etype == 'verse':
            ch, v, text = data
            verse_entries.append((ch, v, text, list(pending_headings)))
            pending_headings = []

    # Separate ch1-2 and ch3+
    ch12 = [(ch, v, text, hdgs) for ch, v, text, hdgs in verse_entries if ch <= 2]
    ch3plus = [(ch, v, text, hdgs) for ch, v, text, hdgs in verse_entries if ch >= 3]

    # Sort ch3+ by (ch, v)
    ch3plus.sort(key=lambda x: (x[0], x[1]))

    # Deduplicate headings globally: each heading text appears only once in the file
    seen_headings_global = set()

    # Build output
    out = list(fm_lines)

    # Ch 1-2
    for ch_num in [1, 2]:
        out.append("")
        out.append(f"## Chapter {ch_num}")
        out.append("")
        for ch, v, text, hdgs in ch12:
            if ch == ch_num:
                for h in hdgs:
                    if h not in seen_headings_global:
                        seen_headings_global.add(h)
                        out.append("")
                        out.append(h)
                        out.append("")
                out.append(f"JOB.{ch}:{v} {text}")

    # Ch 3+
    current_ch = 2
    for ch, v, text, hdgs in ch3plus:
        if ch != current_ch:
            current_ch = ch
            out.append(f"## Chapter {current_ch}")
            out.append("")

        for h in hdgs:
            if h not in seen_headings_global:
                seen_headings_global.add(h)
                out.append("")
                out.append(h)
                out.append("")

        out.append(f"JOB.{ch}:{v} {text}")

    content = "\n".join(out) + "\n"
    JOB_MD.write_text(content)

    # Verify
    v_count = len(re.findall(r'^JOB\.\d+:\d+', content, re.MULTILINE))
    ch_count = len(re.findall(r'^## Chapter', content, re.MULTILINE))
    anchors = re.findall(r'^(JOB\.\d+:\d+)', content, re.MULTILINE)
    unique_anchors = len(set(anchors))
    dup_count = len(anchors) - unique_anchors
    print(f"\nOutput: {v_count} verses, {ch_count} chapters, {unique_anchors} unique anchors, {dup_count} duplicates remaining", file=sys.stderr)


if __name__ == "__main__":
    main()
