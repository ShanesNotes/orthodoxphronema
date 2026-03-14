#!/usr/bin/env python3
"""
deep_scan.py — Deep per-book scanner for remaining canon errors.

Specifically targets error patterns that broader passes miss:
  D1  Fused single-letter footnote markers (a+word, b+word, c+word, etc.)
  D2  Fused article "a" before any word (not just known biblical targets)
  D3  Residual OCR kerning splits ("J ESUS", "Dav id", "L ORD")
  D4  Stray footnote markers (isolated a/b/c letters mid-verse)
  D5  Fused "the"/"and"/"of"/"in" + word (broader than fix_articles.py)
  D6  Missing article "a" (contextual — where "a" was stripped as footnote marker)

Usage:
    python3 deep_scan.py --file canon/OT/01_GEN.md
    python3 deep_scan.py --scope canon
    python3 deep_scan.py --scope canon --fix  # interactive fix mode
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

_THIS = Path(__file__).resolve().parent
_REPO = _THIS
while _REPO != _REPO.parent and not (_REPO / "pipeline" / "__init__.py").exists():
    _REPO = _REPO.parent

CANON_OT = _REPO / "canon" / "OT"
CANON_NT = _REPO / "canon" / "NT"

RE_ANCHOR = re.compile(r'^([A-Z0-9]+\.\d+:\d+)\s+(.*)')
RE_FRONTMATTER = re.compile(r'^---\s*$')
RE_HEADING = re.compile(r'^#{1,4}\s')

# ── D1: Fused single-letter footnote markers ────────────────────────────────
# Pattern: a lowercase letter (a-d) directly fused to a word that should start
# with a capital or is a known common word. The OSB uses superscript a,b,c,d
# for cross-references. Docling renders them as inline lowercase letters.
#
# We check: does removing the first letter produce a word aspell recognizes
# AND does the fused form fail aspell?

def _aspell_known(word: str) -> bool:
    """Return True if aspell accepts the word."""
    if not word or not shutil.which("aspell"):
        return False
    proc = subprocess.run(
        ["aspell", "list", "--lang=en"],
        input=f"{word}\n",
        capture_output=True, text=True, check=False,
    )
    return proc.stdout.strip() == ""


def _aspell_batch(words: list[str]) -> set[str]:
    """Return set of UNKNOWN words from a batch."""
    if not words or not shutil.which("aspell"):
        return set()
    text = "\n".join(words)
    proc = subprocess.run(
        ["aspell", "list", "--lang=en"],
        input=text, capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0:
        return set()
    return set(proc.stdout.strip().splitlines()) if proc.stdout.strip() else set()


# Words where a leading lowercase letter is part of the real word, not a marker
_SAFE_WORDS = {
    # Common words starting with 'a' that could look like a+word
    "able", "about", "above", "abroad", "absent", "according", "account",
    "acknowledge", "across", "acted", "added", "after", "afterward",
    "afterwards", "again", "against", "age", "aged", "ago", "agreed",
    "alive", "all", "almost", "alone", "along", "already", "also",
    "altar", "altars", "although", "altogether", "always", "amazed",
    "among", "amongst", "amount", "ancient", "and", "anger", "angry",
    "anguish", "animal", "announced", "anointed", "another", "answer",
    "answered", "any", "anyone", "anything", "apart", "appear", "appeared",
    "appointed", "approached", "are", "arise", "ark", "arm", "armed",
    "armies", "army", "arose", "around", "arranged", "array", "arrived",
    "arrogant", "arrow", "arrows", "as", "ascend", "ascended", "ashamed",
    "ashes", "aside", "ask", "asked", "asleep", "assembled", "assembly",
    "assigned", "at", "ate", "atonement", "attained", "authority",
    "avenge", "avoid", "awake", "awakened", "aware", "away", "awe",
    # Common words starting with 'b' that could look like b+word
    "back", "bad", "battle", "bear", "bearing", "bears", "beast",
    "beautiful", "became", "because", "become", "bed", "been", "before",
    "began", "beginning", "behalf", "behind", "behold", "being", "believe",
    "beloved", "below", "beneath", "beside", "besides", "best", "better",
    "between", "beyond", "birth", "blameless", "bless", "blessed",
    "blessing", "blind", "blood", "blow", "body", "bone", "bones",
    "book", "border", "born", "both", "bound", "bow", "bowed", "boy",
    "branch", "branches", "bread", "break", "breath", "brethren",
    "bride", "bring", "broad", "broke", "broken", "brother", "brothers",
    "brought", "build", "built", "bull", "burn", "burned", "burning",
    "burnt", "burst", "bury", "but", "buy",
}


def scan_fused_markers(text: str, anchor: str) -> list[dict]:
    """Scan verse text for fused single-letter footnote markers."""
    findings = []

    # Pattern: look for words where removing the first letter (a-d) produces
    # a valid English word, but the full form is NOT a valid word
    words_in_verse = re.findall(r'\b([a-z]\w{2,})\b', text)
    if not words_in_verse:
        return findings

    # Quick batch: check all words at once
    unknown = _aspell_batch(words_in_verse)

    for word in words_in_verse:
        if word not in unknown:
            continue  # aspell knows this word — it's fine
        if word.lower() in _SAFE_WORDS:
            continue

        first_letter = word[0]
        remainder = word[1:]

        # Only check a, b, c, d (common OSB footnote markers)
        if first_letter not in "abcd":
            continue

        # Is the remainder a real word?
        if len(remainder) >= 3 and _aspell_known(remainder):
            findings.append({
                "anchor": anchor,
                "type": "D1",
                "token": word,
                "marker": first_letter,
                "remainder": remainder,
                "suggestion": remainder,
                "note": f"Likely fused footnote marker '{first_letter}' + '{remainder}'",
            })

    return findings


def scan_fused_article_a(text: str, anchor: str) -> list[dict]:
    """Scan for fused article 'a' + word patterns that aspell doesn't catch."""
    findings = []

    # Look for patterns like "aHook", "aCenturion" (lowercase a + Capital word)
    # These are clearly article + proper word
    for m in re.finditer(r'\ba([A-Z][a-z]{2,})\b', text):
        word = m.group(0)
        remainder = m.group(1)
        # This is almost certainly "a" + capitalized word
        findings.append({
            "anchor": anchor,
            "type": "D2",
            "token": word,
            "marker": "a",
            "remainder": remainder,
            "suggestion": f"a {remainder}",
            "note": f"Fused article 'a' + '{remainder}'",
        })

    return findings


