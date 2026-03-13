#!/usr/bin/env python3
"""fix_article_fusing.py — Fix article 'a' fused to next word in NT staging files.

OCR from Docling sometimes fuses the article 'a' with the next word, producing
patterns like 'aloud' (should be 'a loud'), 'athird' (should be 'a third'), etc.

Also fixes standalone stray markers ('a ' or 'b ' floating in text) and other
common OCR artifacts like 'twelvethousand'.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

# Words that look like a+word but are actually real words — NEVER split
REAL_WORDS = {
    'about', 'above', 'abroad', 'absent', 'absorb', 'abstract', 'abundance',
    'abundant', 'accept', 'access', 'accident', 'accomplish', 'according',
    'account', 'accuse', 'accused', 'accuser', 'achieve', 'acknowledge',
    'acquire', 'across', 'act', 'action', 'actual', 'actually', 'add',
    'added', 'addition', 'address', 'adhere', 'adjust', 'administer',
    'administration', 'admire', 'admit', 'adopt', 'adorn', 'adorned',
    'adult', 'adultery', 'advance', 'advantage', 'advent', 'adversary',
    'advice', 'advise', 'affair', 'affect', 'affirm', 'afflict',
    'affliction', 'afford', 'afraid', 'after', 'afternoon', 'afterward',
    'afterwards', 'again', 'against', 'age', 'aged', 'agent', 'agony',
    'agree', 'agreed', 'agreement', 'ahead', 'aid', 'aim', 'air',
    'alas', 'alert', 'alien', 'alike', 'alive', 'all', 'allegiance',
    'allow', 'allowed', 'almost', 'alone', 'along', 'alongside', 'aloud',
    'alphabet', 'already', 'also', 'altar', 'alter', 'although', 'always',
    'amaze', 'amazed', 'amazement', 'ambassador', 'ambition', 'amen',
    'amend', 'amethyst', 'amid', 'among', 'amount', 'ample', 'ancient',
    'and', 'angel', 'anger', 'angry', 'anguish', 'animal', 'ankle',
    'announce', 'announced', 'annual', 'anoint', 'anointed', 'another',
    'answer', 'answered', 'ant', 'anticipate', 'anxious', 'any', 'anyone',
    'anything', 'anywhere', 'apart', 'apostle', 'apostles', 'appeal',
    'appear', 'appearance', 'appeared', 'appetite', 'apple', 'apply',
    'appoint', 'appointed', 'approach', 'appropriate', 'approve', 'are',
    'area', 'argue', 'argument', 'arise', 'ark', 'arm', 'armed',
    'armor', 'arms', 'army', 'arose', 'around', 'arouse', 'arrange',
    'array', 'arrayed', 'arrest', 'arrive', 'arrived', 'arrogance',
    'arrow', 'art', 'article', 'as', 'ascend', 'ascended', 'ascends',
    'ascent', 'ash', 'ashamed', 'ashes', 'aside', 'ask', 'asked',
    'asleep', 'aspect', 'assemble', 'assembled', 'assembly', 'assert',
    'assign', 'assist', 'associate', 'assume', 'assurance', 'assure',
    'astonish', 'astonished', 'astray', 'at', 'ate', 'atmosphere',
    'atone', 'atonement', 'attach', 'attack', 'attain', 'attempt',
    'attend', 'attention', 'attitude', 'attract', 'audience', 'authority',
    'avenge', 'avenged', 'avoid', 'await', 'awake', 'awaken', 'aware',
    'away', 'awe', 'awesome', 'awful', 'awhile', 'axe',
    # b-words
    'back', 'bad', 'bag', 'balance', 'ball', 'ban', 'band', 'bank',
    'banner', 'banquet', 'baptism', 'baptize', 'baptized', 'bar', 'bare',
    'barely', 'barley', 'barn', 'barrel', 'barren', 'barrier', 'base',
    'basic', 'basin', 'basket', 'bat', 'bath', 'bathe', 'battle',
    'bay', 'be', 'beach', 'beam', 'bear', 'beard', 'bearing', 'beast',
    'beat', 'beaten', 'beautiful', 'beauty', 'became', 'because',
    'become', 'bed', 'been', 'beer', 'before', 'beg', 'began', 'beget',
    'beggar', 'begin', 'beginning', 'begotten', 'behalf', 'behave',
    'behavior', 'behead', 'beheaded', 'behind', 'behold', 'being',
    'belief', 'believe', 'believed', 'believer', 'bell', 'belly',
    'belong', 'belongs', 'beloved', 'below', 'belt', 'bend', 'beneath',
    'benefit', 'beside', 'besides', 'best', 'bestow', 'betray',
    'betrayed', 'better', 'between', 'beyond', 'bid', 'big', 'bind',
    'bird', 'birds', 'birth', 'bishop', 'bit', 'bite', 'bitter',
    'black', 'blade', 'blame', 'blameless', 'blank', 'blaspheme',
    'blasphemed', 'blasphemous', 'blasphemy', 'blast', 'blaze', 'bleed',
    'blemish', 'bless', 'blessed', 'blessing', 'blind', 'blinded',
    'block', 'blood', 'bloom', 'blossom', 'blot', 'blow', 'blue',
    'board', 'boast', 'boat', 'body', 'boil', 'bold', 'boldly',
    'boldness', 'bond', 'bondage', 'bone', 'bones', 'book', 'books',
    'border', 'bore', 'born', 'borrow', 'bosom', 'both', 'bother',
    'bottle', 'bottom', 'bottomless', 'bought', 'bound', 'boundary',
    'bow', 'bowl', 'bowls', 'box', 'boy', 'branch', 'branches',
    'brand', 'brass', 'brave', 'breach', 'bread', 'breadth', 'break',
    'breakfast', 'breast', 'breastplate', 'breastplates', 'breath',
    'breathe', 'breed', 'brethren', 'brick', 'bride', 'bridegroom',
    'bridge', 'brief', 'bright', 'brightness', 'brimstone', 'bring',
    'broad', 'broke', 'broken', 'bronze', 'brook', 'brother',
    'brothers', 'brought', 'brow', 'brown', 'bruise', 'brush', 'build',
    'builder', 'building', 'built', 'bull', 'burden', 'burial', 'burn',
    'burned', 'burning', 'burnt', 'burst', 'bury', 'buried', 'bus',
    'bush', 'business', 'busy', 'but', 'buy', 'by',
}

# Article-fused patterns to fix: 'a' + adjective/noun where the result isn't a real word
# These are cases where OCR fused "a" (article) with the next word
# Pattern: word starts with 'a', removing 'a' gives a real word, and the fused form
# is NOT itself a real word
def should_split_article(word: str, prev_word: str) -> bool:
    """Return True if 'a'+rest should be split into 'a rest'."""
    w = word.lower()
    if w in REAL_WORDS:
        return False
    if len(w) < 3:
        return False
    if w[0] != 'a':
        return False
    rest = w[1:]
    # The rest must be a plausible English word
    # Simple heuristic: check if rest starts with consonant cluster or is a known word
    # For now, use a targeted list of known fused patterns found in the corpus
    return False  # disabled - use targeted list instead


# Targeted fused-article patterns found in REV and other NT books
# Format: fused form -> replacement
ARTICLE_FUSED = {
    'aloud': 'a loud',
    'athird': 'a third',
    'awhite': 'a white',
    'ablack': 'a black',
    'apale': 'a pale',
    'astrong': 'a strong',
    'ascroll': 'a scroll',
    'acloud': 'a cloud',
    'athrone': 'a throne',
    'atrumpet': 'a trumpet',
    'agarment': 'a garment',
    'agolden': 'a golden',
    'aflame': 'a flame',
    'asharp': 'a sharp',
    'athief': 'a thief',
    'arainbow': 'a rainbow',
    'asardius': 'a sardius',
    'asea': 'a sea',
    'alion': 'a lion',
    'acalf': 'a calf',
    'aface': 'a face',
    'aman': 'a man',
    'aflying': 'a flying',
    'astar': 'a star',
    'ascorpion': 'a scorpion',
    'avoice': 'a voice',
    'afurnace': 'a furnace',
    'adenarius': 'a denarius',
    'atorch': 'a torch',
    'apair': 'a pair',
    'afourth': 'a fourth',
    'athere': 'a there',  # weird but in REV
    'afig': 'a fig',
    'amighty': 'a mighty',
    'adoor': 'a door',
    'awoman': 'a woman',
    'ascarlet': 'a scarlet',
    'acage': 'a cage',
    'aprison': 'a prison',
    'adwelling': 'a dwelling',
    'adistance': 'a distance',
    'amillstone': 'a millstone',
    'alamp': 'a lamp',
    'astone': 'a stone',
    'abook': 'a book',
    'areed': 'a reed',
    'ameasuring': 'a measuring',
    'asaying': 'a saying',
    'asquare': 'a square',
    'agold': 'a gold',
    'abride': 'a bride',
    'apure': 'a pure',
    'ariver': 'a river',
    'apillar': 'a pillar',
    'arod': 'a rod',
    'asword': 'a sword',
    'amark': 'a mark',
    'atongue': 'a tongue',
    'alamb': 'a lamb',
    'adragon': 'a dragon',
    'amouth': 'a mouth',
    'abear': 'a bear',
    'aleopard': 'a leopard',
    'ablasphemous': 'a blasphemous',
    'abeast': 'a beast',
    'abow': 'a bow',
    'acrown': 'a crown',
    'aplace': 'a place',
    'ashort': 'a short',
    'aflood': 'a flood',
    'agarland': 'a garland',
    'amale': 'a male',
    'afoul': 'a foul',
    'adead': 'a dead',
    'atalent': 'a talent',
    'awhore': 'a whore',  # just in case
    'aharp': 'a harp',
    'arobe': 'a robe',
    'aseal': 'a seal',
    'athousand': 'a thousand',
    'akings': 'a kings',  # actually this might be marker... let me check
    # Likely footnote markers (remove the prefix, don't add 'a')
    'asays': 'says',
    'aprophetess': 'prophetess',
    'asickbed': 'a sickbed',
    'asynagogue': 'a synagogue',
    'astumbling': 'a stumbling',
    'aelders': 'elders',
    'aheard': 'heard',
    'atenth': 'a tenth',
    'afollowed': 'followed',
    'asmall': 'small',
    'asaw': 'saw',
    'aabominable': 'abominable',
    'aan': 'an',
    'alie': 'a lie',
    'aoutside': 'outside',
    'aprophets': 'prophets',
    'afestival': 'a festival',
    'acause': 'a cause',
    'alittle': 'a little',
    'apeople': 'a people',
    'adoes': 'does',
    'amany': 'many',
    'atime': 'a time',
    'acame': 'came',
    'anot': 'not',
    'awill': 'will',
    'aonly': 'only',
    'agood': 'a good',
    'ainto': 'into',
    'ajust': 'a just',
    'awhich': 'which',
    'aword': 'a word',
    'adid': 'did',
    'aday': "a day",
    'abelieving': 'a believing',
    'abut': 'but',
    'bbut': 'but',
    'bdo': 'do',
    'bdid': 'did',
    'bfrom': 'from',
    'bmay': 'may',
    'bseven': 'seven',
    'bbecame': 'became',
    'bput': 'put',
    'bto': 'to',
    'band': 'and',  # only when it appears to be marker+and
    'cshall': 'shall',
    'cmy': 'My',
    'alet': 'let',
    'ashe': 'she',
    'aan': 'an',
    'aare': 'are',
    'ahas': 'has',
    'ahave': 'have',
    'ais': 'is',
    'ait': 'it',
    'awas': 'was',
    'awere': 'were',
    'ayou': 'you',
    'ain': 'in',
    'ato': 'to',
    'awho': 'who',
    'abecause': 'because',
    'abefore': 'before',
    'aname': 'a name',
    'afor': 'for',
    'athat': 'that',
    'athey': 'they',
    'aif': 'if',
    'awhen': 'when',
    'ashall': 'shall',
    'awe': 'we',  # be careful — 'awe' is a real word
    'awith': 'with',
    'bwith': 'with',
    'ahis': 'his',
    'aher': 'her',
    'bher': 'her',
    'aor': 'or',
    'abeing': 'being',
    'aperson': 'a person',
    'anew': 'a new',
    'afew': 'a few',
    'ajasper': 'a jasper',
    'acovering': 'a covering',
    'athis': 'this',
}

# Remove ambiguous entries where context matters
# 'awe' could be the word 'awe' or 'a we' — skip it
# 'band' could be the word 'band' — handle specially
AMBIGUOUS = {'awe', 'band', 'bare', 'bit', 'bore'}

# OCR artifacts to fix
OCR_FIXES = {
    'twelvethousand': 'twelve thousand',
    'haveshed': 'have shed',
    'itwelvethousand': 'i twelve thousand',  # from "Lev itwelvethousand"
}


def fix_line(line: str) -> str:
    """Apply all fixes to a single verse line."""
    if not re.match(r'^[A-Z0-9]+\.\d+:\d+\s', line):
        return line

    # Fix OCR artifacts
    for old, new in OCR_FIXES.items():
        line = line.replace(old, new)

    # Fix article-fused and marker-fused words
    words = line.split(' ')
    new_words = []
    for w in words:
        # Preserve punctuation
        prefix_punct = ''
        suffix_punct = ''
        core = w
        while core and core[0] in "'\"(":
            prefix_punct += core[0]
            core = core[1:]
        while core and core[-1] in ".,;:!?'\")-":
            suffix_punct = core[-1] + suffix_punct
            core = core[1:] if not core[:-1] else core[:-1]

        lower_core = core.lower()
        if lower_core in ARTICLE_FUSED and lower_core not in AMBIGUOUS:
            replacement = ARTICLE_FUSED[lower_core]
            # Preserve original case of first letter if it was uppercase
            if core and core[0].isupper() and replacement and replacement[0].islower():
                # Check if the original fused word started with uppercase
                # e.g., 'Aloud' -> keep as is if it's start of sentence
                pass
            new_words.append(prefix_punct + replacement + suffix_punct)
        elif lower_core in REAL_WORDS or core.lower() in REAL_WORDS:
            new_words.append(w)
        else:
            # Check for standalone stray markers: single 'a' or 'b' before a word
            # These appear as separate tokens already, like "a Lord" where 'a' is stray
            new_words.append(w)

    result = ' '.join(new_words)

    # Fix standalone stray markers: " a " or " b " floating between words
    # Pattern: comma/semicolon + ' a ' or ' b ' + capitalized or lowercase word
    # e.g., "blood, 6 and has made" — already fixed V12
    # e.g., "a Lord" where 'a' is a stray marker before a proper name
    # These are tricky - skip for now as they need manual review

    return result


def process_file(filepath: Path) -> int:
    """Fix all article-fusing in a file. Returns count of lines changed."""
    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()
    fixed = 0
    for i, line in enumerate(lines):
        new_line = fix_line(line)
        if new_line != line:
            lines[i] = new_line
            fixed += 1
    if fixed:
        filepath.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return fixed


def main():
    books = ["MAT", "MRK", "LUK", "JOH", "ACT", "ROM", "1CO", "PHP", "COL", "1PE", "REV"]
    total = 0
    for code in books:
        path = REPO / "staging" / "validated" / "NT" / f"{code}.md"
        if not path.exists():
            continue
        fixed = process_file(path)
        total += fixed
        print(f"  {code}: {fixed} lines fixed")
    print(f"\n  Total: {total} lines fixed")


if __name__ == "__main__":
    main()
