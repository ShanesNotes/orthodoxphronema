#!/usr/bin/env python3
"""
fix_hos_chapters.py — Restructure HOS.md from broken chapter assignments.

Uses Brenton reference for word-overlap matching and registry CVC for expected verse counts.
Matches each verse in the file to its correct (chapter, verse) by comparing word overlap
with all Brenton verses, constrained to sequential order.
"""

import json
import re
import sys
import hashlib
from pathlib import Path
from collections import Counter

REPO = Path(__file__).resolve().parent.parent.parent


def load_brenton():
    """Load Brenton reference for HOS."""
    path = REPO / "staging" / "reference" / "brenton" / "HOS.json"
    with open(path) as f:
        data = json.load(f)
    ref = {}
    for ch_str, ch_data in data["chapters"].items():
        ch = int(ch_str)
        for i, text in enumerate(ch_data["verses"]):
            ref[(ch, i + 1)] = text
    return ref


def word_bag(text):
    """Extract bag of lowercase words (3+ chars) for matching."""
    return Counter(w.lower() for w in re.findall(r'[A-Za-z]+', text) if len(w) >= 3)


def word_overlap_score(osb_text, brenton_text):
    """Compute overlap score between OSB and Brenton text."""
    osb_words = word_bag(osb_text)
    brent_words = word_bag(brenton_text)
    if not osb_words or not brent_words:
        return 0.0
    # Count shared word occurrences
    shared = 0
    for w in osb_words:
        if w in brent_words:
            shared += min(osb_words[w], brent_words[w])
    total = sum(osb_words.values())
    return shared / total if total > 0 else 0.0


def fix_split_words(text):
    """Fix Docling column-split artifacts."""
    # "Xv e..." pattern (most common)
    text = re.sub(r'([a-z])(v)\s(e\w*)', r'\1\2\3', text)
    # "y ou" -> "you"
    text = re.sub(r'\by\s(ou\w*)', r'y\1', text)
    # "Egy pt" -> "Egypt"
    text = re.sub(r'Egy\spt', 'Egypt', text)
    # "Assy rians" -> "Assyrians" and variants
    text = re.sub(r'Assy\s(ri\w*)', r'Assy\1', text)
    # "My self" -> "Myself"
    text = re.sub(r'My\sself\b', 'Myself', text)
    # "say sthe" -> "says the"
    text = re.sub(r'say\ssthe', 'says the', text)
    # "say sing" -> "saying"
    text = re.sub(r'say\ssing', 'saying', text)
    # "day sof" -> "days of"
    text = re.sub(r'day\ssof', 'days of', text)
    # "day s " -> "days "
    text = re.sub(r'day\ss\b', 'days', text)
    # "way s" -> "ways"
    text = re.sub(r'way\ss\b', 'ways', text)
    # "ly ing" -> "lying"
    text = re.sub(r'\bly\sing\b', 'lying', text)
    # "Sy ria" -> "Syria"
    text = re.sub(r'Sy\sria', 'Syria', text)
    # "ey es" -> "eyes"
    text = re.sub(r'\bey\ses\b', 'eyes', text)
    # "sso" -> "so"
    text = re.sub(r'\bsso\b', 'so', text)
    # "Av en" -> "Aven"
    text = re.sub(r'\bAv\sen\b', 'Aven', text)
    return text


