"""
fix_articles.py — Detect and fix fused article compounds in staged canon files.

Finds patterns like "aman" → "a man", "anoffering" → "an offering",
"thechildren" → "the children" where an article (a/an/the) is fused
to the following word.

Uses Brenton reference for confirmation when available.

Rules:
  A1  Fused "a" + word  ("aman" → "a man")
  A2  Fused "an" + word ("anoffering" → "an offering")
  A3  Fused "the" + word ("thechildren" → "the children")

Usage:
    python3 fix_articles.py staging/validated/OT/GEN.md                    # dry-run
    python3 fix_articles.py staging/validated/OT/GEN.md --in-place         # apply fixes
    python3 fix_articles.py staging/validated/OT/GEN.md --report           # JSON report
    python3 fix_articles.py staging/validated/OT/GEN.md --editorial-report # editorial queue JSON
    python3 fix_articles.py staging/validated/OT/GEN.md --editorial-out staging/validated/OT/GEN_editorial_candidates.json
    python3 fix_articles.py staging/validated/OT/GEN.md --reference brenton  # Brenton confirm
"""

from __future__ import annotations

import argparse
from datetime import date
import json
import re
import shutil
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import sys as _sys; from pathlib import Path as _Path
_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists(): _R = _R.parent
if str(_R) not in _sys.path: _sys.path.insert(0, str(_R))
from pipeline.common.paths import REPO_ROOT, BRENTON_DIR

# ---------------------------------------------------------------------------
# Known English words that commonly follow articles in biblical text.
# This allowlist prevents false positives on words like "these", "then",
# "another", "angel" etc. where stripping the article would be wrong.
# ---------------------------------------------------------------------------

