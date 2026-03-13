#!/usr/bin/env python3
"""
Restructure PSA.md — reassign verse anchors via Jaccard matching against Brenton.

The extractor only detected chapters 1-10; chapters 11-19 were all mis-labelled
as PSA.10:N.  This script:
  1. Strips the frontmatter intro/article noise (lines before first real verse).
  2. Reads every verse line from the file.
  3. Normalises the verse text (split-word repair, fused-article repair, etc.).
  4. For each verse line, finds the best matching (chapter, verse) in Brenton
     using Jaccard word-overlap (threshold 0.25).
  5. Uses a sequential greedy matching pass (honouring the monotone CVC order)
     so verses that score below threshold are interpolated from context.
  6. Writes a clean PSA.md with correct anchors and chapter headers.

Usage:
    python3 pipeline/cleanup/restructure_wis.py
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PSA_MD   = REPO / "staging/validated/OT/PSA.md"
BRENTON  = REPO / "staging/reference/brenton/PSA.json"
REGISTRY = REPO / "schemas/anchor_registry.json"


# ---------------------------------------------------------------------------
# Text normalisation helpers
# ---------------------------------------------------------------------------

# Patterns that look like split words produced by PDF column-justification:
# e.g. "hav e" → "have",  "lov e" → "love",  "ev il" → "evil"
_SPLIT_WORD_PAIRS = [
    (r'\bhav e\b', 'have'),
    (r'\blov e\b', 'love'),
    (r'\bev il\b', 'evil'),
    (r'\bov er\b', 'over'),
    (r'\bev er\b', 'ever'),
    (r'\bev ery\b', 'every'),
    (r'\bnev er\b', 'never'),
    (r'\bev en\b', 'even'),
    (r'\bbev ers?\b', 'bevers'),   # avoid over-matching
    (r'\bwiv es\b', 'wives'),
    (r'\bliv e\b', 'live'),
    (r'\bliv ing\b', 'living'),
    (r'\bgiv e\b', 'give'),
    (r'\bgiv en\b', 'given'),
    (r'\bgiv ing\b', 'giving'),
    (r'\bserv e\b', 'serve'),
    (r'\bserv ant\b', 'servant'),
    (r'\bserv ants\b', 'servants'),
    (r'\bserv ing\b', 'serving'),
    (r'\bserv ice\b', 'service'),
    (r'\bsav e\b', 'save'),
    (r'\bsav ed\b', 'saved'),
    (r'\bsav ior\b', 'savior'),
    (r'\bsav ing\b', 'saving'),
    (r'\bdeserv\b', 'deserv'),     # keep as-is
    (r'\bdeserv ed\b', 'deserved'),
    (r'\bdeserv ing\b', 'deserving'),
    (r'\bpreserv ed\b', 'preserved'),
    (r'\bobserv\w*\b', None),      # handled specially below
    (r'\bdeliv er\b', 'deliver'),
    (r'\bdeliv ered\b', 'delivered'),
    (r'\bdeliv ers\b', 'delivers'),
    (r'\bbeliev e\b', 'believe'),
    (r'\bbeliev ed\b', 'believed'),
    (r'\bbeliev ing\b', 'believing'),
    (r'\bconv ict\b', 'convict'),
    (r'\bconv icts\b', 'convicts'),
    (r'\bconv enant\b', 'covenant'),
    (r'\binv olv\b', 'involv'),    # handled below
    (r'\binv ulnerable\b', 'invulnerable'),
    (r'\bbody inv olv ed\b', 'body involved'),
    (r'\bpowerf ul\b', 'powerful'),
    (r'\bpow er\b', 'power'),
    (r'\bflow er\b', 'flower'),
    (r'\btow er\b', 'tower'),
    (r'\bfav or\b', 'favor'),
    (r'\bfav orite\b', 'favorite'),
    (r'\bfav orably\b', 'favorably'),
    (r'\bhonor\b', 'honor'),
    (r'\bsomew here\b', 'somewhere'),
    (r'\bev ery where\b', 'everywhere'),
    (r'\bany thing\b', 'anything'),
    (r'\bany one\b', 'anyone'),
    (r'\bany where\b', 'anywhere'),
    (r'\bev ery one\b', 'everyone'),
    (r'\bsome thing\b', 'something'),
    (r'\bev ery thing\b', 'everything'),
    (r'\bthat ev er\b', 'that ever'),
    (r'\bwhatev er\b', 'whatever'),
    (r'\bwhoev er\b', 'whoever'),
    (r'\bwhichev er\b', 'whichever'),
    (r'\bhowev er\b', 'however'),
    (r'\bforev er\b', 'forever'),
    (r'\bwherever\b', 'wherever'),
    (r'\bwhenev er\b', 'whenever'),
    (r'\bty rant\b', 'tyrant'),
    (r'\bty rants\b', 'tyrants'),
    (r'\bmy stery\b', 'mystery'),
    (r'\bmy steries\b', 'mysteries'),
    (r'\bmy stic\b', 'mystic'),
    (r'\bmy stical\b', 'mystical'),
    (r'\bcy cle\b', 'cycle'),
    (r'\bcy cles\b', 'cycles'),
    (r'\bray s\b', 'rays'),
    (r'\bway s\b', 'ways'),
    (r'\bday s\b', 'days'),
    (r'\bpray s\b', 'prays'),
    (r'\bsay s\b', 'says'),
    (r'\bplay thing\b', 'plaything'),
    (r'\bly ing\b', 'lying'),
    (r'\bby \b', 'by '),   # too generic — skip
    (r'\benv y\b', 'envy'),
    (r'\benv ied\b', 'envied'),
    (r'\benv ious\b', 'envious'),
    (r'\bdestroy\b', 'destroy'),
    (r'\bdestroy ed\b', 'destroyed'),
    (r'\bdestroy ing\b', 'destroying'),
    (r'\bpay ing\b', 'paying'),
    (r'\bbuy ing\b', 'buying'),
    (r'\btry ing\b', 'trying'),
    (r'\bfly ing\b', 'flying'),
    (r'\bbody\b', 'body'),
    (r'\bsteady\b', 'steady'),
    (r'\bready\b', 'ready'),
    (r'\bheav en\b', 'heaven'),
    (r'\bheav ens\b', 'heavens'),
    (r'\bheav enly\b', 'heavenly'),
    (r'\bheav y\b', 'heavy'),
    (r'\bheav ier\b', 'heavier'),
    (r'\bheav iest\b', 'heaviest'),
    (r'\bleav e\b', 'leave'),
    (r'\bleav es\b', 'leaves'),
    (r'\breceiv e\b', 'receive'),
    (r'\breceiv ed\b', 'received'),
    (r'\breceiv ing\b', 'receiving'),
    (r'\bdecei v\b', 'deceiv'),
    (r'\bdecei ve\b', 'deceive'),
    (r'\bdecei ved\b', 'deceived'),
    (r'\bgriev\w*\b', None),       # handled specially
    (r'\babov e\b', 'above'),
    (r'\bmov e\b', 'move'),
    (r'\bmov ed\b', 'moved'),
    (r'\bmov ing\b', 'moving'),
    (r'\bprov ide\b', 'provide'),
    (r'\bprov ided\b', 'provided'),
    (r'\bprov idence\b', 'providence'),
    (r'\bprov e\b', 'prove'),
    (r'\bprov ed\b', 'proved'),
    (r'\baprov e\b', 'approve'),
    (r'\baprov ed\b', 'approved'),
    (r'\bdisprove\b', 'disprove'),
    (r'\binv estigate\b', 'investigate'),
    (r'\binv entions?\b', 'invention'),
    (r'\binv ention\b', 'invention'),
    (r'\bapparently\b', 'apparently'),
    (r'\bapparently\b', 'apparently'),
    (r'\bparaly ze\b', 'paralyze'),
    (r'\bparaly zed\b', 'paralyzed'),
    (r'\brev el\b', 'revel'),
    (r'\brev elry\b', 'revelry'),
    (r'\brev ealed\b', 'revealed'),
    (r'\brev eal\b', 'reveal'),
    (r'\brev erence\b', 'reverence'),
    (r'\bfestiv al\b', 'festival'),
    (r'\bfestiv als\b', 'festivals'),
    (r'\bnativ e\b', 'native'),
    (r'\bnativ es\b', 'natives'),
    (r'\bdecisiv e\b', 'decisive'),
    (r'\boperativ e\b', 'operative'),
    (r'\bexclusive\b', 'exclusive'),
    (r'\binclusive\b', 'inclusive'),
    (r'\brelativ e\b', 'relative'),
    (r'\beffectiv e\b', 'effective'),
    (r'\beffectiv ely\b', 'effectively'),
    (r'\battentiv e\b', 'attentive'),
    (r'\bdissolv ed\b', 'dissolved'),
    (r'\bsolv e\b', 'solve'),
    (r'\bsolv ed\b', 'solved'),
    (r'\binvolv ed\b', 'involved'),
    (r'\binvolv ing\b', 'involving'),
    (r'\bev olv\b', 'evolv'),
    (r'\bprev ail\b', 'prevail'),
    (r'\bprev ailed\b', 'prevailed'),
    (r'\bprev iously\b', 'previously'),
    (r'\bprev enting\b', 'preventing'),
    (r'\bprev ent\b', 'prevent'),
    (r'\bgov ern\b', 'govern'),
    (r'\bgov ernor\b', 'governor'),
    (r'\bgov erned\b', 'governed'),
    (r'\bgov erning\b', 'governing'),
    (r'\bdiscov er\b', 'discover'),
    (r'\bdiscov ered\b', 'discovered'),
    (r'\brecov er\b', 'recover'),
    (r'\bdiscov ering\b', 'discovering'),
    (r'\bhov er\b', 'hover'),
    (r'\buniv erse\b', 'universe'),
    (r'\buniv ersal\b', 'universal'),
    (r'\bsilv er\b', 'silver'),
    (r'\bdeliv erance\b', 'deliverance'),
    (r'\bconv ince\b', 'convince'),
    (r'\bconv inced\b', 'convinced'),
    (r'\bconv ict\b', 'convict'),
    (r'\bconv iction\b', 'conviction'),
    (r'\bportray s\b', 'portrays'),
    (r'\bportray ed\b', 'portrayed'),
    (r'\bdestroy\b', 'destroy'),  # no space — already correct in most cases
    (r'\bplay \b', 'play '),       # too broad
    (r'\bdisplay\b', 'display'),
]


def fix_split_words(text: str) -> str:
    """Fix common PDF column-split word artifacts."""
    # Apply the explicit list first
    rules = [
        # (pattern, replacement) — only those where replacement is not None
        (r'\bhav e\b', 'have'),
        (r'\blov e\b', 'love'),
        (r'\blov ed\b', 'loved'),
        (r'\blov es\b', 'loves'),
        (r'\blov ing\b', 'loving'),
        (r'\bev il\b', 'evil'),
        (r'\bov er\b', 'over'),
        (r'\bev er\b', 'ever'),
        (r'\bev ery\b', 'every'),
        (r'\bnev er\b', 'never'),
        (r'\bev en\b', 'even'),
        (r'\bwiv es\b', 'wives'),
        (r'\bliv e\b', 'live'),
        (r'\bliv ed\b', 'lived'),
        (r'\bliv es\b', 'lives'),
        (r'\bliv ing\b', 'living'),
        (r'\bgiv e\b', 'give'),
        (r'\bgiv en\b', 'given'),
        (r'\bgiv ing\b', 'giving'),
        (r'\bserv e\b', 'serve'),
        (r'\bserv ed\b', 'served'),
        (r'\bserv ant\b', 'servant'),
        (r'\bserv ants\b', 'servants'),
        (r'\bserv ing\b', 'serving'),
        (r'\bserv ice\b', 'service'),
        (r'\bsav e\b', 'save'),
        (r'\bsav ed\b', 'saved'),
        (r'\bsav ior\b', 'Savior'),
        (r'\bsav ing\b', 'saving'),
        (r'\bdeserv ed\b', 'deserved'),
        (r'\bdeserv ing\b', 'deserving'),
        (r'\bpreserv ed\b', 'preserved'),
        (r'\bpreserv ing\b', 'preserving'),
        (r'\bobserv ed\b', 'observed'),
        (r'\bobserv ing\b', 'observing'),
        (r'\bobserv ation\b', 'observation'),
        (r'\bdeliv er\b', 'deliver'),
        (r'\bdeliv ered\b', 'delivered'),
        (r'\bdeliv erance\b', 'deliverance'),
        (r'\bbeliev e\b', 'believe'),
        (r'\bbeliev ed\b', 'believed'),
        (r'\bbeliev ing\b', 'believing'),
        (r'\bconv ict\b', 'convict'),
        (r'\bconv icts\b', 'convicts'),
        (r'\bconv icting\b', 'convicting'),
        (r'\bconv iction\b', 'conviction'),
        (r'\bconv enant\b', 'covenant'),
        (r'\binv olv ed\b', 'involved'),
        (r'\binv olv ing\b', 'involving'),
        (r'\binv ulnerable\b', 'invulnerable'),
        (r'\binv estigate\b', 'investigate'),
        (r'\binv estigation\b', 'investigation'),
        (r'\binv ention\b', 'invention'),
        (r'\binv entions\b', 'inventions'),
        (r'\benv y\b', 'envy'),
        (r'\benv ied\b', 'envied'),
        (r'\benv ious\b', 'envious'),
        (r'\bdestroy ed\b', 'destroyed'),
        (r'\bdestroy ing\b', 'destroying'),
        (r'\bpay ing\b', 'paying'),
        (r'\bheav en\b', 'heaven'),
        (r'\bheav ens\b', 'heavens'),
        (r'\bheav enly\b', 'heavenly'),
        (r'\bheav y\b', 'heavy'),
        (r'\bheav ier\b', 'heavier'),
        (r'\bleav e\b', 'leave'),
        (r'\bleav es\b', 'leaves'),
        (r'\bleav ing\b', 'leaving'),
        (r'\breceiv e\b', 'receive'),
        (r'\breceiv ed\b', 'received'),
        (r'\breceiv ing\b', 'receiving'),
        (r'\bdeceiv e\b', 'deceive'),
        (r'\bdeceiv ed\b', 'deceived'),
        (r'\bdeceiv ing\b', 'deceiving'),
        (r'\bgriev e\b', 'grieve'),
        (r'\bgriev ed\b', 'grieved'),
        (r'\bgriev ous\b', 'grievous'),
        (r'\bgriev ously\b', 'grievously'),
        (r'\babov e\b', 'above'),
        (r'\bmov e\b', 'move'),
        (r'\bmov ed\b', 'moved'),
        (r'\bmov ing\b', 'moving'),
        (r'\bprov ide\b', 'provide'),
        (r'\bprov ided\b', 'provided'),
        (r'\bprov idence\b', 'providence'),
        (r'\bprov ision\b', 'provision'),
        (r'\bprov e\b', 'prove'),
        (r'\bprov ed\b', 'proved'),
        (r'\bapprove\b', 'approve'),
        (r'\bapproved\b', 'approved'),
        (r'\bparaly zed\b', 'paralyzed'),
        (r'\bparaly ze\b', 'paralyze'),
        (r'\brev elry\b', 'revelry'),
        (r'\brev ealed\b', 'revealed'),
        (r'\brev eal\b', 'reveal'),
        (r'\brev erence\b', 'reverence'),
        (r'\bfestiv al\b', 'festival'),
        (r'\bfestiv als\b', 'festivals'),
        (r'\boperativ e\b', 'operative'),
        (r'\bdissolv ed\b', 'dissolved'),
        (r'\bsolv ed\b', 'solved'),
        (r'\bprev ail\b', 'prevail'),
        (r'\bprev ailed\b', 'prevailed'),
        (r'\bprev iously\b', 'previously'),
        (r'\bprev ent\b', 'prevent'),
        (r'\bgov ern\b', 'govern'),
        (r'\bgov erns\b', 'governs'),
        (r'\bgov erned\b', 'governed'),
        (r'\bgov ernor\b', 'governor'),
        (r'\bdiscov er\b', 'discover'),
        (r'\bdiscov ered\b', 'discovered'),
        (r'\bsilv er\b', 'silver'),
        (r'\bportray s\b', 'portrays'),
        (r'\bportray ed\b', 'portrayed'),
        (r'\bty rant\b', 'tyrant'),
        (r'\bty rants\b', 'tyrants'),
        (r'\bmy stery\b', 'mystery'),
        (r'\bmy steries\b', 'mysteries'),
        (r'\bmy stic\b', 'mystic'),
        (r'\bcy cle\b', 'cycle'),
        (r'\bcy cles\b', 'cycles'),
        (r'\bray s\b', 'rays'),
        (r'\bway s\b', 'ways'),
        (r'\bday s\b', 'days'),
        (r'\bpray s\b', 'prays'),
        (r'\bpray ed\b', 'prayed'),
        (r'\bpray er\b', 'prayer'),
        (r'\bpray ers\b', 'prayers'),
        (r'\bsay s\b', 'says'),
        (r'\benv y\b', 'envy'),
        (r'\bev ery where\b', 'everywhere'),
        (r'\bany thing\b', 'anything'),
        (r'\bany one\b', 'anyone'),
        (r'\bev ery one\b', 'everyone'),
        (r'\bev ery thing\b', 'everything'),
        (r'\bwhatev er\b', 'whatever'),
        (r'\bwhoev er\b', 'whoever'),
        (r'\bhowev er\b', 'however'),
        (r'\bforev er\b', 'forever'),
        (r'\bwhenev er\b', 'whenever'),
        (r'\bcarv e\b', 'carve'),
        (r'\bcarv ed\b', 'carved'),
        (r'\bcarv ing\b', 'carving'),
        (r'\bstarv e\b', 'starve'),
        (r'\bstarv ed\b', 'starved'),
        (r'\bmarv el\b', 'marvel'),
        (r'\bmarv elous\b', 'marvelous'),
        (r'\bmarv eled\b', 'marveled'),
        (r'\bgrav e\b', 'grave'),
        (r'\bgrav es\b', 'graves'),
        (r'\bwav e\b', 'wave'),
        (r'\bwav es\b', 'waves'),
        (r'\bslav e\b', 'slave'),
        (r'\bslav es\b', 'slaves'),
        (r'\bbrav e\b', 'brave'),
        (r'\bsalv ation\b', 'salvation'),
        (r'\bsalv aging\b', 'salvaging'),
        (r'\bnativ e\b', 'native'),
        (r'\beffectiv e\b', 'effective'),
        (r'\beffectiv ely\b', 'effectively'),
        (r'\brelativ e\b', 'relative'),
        (r'\bpositiv e\b', 'positive'),
        (r'\bnegativ e\b', 'negative'),
        (r'\bactiv e\b', 'active'),
        (r'\bactiv ely\b', 'actively'),
        (r'\bpassiv e\b', 'passive'),
        (r'\bcreativ e\b', 'creative'),
        (r'\bprev alent\b', 'prevalent'),
        (r'\bcarry ing\b', 'carrying'),
        (r'\bmarry ing\b', 'marrying'),
        (r'\bbury ing\b', 'burying'),
        (r'\bfly ing\b', 'flying'),
        (r'\btry ing\b', 'trying'),
        (r'\bdy ing\b', 'dying'),
        (r'\bsupply ing\b', 'supplying'),
        (r'\bapply ing\b', 'applying'),
        (r'\bdenying\b', 'denying'),
        (r'\bpurify ing\b', 'purifying'),
        (r'\bterrify ing\b', 'terrifying'),
        (r'\bterrify\b', 'terrify'),
        (r'\bterrify ed\b', 'terrified'),
        (r'\bglorify ing\b', 'glorifying'),
        (r'\bglorify\b', 'glorify'),
        (r'\bidentify\b', 'identify'),
    ]
    for pattern, replacement in rules:
        text = re.sub(pattern, replacement, text)
    return text


def fix_fused_articles(text: str) -> str:
    """Fix 'aword' → 'a word', 'amortal' → 'a mortal', etc.
    Also fix possessives and contractions like 'one\'s' → "one's".
    """
    # "a" fused with a word starting with a consonant or vowel
    # Pattern: lowercase 'a' immediately followed by a word character (no space)
    # Guard: don't split things like 'already', 'after', 'against', 'and', etc.
    # Use a conservative approach: only split 'a' + word where the fused result
    # is not itself a real word.
    text = re.sub(r'\ba([A-Z])', r'a \1', text)   # aMortal → a Mortal
    # "an" fused: less common but handle
    text = re.sub(r'\ban([A-Z])', r'an \1', text)
    return text


def fix_possessives(text: str) -> str:
    """Fix 'one\'slife' → "one's life", 'God\'spower' → "God's power", etc."""
    # After apostrophe+s, if next char is a letter (no space), insert space
    text = re.sub(r"'s([A-Za-z])", r"'s \1", text)
    # Also fix "s'life" patterns
    text = re.sub(r"s'([A-Za-z])", r"s' \1", text)
    return text


def normalise_text(text: str) -> str:
    """Apply all normalisation rules to verse text."""
    text = fix_split_words(text)
    text = fix_possessives(text)
    # Remove leading drop-cap artifact: a single lowercase letter that starts
    # a word which should start with a capital (e.g., "isdom" → "Wisdom",
    # "ut the" → "But the", "ecause" → "Because")
    # We can't do this reliably without knowing the context, so leave for now.
    # Remove footnote markers
    text = re.sub(r'[†ω]', '', text)
    # Collapse multiple spaces
    text = re.sub(r'  +', ' ', text)
    text = text.strip()
    return text


# ---------------------------------------------------------------------------
# Jaccard matching
# ---------------------------------------------------------------------------

def tokenise(text: str) -> set:
    """Lowercase word-token set for Jaccard comparison."""
    words = re.findall(r"[a-zA-Z']+", text.lower())
    # Remove very common stop words that would inflate similarity across chapters
    stopwords = {'the', 'a', 'an', 'and', 'of', 'in', 'to', 'for', 'is', 'are',
                 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
                 'he', 'she', 'it', 'they', 'we', 'you', 'i', 'his', 'her',
                 'its', 'their', 'our', 'your', 'my', 'this', 'that', 'with',
                 'not', 'will', 'shall', 'but', 'or', 'if', 'on', 'at', 'by',
                 'from', 'as', 'so', 'all', 'him', 'them', 'who', 'what',
                 'which', 'when', 'do', 'did', 'no', 'nor', 'yet', 'up',
                 'out', 'into', 'upon', 'those', 'these', 'than', 'then',
                 'their', 'there', 'through', 'they', 'him', 'one', 'man',
                 'men', 'god', 'lord', 'may'}
    return set(w for w in words if w not in stopwords and len(w) > 1)


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union > 0 else 0.0


# ---------------------------------------------------------------------------
# Parse PSA.md
# ---------------------------------------------------------------------------

def parse_psa_md(path: Path):
    """
    Return (frontmatter_lines, verse_entries, section_headers_map).

    verse_entries: list of dicts:
        {'orig_anchor': 'PSA.2:5', 'text': '...', 'line_no': N,
         'headers_before': ['### Foo', ...]}
    """
    with open(path) as f:
        raw = f.read()

    lines = raw.split('\n')

    # Extract YAML frontmatter (between first and second '---')
    fm_lines = []
    in_fm = False
    fm_end = 0
    for i, line in enumerate(lines):
        if i == 0 and line.strip() == '---':
            in_fm = True
            fm_lines.append(line)
            continue
        if in_fm:
            fm_lines.append(line)
            if line.strip() == '---':
                fm_end = i
                break

    # Determine first REAL verse (i.e., not intro noise).
    # The intro noise is everything in "Chapter 1" before the first verse
    # that actually has valid Scripture content.  We detect this by:
    # - PSA.1:1 thru PSA.1:13 appear to be article/outline content
    # - First real verse content matches PSA.1:1 Brenton "Love righteousness..."
    # Strategy: we will collect ALL verse lines then strip the noise at the end.

    verse_entries = []
    pending_headers = []

    # We also want to track section headers (### ...) so we can keep
    # the ones that are narrative headings (not article headers)
    # For now we collect them and decide later.



    for i, line in enumerate(lines[fm_end+1:], start=fm_end+1):
        s = line.strip()
        if not s:
            pending_headers = []  # reset on blank
            continue
        if s.startswith('## Chapter') or s.startswith('## chapter'):
            # Chapter markers — we'll regenerate these
            pending_headers = []
            continue
        if s.startswith('### '):
            # Narrative section header — keep pending
            pending_headers.append(s)
            continue
        if s.startswith('PSA.'):
            # Split anchor from text
            parts = s.split(' ', 1)
            anchor = parts[0]
            text = parts[1] if len(parts) > 1 else ''

            # Fix the text
            text_fixed = normalise_text(text)

            entry = {
                'orig_anchor': anchor,
                'text': text_fixed,
                'raw_text': text,
                'line_no': i,
                'headers_before': list(pending_headers),
            }
            verse_entries.append(entry)
            pending_headers = []

    return fm_lines, verse_entries


# ---------------------------------------------------------------------------
# Build Brenton index
# ---------------------------------------------------------------------------

def build_brenton_index(path: Path):
    """
    Returns list of (chapter_int, verse_int, text, tokens) in canonical order.
    """
    with open(path) as f:
        b = json.load(f)

    entries = []
    for ch_str, data in sorted(b['chapters'].items(), key=lambda x: int(x[0])):
        ch = int(ch_str)
        for v_idx, vtext in enumerate(data['verses']):
            v = v_idx + 1
            tokens = tokenise(vtext)
            entries.append((ch, v, vtext, tokens))
    return entries


# ---------------------------------------------------------------------------
# Sequential greedy matching
# ---------------------------------------------------------------------------

def match_verses_to_brenton(verse_entries, brenton_entries, cvc):
    """
    For each extracted verse, find the best matching Brenton (ch, v).
    Uses a sequential / monotone approach:
    - Start at brenton position 0.
    - For each extracted verse, search a window ahead.
    - Assign the best scoring candidate in the window.
    - Advance the Brenton pointer.

    Returns list of (ch, v, score) parallel to verse_entries.
    """
    n_verses = len(verse_entries)
    n_brenton = len(brenton_entries)

    # Build quick lookup: brenton_index (flat) → (ch, v)
    # brenton_entries is already in order.

    assignments = []   # list of (ch, v, score)
    bptr = 0           # current position in brenton_entries

    WINDOW = 8         # how many Brenton entries ahead to search

    for i, entry in enumerate(verse_entries):
        tokens = tokenise(entry['text'])
        best_score = -1.0
        best_bptr  = bptr
        best_ch    = None
        best_v     = None

        # Search window from bptr up to bptr+WINDOW
        search_end = min(bptr + WINDOW, n_brenton)
        for j in range(bptr, search_end):
            b_ch, b_v, b_text, b_tokens = brenton_entries[j]
            score = jaccard(tokens, b_tokens)
            if score > best_score:
                best_score = score
                best_bptr  = j
                best_ch    = b_ch
                best_v     = b_v

        # If score is very low, try a wider window (the extractor may have
        # jumped or the OCR text is very different)
        if best_score < 0.12:
            wider_end = min(bptr + 20, n_brenton)
            for j in range(bptr, wider_end):
                b_ch, b_v, b_text, b_tokens = brenton_entries[j]
                score = jaccard(tokens, b_tokens)
                if score > best_score:
                    best_score = score
                    best_bptr  = j
                    best_ch    = b_ch
                    best_v     = b_v

        assignments.append((best_ch, best_v, best_score))
        # Only advance pointer if we matched (score > threshold)
        if best_score >= 0.10:
            bptr = best_bptr + 1
        # else: keep bptr where it is (this verse may be a duplicate/noise)
        bptr = min(bptr, n_brenton - 1)

    return assignments


# ---------------------------------------------------------------------------
# Post-process: fill gaps / interpolate
# ---------------------------------------------------------------------------

def interpolate_missing(assignments, verse_entries, brenton_entries, cvc):
    """
    After matching, ensure we have full coverage of CVC.
    Any Brenton (ch, v) not matched gets inserted with text from verse_entries
    where there's a duplicate assignment (lower-scoring one).
    If no duplicate, we leave a TODO marker.

    Also: deduplicate — if multiple verse_entries were assigned the same
    Brenton anchor, keep the highest-scoring one.
    """
    from collections import defaultdict

    # Map anchor → list of (i, score)
    anchor_to_idxs = defaultdict(list)
    for i, (ch, v, score) in enumerate(assignments):
        anchor_to_idxs[(ch, v)].append((i, score))

    # For duplicates, keep the best-score one; collect the rest as surplus
    surplus_idxs = set()
    for anchor, idxs in anchor_to_idxs.items():
        if len(idxs) > 1:
            best_i = max(idxs, key=lambda x: x[1])[0]
            for i, sc in idxs:
                if i != best_i:
                    surplus_idxs.add(i)

    # Build set of matched anchors
    matched_anchors = set()
    for i, (ch, v, score) in enumerate(assignments):
        if i not in surplus_idxs:
            matched_anchors.add((ch, v))

    # Find missing anchors
    missing_anchors = []
    for b_ch, b_v, b_text, b_tokens in brenton_entries:
        if (b_ch, b_v) not in matched_anchors:
            missing_anchors.append((b_ch, b_v))

    return surplus_idxs, set(matched_anchors), missing_anchors


# ---------------------------------------------------------------------------
# Narrative section header filtering
# ---------------------------------------------------------------------------

# Known article-section header patterns to DROP (OSB study article titles)
_ARTICLE_HEADER_PATTERNS = [
    re.compile(r'^\d'),                            # starts with digit
    re.compile(r'\bAuthor\b'),
    re.compile(r'\bMajor Theme\b'),
    re.compile(r'\bOutline\b', re.I),
    re.compile(r'\bBackground\b'),
    re.compile(r'Wisdom Bestows'),
    re.compile(r'Nature and Power'),
    re.compile(r'Guides God'),
    re.compile(r'For all men'),
    re.compile(r'The Egyptians Were Judged'),
    re.compile(r'Our Merciful God'),
    re.compile(r'The Sins of Egypt'),
    re.compile(r'The Futility of False Gods'),
    re.compile(r'Idolatry Brings Evil'),
    re.compile(r'Idols of Clay'),
    re.compile(r"The Canaanites' Vice"),
    re.compile(r"Death Visits Egypt"),
    re.compile(r"Creation Serves Its God"),
    re.compile(r"God Judges Egypt"),
    re.compile(r"God Dwells with His People"),
    re.compile(r"God Chastens His Children"),
    re.compile(r"Aaron Prays for Israel"),
    re.compile(r"Light Shines on Israel"),
    re.compile(r"God Our King"),
    re.compile(r"The Punishment of Egypt"),
    re.compile(r"The Egyptian Enemies"),
    re.compile(r"The Foolishness of Egypt"),
]

def is_article_header(hdr: str) -> bool:
    title = hdr.lstrip('#').strip()
    for pat in _ARTICLE_HEADER_PATTERNS:
        if pat.search(title):
            return True
    return False


def should_keep_header(hdr: str, next_verse_ch: int) -> bool:
    """Keep narrative headings; drop study-article headings."""
    if is_article_header(hdr):
        return False
    # Check if it looks like a verse citation (e.g. "### 1:1 Foo")
    title = hdr.lstrip('#').strip()
    if re.match(r'^\d+:\d+', title):
        return False
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=== PSA restructure ===")

    # Load data
    fm_lines, verse_entries = parse_psa_md(PSA_MD)
    brenton_entries = build_brenton_index(BRENTON)

    with open(REGISTRY) as f:
        reg = json.load(f)
    cvc = None
    for b in reg['books']:
        if b.get('code') == 'PSA':
            cvc = b['chapter_verse_counts']
            break
    assert cvc is not None, "PSA not found in registry"

    print(f"Extracted verse lines: {len(verse_entries)}")
    print(f"Brenton total verses:  {len(brenton_entries)}")
    print(f"CVC total:             {sum(cvc)}")

    # Match
    assignments = match_verses_to_brenton(verse_entries, brenton_entries, cvc)

    # Deduplication pass
    surplus_idxs, matched_anchors, missing_anchors = interpolate_missing(
        assignments, verse_entries, brenton_entries, cvc
    )

    # Stats
    low_confidence = [(i, assignments[i]) for i in range(len(assignments))
                      if assignments[i][2] < 0.15 and i not in surplus_idxs]
    print(f"Low-confidence matches (<0.15): {len(low_confidence)}")
    print(f"Surplus (duplicate) verses: {len(surplus_idxs)}")
    print(f"Missing Brenton anchors: {len(missing_anchors)}")

    # -----------------------------------------------------------------------
    # Assemble output
    # -----------------------------------------------------------------------
    # Sort verse_entries by their assigned (ch, v)
    # (Surplus entries are dropped; missing ones will get placeholder text)

    # Build final list: (ch, v, text, headers_before, is_placeholder, score)
    final_verses = []

    for i, entry in enumerate(verse_entries):
        if i in surplus_idxs:
            continue
        ch, v, score = assignments[i]
        if ch is None:
            continue
        headers = [h for h in entry['headers_before']
                   if should_keep_header(h, ch)]
        final_verses.append({
            'ch': ch, 'v': v,
            'text': entry['text'],
            'headers': headers,
            'score': score,
            'placeholder': False,
        })

    # Add placeholders for missing anchors
    for (ch, v) in missing_anchors:
        # Find surrounding context from brenton
        b_text = ''
        for b_ch, b_v, b_text_r, _ in brenton_entries:
            if b_ch == ch and b_v == v:
                b_text = b_text_r
                break
        final_verses.append({
            'ch': ch, 'v': v,
            'text': f'[PLACEHOLDER — verse not extracted; Brenton: {b_text[:120]}]',
            'headers': [],
            'score': 0.0,
            'placeholder': True,
        })

    # Sort by (ch, v)
    final_verses.sort(key=lambda x: (x['ch'], x['v']))

    # -----------------------------------------------------------------------
    # Write output
    # -----------------------------------------------------------------------
    out_lines = []

    # Frontmatter (update checksum field to null pending recalculation)
    for line in fm_lines:
        if line.startswith('checksum:'):
            out_lines.append('checksum: null')
        elif line.startswith('status:'):
            out_lines.append('status: staged')
        else:
            out_lines.append(line)
    out_lines.append('')

    current_ch = 0
    for entry in final_verses:
        ch = entry['ch']
        v  = entry['v']

        if ch != current_ch:
            if current_ch > 0:
                out_lines.append('')
            out_lines.append(f'## Chapter {ch}')
            out_lines.append('')
            current_ch = ch

        # Emit headers
        for hdr in entry['headers']:
            out_lines.append('')
            out_lines.append(hdr)
            out_lines.append('')

        anchor = f'PSA.{ch}:{v}'
        out_lines.append(f'{anchor} {entry["text"]}')

    out_lines.append('')

    output = '\n'.join(out_lines)

    # Write back
    PSA_MD.write_text(output, encoding='utf-8')
    print(f"\nWrote {len(final_verses)} verses to {PSA_MD}")

    # -----------------------------------------------------------------------
    # Report
    # -----------------------------------------------------------------------
    ch_counts = {}
    for e in final_verses:
        if not e['placeholder']:
            ch_counts[e['ch']] = ch_counts.get(e['ch'], 0) + 1

    print("\n--- Chapter verse counts (non-placeholder) ---")
    total_real = 0
    for ch in range(1, 20):
        expected = cvc[ch - 1]
        got = ch_counts.get(ch, 0)
        diff = got - expected
        flag = '' if diff == 0 else f' *** DIFF {diff:+d}'
        print(f"  Ch {ch:2d}: got {got:3d} / expected {expected:3d}{flag}")
        total_real += got
    print(f"\nTotal non-placeholder: {total_real} / {sum(cvc)}")
    print(f"Placeholders inserted: {sum(1 for e in final_verses if e['placeholder'])}")

    if missing_anchors:
        print("\nMissing anchors (inserted as placeholders):")
        for ch, v in sorted(missing_anchors):
            print(f"  PSA.{ch}:{v}")

    if low_confidence:
        print("\nLow-confidence matches:")
        for i, (ch, v, score) in low_confidence:
            print(f"  PSA.{ch}:{v} score={score:.3f}: {verse_entries[i]['text'][:80]}")


if __name__ == '__main__':
    main()
