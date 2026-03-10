#!/usr/bin/env python3
"""
fix_hos_final.py — Restructure HOS.md with correct chapter assignments.

Uses Brenton overlap matching to identify each verse, maps to OSB versification,
then writes the file with correct HOS.{ch}:{v} anchors.

Also fixes: split words, fused articles, possessive fusions.
"""

import json
import re
import hashlib
from pathlib import Path
from collections import Counter

REPO = Path(__file__).resolve().parent.parent.parent

CVC = [11, 23, 5, 19, 15, 11, 16, 14, 17, 15, 12, 14, 16, 9]  # 197 total


def load_brenton():
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
    return Counter(w.lower() for w in re.findall(r'[A-Za-z]+', text) if len(w) >= 3)


def jaccard(a, b):
    wa, wb = word_bag(a), word_bag(b)
    if not wa or not wb:
        return 0.0
    shared = sum((wa & wb).values())
    total = sum((wa | wb).values())
    return shared / total if total else 0.0


def build_versification():
    """Build OSB<->Brenton versification maps for HOS."""
    o2b, b2o = {}, {}

    # Ch1: OSB 1:1-9 = Brenton 1:1-9; OSB 1:10=Brenton 2:1; OSB 1:11=Brenton 2:2
    for v in range(1, 10):
        o2b[(1, v)] = (1, v)
    o2b[(1, 10)] = (2, 1)
    o2b[(1, 11)] = (2, 2)

    # Ch2: OSB 2:v = Brenton 2:(v+2) for v=1..23
    for v in range(1, 24):
        o2b[(2, v)] = (2, v + 2)

    # Ch3-10: same
    for ch in range(3, 11):
        for v in range(1, CVC[ch - 1] + 1):
            o2b[(ch, v)] = (ch, v)

    # Ch11: OSB 11:1-11 = Brenton 11:1-11; OSB 11:12 = Brenton 12:1
    for v in range(1, 12):
        o2b[(11, v)] = (11, v)
    o2b[(11, 12)] = (12, 1)

    # Ch12: OSB 12:v = Brenton 12:(v+1) for v=1..14
    for v in range(1, 15):
        o2b[(12, v)] = (12, v + 1)

    # Ch13: OSB 13:1-15=Brenton 13:1-15; OSB 13:16=Brenton 14:1
    for v in range(1, 16):
        o2b[(13, v)] = (13, v)
    o2b[(13, 16)] = (14, 1)

    # Ch14: OSB 14:v = Brenton 14:(v+1) for v=1..9
    for v in range(1, 10):
        o2b[(14, v)] = (14, v + 1)

    for ok, bk in o2b.items():
        b2o[bk] = ok
    return o2b, b2o


# ────────── TEXT FIXING ──────────