# Words that start with the same letters as articles but are NOT fused
_FALSE_POSITIVE_PREFIXES = {
    # "a" prefix false positives — real words starting with 'a'
    "able", "abode", "about", "above", "abroad", "absent", "according",
    "account", "accounted", "accursed", "acknowledged", "acquainted",
    "across", "acted", "added", "administered", "admonished", "adorned",
    "advanced", "advantage", "advised", "afar", "afraid", "after",
    "afterward", "afterwards", "again", "against", "age", "aged", "ago",
    "agreed", "alive", "all", "allegory", "allowed", "almighty", "almost",
    "alone", "along", "already", "also", "altar", "altars", "altered",
    "although", "altogether", "always", "amazed", "ambush", "amen",
    "amid", "amidst", "among", "amongst", "amount", "ancient", "and",
    "anger", "angry", "anguish", "animal", "announced", "anointed",
    "another", "answer", "answered", "any", "anyone", "anything",
    "apart", "apostle", "apostles", "appeal", "appear", "appeared",
    "appearance", "appearing", "apple", "applied", "appointed",
    "approached", "approved", "are", "arise", "ark", "arm", "armed",
    "armies", "armor", "army", "arose", "around", "arranged", "array",
    "arrived", "arrogant", "arrow", "arrows", "as", "ascend", "ascended",
    "ashamed", "ashes", "aside", "ask", "asked", "asleep", "assembled",
    "assembly", "assigned", "at", "ate", "atonement", "attained",
    "attended", "authority", "avenge", "avenged", "avoid", "avoided",
    "awake", "awakened", "aware", "away", "awe", "awhile",
    "abhor", "abhorred", "abomination", "abominations",
    "accept", "acceptable", "accepted", "accomplish", "accomplished",
    "acknowledge", "acknowledged", "acquire", "acquired",
    "address", "addressed", "adjust", "admire", "admit",
    "adopt", "adopted", "adore", "adorn", "adorned",
    "afflict", "afflicted", "affliction",
    "agree", "agreed", "aground",
    "alien", "aliens", "align", "aligned",
    "allow", "allowed", "allows",
    "amaze", "amazement", "ambition",
    "approach", "approached", "appropriate",
    "aroma", "aromas", "arouse", "aroused",
    "arrange", "arranged", "arrangement",
    "assemble", "assembled", "assign", "assigned",
    "attach", "attached", "attack", "attacked", "attain",
    "attempt", "attempted", "attend", "attendance",
    "attract", "attracted", "attribute", "attributed",
    "avow", "avowed",
    # Biblical proper names starting with article-like prefix
    "abihu", "abijah", "abram", "abraham", "abner", "abimelech",
    "abishai", "abiathar", "ahab", "ahaz", "ahaziah", "ahijah",
    "amalekite", "amalekites", "ammon", "ammonite", "ammonites",
    "amos", "ananias", "andrew", "anna", "annas",
    "aholiab", "amalek", "amalekite", "amalekites", "amorite", "amorites",
    "abel", "achbor", "adam", "adah", "adullamite", "amraphel",
    "anah", "anamim", "aner", "aholibamah", "arba", "arioch",
    "arphaxad", "asenath", "atad",
    "amram", "aram", "antioch", "apollos", "asher", "assyria", "assyrians",
    "thessalonians",
    "abhorrent", "abominable", "abominably", "abolish", "abolishes",
    "abundance", "abundant", "abundantly",
    "acts", "active", "actively", "actual", "actually",
    "adult", "adults", "adultery", "adulterer", "adulteress", "adulterous",
    "afford", "affords", "afforded",
    "agreement", "agreements",
    "alarmed",
    "anoint", "anointing", "anoints",
    "anxiety", "anxious", "anymore",
    "appoint", "appointed", "appointments",
    "appendage", "appendages",
    "approach", "approaches",
    "article", "articles", "artisan", "artisans", "artistic",
    "adornment", "adornments",
    "afternoon",
    "aloud",
    "asphalt",
    "abounded", "abound", "abounds",
    "anywhere",
    "arrive", "arrived", "arrives",
    "ascend", "ascending", "ascended",
    "awoke",
    "attention", "attire", "attired",
    "appears", "appearing", "appear",
    # "an" prefix false positives
    "ancestor", "ancestors", "ancestral", "anchor", "ancient",
    "angel", "angels", "anger", "angry", "anguish", "animal", "animals",
    "ankle", "announced", "annual", "anointed", "another", "answer",
    "answered", "ant", "antichrist", "any", "anyone", "anything",
    # "the" prefix false positives — real words starting with 'the'
    "theatre", "thee", "theft", "their", "theirs", "them", "theme",
    "themselves", "then", "thence", "thenceforth", "there", "thereafter",
    "thereby", "therefore", "therein", "thereof", "thereon", "thereto",
    "thereupon", "these", "they", "thick", "thief", "thieves", "thigh",
    "thin", "thine", "thing", "things", "think", "third", "thirst",
    "thirsty", "thirteen", "thirteenth", "thirtieth", "thirty", "this",
    "thither", "thorn", "thorns", "thorny", "thoroughly", "those",
    "thou", "though", "thought", "thoughts", "thousand", "thousands",
    "thread", "threat", "threatened", "three", "threshold", "threw",
    "thrice", "throne", "thrones", "throng", "through", "throughout",
    "throw", "thrown", "thrust", "thunder", "thunders", "thus",
}