def fix_fused_articles(text):
    """Fix fused articles and possessive fusions."""
    fused = {
        'ason': 'a son', 'adaughter': 'a daughter', 'alittle': 'a little',
        'awoman': 'a woman', 'aking': 'a king', 'ahomer': 'a homer',
        'ajar': 'a jar', 'adry': 'a dry', 'amad': 'a mad',
        'alamb': 'a lamb', 'awide': 'a wide', 'ablast': 'a blast',
        'asnare': 'a snare', 'anet': 'a net', 'aspirit': 'a spirit',
        'aman': 'a man', 'acity': 'a city', 'apirate': 'a pirate',
        'arobber': 'a robber', 'amorning': 'a morning', 'aflame': 'a flame',
        'acake': 'a cake', 'asilly': 'a silly', 'aheart': 'a heart',
        'astretched': 'a stretched', 'aworthless': 'a worthless',
        'adeceiver': 'a deceiver', 'amultitude': 'a multitude',
        'asacrifice': 'a sacrifice', 'apriest': 'a priest',
        'apriesthood': 'a priesthood', 'aprince': 'a prince',
        'ajudgment': 'a judgment', 'aharlot': 'a harlot',
        'aconfusion': 'a confusion', 'asting': 'a sting',
        'apanther': 'a panther', 'alion': 'a lion',
        'aheifer': 'a heifer', 'aparched': 'a parched',
        'aprey': 'a prey', 'achild': 'a child',
        'abird': 'a bird', 'adove': 'a dove',
        'aleafy': 'a leafy', 'afruitful': 'a fruitful',
        'ashepherd': 'a shepherd', 'aleopard': 'a leopard',
        'aconspiracy': 'a conspiracy', 'adivision': 'a division',
        'atestimony': 'a testimony', 'abalance': 'a balance',
        'acovenant': 'a covenant', 'agift': 'a gift',
        'atwig': 'a twig', 'acrooked': 'a crooked',
        'aword': 'a word', 'awife': 'a wife',
        'aprophet': 'a prophet',
    }
    for fused_word, replacement in fused.items():
        text = re.sub(r'\b' + fused_word + r'\b', replacement, text)
    # Possessive fusions: "'s" fused with next word
    text = re.sub(r"'s([a-z])", r"'s \1", text)
    return text


def parse_file(filepath):
    """Parse HOS.md into frontmatter + body items."""
    with open(filepath) as f:
        text = f.read()
    lines = text.split('\n')

    # Find frontmatter
    fm_lines = []
    body_start = 0
    if lines[0].strip() == '---':
        fm_lines.append(lines[0])
        for i in range(1, len(lines)):
            fm_lines.append(lines[i])
            if lines[i].strip() == '---':
                body_start = i + 1
                break

    # Parse body items
    # Match both HOS.0:N and HOS.N:N patterns (since file may be partially restructured)
    verse_re = re.compile(r'^HOS\.(\d+):(\d+)\s(.+)$')
    heading_re = re.compile(r'^(#{2,3}\s.+)$')
    chapter_hdr_re = re.compile(r'^##\s+Chapter\s+(\d+)')

    items = []
    for i in range(body_start, len(lines)):
        line = lines[i]
        m_ch = chapter_hdr_re.match(line)
        m_v = verse_re.match(line)
        m_h = heading_re.match(line)

        if m_ch:
            items.append(('chapter_hdr', int(m_ch.group(1)), line))
        elif m_v:
            orig_ch = int(m_v.group(1))
            orig_v = int(m_v.group(2))
            text = m_v.group(3)
            items.append(('verse', orig_ch, orig_v, text))
        elif m_h:
            items.append(('heading', 0, 0, m_h.group(1)))
        elif line.strip() == '':
            items.append(('blank',))
        else:
            items.append(('other', line))

    return fm_lines, items