# Specific split-word replacements (applied as whole-word or context matches)
SPLIT_WORD_FIXES = [
    # "Xv e" patterns where the result should be one word
    # We handle these with specific known patterns instead of a blind regex
    (r'\bhav e\b', 'have'),
    (r'\bgav e\b', 'gave'),
    (r'\bgiv e\b', 'give'),
    (r'\bliv e\b', 'live'),
    (r'\blov e\b', 'love'),
    (r'\bsav e\b', 'save'),
    (r'\bmov e\b', 'move'),
    (r'\bserv e\b', 'serve'),
    (r'\bcov e\b', 'cove'),
    (r'\bbeliev e\b', 'believe'),
    (r'\breciev e\b', 'receive'),
    (r'\breceiv e\b', 'receive'),
    (r'\bdeliv er\b', 'deliver'),
    (r'\bDeliv er\b', 'Deliver'),
    (r'\bsilv er\b', 'silver'),
    (r'\bov er\b', 'over'),
    (r'\bev er\b', 'ever'),
    (r'\bev en\b', 'even'),
    (r'\bev il\b', 'evil'),
    (r'\bev ery\b', 'every'),
    (r'\brev ealed\b', 'revealed'),
    (r'\brev enge\b', 'revenge'),
    (r'\bav enge\b', 'avenge'),
    (r'\bdev our\b', 'devour'),
    (r'\bdev oured\b', 'devoured'),
    (r'\bdev ise\b', 'devise'),
    (r'\bdev ised\b', 'devised'),
    (r'\bfav or\b', 'favor'),
    (r'\bprev ail\b', 'prevail'),
    (r'\bprev ailed\b', 'prevailed'),
    (r'\blov ers\b', 'lovers'),
    (r'\blov ed\b', 'loved'),
    (r'\bliv es\b', 'lives'),
    (r'\bliv ing\b', 'living'),
    (r'\bliv ebefore\b', 'live before'),
    (r'\bliv eand\b', 'live and'),
    (r'\bsav ethem\b', 'save them'),
    (r'\bgiv eto\b', 'give to'),
    (r'\bgiv eme\b', 'give me'),
    (r'\bGiv eme\b', 'Give me'),
    (r'\bGiv eto\b', 'Give to'),
    (r'\bgav eher\b', 'gave her'),
    (r'\bgiv eher\b', 'give her'),
    (r'\bremov e\b', 'remove'),
    (r'\bremov eher\b', 'remove her'),
    (r'\bremov ed\b', 'removed'),
    (r'\bcov er\b', 'cover'),
    (r'\bcov enant\b', 'covenant'),
    (r'\bov ertake\b', 'overtake'),
    (r'\bforev er\b', 'forever'),
    (r'\bwhatsoev er\b', 'whatsoever'),
    (r'\bfestiv als\b', 'festivals'),
    (r'\bfestiv al\b', 'festival'),
    (r'\bstav es\b', 'staves'),
    (r'\badv ersary\b', 'adversary'),
    (r'\breciv e\b', 'receive'),
    (r'\breceiv ethem\b', 'receive them'),
    (r'\breceiv eit\b', 'receive it'),
    (r'\breceiv ethe\b', 'receive the'),
    (r'\breceiv egood\b', 'receive good'),
    (r'\blov ethem\b', 'love them'),
    (r'\bdov e\b', 'dove'),
    (r'\bdov eout\b', 'dove out'),
    (r'\badov eout\b', 'a dove out'),
    (r'\badov e\b', 'a dove'),
    (r'\bSav ior\b', 'Savior'),
    (r'\bbelov ed\b', 'beloved'),
    (r'\bbereav ed\b', 'bereaved'),
    (r'\bdeceiv er\b', 'deceiver'),
    (r'\bbeliev ed\b', 'believed'),
    (r'\bpreserv ed\b', 'preserved'),
    (r'\bobserv emercy\b', 'observe mercy'),
    (r'\bobserv e\b', 'observe'),
    (r'\bserv ed\b', 'served'),
    (r'\bheav en\b', 'heaven'),
    (r'\bgrav en\b', 'graven'),
    (r'\bleav ened\b', 'leavened'),
    (r'\bcalv es\b', 'calves'),
    (r'\btrav ail\b', 'travail'),
    (r'\boliv e\b', 'olive'),
    (r'\boliv etree\b', 'olive tree'),
    (r'\bDiv ision\b', 'Division'),
    (r'\bdiv ision\b', 'division'),
    (r'\bhav ing\b', 'having'),
    (r'\bsav eus\b', 'save us'),
    # Specific fused patterns from HOS
    (r'\bhav emercy\b', 'have mercy'),
    (r'\bhav eno\b', 'have no'),
    (r'\bhav erejected\b', 'have rejected'),
    (r'\bhav eforgotten\b', 'have forgotten'),
    (r'\bhav eabandoned\b', 'have abandoned'),
    (r'\bhav ecompared\b', 'have compared'),
    (r'\bhav ebeen\b', 'have been'),
    (r'\bhav efixed\b', 'have fixed'),
    (r'\bhav eforsaken\b', 'have forsaken'),
    (r'\bhav eshown\b', 'have shown'),
    (r'\bhav enot\b', 'have not'),
    (r'\bhav eturned\b', 'have turned'),
    (r'\bhav ecommitted\b', 'have committed'),
    (r'\bhav eworked\b', 'have worked'),
    (r'\bhav eencircled\b', 'have encircled'),
    (r'\bhav egone\b', 'have gone'),
    (r'\bhav ebecome\b', 'have become'),
    (r'\bhav egiv en\b', 'have given'),
    (r'\bhav ecorrupted\b', 'have corrupted'),
    (r'\bhav esacrificed\b', 'have sacrificed'),
    (r'\bhav eseen\b', 'have seen'),
    (r'\bhav ehidden\b', 'have hidden'),
    (r'\bhav edone\b', 'have done'),
    (r'\bhav esinned\b', 'have sinned'),
    (r'\bhav ecut\b', 'have cut'),
    (r'\bhav eslain\b', 'have slain'),
    (r'\bhav efound\b', 'have found'),
    (r'\bhav emultiplied\b', 'have multiplied'),
    (r'\bhav ehumbled\b', 'have humbled'),
    (r'\bhav ecome\b', 'have come'),
    (r'\bhav ecalled\b', 'have called'),
    (r'\bhav ehoped\b', 'have hoped'),
    (r'\bsav ethem\b', 'save them'),
    (r'\blov eher\b', 'love her'),
    (r'\blov evictory\b', 'love victory'),
    (r'\blov ethem\b', 'love them'),
    (r'\bdev ised\b', 'devised'),
    (r'\bdev ils\b', 'evils'),  # "ev ils" -> "evils"
    (r'\breceiv ed\b', 'received'),
    (r'\bthemselv es\b', 'themselves'),
    (r'\byourselv es\b', 'yourselves'),
    (r'\bmyselv es\b', 'myselves'),
    # Remaining "v space e" that should just collapse
    (r'\bclev er\b', 'clever'),
    (r'\bnev er\b', 'never'),
]

