#!/usr/bin/env python3
"""
Fix ECC.md chapter/verse assignments.
The extractor collapsed chapters 4-12 into chapter 3 due to short chapters.
Uses Jaccard word overlap with Brenton to reassign correct anchors.
"""
import json
import re
import hashlib
from pathlib import Path

REPO = Path("/home/ark/orthodoxphronema")
ECC_MD = REPO / "staging/validated/OT/ECC.md"
BRENTON = REPO / "staging/reference/brenton/ECC.json"
REGISTRY = REPO / "schemas/anchor_registry.json"

# ── helpers ──────────────────────────────────────────────────────────────────

def words(text: str) -> set:
    return set(re.findall(r"[a-zA-Z']+", text.lower()))

def jaccard(a: str, b: str) -> float:
    wa, wb = words(a), words(b)
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)

# ── load resources ────────────────────────────────────────────────────────────

with open(BRENTON) as f:
    bref = json.load(f)

# Build Brenton lookup: (chapter_int, verse_int) -> text
brenton_verses = {}
for ch_str, ch_data in bref["chapters"].items():
    ch = int(ch_str)
    for idx, vtext in enumerate(ch_data["verses"]):
        brenton_verses[(ch, idx + 1)] = vtext

# CVC from registry
with open(REGISTRY) as f:
    reg = json.load(f)
cvc = next(b for b in reg["books"] if b["code"] == "ECC")["chapter_verse_counts"]
print("ECC CVC:", cvc)
print("Total Brenton verses:", len(brenton_verses))

# ── read current ECC.md ───────────────────────────────────────────────────────

raw = ECC_MD.read_text(encoding="utf-8")

# Split front matter and body
fm_match = re.match(r"^(---\n.*?\n---\n)(.*)", raw, re.DOTALL)
if not fm_match:
    raise ValueError("No front matter found")
frontmatter_block = fm_match.group(1)
body = fm_match.group(2)

# ── parse lines ───────────────────────────────────────────────────────────────

class Line:
    def __init__(self, kind, content, orig_anchor=None):
        self.kind = kind        # 'verse', 'heading', 'chapter_header', 'blank'
        self.content = content  # raw text
        self.orig_anchor = orig_anchor  # e.g. 'ECC.3:17'

parsed_lines = []
for raw_line in body.split("\n"):
    line = raw_line.strip()
    if not line:
        parsed_lines.append(Line('blank', ''))
        continue
    if re.match(r'^## Chapter \d+', line):
        parsed_lines.append(Line('chapter_header', line))
        continue
    if line.startswith('### '):
        parsed_lines.append(Line('heading', line))
        continue
    m = re.match(r'^(ECC\.\d+:\d+)\s+(.*)', line)
    if m:
        parsed_lines.append(Line('verse', m.group(2), orig_anchor=m.group(1)))
        continue
    parsed_lines.append(Line('blank', ''))  # discard noise

# ── filter noise verses ────────────────────────────────────────────────────────

NOISE_PATTERNS = [
    r'^\d{3,4}\s*$',
    r'^(I\.|II\.|III\.)',
    r'^Background\s*[-–]',
    r'^Author\s*[-–]',
    r'^Date\s*[-–]',
    r'^Major Theme',
    r'^Outline$',
]

def is_noise(text: str) -> bool:
    t = text.strip()
    for pat in NOISE_PATTERNS:
        if re.search(pat, t):
            return True
    if re.fullmatch(r'\d{2,4}', t.strip()):
        return True
    return False

verse_lines = []
for pl in parsed_lines:
    if pl.kind == 'verse':
        if is_noise(pl.content):
            print(f"  [NOISE] Dropping: {pl.orig_anchor!r} {pl.content[:60]!r}")
        else:
            verse_lines.append(pl)

print(f"\nTotal verse lines to reassign: {len(verse_lines)}")

# ── text normalisation ────────────────────────────────────────────────────────