def match_verses(items, brenton_ref, cvc):
    """
    Match each verse to correct (chapter, verse) using sequential Brenton overlap.

    The CVC for HOS in the registry (OSB versification):
    [11, 23, 5, 19, 15, 11, 16, 14, 17, 15, 12, 14, 16, 9]

    Note: OSB has HOS ch1 with 11 verses and ch2 with 23 verses.
    Brenton has ch1 with 9 and ch2 with 25 (2 extra at start = OSB 1:10-11).
    Brenton ch2 starts at "Say to your brother" = OSB 2:1.
    But OSB 2:1 includes the Brenton 2:1-2 content differently.

    We map using Brenton cross-versification:
    - Brenton 1:1-9 = OSB 1:1-9
    - Brenton 2:1-2 = OSB 1:10-11
    - Brenton 2:3 = OSB 2:1
    - Brenton 2:4-25 = OSB 2:2-23 (shift by 2)
    - Ch3+ same as Brenton
    - ch13:15 (Brenton) = ch13:15 + ch14:1 merged in some versifications
    - Brenton ch14 has 10 verses, OSB has 9 (14:1 = end of 13:15 Brenton)
    """
    # Build the OSB-to-Brenton mapping
    # OSB CVC: [11, 23, 5, 19, 15, 11, 16, 14, 17, 15, 12, 14, 16, 9] = 197
    # Brenton CVC: [9, 25, 5, 19, 15, 11, 16, 14, 17, 15, 12, 15, 15, 10] = 197 (wait, same total?)
    # Let me count Brenton:
    brenton_counts = {}
    for (ch, v) in brenton_ref:
        brenton_counts[ch] = max(brenton_counts.get(ch, 0), v)
    print("Brenton verse counts:", {ch: brenton_counts[ch] for ch in sorted(brenton_counts)})
    brenton_total = sum(brenton_counts.values())
    osb_total = sum(cvc)
    print(f"Brenton total: {brenton_total}, OSB total: {osb_total}")

    # Build ordered sequence of expected (osb_ch, osb_v) -> brenton (ch, v) for matching
    # OSB 1:1-9 = Brenton 1:1-9
    # OSB 1:10 = Brenton 2:1
    # OSB 1:11 = Brenton 2:2
    # OSB 2:1 = Brenton 2:3
    # OSB 2:2 = Brenton 2:4
    # ... OSB 2:23 = Brenton 2:25
    # OSB 3:1 = Brenton 3:1 ... same from here
    # For ch13/14: Brenton 13:15 includes text that in OSB is 13:15+13:16
    # Brenton 14:1 = OSB 13:16? Actually let's check...
    # OSB ch13 has 16 verses, Brenton ch13 has 15.
    # OSB ch14 has 9 verses, Brenton ch14 has 10.
    # So: Brenton 13:15 end = OSB 13:15; Brenton 14:1 = OSB 13:16
    # Brenton 14:2 = OSB 14:1; ... Brenton 14:10 = OSB 14:9

    osb_to_brenton = {}
    # Ch1
    for v in range(1, 10):
        osb_to_brenton[(1, v)] = (1, v)
    osb_to_brenton[(1, 10)] = (2, 1)
    osb_to_brenton[(1, 11)] = (2, 2)
    # Ch2
    for v in range(1, 24):
        osb_to_brenton[(2, v)] = (2, v + 2)
    # Ch3-12 same
    for ch in range(3, 13):
        for v in range(1, cvc[ch-1] + 1):
            osb_to_brenton[(ch, v)] = (ch, v)
    # Ch13: OSB 13:1-15 = Brenton 13:1-15; OSB 13:16 = Brenton 14:1
    for v in range(1, 16):
        osb_to_brenton[(13, v)] = (13, v)
    osb_to_brenton[(13, 16)] = (14, 1)
    # Ch14: OSB 14:1-9 = Brenton 14:2-10
    for v in range(1, 10):
        osb_to_brenton[(14, v)] = (14, v + 1)

    print(f"OSB-to-Brenton mapping: {len(osb_to_brenton)} entries")

    # Build expected sequence
    expected = []
    for ch_idx, count in enumerate(cvc):
        ch = ch_idx + 1
        for v in range(1, count + 1):
            expected.append((ch, v))

    # Extract verse items
    verse_indices = []
    for i, item in enumerate(items):
        if item[0] == 'verse':
            verse_indices.append(i)

    print(f"File has {len(verse_indices)} verses, expected {len(expected)}")

    # Match each verse to expected position using Brenton overlap
    assignments = {}
    exp_ptr = 0

    for vi, item_idx in enumerate(verse_indices):
        item = items[item_idx]
        _, orig_ch, orig_v, text = item

        if exp_ptr >= len(expected):
            print(f"WARNING: Extra verse at item {item_idx}: HOS.{orig_ch}:{orig_v}")
            continue

        # Try matching current position and a few alternatives
        best_idx = exp_ptr
        best_score = -1.0

        # Search window: try current position and up to 3 ahead
        for try_offset in range(min(4, len(expected) - exp_ptr)):
            try_ch, try_v = expected[exp_ptr + try_offset]
            brenton_key = osb_to_brenton.get((try_ch, try_v))
            if brenton_key and brenton_key in brenton_ref:
                brent_text = brenton_ref[brenton_key]
                score = word_overlap_score(text, brent_text)
                if score > best_score:
                    best_score = score
                    best_idx = exp_ptr + try_offset

        match_ch, match_v = expected[best_idx]
        assignments[item_idx] = (match_ch, match_v)

        if best_score < 0.25:
            brenton_key = osb_to_brenton.get((match_ch, match_v))
            brent_text = brenton_ref.get(brenton_key, "N/A") if brenton_key else "N/A"
            print(f"  LOW ({best_score:.2f}): HOS.{orig_ch}:{orig_v} -> HOS.{match_ch}:{match_v}")
            print(f"    OSB:     {text[:80]}")
            print(f"    Brenton: {brent_text[:80]}")

        exp_ptr = best_idx + 1

    return assignments