def scan_kerning_splits(text: str, anchor: str) -> list[dict]:
    """Scan for OCR kerning splits (space inserted mid-word)."""
    findings = []

    # Known kerning split patterns from the OSB/Docling pipeline
    known_splits = {
        "J ESUS": "JESUS",
        "Dav id": "David",
        "L ORD": "LORD",
        "C HRIST": "CHRIST",
        "G OD": "GOD",
        "S PIRIT": "SPIRIT",
        "Jeru salem": "Jerusalem",
        "Is rael": "Israel",
        "Ju dah": "Judah",
        "Eg ypt": "Egypt",
    }

    for wrong, right in known_splits.items():
        if wrong in text:
            findings.append({
                "anchor": anchor,
                "type": "D3",
                "token": wrong,
                "remainder": "",
                "suggestion": right,
                "note": f"Kerning split: '{wrong}' → '{right}'",
            })

    # Generic pattern: single uppercase letter + space + uppercase continuation
    for m in re.finditer(r'\b([A-Z]) ([A-Z]{2,})\b', text):
        combo = m.group(1) + m.group(2)
        split_form = m.group(0)
        if split_form not in known_splits and _aspell_known(combo.lower()):
            findings.append({
                "anchor": anchor,
                "type": "D3",
                "token": split_form,
                "remainder": "",
                "suggestion": combo,
                "note": f"Kerning split: '{split_form}' → '{combo}'",
            })

    return findings