def fix_fusions(text: str) -> str:
    """Fix specific OCR/column-split fusions. Do NOT use broad article regex."""
    # Known split words – only fix ones that appear exactly as broken forms
    fixes = [
        # Split words with space in middle
        (r'\bforev er\b', 'forever'),
        (r'\bnev er\b', 'never'),
        (r'\bev er\b', 'ever'),
        (r'\bev ery\b', 'every'),
        (r'\bev erything\b', 'everything'),
        (r'\bev ent\b', 'event'),
        (r'\bev en\b', 'even'),
        (r'\bev il\b', 'evil'),
        (r'\bov er\b', 'over'),
        (r'\bov erly\b', 'overly'),
        (r'\bwhat ev er\b', 'whatever'),
        (r'\bwhen ev er\b', 'whenever'),
        (r'\bwhere ev er\b', 'wherever'),
        (r'\bhow ev er\b', 'however'),
        (r'\bwhat so ev er\b', 'whatsoever'),
        (r'\bserv ant\b', 'servant'),
        (r'\bserv ants\b', 'servants'),
        (r'\bsilv er\b', 'silver'),
        (r'\boliv e\b', 'olive'),
        (r'\baliv e\b', 'alive'),
        (r'\bgiv e\b', 'give'),
        (r'\bgiv en\b', 'given'),
        (r'\blov e\b', 'love'),
        (r'\blov ed\b', 'loved'),
        (r'\bliv e\b', 'live'),
        (r'\bliv ing\b', 'living'),
        (r'\bliv es\b', 'lives'),
        (r'\bdepriv e\b', 'deprive'),
        (r'\bpreserv e\b', 'preserve'),
        (r'\bremov e\b', 'remove'),
        (r'\bremov ed\b', 'removed'),
        (r'\bey e\b', 'eye'),
        (r'\bey es\b', 'eyes'),
        (r'\briv ers\b', 'rivers'),
        (r'\bday s\b', 'days'),
        (r'\bway s\b', 'ways'),
        (r'\bsay s\b', 'says'),
        (r'\bdestroy s\b', 'destroys'),
        (r'\bwiv es\b', 'wives'),
        (r'\bkniv es\b', 'knives'),
        (r'\by ou\b', 'you'),
        (r'\by our\b', 'your'),
        (r'\badv antage\b', 'advantage'),
        (r'\badv ice\b', 'advice'),
        (r'\benv y\b', 'envy'),
        (r'\bheav y\b', 'heavy'),
        (r'\bheav en\b', 'heaven'),
        (r'\bheav ens\b', 'heavens'),
        (r'\bknow s\b', 'knows'),
        (r'\bflow s\b', 'flows'),
        (r'\bgrow s\b', 'grows'),
        (r'\bsow s\b', 'sows'),
        (r'\bshow s\b', 'shows'),
        (r'\barriv e\b', 'arrive'),
        (r'\barriv ed\b', 'arrived'),
        (r'\bdev otes\b', 'devotes'),
        (r'\bobserv es\b', 'observes'),
        # No-space fusions (two words run together)
        (r'\bsay sthe\b', 'says the'),
        (r'\bsay sto\b', 'says to'),
        (r'\bhav enot\b', 'have not'),
        (r'\bhav eno\b', 'have no'),
        (r'\bhav ecursed\b', 'have cursed'),
        (r'\bhav esought\b', 'have sought'),
        (r'\bgiv elife\b', 'give life'),
        (r'\bgiv ebirth\b', 'give birth'),
        (r'\bliv ein\b', 'live in'),
        (r'\bey ebe\b', 'eye be'),
        (r'\boliv eoil\b', 'olive oil'),
        (r'\bdestroy shis\b', 'destroys his'),
        (r'\bdestroy smuch\b', 'destroys much'),
        (r'\baday s\b', 'a days'),  # edge case
        (r'\bday sto\b', 'days to'),
        (r'\bway sof\b', 'ways of'),
        (r'\bday sof\b', 'days of'),
        (r'\bday scome\b', 'days come'),
        (r'\bday sbetter\b', 'days better'),
        (r'\bsay sthe\b', 'says the'),
        # Drop-cap first char missing
        (r'^oeverything\b', 'To everything'),
        (r'\boeverything\b', 'To everything'),
        # Possessive/article fused with next word (only fix known cases)
        (r"\bGod'ssight\b", "God's sight"),
        (r"\bGod'swork\b", "God's work"),
        (r"\bGod'sgift\b", "God's gift"),
        (r"\bman'swisdom\b", "man's wisdom"),
        (r"\bman'sheart\b", "man's heart"),
        (r"\bman'seyes\b", "man's eyes"),
        (r"\bone'sspirit\b", "one's spirit"),
        (r"\bone'sdeath\b", "one's death"),
        (r"\bone'sbirth\b", "one's birth"),
        (r"\bking'splace\b", "king's place"),
        (r"\bking'scommandment\b", "king's commandment"),
        (r"\bpoor man'swisdom\b", "poor man's wisdom"),
        # Articles fused (only explicit known patterns, not broad regex)
        (r'\baservant\b', 'a servant'),
        (r'\baseason\b', 'a season'),
        (r'\batime\b', 'a time'),
        (r'\bawise\b', 'a wise'),
        (r'\basenseless\b', 'a senseless'),
        (r'\bamiscarried\b', 'a miscarried'),
        (r'\bapainful\b', 'a painful'),
        (r'\bagreat\b', 'a great'),
        (r'\bageneration\b', 'a generation'),
        (r'\bagood\b', 'a good'),
        (r'\bathreefold\b', 'a threefold'),
        (r'\bahandful\b', 'a handful'),
        (r'\baman\b', 'a man'),
        (r'\bawoman\b', 'a woman'),
        (r'\bastrange\b', 'a strange'),
        (r'\bastranger\b', 'a stranger'),
        (r'\bashadow\b', 'a shadow'),
        (r'\baserpent\b', 'a serpent'),
        (r'\basnare\b', 'a snare'),
        (r'\banet\b', 'a net'),
        (r'\baking\b', 'a king'),
        (r'\baccount\b', 'account'),  # 'a count' not same as 'account'
    ]
    for pattern, replacement in fixes:
        text = re.sub(pattern, replacement, text)
    return text