def rebuild_file(fm_lines, items, assignments, cvc):
    """Rebuild the file with correct chapter:verse assignments."""
    output = []

    # Frontmatter
    for line in fm_lines:
        output.append(line)

    # Build structured verse list with headings
    structured = []
    pending_headings = []

    for i, item in enumerate(items):
        if item[0] == 'heading':
            pending_headings.append(item[3])
        elif item[0] == 'verse' and i in assignments:
            ch, v = assignments[i]
            text = item[3]
            text = fix_split_words(text)
            text = fix_fused_articles(text)
            structured.append({
                'ch': ch, 'v': v, 'text': text,
                'headings': pending_headings[:],
            })
            pending_headings = []
        # Skip blanks, chapter headers, and other lines

    # Output
    current_ch = 0
    for entry in structured:
        ch = entry['ch']
        v = entry['v']
        text = entry['text']

        if ch != current_ch:
            if current_ch > 0:
                output.append('')
            output.append(f'## Chapter {ch}')
            output.append('')
            current_ch = ch

        for h in entry['headings']:
            output.append('')
            output.append(h)
            output.append('')

        output.append(f'HOS.{ch}:{v} {text}')

    output.append('')  # final newline

    return '\n'.join(output)


def compute_checksum(content):
    """Compute SHA-256 of the body (after frontmatter)."""
    # Find body after second ---
    parts = content.split('---', 2)
    if len(parts) >= 3:
        body = parts[2]
    else:
        body = content
    return hashlib.sha256(body.encode('utf-8')).hexdigest()


def main():
    cvc = [11, 23, 5, 19, 15, 11, 16, 14, 17, 15, 12, 14, 16, 9]

    filepath = REPO / "staging" / "validated" / "OT" / "HOS.md"
    brenton_ref = load_brenton()

    print(f"Loaded Brenton reference: {len(brenton_ref)} verses")
    print(f"Expected CVC: {cvc}, total={sum(cvc)}")
    print()

    fm_lines, items = parse_file(filepath)

    # Match
    assignments = match_verses(items, brenton_ref, cvc)
    print(f"\nAssigned {len(assignments)} verses")

    # Verify
    ch_counts = Counter()
    for ch, v in assignments.values():
        ch_counts[ch] += 1

    print("\nChapter counts:")
    all_ok = True
    for ch_idx, expected_count in enumerate(cvc):
        ch = ch_idx + 1
        actual = ch_counts.get(ch, 0)
        status = "OK" if actual == expected_count else f"MISMATCH (expected {expected_count})"
        if actual != expected_count:
            all_ok = False
        print(f"  Ch {ch:2d}: {actual:3d} / {expected_count} {status}")

    # Check for duplicate assignments
    assigned_pairs = list(assignments.values())
    dup_check = Counter(assigned_pairs)
    dups = {k: v for k, v in dup_check.items() if v > 1}
    if dups:
        print(f"\nDUPLICATE assignments: {dups}")
        all_ok = False

    # Check for missing assignments
    all_expected = set()
    for ch_idx, count in enumerate(cvc):
        ch = ch_idx + 1
        for v in range(1, count + 1):
            all_expected.add((ch, v))
    assigned_set = set(assigned_pairs)
    missing = all_expected - assigned_set
    if missing:
        print(f"\nMISSING {len(missing)} verses: {sorted(missing)[:20]}...")
        all_ok = False

    if not all_ok:
        print("\n*** ASSIGNMENT ISSUES DETECTED - review before writing ***")
        resp = input("Write file anyway? (y/n): ").strip().lower()
        if resp != 'y':
            print("Aborted.")
            return

    # Rebuild
    new_content = rebuild_file(fm_lines, items, assignments, cvc)

    # Update checksum in frontmatter
    new_checksum = compute_checksum(new_content)
    new_content = re.sub(
        r'checksum:\s*"[^"]*"',
        f'checksum: "{new_checksum}"',
        new_content
    )

    filepath.write_text(new_content, encoding='utf-8')
    print(f"\nWrote restructured file to {filepath}")
    print(f"New checksum: {new_checksum}")


if __name__ == '__main__':
    main()
