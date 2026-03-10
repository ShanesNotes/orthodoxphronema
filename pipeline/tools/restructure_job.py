#!/usr/bin/env python3
"""Restructure JOB.md by reassigning verses to correct chapters using Brenton reference data."""

import json
import re
import sys
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


def load_brenton():
    """Load Brenton reference, returns dict: (ch_int, v_int) -> verse_text."""
    data = json.load(open(BRENTON))
    ref = {}
    for ch_str, ch_data in data["chapters"].items():
        ch = int(ch_str)
        for i, vtext in enumerate(ch_data["verses"]):
            ref[(ch, i + 1)] = vtext
    return ref


def parse_job_md():
    """Parse JOB.md into frontmatter + list of (type, data) entries."""
    lines = JOB_MD.read_text().splitlines()

    # Extract frontmatter
    fm_lines = []
    body_start = 0
    if lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                fm_lines = lines[:i + 1]
                body_start = i + 1
                break

    entries = []  # list of (type, data)
    # type: 'chapter', 'verse', 'heading', 'blank'
    for line in lines[body_start:]:
        m_ch = RE_CHAPTER.match(line)
        m_v = RE_VERSE.match(line)
        if m_ch:
            entries.append(('chapter', int(m_ch.group(1))))
        elif m_v:
            ch = int(m_v.group(2))
            v = int(m_v.group(3))
            text = m_v.group(4)
            entries.append(('verse', (ch, v, text, line)))
        elif RE_HEADING.match(line):
            entries.append(('heading', line))
        elif line.strip() == '':
            entries.append(('blank', ''))
        else:
            # Stray line — keep as-is
            entries.append(('other', line))

    return fm_lines, entries


def match_verses(entries, brenton_ref):
    """Match all verses from ch3+ against Brenton. Return list of (new_ch, new_v, text, orig_line, heading_before)."""
    # First, collect verse entries with their associated headings
    results = []  # (orig_ch, orig_v, text, orig_line, headings_before)
    pending_headings = []

    for etype, data in entries:
        if etype == 'heading':
            pending_headings.append(data)
        elif etype == 'verse':
            ch, v, text, line = data
            results.append((ch, v, text, line, list(pending_headings)))
            pending_headings = []
        # chapter headers and blanks are discarded — we'll rebuild them

    # Separate ch1-2 (keep as-is) from ch3+ (need matching)
    ch12_verses = [(ch, v, text, line, hdgs) for ch, v, text, line, hdgs in results if ch <= 2]
    ch3plus_verses = [(ch, v, text, line, hdgs) for ch, v, text, line, hdgs in results if ch >= 3]

    # Build Brenton lookup for ch3+ only
    brenton_ch3plus = {k: v for k, v in brenton_ref.items() if k[0] >= 3}

    # Track which Brenton verses have been matched (to avoid double-matching)
    matched_brenton = set()

    # For each OSB verse, find best Brenton match
    reassigned = []
    prev_ch = 2
    prev_v = 18  # last verse of ch2

    for orig_ch, orig_v, text, line, hdgs in ch3plus_verses:
        best_score = 0.0
        best_key = None

        for bkey, btext in brenton_ch3plus.items():
            if bkey in matched_brenton:
                continue
            score = jaccard(text, btext)
            if score > best_score:
                best_score = score
                best_key = bkey

        if best_score >= 0.25 and best_key is not None:
            new_ch, new_v = best_key
            matched_brenton.add(best_key)
            prev_ch = new_ch
            prev_v = new_v
        else:
            # Assign to previous chapter with next sequential verse
            new_ch = prev_ch
            new_v = prev_v + 1
            prev_v = new_v
            print(f"  LOW MATCH: JOB.{orig_ch}:{orig_v} -> JOB.{new_ch}:{new_v} (best={best_score:.3f})", file=sys.stderr)

        reassigned.append((new_ch, new_v, text, line, hdgs, best_score))

    return ch12_verses, reassigned


def rebuild_file(fm_lines, ch12_verses, reassigned):
    """Rebuild JOB.md with correct chapter structure."""
    out = list(fm_lines)

    # Group ch1-2 by chapter
    for ch_num in [1, 2]:
        out.append("")
        out.append(f"## Chapter {ch_num}")
        out.append("")
        for orig_ch, orig_v, text, line, hdgs in ch12_verses:
            if orig_ch == ch_num:
                for h in hdgs:
                    out.append("")
                    out.append(h)
                    out.append("")
                out.append(line)

    # Sort reassigned by (new_ch, new_v)
    reassigned.sort(key=lambda x: (x[0], x[1]))

    current_ch = 2
    for new_ch, new_v, text, orig_line, hdgs, score in reassigned:
        if new_ch != current_ch:
            current_ch = new_ch
            out.append(f"## Chapter {current_ch}")
            out.append("")

        for h in hdgs:
            out.append("")
            out.append(h)
            out.append("")

        # Build new line with corrected anchor
        new_line = f"JOB.{new_ch}:{new_v} {text}"
        out.append(new_line)

    return "\n".join(out) + "\n"


def main():
    print("Loading Brenton reference...", file=sys.stderr)
    brenton_ref = load_brenton()
    print(f"  Brenton has {len(brenton_ref)} verses across {max(k[0] for k in brenton_ref)} chapters", file=sys.stderr)

    print("Parsing JOB.md...", file=sys.stderr)
    fm_lines, entries = parse_job_md()
    verse_count = sum(1 for e in entries if e[0] == 'verse')
    print(f"  Found {verse_count} verse lines", file=sys.stderr)

    print("Matching verses against Brenton...", file=sys.stderr)
    ch12_verses, reassigned = match_verses(entries, brenton_ref)
    print(f"  Ch1-2: {len(ch12_verses)} verses (kept as-is)", file=sys.stderr)
    print(f"  Ch3+: {len(reassigned)} verses reassigned", file=sys.stderr)

    # Stats
    matched = sum(1 for r in reassigned if r[5] >= 0.25)
    unmatched = len(reassigned) - matched
    print(f"  Matched: {matched}, Unmatched (fallback): {unmatched}", file=sys.stderr)

    # Chapter distribution
    from collections import Counter
    ch_dist = Counter(r[0] for r in reassigned)
    print(f"  Chapters covered: {sorted(ch_dist.keys())}", file=sys.stderr)

    # Check for expected chapter count
    expected_total = sum(CVC)
    actual_ch12 = len(ch12_verses)
    actual_ch3plus = len(reassigned)
    print(f"  Expected total verses (CVC): {expected_total}", file=sys.stderr)
    print(f"  Actual verses: {actual_ch12 + actual_ch3plus}", file=sys.stderr)

    print("Rebuilding file...", file=sys.stderr)
    content = rebuild_file(fm_lines, ch12_verses, reassigned)

    JOB_MD.write_text(content)
    print(f"Written to {JOB_MD}", file=sys.stderr)

    # Verify chapter count
    ch_headers = re.findall(r'^## Chapter (\d+)', content, re.MULTILINE)
    print(f"  Chapter headers in output: {len(ch_headers)} ({', '.join(ch_headers[:5])}...{', '.join(ch_headers[-3:])})", file=sys.stderr)

    v_lines = re.findall(r'^JOB\.\d+:\d+', content, re.MULTILINE)
    print(f"  Verse lines in output: {len(v_lines)}", file=sys.stderr)


if __name__ == "__main__":
    main()