# Other split-word patterns (non v-e)
OTHER_SPLITS = [
    (r'\by ou\b', 'you'),
    (r'\by our\b', 'your'),
    (r'Egy pt', 'Egypt'),
    (r'Assy rians', 'Assyrians'),
    (r'Assy rian', 'Assyrian'),
    (r'Assy ria', 'Assyria'),
    (r'My self\b', 'Myself'),
    (r'say sthe', 'says the'),
    (r'say sing', 'saying'),
    (r'day sof', 'days of'),
    (r'way sof', 'ways of'),
    (r'day s\b', 'days'),
    (r'way s\b', 'ways'),
    (r'\bmy self\b', 'myself'),
    (r'\bly ing\b', 'lying'),
    (r'Sy ria', 'Syria'),
    (r'\bey es\b', 'eyes'),
    (r'\bdestroy ed\b', 'destroyed'),
    (r'\bsso\b', 'so'),
    (r'\bAv en\b', 'Aven'),
    (r'\banaly ze\b', 'analyze'),
    (r'\bheav en\b', 'heaven'),
]

FUSED_ARTICLES = {
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
    'abird': 'a bird', 'adove': 'a dove', 'adoveout': 'a dove out',
    'aleafy': 'a leafy', 'afruitful': 'a fruitful',
    'ashepherd': 'a shepherd', 'aleopard': 'a leopard',
    'aconspiracy': 'a conspiracy', 'adivision': 'a division',
    'atestimony': 'a testimony', 'abalance': 'a balance',
    'acovenant': 'a covenant', 'agift': 'a gift',
    'atwig': 'a twig', 'acrooked': 'a crooked',
    'aword': 'a word', 'awife': 'a wife',
    'aprophet': 'a prophet',
}


def fix_text(text):
    """Apply all text fixes."""
    # First handle the specific "v e" fused patterns (like "hav emercy")
    # These MUST be done before the simple split-word patterns
    for pattern, replacement in SPLIT_WORD_FIXES:
        text = re.sub(pattern, replacement, text)

    # Then handle remaining "v space e" that weren't caught
    # Use a catch-all that just collapses the space for short suffixes
    def catchall_ve(m):
        pre = m.group(1)
        epart = m.group(3)
        if len(epart) <= 4:  # short suffix like "e", "ed", "er", "en"
            return pre + 'v' + epart
        # Longer: insert space after ve
        return pre + 've ' + epart[1:]
    text = re.sub(r'([a-z])(v)\s(e\w*)', catchall_ve, text)

    # Other splits
    for pattern, replacement in OTHER_SPLITS:
        text = re.sub(pattern, replacement, text)

    # Fused articles
    for fw, rpl in FUSED_ARTICLES.items():
        text = re.sub(r'\b' + fw + r'\b', rpl, text)

    # Possessive fusions
    text = re.sub(r"'s([a-z])", r"'s \1", text)

    # Fix "ev il" -> "evil" (this one uses 'v space i' not 'v space e')
    text = re.sub(r'\bev il\b', 'evil', text)
    text = re.sub(r'\bev ils\b', 'evils', text)

    return text


# ────────── MAIN LOGIC ──────────