# Known biblical words commonly fused with articles in OSB OCR output.
# If the remainder matches one of these, boost confidence by 0.3.
_KNOWN_BIBLICAL_TARGETS = {
    "burnt", "sin", "grain", "peace", "wave", "trespass", "guilt",
    "whole", "male", "female", "young", "man", "woman", "child",
    "soul", "gift", "sacrifice", "offering", "sweet", "memorial",
    "holy", "pan", "priest", "ruler", "native", "resident", "foreigner",
    "hired", "leprous", "discharge", "defect", "deposit", "sheep",
    "goat", "lamb", "bull", "bullock", "ram", "kid", "heifer",
    "choice", "shiny", "scar", "prostitute", "harlot", "stranger",
    "slave", "servant", "cubit", "cubits", "sign", "skin",
    "sabbath", "statute", "covenant", "commandment",
    "donkey", "donkeys", "knob", "knobs", "weaver", "weavers",
    "network", "networks", "drachma", "drachmas",
    "foreign", "foreigner", "foreigners",
    "daily", "bronze", "thanksgiving", "voluntary",
    "defilement", "cake", "cakes", "handful",
    "clean", "unclean", "carcass", "cistern", "spring",
    "turtledove", "turtledoves", "burn", "lesion", "lesions",
    "standstill", "reddish", "spreading", "second",
    "perpetual", "continual", "sacred", "solemn",
    "talent", "talents", "shekel", "shekels",
    "hundred", "thousand", "forty", "fifty", "sixty", "seventy",
    "blue", "scarlet", "purple", "crimson",
    "dedicated", "consecrated", "signet", "cord", "cords",
    "prince", "princess", "midwife", "nurse",
    "flame", "rod", "sharp", "strong",
    "daughter", "daughters", "son", "sons",
    "new", "beautiful", "good", "great",
    "distance", "judge", "well", "maid",
    "sojourner", "sword", "feast", "wonder",
    "time", "mighty", "serpent", "land",
    "bush", "god", "charmer", "ventriloquist",
    "house", "bright", "mark", "seminal",
    "suitable", "manner", "stand", "concubine",
    "bald", "wife", "defiled",
    "decree", "decrees", "ephod", "ephods", "ephah", "ephahs",
    "husband", "relative", "pile", "relation", "result",
    "demand", "response", "certain", "deceiving", "handbreadth", "close",
    "bandage", "bin", "calf", "cavalryman", "cave", "couple", "cup",
    "drinking", "eunuch", "fire", "forked", "furrow", "horse", "jar",
    "little", "lion", "morsel", "monument", "nation", "prophet", "severe",
    "ship", "small", "treaty", "vessel", "widow", "wound", "lily",
}

# Minimum word length after article split for auto-fix
_MIN_WORD_LEN = 3

# Regex: find a token that looks like article + word (lowercase continuing)
# We look for word boundaries
_RE_FUSED_A = re.compile(r'\b(a)([a-z]{2,})\b')  # "a" + word
_RE_FUSED_AN = re.compile(r'\b(an)([a-z]{3,})\b')
_RE_FUSED_THE = re.compile(r'\b(the)([a-z]{3,})\b')
# Also catch capitalized: "Aman" at start of verse
_RE_FUSED_A_CAP = re.compile(r'\b(A)([a-z]{2,})\b')
_RE_FUSED_AN_CAP = re.compile(r'\b(An)([a-z]{3,})\b')
_RE_FUSED_THE_CAP = re.compile(r'\b(The)([a-z]{3,})\b')

# Common English words for confidence scoring
_COMMON_WORDS_FILE = None  # Could load from file, but we use Brenton instead

# Verse line pattern
_RE_VERSE_LINE = re.compile(r'^(\d+)\s+(.*)')
_RE_ANCHOR = re.compile(r'^(?:\[)?([A-Z0-9]+\.\d+:\d+)(?:\])?')


def load_brenton_index(book_code: str) -> dict[str, str] | None:
    """Load Brenton reference for a book. Returns {anchor: text} or None."""
    path = BRENTON_DIR / f"{book_code}.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    result = {}
    for ch_str, ch_data in data.get("chapters", {}).items():
        for i, text in enumerate(ch_data.get("verses", []), 1):
            anchor = f"{book_code}.{ch_str}:{i}"
            result[anchor] = text
    return result


def _is_false_positive(full_token: str, article: str, remainder: str) -> bool:
    """Check if the full token is a known real word, not a fusion."""
    lower = full_token.lower()
    if lower in _FALSE_POSITIVE_PREFIXES:
        return True
    # Very short remainders are suspect
    if len(remainder) < _MIN_WORD_LEN:
        return True
    return False


