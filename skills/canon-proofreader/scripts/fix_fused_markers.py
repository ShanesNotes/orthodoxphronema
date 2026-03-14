#!/usr/bin/env python3
"""
fix_fused_markers.py — Fix remaining fused footnote markers across all canon books.

Uses a manually curated replacement map for all 211 known fused tokens found by deep_scan.py.
Each token is classified as either:
  - Article "a" insertion: "acrop" → "a crop"
  - Footnote marker strip: "atook" → "took"
  - "b" marker strip: "bside" → "side"
  - False positive: skip

Usage:
    python3 fix_fused_markers.py --scope canon --dry-run
    python3 fix_fused_markers.py --scope canon
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

CANON_OT = Path("canon/OT")
CANON_NT = Path("canon/NT")

# ═══════════════════════════════════════════════════════════════════════════════
# REPLACEMENT MAP: token → replacement
# Classified by examining each token in its verse context.
# ═══════════════════════════════════════════════════════════════════════════════

REPLACEMENTS = {
    # ── STRIP marker (verbs, already-determined words, function words) ──────
    # Past tense / finite verbs
    "aanswered": "answered",
    "aappeared": "appeared",
    "aasked": "asked",
    "abegan": "began",
    "acomplained": "complained",
    "acrowed": "crowed",
    "adesires": "desires",
    "agot": "got",
    "akilled": "killed",
    "amaintaining": "maintaining",
    "areceived": "received",
    "areturned": "returned",
    "astood": "stood",
    "atook": "took",
    "aworshiped": "worshiped",
    "awounded": "wounded",
    # Present tense / imperatives / infinitives
    "aask": "ask",
    "abelieve": "believe",
    "abrings": "brings",
    "acast": "cast",  # "cast out demons" / "cast him into"
    "aexorcise": "exorcise",
    "ahear": "hear",
    "arebuke": "rebuke",
    "arejoice": "rejoice",
    "aremember": "remember",
    "asin": "sin",  # "go and sin no more"
    "awrite": "write",
    # Participles used as main verbs (not adjective before noun)
    "ablessing": "blessing",  # "praising and blessing God"
    "afilled": "filled",  # "became strong, filled with wisdom"
    "atossed": "tossed",  # "tossed by the waves"
    # Function words / adverbs / prepositions / conjunctions
    "aabout": "about",
    "aaway": "away",
    "aboth": "both",
    "adaily": "daily",  # "added to the church daily"
    "aexcept": "except",
    "anor": "nor",
    "aout": "out",  # "Bring out the best robe"
    "athroughout": "throughout",
    "auntil": "until",
    # Possessive/determiner context (another determiner already present)
    "aapostles": "apostles",  # "the twelve apostles"
    "afathers": "fathers",  # "our fathers"
    "afeet": "feet",  # "Jesus' feet"
    "aperplexed": "perplexed",  # "greatly perplexed"
    "awords": "words",  # "blasphemous words"
    "ayour": "your",  # "what hour your Lord"
    # "b" marker
    "bside": "side",  # "on our side"

    # ── ARTICLE "a" insertion (nouns, adjectives before nouns) ──────────────
    "aangels": "angels",  # "the holy aangels" → already has "the", strip marker
    "abaptism": "a baptism",
    "abasket": "a basket",
    "abay": "a bay",
    "abeach": "a beach",
    "abehold": "behold",  # "abehold, Jesus met them" → strip marker
    "abranch": "a branch",
    "abright": "a bright",
    "abush": "a bush",
    "acalm": "a calm",
    "acamel": "a camel",
    "acase": "a case",
    "acatch": "a catch",
    "acertificate": "a certificate",
    "acharge": "a charge",
    "achief": "a chief",
    "acircle": "a circle",
    "acitizen": "a citizen",
    "acolony": "a colony",
    "acommand": "a command",
    "acomplaint": "a complaint",
    "aconscience": "a conscience",
    "aconsultation": "a consultation",
    "aconvenient": "a convenient",
    "acorner": "a corner",
    "acouncil": "a council",
    "acovenant": "a covenant",
    "acreator": "a creator",
    "acripple": "a cripple",
    "acrop": "a crop",
    "acry": "a cry",
    "adazzling": "a dazzling",
    "adecision": "a decision",
    "adelegation": "a delegation",
    "adeliverer": "a deliverer",
    "adeserted": "a deserted",
    "adevil": "a devil",
    "adispute": "a dispute",
    "adissension": "a dissension",
    "aditch": "a ditch",
    "adove": "a dove",
    "adragnet": "a dragnet",
    "adweller": "a dweller",
    "aeunuch": "a eunuch",
    "afaithful": "a faithful",
    "afavor": "a favor",
    "afeast": "a feast",
    "afellow": "a fellow",
    "afever": "a fever",
    "afish": "a fish",
    "afive": "a five",
    "aflow": "a flow",
    "aforeign": "a foreign",
    "afoundation": "a foundation",
    "aghost": "a ghost",
    "agift": "a gift",
    "aglutton": "a glutton",
    "agnat": "a gnat",
    "agod": "a god",
    "agorgeous": "a gorgeous",
    "agrain": "a grain",
    "agreater": "a greater",
    "aguard": "a guard",
    "aguest": "a guest",
    "ahair": "a hair",
    "ahandkerchief": "a handkerchief",
    "ahard": "a hard",
    "aheathen": "a heathen",
    "ahedge": "a hedge",
    "ahelpless": "a helpless",
    "ahen": "a hen",
    "aherd": "a herd",
    "aholy": "a holy",
    "ahundredfold": "a hundredfold",
    "ahusband": "a husband",
    "ahymn": "a hymn",
    "ajourney": "a journey",
    "ajudge": "a judge",
    "ajudgment": "a judgment",
    "aking": "a king",
    "akingdom": "a kingdom",
    "akiss": "a kiss",
    "aknapsack": "a knapsack",
    "alad": "a lad",
    "aland": "a land",
    "alandowner": "a landowner",
    "alaw": "a law",
    "alawyer": "a lawyer",
    "aletter": "a letter",
    "alinen": "a linen",
    "alonger": "a longer",
    "aman": "a man",
    "amarriage": "a marriage",
    "amarvelous": "a marvelous",
    "amatter": "a matter",
    "amemorial": "a memorial",
    "amerchant": "a merchant",
    "amoney": "a money",
    "amultitude": "a multitude",
    "amurderer": "a murderer",
    "amute": "a mute",
    "anation": "a nation",
    "aneedle": "a needle",
    "anoble": "a noble",
    "anotable": "a notable",
    "anotorious": "a notorious",
    "aone": "a one",
    "apillow": "a pillow",
    "apit": "a pit",
    "apitcher": "a pitcher",
    "aplague": "a plague",
    "aplatter": "a platter",
    "apossession": "a possession",
    "aprayer": "a prayer",
    "apretense": "a pretense",
    "aprophet": "a prophet",
    "aproselyte": "a proselyte",
    "arebellion": "a rebellion",
    "aresurrection": "a resurrection",
    "arighteous": "a righteous",
    "aring": "a ring",
    "aringleader": "a ringleader",
    "arobber": "a robber",
    "asacrifice": "a sacrifice",
    "asad": "a sad",
    "asecond": "a second",
    "asecret": "a secret",
    "asect": "a sect",
    "aseller": "a seller",
    "aserpent": "a serpent",
    "asevere": "a severe",
    "asheep": "a sheep",
    "ashepherd": "a shepherd",
    "asignal": "a signal",
    "asister": "a sister",
    "asnare": "a snare",
    "ason": "a son",
    "asponge": "a sponge",
    "asteward": "a steward",
    "astranger": "a stranger",
    "astronger": "a stronger",
    "asum": "a sum",
    "asycamore": "a sycamore",
    "atempestuous": "a tempestuous",
    "atestimony": "a testimony",
    "atomb": "a tomb",
    "atooth": "a tooth",
    "atower": "a tower",
    "atreasure": "a treasure",
    "atree": "a tree",
    "atumult": "a tumult",
    "avillage": "a village",
    "avineyard": "a vineyard",
    "aviolent": "a violent",
    "awedding": "a wedding",
    "aweek": "a week",
    "awife": "a wife",
    "awindow": "a window",
    "awindstorm": "a windstorm",
    "awine": "a wine",
    "awithered": "a withered",
    "awork": "a work",
    "aworshiper": "a worshiper",
    "ayear": "a year",
    "ayoke": "a yoke",
    # ── Additional tokens missed by deep_scan (aspell accepts the fused form) ──
    "alampstand": "a lampstand",
    "awinepress": "a winepress",
    "awinebibber": "a winebibber",
    "abed": "a bed",  # Context-checked: "under abed" → "under a bed"
}

# Context-sensitive replacements: (regex_pattern, replacement)
# These handle words where the fused form is a real English word but contextually wrong
CONTEXT_REPLACEMENTS = [
    # "along time" → "a long time" (but NOT "came along" or "along the road")
    (re.compile(r'\balong time\b'), "a long time"),
    # "afar country" → "a far country" (but NOT "afar off" which is correct)
    (re.compile(r'\bafar country\b'), "a far country"),
]

# False positives — these are real English words, not fused markers
FALSE_POSITIVES = {"dwelled", "coffered", "bended", "subsided"}

RE_ANCHOR = re.compile(r'^([A-Z0-9]+\.\d+:\d+)\s+(.*)')


def fix_file(filepath: Path, dry_run: bool = False) -> list[dict]:
    """Fix all fused markers in a single file. Returns list of fixes applied."""
    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()
    fixes = []
    new_lines = []

    for line in lines:
        m = RE_ANCHOR.match(line)
        if not m:
            new_lines.append(line)
            continue

        anchor = m.group(1)
        verse_text = m.group(2)
        original = verse_text

        # Check every token in the replacement map
        for token, replacement in REPLACEMENTS.items():
            pattern = re.compile(r'\b' + re.escape(token) + r'\b')
            if pattern.search(verse_text):
                verse_text = pattern.sub(replacement, verse_text)
                fixes.append({
                    "anchor": anchor,
                    "token": token,
                    "replacement": replacement,
                })

        # Apply context-sensitive replacements
        for ctx_pattern, ctx_replacement in CONTEXT_REPLACEMENTS:
            if ctx_pattern.search(verse_text):
                verse_text = ctx_pattern.sub(ctx_replacement, verse_text)
                fixes.append({
                    "anchor": anchor,
                    "token": ctx_pattern.pattern,
                    "replacement": ctx_replacement,
                })

        if verse_text != original:
            new_lines.append(f"{anchor} {verse_text}")
        else:
            new_lines.append(line)

    if fixes and not dry_run:
        new_text = "\n".join(new_lines)
        if text.endswith("\n"):
            new_text += "\n"
        filepath.write_text(new_text, encoding="utf-8")

    return fixes


def discover_canon() -> list[Path]:
    """Discover all canon files in biblical order."""
    files = []
    for d in (CANON_OT, CANON_NT):
        if d.exists():
            files.extend(sorted(d.glob("*.md")))
    return files


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Fix fused footnote markers")
    parser.add_argument("--dry-run", action="store_true", help="Show fixes without applying")
    parser.add_argument("--file", type=Path, help="Single file to fix")
    parser.add_argument("--scope", choices=["canon", "ot", "nt"])
    args = parser.parse_args()

    if args.file:
        files = [args.file]
    elif args.scope == "ot":
        files = sorted(CANON_OT.glob("*.md"))
    elif args.scope == "nt":
        files = sorted(CANON_NT.glob("*.md"))
    elif args.scope == "canon":
        files = discover_canon()
    else:
        files = discover_canon()

    total_fixes = 0
    for filepath in files:
        fixes = fix_file(filepath, dry_run=args.dry_run)
        if fixes:
            print(f"\n{filepath.name}: {len(fixes)} fixes", file=sys.stderr)
            for f in fixes:
                action = "→" if not args.dry_run else "would →"
                print(f"  {f['anchor']:15s} {f['token']:25s} {action} {f['replacement']}")
            total_fixes += len(fixes)

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"  Total fixes: {total_fixes}" + (" (dry run)" if args.dry_run else ""), file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)


if __name__ == "__main__":
    main()