def main():
    brenton = load_brenton()
    o2b, b2o = build_versification()

    # Build expected OSB sequence
    expected = []
    for ch_idx, count in enumerate(CVC):
        for v in range(1, count + 1):
            expected.append((ch_idx + 1, v))

    # Restore original file first
    print("Restoring original HOS.md from reconstruct script...")
    import importlib.util
    spec = importlib.util.spec_from_file_location("reconstruct", REPO / "pipeline/tools/reconstruct_hos.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    filepath = REPO / "staging" / "validated" / "OT" / "HOS.md"
    original = mod.ORIGINAL_CONTENT.lstrip('\n')
    filepath.write_text(original, encoding='utf-8')
    print("  Restored.")

    # Now parse the original file (HOS.0:N format)
    raw_lines = original.split('\n')
    fm_end = 0
    if raw_lines[0].strip() == '---':
        for i in range(1, len(raw_lines)):
            if raw_lines[i].strip() == '---':
                fm_end = i + 1
                break
    fm_text = '\n'.join(raw_lines[:fm_end])

    verse_re = re.compile(r'^HOS\.0:(\d+)\s(.+)$')
    heading_re = re.compile(r'^(###\s.+)$')

    items = []
    for line in raw_lines[fm_end:]:
        m_v = verse_re.match(line)
        m_h = heading_re.match(line)
        if m_v:
            items.append(('verse', int(m_v.group(1)), m_v.group(2)))
        elif m_h:
            items.append(('heading', 0, m_h.group(1)))

    # Build verse list with headings
    verses = []  # list of dicts: {text, vnum, headings, best_brenton}
    pending_headings = []
    for item in items:
        if item[0] == 'heading':
            pending_headings.append(item[2])
        elif item[0] == 'verse':
            vnum, text = item[1], item[2]
            # Find best Brenton match
            best_bkey, best_score = None, -1
            for bk, bt in brenton.items():
                s = jaccard(text, bt)
                if s > best_score:
                    best_score = s
                    best_bkey = bk
            osb_key = b2o.get(best_bkey, best_bkey) if best_bkey else (0, vnum)
            verses.append({
                'text': text, 'vnum': vnum, 'headings': pending_headings[:],
                'brent_key': best_bkey, 'osb_key': osb_key, 'score': best_score,
            })
            pending_headings = []

    print(f"Parsed {len(verses)} verses from original file")

    # ── Pre-processing: merges and splits ──

    processed = []
    i = 0
    while i < len(verses):
        v = verses[i]

        # Merge: v24 after v23 in ch2 area (tail of Brenton 2:25)
        if v['osb_key'] == (2, 23) and i + 1 < len(verses) and verses[i + 1]['vnum'] == 24:
            v = dict(v)
            v['headings'] = v['headings'] + verses[i + 1]['headings']
            v['text'] += ' ' + verses[i + 1]['text']
            processed.append(v)
            i += 2
            continue

        # Merge: v7 drop after v9 in ch6 area (continuation of 6:9)
        if v['brent_key'] == (6, 9) and i + 1 < len(verses) and verses[i + 1]['vnum'] == 7:
            next_v = verses[i + 1]
            # Verify next is also ch6 content (Shechem murder = Brenton 6:9 tail)
            if 'Shechem' in next_v['text'] or 'murdered' in next_v['text']:
                v = dict(v)
                v['text'] += ' ' + next_v['text']
                processed.append(v)
                i += 2
                continue

        # Split: fused 6:11 + 7:1
        if v['brent_key'] in [(6, 11), (7, 1)] and "'When I have healed Israel" in v['text']:
            split_pos = v['text'].index("'When I have healed Israel")
            text_a = v['text'][:split_pos].strip()
            text_b = v['text'][split_pos:].strip()
            if text_a:
                va = dict(v)
                va['text'] = text_a
                va['brent_key'] = (6, 11)
                va['osb_key'] = (6, 11)
                processed.append(va)
            vb = {
                'text': text_b, 'vnum': 1, 'headings': [],
                'brent_key': (7, 1), 'osb_key': (7, 1), 'score': 0.5,
            }
            processed.append(vb)
            i += 1
            continue

        # Split: fused 13:15 + 14:1 (Brenton numbering)
        if v['brent_key'] == (13, 15) and 'Samaria shall be' in v['text']:
            split_pos = v['text'].index('Samaria shall be')
            text_a = v['text'][:split_pos].strip()
            text_b = v['text'][split_pos:].strip()
            if text_a:
                va = dict(v)
                va['text'] = text_a
                va['brent_key'] = (13, 15)
                va['osb_key'] = (13, 15)
                processed.append(va)
            vb = {
                'text': text_b, 'vnum': 16, 'headings': [],
                'brent_key': (14, 1), 'osb_key': (13, 16), 'score': 0.5,
            }
            processed.append(vb)
            i += 1
            continue

        # Fix: "Israel's Apostasy" heading leak in 8:1
        if v['brent_key'] == (8, 1) and "Israel's Apostasy" in v['text']:
            v = dict(v)
            v['text'] = re.sub(r"^Israel's Apostasy\s*", "", v['text'])

        # Fix: "14 " prefix leak in 13:10
        if v['brent_key'] == (13, 10) and v['text'].startswith('14 '):
            v = dict(v)
            v['text'] = v['text'][3:]

        processed.append(v)
        i += 1

    print(f"After pre-processing: {len(processed)} verses")

    # ── Re-compute Brenton matches after merges/splits ──
    for pv in processed:
        best_bk, best_s = None, -1
        for bk, bt in brenton.items():
            s = jaccard(pv['text'], bt)
            if s > best_s:
                best_s = s
                best_bk = bk
        pv['brent_key'] = best_bk
        pv['osb_key'] = b2o.get(best_bk, best_bk) if best_bk else (0, 0)
        pv['score'] = best_s

    # ── Sequential assignment ──
    assignments = []
    exp_ptr = 0

    for pv in processed:
        if exp_ptr >= len(expected):
            print(f"  OVERFLOW: {pv['text'][:40]}")
            continue

        osb_key = pv['osb_key']
        score = pv['score']

        # Try to find this osb_key in expected, at or after exp_ptr
        target_idx = None
        if score >= 0.20:
            for k in range(exp_ptr, min(exp_ptr + 20, len(expected))):
                if expected[k] == osb_key:
                    target_idx = k
                    break

        # Require higher confidence to skip forward (avoid cascading offset errors)
        if target_idx is not None and target_idx > exp_ptr and score < 0.40:
            target_idx = None  # Low-confidence skip: fall back to sequential

        if target_idx is not None:
            ch, v = expected[target_idx]
            assignments.append((ch, v, pv['text'], pv['headings']))
            exp_ptr = target_idx + 1
        else:
            ch, v = expected[exp_ptr]
            assignments.append((ch, v, pv['text'], pv['headings']))
            exp_ptr += 1

    # ── Verify ──
    print(f"\nAssigned {len(assignments)} verses (expected {sum(CVC)})")
    ch_counts = Counter(ch for ch, v, _, _ in assignments)
    all_ok = True
    for ch_idx, exp in enumerate(CVC):
        ch = ch_idx + 1
        actual = ch_counts.get(ch, 0)
        status = "OK" if actual == exp else f"({actual}/{exp})"
        if actual != exp:
            all_ok = False
        print(f"  Ch {ch:2d}: {actual:3d} / {exp} {status}")

    # Check duplicates
    anchor_c = Counter((ch, v) for ch, v, _, _ in assignments)
    dups = {k: n for k, n in anchor_c.items() if n > 1}
    if dups:
        print(f"\n  DUPLICATE ANCHORS: {dups}")

    # Check missing
    assigned_set = set((ch, v) for ch, v, _, _ in assignments)
    missing = sorted(set(expected) - assigned_set)
    if missing:
        print(f"\n  MISSING {len(missing)} verses: {missing}")

    # ── Write output ──
    output = [fm_text, '']
    current_ch = 0
    for ch, v, text, headings in assignments:
        text = fix_text(text)
        if ch != current_ch:
            if current_ch > 0:
                output.append('')
            output.append(f'## Chapter {ch}')
            output.append('')
            current_ch = ch
        for h in headings:
            output.append('')
            output.append(h)
            output.append('')
        output.append(f'HOS.{ch}:{v} {text}')
    output.append('')

    final = '\n'.join(output)

    # Update checksum
    parts = final.split('---', 2)
    body = parts[2] if len(parts) >= 3 else final
    new_cksum = hashlib.sha256(body.encode('utf-8')).hexdigest()
    final = re.sub(r'checksum:\s*"[^"]*"', f'checksum: "{new_cksum}"', final)

    filepath.write_text(final, encoding='utf-8')
    print(f"\nWrote {filepath}")
    print(f"Checksum: {new_cksum}")
    print(f"Total anchors: {len(assignments)}")

    return all_ok


if __name__ == '__main__':
    import sys
    ok = main()
    sys.exit(0 if ok else 1)