@lru_cache(maxsize=8192)
def _aspell_known(word: str) -> bool | None:
    """
    Return True if aspell accepts the word, False if it flags it, or None if
    aspell is unavailable.
    """
    if not word or shutil.which("aspell") is None:
        return None
    proc = subprocess.run(
        ["aspell", "list"],
        input=f"{word}\n",
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout.strip() == ""


def _spell_audit_boost(article: str, remainder: str, full_token: str) -> tuple[float, str | None]:
    """
    Use aspell as a second signal for obvious fused-article OCR defects.

    High-confidence pattern:
      - fused token is misspelled
      - split target remainder is a known dictionary word or known biblical target
    """
    full_known = _aspell_known(full_token.lower())
    remainder_known = _aspell_known(remainder.lower())
    split_hint = remainder.lower() in _KNOWN_BIBLICAL_TARGETS or remainder_known is True

    if full_known is False and split_hint:
        return 0.25, "aspell_split_confirms"
    if full_known is False:
        return 0.10, "aspell_fused_unknown"
    if full_known is True and split_hint:
        return -0.15, "aspell_token_known"
    return 0.0, None


def _replacement_phrase(article: str, remainder: str) -> str:
    """
    Build the suggested split phrase.

    OCR occasionally drops the trailing "n" in "an" before vowel-initial words,
    leaving forms like "aephod". Prefer "an ephod" in those cases.
    """
    if article.lower() == "a" and remainder[:1].lower() in "aeiou":
        resolved_article = "an" if article.islower() else "An"
        return f"{resolved_article} {remainder}"
    return f"{article} {remainder}"


def _brenton_confirms(anchor: str, article: str, remainder: str,
                      brenton: dict[str, str] | None) -> float:
    """
    Check if Brenton text contains "article remainder" as separate words.
    Returns confidence boost (0.0 to 0.5).
    """
    if brenton is None:
        return 0.0
    ref_text = brenton.get(anchor, "")
    if not ref_text:
        return 0.0
    # Check for "article remainder" in Brenton (case-insensitive)
    pattern = re.compile(rf'\b{re.escape(article)}\s+{re.escape(remainder)}\b', re.IGNORECASE)
    if pattern.search(ref_text):
        return 0.4
    # Check if just the remainder appears as a standalone word
    if re.search(rf'\b{re.escape(remainder)}\b', ref_text, re.IGNORECASE):
        return 0.2
    return 0.0


def find_fused_articles(text: str, anchor: str,
                        brenton: dict[str, str] | None) -> list[dict]:
    """
    Find fused article candidates in verse text.
    Returns list of {token, article, remainder, confidence, position, rule}.
    """
    candidates = []

    patterns = [
        (_RE_FUSED_A, "a", "A1"),
        (_RE_FUSED_AN, "an", "A2"),
        (_RE_FUSED_THE, "the", "A3"),
        (_RE_FUSED_A_CAP, "A", "A1"),
        (_RE_FUSED_AN_CAP, "An", "A2"),
        (_RE_FUSED_THE_CAP, "The", "A3"),
    ]

    for pattern, article_example, rule in patterns:
        for m in pattern.finditer(text):
            article = m.group(1)
            remainder = m.group(2)
            full_token = m.group(0)

            if _is_false_positive(full_token, article, remainder):
                continue

            # Base confidence
            confidence = 0.5

            # Boost if remainder is capitalized (strong signal for "a" fusions)
            if remainder[0].isupper():
                confidence += 0.3

            # Boost if remainder is a known biblical word
            if remainder.lower() in _KNOWN_BIBLICAL_TARGETS:
                confidence += 0.3

            # Brenton confirmation
            confidence += _brenton_confirms(anchor, article.lower(), remainder, brenton)

            spell_delta, spell_hint = _spell_audit_boost(article, remainder, full_token)
            confidence += spell_delta

            # Cap at 1.0
            confidence = max(0.0, min(confidence, 1.0))

            source_hints = []
            if remainder.lower() in _KNOWN_BIBLICAL_TARGETS:
                source_hints.append("biblical_target")
            if spell_hint:
                source_hints.append(spell_hint)
            brenton_boost = _brenton_confirms(anchor, article.lower(), remainder, brenton)
            if brenton and brenton_boost > 0:
                source_hints.append("brenton")

            # Titlecase tokens are often names/places. Only keep them when we
            # have stronger evidence than a generic spell split.
            if full_token[:1].isupper() and article[:1].isupper():
                strong_titlecase_signal = (
                    remainder.lower() in _KNOWN_BIBLICAL_TARGETS
                    or brenton_boost >= 0.4
                )
                if not strong_titlecase_signal:
                    continue

            candidates.append({
                "token": full_token,
                "article": article,
                "remainder": remainder,
                "confidence": confidence,
                "position": m.start(),
                "rule": rule,
                "replacement": _replacement_phrase(article, remainder),
                "category": "fused_article_explicit",
                "source_hint": ", ".join(source_hints) if source_hints else "heuristic",
            })

    return candidates


def process_file(filepath: Path, brenton: dict[str, str] | None,
                 threshold: float = 0.70,
                 apply_fixes: bool = False) -> tuple[list[str], list[dict]]:
    """
    Process a staged canon file.
    Returns (fixed_lines, all_candidates).
    """
    lines = filepath.read_text(encoding="utf-8").splitlines()
    fixed_lines = []
    all_candidates = []
    in_frontmatter = False
    frontmatter_done = False

    for line_number, line in enumerate(lines, 1):
        # Handle YAML frontmatter
        if line.strip() == "---":
            if not frontmatter_done:
                in_frontmatter = not in_frontmatter
                if not in_frontmatter:
                    frontmatter_done = True
            fixed_lines.append(line)
            continue

        if in_frontmatter:
            fixed_lines.append(line)
            continue

        # Extract anchor from line
        anchor_match = _RE_ANCHOR.match(line)
        if not anchor_match:
            fixed_lines.append(line)
            continue

        anchor = anchor_match.group(1)
        rest = line[anchor_match.end():]

        # Find fused articles
        candidates = find_fused_articles(rest, anchor, brenton)

        if not candidates:
            fixed_lines.append(line)
            continue

        # Apply fixes above threshold when explicitly requested
        fixed_rest = rest
        # Sort by position descending to avoid offset issues
        for cand in sorted(candidates, key=lambda c: c["position"], reverse=True):
            cand["anchor"] = anchor
            cand["line"] = line_number
            cand["line_text"] = line.rstrip()
            all_candidates.append(cand)

            if cand["confidence"] >= threshold:
                cand["auto_fixable"] = True
                if apply_fixes:
                    old = cand["token"]
                    new = cand["replacement"]
                    fixed_rest = fixed_rest.replace(old, new, 1)
                    cand["output_resolved"] = True
                else:
                    cand["output_resolved"] = False
            else:
                cand["auto_fixable"] = False
                cand["output_resolved"] = False

        fixed_lines.append(f"{line[:anchor_match.end()]}{fixed_rest}")

    return fixed_lines, all_candidates


def build_editorial_report(
    book_code: str,
    filepath: Path,
    candidates: list[dict],
    min_confidence: float = 0.75,
) -> dict:
    flagged = [
        c for c in candidates
        if not c.get("output_resolved") and float(c.get("confidence", 0.0)) >= min_confidence
    ]
    by_category: dict[str, int] = {}
    report_candidates = []
    for cand in flagged:
        category = cand.get("category", "fused_article_explicit")
        by_category[category] = by_category.get(category, 0) + 1
        report_candidates.append({
            "line": cand["line"],
            "anchor": cand["anchor"],
            "category": category,
            "token": cand["token"],
            "confidence": round(float(cand["confidence"]), 2),
            "source_hint": cand.get("source_hint", "heuristic"),
            "manual_status": "pending",
            "replacement": cand["replacement"],
        })

    return {
        "book": book_code,
        "file": str(filepath),
        "generated": str(date.today()),
        "total_candidates": len(report_candidates),
        "by_category": by_category,
        "candidates": report_candidates,
        "notes": [
            "Explicit fused article audit from fix_articles.py",
            f"High-confidence article-conjunction fusions (>= {min_confidence:.2f}) should block promotion until resolved",
        ],
    }


def merge_editorial_report(existing: dict | None, new_report: dict) -> dict:
    if not existing:
        return new_report

    merged = dict(existing)
    existing_candidates = list(existing.get("candidates", []))
    seen = {
        (
            item.get("anchor"),
            item.get("line"),
            item.get("category"),
            item.get("token"),
        )
        for item in existing_candidates
    }
    for item in new_report.get("candidates", []):
        key = (item.get("anchor"), item.get("line"), item.get("category"), item.get("token"))
        if key not in seen:
            existing_candidates.append(item)
            seen.add(key)
    merged["candidates"] = existing_candidates
    merged["total_candidates"] = len(existing_candidates)

    by_category: dict[str, int] = {}
    for item in existing_candidates:
        category = item.get("category", "unknown")
        by_category[category] = by_category.get(category, 0) + 1
    merged["by_category"] = by_category

    notes = list(existing.get("notes", []))
    for note in new_report.get("notes", []):
        if note not in notes:
            notes.append(note)
    merged["notes"] = notes
    merged["generated"] = new_report["generated"]
    merged["file"] = new_report["file"]
    merged["book"] = new_report["book"]
    return merged


def main():
    parser = argparse.ArgumentParser(
        description="Detect and fix fused article compounds in staged canon files."
    )
    parser.add_argument("file", type=Path, help="Staged canon .md file")
    parser.add_argument("--in-place", action="store_true",
                        help="Apply fixes to file in place")
    parser.add_argument("--report", action="store_true",
                        help="Output JSON report instead of diff")
    parser.add_argument("--reference", choices=["brenton"],
                        help="Use reference for confirmation")
    parser.add_argument("--threshold", type=float, default=0.70,
                        help="Confidence threshold for auto-fix (default: 0.70)")
    parser.add_argument("--editorial-report", action="store_true",
                        help="Output BOOK_editorial_candidates-style JSON for unresolved candidates")
    parser.add_argument("--editorial-out", type=Path,
                        help="Write or merge unresolved candidates into editorial sidecar JSON")
    parser.add_argument("--editorial-min-confidence", type=float, default=0.75,
                        help="Minimum confidence for editorial sidecar candidates (default: 0.75)")

    args = parser.parse_args()

    if not args.file.exists():
        print(f"ERROR: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    # Detect book code from filename
    book_code = args.file.stem.split("_")[0]

    # Load Brenton if requested
    brenton = None
    if args.reference == "brenton":
        brenton = load_brenton_index(book_code)
        if brenton:
            print(f"Loaded Brenton reference: {len(brenton)} verses", file=sys.stderr)
        else:
            print(f"WARNING: No Brenton index for {book_code}", file=sys.stderr)

    fixed_lines, candidates = process_file(
        args.file,
        brenton,
        args.threshold,
        apply_fixes=args.in_place,
    )

    applied = [c for c in candidates if c.get("output_resolved")]
    flagged = [c for c in candidates if not c.get("output_resolved")]

    if args.report:
        report = {
            "book": book_code,
            "file": str(args.file),
            "threshold": args.threshold,
            "total_candidates": len(candidates),
            "auto_fixed": len(applied),
            "flagged_for_review": len(flagged),
            "candidates": [
                {k: v for k, v in c.items() if k != "line"}
                for c in candidates
            ],
        }
        print(json.dumps(report, indent=2))
        return

    if args.editorial_report or args.editorial_out:
        editorial = build_editorial_report(
            book_code, args.file, candidates, min_confidence=args.editorial_min_confidence
        )
        if args.editorial_out:
            existing = None
            if args.editorial_out.exists():
                existing = json.loads(args.editorial_out.read_text(encoding="utf-8"))
            merged = merge_editorial_report(existing, editorial)
            args.editorial_out.write_text(
                json.dumps(merged, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        if args.editorial_report:
            print(json.dumps(editorial, indent=2, ensure_ascii=False))
            return

    # Print summary
    print(f"\nFused Article Report — {book_code}")
    print(f"  Total candidates: {len(candidates)}")
    print(f"  Auto-fixable (≥{args.threshold}): {len(applied)}")
    print(f"  Flagged for review: {len(flagged)}")

    if applied:
        print(f"\n  Auto-fixes:")
        for c in applied[:30]:
            print(f"    {c.get('anchor','?'):15s}  {c['token']} → {c['replacement']}  "
                  f"(conf={c['confidence']:.2f}, {c['rule']})")
        if len(applied) > 30:
            print(f"    ... and {len(applied) - 30} more")

    if flagged:
        print(f"\n  Flagged (review needed):")
        for c in flagged[:20]:
            print(f"    {c.get('anchor','?'):15s}  {c['token']} → {c['replacement']}  "
                  f"(conf={c['confidence']:.2f}, {c['rule']})")
        if len(flagged) > 20:
            print(f"    ... and {len(flagged) - 20} more")

    if args.in_place and applied:
        args.file.write_text("\n".join(fixed_lines) + "\n", encoding="utf-8")
        print(f"\n  Applied {len(applied)} fixes to {args.file}")
    elif applied and not args.in_place:
        print(f"\n  Run with --in-place to apply {len(applied)} fixes.")


if __name__ == "__main__":
    main()
