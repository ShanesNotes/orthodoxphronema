#!/usr/bin/env python3
"""Restructure SIR.md — FINAL DEFINITIVE VERSION.

Uses verse-number cycling to detect chapter boundaries, with specific
handling for:
- False v=2 drop at idx 24 (column-split artifact within ch1)
- Ch49 boundary at idx 1295 (drops to v7 not v2)
- Chapter-lead artifacts (standalone chapter numbers before first verse)
- Navigation noise from Hosea nav pages at end of file
"""

import json
import re

SIR_MD = "/home/ark/orthodoxphronema/staging/validated/OT/SIR.md"

OSB_CVC = [27, 18, 29, 31, 15, 37, 36, 19, 18, 29, 32, 18, 25, 27, 20, 28, 27, 32, 27, 31, 28, 27, 27, 34, 25, 20, 30, 26, 28, 25, 31, 24, 33, 26, 24, 27, 31, 34, 35, 30, 27, 25, 33, 23, 26, 20, 25, 25, 16, 29, 30]

def main():
    with open(SIR_MD) as f:
        content = f.read()

    parts = content.split('---', 2)
    frontmatter = '---' + parts[1] + '---'
    body = parts[2]

    heading_re = re.compile(r'^### (.+)')
    chapter_re = re.compile(r'^## Chapter')
    verse_re = re.compile(r'^SIR\.0:(\d+)\s+(.*)')

    elements = []
    for line in body.split('\n'):
        stripped = line.strip()
        if not stripped or chapter_re.match(stripped):
            continue
        m_h = heading_re.match(stripped)
        if m_h:
            elements.append(('heading', stripped, m_h.group(1), -1))
            continue
        m_v = verse_re.match(stripped)
        if m_v:
            vnum = int(m_v.group(1))
            vtext = m_v.group(2)
            elements.append(('verse', stripped, vtext, vnum))
            continue

    verse_elems = [(i, e) for i, e in enumerate(elements) if e[0] == 'verse']
    total = len(verse_elems)
    vnums = [e[3] for _, e in verse_elems]
    vtexts = [e[2] for _, e in verse_elems]
    print(f"Parsed: {total} verses, {sum(1 for e in elements if e[0]=='heading')} headings")

    # ---- FIND CHAPTER BOUNDARIES ----
    # Find all v=2 drops (where verse goes from high number to 2)
    raw_starts = [0]  # ch1 starts at idx 0
    for i in range(1, total):
        if vnums[i] == 2 and vnums[i-1] > 3:
            raw_starts.append(i)

    # Remove false boundary at idx 24 (column-split artifact within ch1)
    if 24 in raw_starts:
        raw_starts.remove(24)

    # Add ch49 boundary at idx 1295 (drops to v7, not v2)
    # Ch49 starts where v drops from 19 to 7 (Ezekiel/prophets section)
    if 1295 not in raw_starts:
        raw_starts.append(1295)
        raw_starts.sort()

    print(f"Chapter starts: {len(raw_starts)}")

    # Verify we have exactly 51
    if len(raw_starts) != 51:
        print(f"WARNING: Expected 51, got {len(raw_starts)}")
        # Show the sizes for debugging
        for i in range(len(raw_starts)):
            s = raw_starts[i]
            e = raw_starts[i+1] if i+1 < len(raw_starts) else total
            print(f"  Ch{i+1}: idx={s}, size={e-s}")

    # ---- IDENTIFY CHAPTER LEADS TO REMOVE ----
    # Chapter leads are standalone verse numbers that match the chapter number
    # They appear right before the first verse of a new chapter
    ch_leads = set()

    # Known leads: verse at idx-1 whose verse number matches the chapter number
    # when followed by v=2 at idx
    for idx_in_list, start_idx in enumerate(raw_starts):
        if start_idx > 0 and idx_in_list > 0:
            prev_vn = vnums[start_idx - 1]
            ch_num = idx_in_list + 1  # chapter number (1-indexed)
            # Check if previous verse number matches a plausible chapter number
            if prev_vn == ch_num or (prev_vn >= 30 and prev_vn == ch_num):
                ch_leads.add(start_idx - 1)
            # Also check for high-numbered leads: prev verse = ch_num, prev-prev was higher
            elif start_idx >= 2 and prev_vn > vnums[start_idx - 2] + 5:
                # The previous verse dropped suddenly — likely a chapter lead
                if prev_vn <= 51:
                    ch_leads.add(start_idx - 1)

    # Also add the false v2 at idx 24 as an artifact to remove
    ch_leads.add(24)

    # Navigation noise at the end
    nav_noise = set()
    for i in range(total):
        text = vtexts[i]
        if any(noise in text for noise in ['Back to', 'Chapters in Hosea',
                                             'Previous Home Next',
                                             'Table of Contents']):
            nav_noise.add(i)

    skip_indices = ch_leads | nav_noise
    print(f"Chapter leads to remove: {len(ch_leads)}")
    print(f"Nav noise to remove: {len(nav_noise)}")

    # ---- ASSIGN CHAPTERS AND VERSE NUMBERS ----
    assignments = [None] * total

    for ch_idx in range(len(raw_starts)):
        ch = ch_idx + 1
        start = raw_starts[ch_idx]
        end = raw_starts[ch_idx + 1] if ch_idx + 1 < len(raw_starts) else total

        for vi in range(start, end):
            if vi in skip_indices:
                continue
            # Use original verse number from the extraction
            assignments[vi] = (ch, vnums[vi])

    # ---- REPORT ----
    ch_counts = {}
    for a in assignments:
        if a:
            ch_counts[a[0]] = ch_counts.get(a[0], 0) + 1

    assigned_total = sum(ch_counts.values())
    print(f"\nAssigned {assigned_total} verses to {len(ch_counts)} chapters")

    mismatches = 0
    for ch in range(1, 52):
        exp = OSB_CVC[ch - 1]
        act = ch_counts.get(ch, 0)
        if act != exp:
            mismatches += 1
            if abs(act - exp) > 2:
                print(f"  Ch {ch}: {act} (expected {exp}, delta {act-exp:+d})")
    print(f"Mismatches: {mismatches}/51 (showing >2 delta)")

    # ---- BUILD OUTPUT ----
    seen_headings = set()
    verse_assign = {}
    for vi, (elem_idx, _) in enumerate(verse_elems):
        if assignments[vi]:
            verse_assign[elem_idx] = assignments[vi]

    chapters_out = {}
    for i, (etype, raw, data, vnum) in enumerate(elements):
        if etype == 'verse' and i in verse_assign:
            ch, v = verse_assign[i]
            if ch not in chapters_out:
                chapters_out[ch] = []
            new_anchor = f"SIR.{ch}:{v}"
            new_line = re.sub(r'^SIR\.\d+:\d+', new_anchor, raw)
            chapters_out[ch].append(('verse', new_line))
        elif etype == 'heading':
            if data in seen_headings:
                continue
            seen_headings.add(data)
            # Find chapter of next verse
            next_ch = None
            for j in range(i + 1, len(elements)):
                if elements[j][0] == 'verse':
                    for vi, (ei, _) in enumerate(verse_elems):
                        if ei == j and assignments[vi]:
                            next_ch = assignments[vi][0]
                            break
                    if next_ch:
                        break
            if next_ch:
                if next_ch not in chapters_out:
                    chapters_out[next_ch] = []
                chapters_out[next_ch].append(('heading', raw))

    # ---- WRITE ----
    with open(SIR_MD, 'w') as f:
        f.write(frontmatter)
        f.write('\n\n')
        for ch in sorted(chapters_out.keys()):
            f.write(f'## Chapter {ch}\n\n')
            for etype, line in chapters_out[ch]:
                if etype == 'heading':
                    f.write(f'\n{line}\n\n')
                else:
                    f.write(f'{line}\n\n')

    total_v = sum(1 for items in chapters_out.values() for t, _ in items if t == 'verse')
    total_h = sum(1 for items in chapters_out.values() for t, _ in items if t == 'heading')
    print(f"\nWritten: {len(chapters_out)} chapters, {total_v} verses, {total_h} headings")

if __name__ == '__main__':
    main()