# ── Brenton matching ──────────────────────────────────────────────────────────

THRESHOLD = 0.25

def best_brenton_match(text: str):
    """Return ((ch, v), score) for best Brenton match."""
    best_score = 0.0
    best_ref = (1, 1)
    for (ch, v), btext in brenton_verses.items():
        s = jaccard(text, btext)
        if s > best_score:
            best_score = s
            best_ref = (ch, v)
    return best_ref, best_score

# ── Sequential assignment with look-ahead ────────────────────────────────────

assignments = []  # list of (ch, v, text, orig_anchor, score)

cursor_ch = 1
cursor_v = 1

def next_expected(ch, v, cvc_list):
    if v < cvc_list[ch - 1]:
        return ch, v + 1
    elif ch < len(cvc_list):
        return ch + 1, 1
    return None

for pl in verse_lines:
    text = pl.content
    (best_ch, best_v), score = best_brenton_match(text)

    if score >= THRESHOLD:
        assignments.append((best_ch, best_v, text, pl.orig_anchor, score))
    else:
        assignments.append((cursor_ch, cursor_v, text, pl.orig_anchor, score))

    assigned_ch, assigned_v = assignments[-1][0], assignments[-1][1]
    nxt = next_expected(assigned_ch, assigned_v, cvc)
    if nxt:
        cursor_ch, cursor_v = nxt

print(f"\nAssignment sample (first 30):")
for ch, v, text, orig, score in assignments[:30]:
    print(f"  {orig} → ECC.{ch}:{v}  score={score:.2f}  {text[:50]!r}")

# ── Detect and resolve duplicates ─────────────────────────────────────────────

from collections import defaultdict
bucket = defaultdict(list)
for ch, v, text, orig, score in assignments:
    bucket[(ch, v)].append((text, orig, score))