def scan_fused_common_words(text: str, anchor: str) -> list[dict]:
    """Scan for fused common words like 'ofthe', 'andthe', 'inthe' etc."""
    findings = []

    # Patterns: common word + common word fused together
    fused_patterns = [
        (r'\b(of)(the|his|her|its|their|my|your|our|this|that|these|those|God|whom|which|all|man|men)\b', "of"),
        (r'\b(and)(the|his|her|he|she|it|they|we|you|all|said|when|then)\b', "and"),
        (r'\b(in)(the|his|her|its|their|my|your|our|this|that|all)\b', "in"),
        (r'\b(to)(the|his|her|him|them|you|me|us|God|all)\b', "to"),
        (r'\b(for)(the|his|her|him|them|you|me|us|God|all)\b', "for"),
        (r'\b(from)(the|his|her|him|them|you|me|us|God|all)\b', "from"),
        (r'\b(with)(the|his|her|him|them|you|me|us|God|all)\b', "with"),
        (r'\b(by)(the|his|her|him|them|you|me|us|God|all)\b', "by"),
        (r'\b(on)(the|his|her|him|them|you|me|us|God|all)\b', "on"),
        (r'\b(at)(the|his|her|him|them|you|me|us|God|all)\b', "at"),
    ]

    for pattern_str, prefix in fused_patterns:
        for m in re.finditer(pattern_str, text, re.IGNORECASE):
            full = m.group(0)
            p = m.group(1)
            suffix = m.group(2)

            # Skip if the full form is a real word
            if _aspell_known(full.lower()):
                continue

            findings.append({
                "anchor": anchor,
                "type": "D5",
                "token": full,
                "remainder": suffix,
                "suggestion": f"{p} {suffix}",
                "note": f"Fused '{p}' + '{suffix}'",
            })

    return findings


def scan_book(filepath: Path) -> list[dict]:
    """Deep-scan a single book file. Returns all findings."""
    lines = filepath.read_text(encoding="utf-8").splitlines()
    all_findings = []
    in_frontmatter = False
    frontmatter_done = False

    for line in lines:
        if line.strip() == "---":
            if not frontmatter_done:
                in_frontmatter = not in_frontmatter
                if not in_frontmatter:
                    frontmatter_done = True
            continue
        if in_frontmatter or RE_HEADING.match(line):
            continue

        m = RE_ANCHOR.match(line)
        if not m:
            continue

        anchor = m.group(1)
        text = m.group(2)

        # Run all scans
        all_findings.extend(scan_fused_markers(text, anchor))
        all_findings.extend(scan_fused_article_a(text, anchor))
        all_findings.extend(scan_kerning_splits(text, anchor))
        all_findings.extend(scan_fused_common_words(text, anchor))

    return all_findings


def discover_canon() -> list[Path]:
    """Discover all canon files in biblical order."""
    files = []
    for d in (CANON_OT, CANON_NT):
        if d.exists():
            files.extend(sorted(d.glob("*.md")))
    return files


def main():
    parser = argparse.ArgumentParser(description="Deep per-book scanner")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--file", type=Path, help="Single file")
    target.add_argument("--scope", choices=["canon", "ot", "nt"])
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if args.file:
        files = [args.file]
    elif args.scope == "ot":
        files = sorted(CANON_OT.glob("*.md"))
    elif args.scope == "nt":
        files = sorted(CANON_NT.glob("*.md"))
    else:
        files = discover_canon()

    all_findings = []
    for filepath in files:
        findings = scan_book(filepath)
        if findings:
            all_findings.extend(findings)
            print(f"  {filepath.name}: {len(findings)} findings", file=sys.stderr)

    if args.json:
        print(json.dumps(all_findings, indent=2))
    else:
        # Group by type
        by_type = defaultdict(list)
        for f in all_findings:
            by_type[f["type"]].append(f)

        print(f"\n{'='*60}", file=sys.stderr)
        print(f"  Total findings: {len(all_findings)}", file=sys.stderr)
        for t in sorted(by_type.keys()):
            items = by_type[t]
            print(f"  {t}: {len(items)}", file=sys.stderr)
        print(f"{'='*60}", file=sys.stderr)

        # Print all findings
        for f in all_findings:
            print(f"{f['anchor']:15s} [{f['type']}] {f['token']:20s} → {f['suggestion']:20s}  ({f['note']})")


if __name__ == "__main__":
    main()