dups = {k: v for k, v in bucket.items() if len(v) > 1}
if dups:
    print(f"\nDuplicate anchor assignments ({len(dups)} positions):")
    for k, items in sorted(dups.items()):
        print(f"  ECC.{k[0]}:{k[1]}:")
        for text, orig, score in items:
            print(f"    {orig}  score={score:.2f}  {text[:60]!r}")

seen = {}
deduped = []
for ch, v, text, orig, score in assignments:
    key = (ch, v)
    if key not in seen:
        seen[key] = (ch, v, text, orig, score)
        deduped.append((ch, v, text, orig, score))
    else:
        prev_score = seen[key][4]
        if score > prev_score:
            idx = next(i for i, x in enumerate(deduped) if x[0] == ch and x[1] == v)
            print(f"  [DUP] Replacing ECC.{ch}:{v} (score {prev_score:.2f}→{score:.2f})")
            deduped[idx] = (ch, v, text, orig, score)
            seen[key] = (ch, v, text, orig, score)
        else:
            print(f"  [DUP] Dropping ECC.{ch}:{v} score={score:.2f} (keeping score={prev_score:.2f})")

# Report missing
assigned_set = {(ch, v) for ch, v, *_ in deduped}
missing = []
for ch in range(1, 13):
    for v in range(1, cvc[ch-1] + 1):
        if (ch, v) not in assigned_set:
            missing.append((ch, v))
if missing:
    print(f"\nMissing verses (no OSB assignment): {len(missing)}")
    for ch, v in missing:
        print(f"  ECC.{ch}:{v}")

deduped.sort(key=lambda x: (x[0], x[1]))

# ── Rebuild narrative headings ─────────────────────────────────────────────────

orig_sequence = []
for pl in parsed_lines:
    if pl.kind == 'heading':
        orig_sequence.append(('heading', pl.content))
    elif pl.kind == 'verse' and not is_noise(pl.content):
        orig_sequence.append(('verse', pl.orig_anchor, pl.content))

orig_to_new = {}
for ch, v, text, orig, score in deduped:
    orig_to_new[orig] = (ch, v)

verse_headings = {}
current_headings = []
for item in orig_sequence:
    if item[0] == 'heading':
        current_headings.append(item[1])
    elif item[0] == 'verse':
        orig_anchor = item[1]
        if current_headings:
            verse_headings[orig_anchor] = list(current_headings)
            current_headings = []

# ── Apply text fixes ──────────────────────────────────────────────────────────

fixed_deduped = []
for ch, v, text, orig, score in deduped:
    fixed_text = fix_fusions(text)
    fixed_deduped.append((ch, v, fixed_text, orig, score))

# ── Write output ──────────────────────────────────────────────────────────────

output_lines = []
current_chapter = 0
seen_headings = set()  # Avoid repeated headings at same chapter boundary

for ch, v, text, orig, score in fixed_deduped:
    if ch != current_chapter:
        if current_chapter != 0:
            output_lines.append("")
        output_lines.append(f"## Chapter {ch}")
        output_lines.append("")
        current_chapter = ch
        seen_headings = set()

    # Headings before this verse
    hdgs = verse_headings.get(orig, [])
    for hdg in hdgs:
        if hdg not in seen_headings:
            output_lines.append(hdg)
            output_lines.append("")
            seen_headings.add(hdg)

    output_lines.append(f"ECC.{ch}:{v} {text}")

output_lines.append("")

body_new = "\n".join(output_lines)

# Update checksum
new_checksum = hashlib.sha256(body_new.encode("utf-8")).hexdigest()
fm_updated = re.sub(
    r'^checksum: ".*?"',
    f'checksum: "{new_checksum}"',
    frontmatter_block,
    flags=re.MULTILINE
)

final = fm_updated + "\n" + body_new

ECC_MD.write_text(final, encoding="utf-8")
print(f"\nWrote {len(fixed_deduped)} verses to {ECC_MD}")
print(f"New checksum: {new_checksum}")
print(f"Chapters covered: {sorted(set(ch for ch,*_ in fixed_deduped))}")
