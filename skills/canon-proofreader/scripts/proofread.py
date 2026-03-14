#!/usr/bin/env python3
"""
proofread.py — Multi-pass proofreader for Orthodox Phronema canon files.

Catches errors that slip through the existing cleanup pipeline:
  P1  Missing space after punctuation   (auto-fix)
  P2  Space before punctuation           (auto-fix)
  P3  Double/repeated words              (auto-fix)
  P4  Fused preposition+word compounds   (review)
  P5  Multiple consecutive spaces        (auto-fix)
  P6  Spelling errors (aspell)           (review)
  P7  Unbalanced quotes                  (report only)
  P8  Fused conjunction+word             (review)

Usage:
    python3 proofread.py --file canon/OT/01_GEN.md --dry-run
    python3 proofread.py --scope all --dry-run --report-dir reports/proofread/
    python3 proofread.py --scope all --apply --report-dir reports/proofread/
    python3 proofread.py --scope all --include-staging --dry-run
    python3 proofread.py --pass regex --file canon/NT/40_MAT.md --dry-run
    python3 proofread.py --pass spell --file canon/NT/40_MAT.md --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

# ── Repo discovery ──────────────────────────────────────────────────────────
_THIS = Path(__file__).resolve().parent
_REPO = _THIS
while _REPO != _REPO.parent and not (_REPO / "pipeline" / "__init__.py").exists():
    _REPO = _REPO.parent

CANON_OT = _REPO / "canon" / "OT"
CANON_NT = _REPO / "canon" / "NT"
STAGING_OT = _REPO / "staging" / "validated" / "OT"
STAGING_NT = _REPO / "staging" / "validated" / "NT"
REPORTS_DIR = _REPO / "reports" / "proofread"
MEMOS_DIR = _REPO / "memos"
BIBLICAL_NAMES = _REPO / "schemas" / "biblical_names.txt"

# ── Regex patterns ──────────────────────────────────────────────────────────
RE_ANCHOR = re.compile(r'^([A-Z0-9]+\.\d+:\d+)\s+(.*)')
RE_FRONTMATTER = re.compile(r'^---\s*$')
RE_HEADING = re.compile(r'^#{1,4}\s')

# P1: Missing space after punctuation (period, comma, semicolon, colon,
#     exclamation, question mark) followed by a letter.
#     Excludes: abbreviations like "v.1", decimal numbers, verse anchors,
#     common abbreviations, and ellipsis patterns.
RE_MISSING_SPACE = re.compile(
    r'(?<![A-Z0-9])(?<!\d)'         # not preceded by anchor-like chars
    r'([,;:!?])'                     # punctuation group 1 (not period — handled separately)
    r'([A-Za-z])'                    # immediately followed by a letter
)
RE_MISSING_SPACE_PERIOD = re.compile(
    r'(?<!\.)(?<![A-Z])'            # not preceded by another period or uppercase (abbreviation)
    r'(\.)(?!\.)'                    # single period
    r'([A-Z])'                       # followed by uppercase (new sentence)
)

# P2: Space before punctuation (but not before opening quotes/parens)
RE_SPACE_BEFORE_PUNCT = re.compile(r' ([,\.;:!?\)\]\}])')
RE_SPACE_BEFORE_POSSESSIVE = re.compile(r" ('s)\b")

# P3: Double words — same word repeated with whitespace between
RE_DOUBLE_WORD = re.compile(r'\b(\w{2,})\s+\1\b', re.IGNORECASE)

# P4: Fused preposition+word (catches what fix_omissions SHORT_PREFIXES misses)
_PREPOSITIONS = [
    "of", "in", "to", "for", "with", "from", "on", "by", "at", "as",
    "into", "upon", "over", "under", "after", "before", "between",
    "through", "about", "against", "among", "within", "without",
    "toward", "towards", "around", "beyond", "during", "until",
    "behind", "beside", "beneath", "above", "across", "along",
]

# P5: Multiple consecutive spaces
RE_MULTI_SPACE = re.compile(r'  +')

# P7: Quote counting
RE_SINGLE_QUOTE = re.compile(r"[''']")
RE_DOUBLE_QUOTE = re.compile(r'["""]')

# P8: Fused conjunction+word
_CONJUNCTIONS = [
    "and", "but", "or", "nor", "for", "yet", "so",
    "that", "when", "while", "where", "which", "because",
    "although", "though", "since", "unless", "whether",
    "if", "then", "than",
]

# ── False positive guards ──────────────────────────────────────────────────
# Words that start with a preposition/conjunction prefix but are real words.
# This set is built lazily and cached.
_ENGLISH_WORDS_CACHE: set[str] | None = None


def _load_false_positive_words() -> set[str]:
    """Load common English words that happen to start with preposition prefixes."""
    # These are real words, not fused compounds.
    # Curated for biblical English to minimize false positives.
    return {
        # "of" prefix
        "off", "offer", "offered", "offering", "offerings", "offers",
        "offense", "offenses", "offensive", "office", "officer", "officers",
        "official", "officials", "officially", "offset", "offspring",
        "often", "oftentimes",
        # "in" prefix
        "increase", "increased", "increasing", "indeed", "inheritance",
        "iniquity", "iniquities", "inner", "innocent", "innocence",
        "innumerable", "inquire", "inquired", "inscription", "inside",
        "insight", "insomuch", "inspire", "inspired", "instead",
        "instruct", "instructed", "instruction", "instructions",
        "instrument", "instruments", "integrity", "intelligence",
        "intend", "intended", "intent", "intention", "intercede",
        "intercession", "interest", "interpret", "interpreted",
        "interpretation", "into", "introduce", "invade", "invaded",
        "invasion", "invent", "invented", "invisible", "invite",
        "invoke", "invoked", "inward", "inwardly",
        # "to" prefix
        "today", "together", "toil", "toiled", "token", "told",
        "tomb", "tombs", "tomorrow", "tongue", "tongues", "tonight",
        "took", "top", "topaz", "tore", "torment", "tormented",
        "torn", "tortoise", "total", "totally", "touch", "touched",
        "toward", "towards", "tower", "towers", "town", "towns",
        # "for" prefix
        "forbid", "forbidden", "forbids", "force", "forced", "forces",
        "ford", "forecast", "forehead", "foreheads", "foreign",
        "foreigner", "foreigners", "foreknew", "foreknowledge",
        "foremost", "forerunner", "foresee", "foreskin", "foreskins",
        "forest", "forests", "forever", "forevermore", "forfeit",
        "forgave", "forget", "forgetful", "forgets", "forgetting",
        "forgive", "forgiven", "forgiveness", "forgives", "forgiving",
        "forgot", "forgotten", "fork", "form", "formal", "formed",
        "former", "formerly", "forming", "forms", "forsake", "forsaken",
        "forsakes", "forsook", "fort", "forth", "fortress", "fortresses",
        "fortunate", "fortune", "forty", "forum", "forward", "fossil",
        "foster", "fought", "foul", "found", "foundation", "foundations",
        "founded", "fountain", "fountains", "four", "fourfold",
        "fourteen", "fourteenth", "fourth",
        # "with" prefix
        "withdraw", "withdrawn", "withdrew", "wither", "withered",
        "withhold", "within", "without", "withstand", "withstood",
        "witness", "witnesses", "witnessed",
        # "from" prefix — "from" + word rarely forms real words
        # "on" prefix
        "once", "one", "ones", "oneself", "only", "onward", "onwards",
        # "by" prefix
        "bypass",
        # "under" prefix
        "undergo", "undergoes", "undergone", "underground", "undergird",
        "undergirding", "undergirded", "underline", "underlying",
        "undermine", "undermined", "underneath", "understand",
        "understanding", "understood", "undertake", "undertaken",
        "undertaking", "undertook",
        # "in" prefix — theological/archaic terms
        "incorruption", "incorruptible", "incorruptibility",
        "inlaw",
        # "un" prefix — via "until" etc.
        "untilled", "untouched", "unused", "unusual",
        # "at" prefix
        "atmosphere", "atone", "atoned", "atonement", "attach", "attached",
        "attack", "attacked", "attain", "attained", "attempt", "attempted",
        "attend", "attended", "attention", "attire", "attired", "attitude",
        "attract", "attracted", "attribute", "attributed",
        # "as" prefix
        "ascend", "ascended", "ascending", "ascent", "ashamed", "ashes",
        "ashore", "aside", "ask", "asked", "asleep", "aspect",
        "assemble", "assembled", "assemblies", "assembly", "assert",
        "assess", "assign", "assigned", "assist", "associate",
        "assume", "assumed", "assurance", "assure", "assured",
        "astonished", "astonishment", "astray",
        # "and" prefix
        "ancestor", "ancestors", "anchor", "ancient", "ancients",
        "anew", "angel", "angels", "anger", "angry", "anguish",
        "animal", "animals", "ankle", "announce", "announced",
        "annoy", "annual", "anoint", "anointed", "anointing",
        "another", "answer", "answered", "answers", "ant", "antichrist",
        "anticipate", "antiquity", "anvil", "anxiety", "anxious",
        "any", "anyone", "anything", "anyway", "anywhere",
        # "but" prefix
        "butler", "butter", "button", "buttress",
        # "that" prefix
        "thatch",
        # "then" prefix — "then" + word: careful
        # "which" prefix — very few real words
        # "through" prefix
        "throughout",
        # "between" — no common suffixed words
        # Common biblical names that start with preposition-like prefixes
        "israel", "isaac", "isaiah", "ishmael", "ishmaelites",
        "indonesia", "india", "indian",
        "bethel", "bethlehem", "benjamin", "beersheba",
        "asher", "assyria", "assyrian", "assyrians", "athenians", "athens",
        "antioch", "andrew", "ananias", "annas",
        "tobias", "tobit",
        "jordan",
        "foreign",
    }


def _is_real_word(word: str) -> bool:
    """Check if a word is a known English word, not a fused compound."""
    global _ENGLISH_WORDS_CACHE
    if _ENGLISH_WORDS_CACHE is None:
        _ENGLISH_WORDS_CACHE = _load_false_positive_words()
    return word.lower() in _ENGLISH_WORDS_CACHE


# ── Aspell integration ──────────────────────────────────────────────────────

def _aspell_available() -> bool:
    return shutil.which("aspell") is not None


def _aspell_check_batch(words: list[str]) -> set[str]:
    """Check a batch of words against aspell, return unknown ones."""
    if not words or not _aspell_available():
        return set()
    text = "\n".join(words)
    proc = subprocess.run(
        ["aspell", "list", "--lang=en"],
        input=text, capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0:
        return set()
    return set(proc.stdout.strip().splitlines()) if proc.stdout.strip() else set()


def _load_biblical_allowlist() -> set[str]:
    """Load biblical names allowlist if available."""
    if BIBLICAL_NAMES.exists():
        return set(BIBLICAL_NAMES.read_text(encoding="utf-8").splitlines())
    return set()


# ── File discovery ──────────────────────────────────────────────────────────

def discover_files(scope: str, include_staging: bool,
                   single_file: Path | None = None) -> list[Path]:
    """Discover all files to proofread."""
    if single_file:
        return [single_file]

    files = []
    if scope in ("all", "canon"):
        for d in (CANON_OT, CANON_NT):
            if d.exists():
                files.extend(sorted(d.glob("*.md")))

    if scope == "all" and include_staging:
        for d in (STAGING_OT, STAGING_NT):
            if d.exists():
                files.extend(sorted(d.glob("*_footnotes.md")))
                files.extend(sorted(d.glob("*_articles.md")))

    if scope == "staging":
        for d in (STAGING_OT, STAGING_NT):
            if d.exists():
                files.extend(sorted(d.glob("*.md")))

    return files


# ── Core analysis ───────────────────────────────────────────────────────────

class Finding:
    """A single proofreading finding."""
    __slots__ = ("file", "line_num", "anchor", "code", "message",
                 "original", "suggested", "auto_fixable", "context")

    def __init__(self, file: str, line_num: int, anchor: str, code: str,
                 message: str, original: str, suggested: str,
                 auto_fixable: bool, context: str = ""):
        self.file = file
        self.line_num = line_num
        self.anchor = anchor
        self.code = code
        self.message = message
        self.original = original
        self.suggested = suggested
        self.auto_fixable = auto_fixable
        self.context = context

    def to_dict(self) -> dict:
        return {
            "file": self.file,
            "line": self.line_num,
            "anchor": self.anchor,
            "code": self.code,
            "message": self.message,
            "original": self.original,
            "suggested": self.suggested,
            "auto_fixable": self.auto_fixable,
            "context": self.context,
        }


def _check_fused_compounds(text: str, anchor: str, file_str: str,
                           line_num: int, prefixes: list[str],
                           code: str, label: str) -> list[Finding]:
    """Check for fused prefix+word patterns.

    Strategy: only flag a token when ALL of these are true:
      1. It starts with a known prefix
      2. The full token is NOT in our false-positive word list
      3. The full token is NOT recognized by aspell (i.e. it's misspelled)
      4. The remainder (after splitting) IS recognized by aspell
    This dramatically reduces false positives — real English words like
    'afternoon', 'understand', 'sojourner' pass the aspell gate and are skipped.
    """
    findings = []

    # Batch-collect all candidate tokens first, then aspell-check them together
    candidates: list[tuple[re.Match, str]] = []
    for prefix in prefixes:
        pattern = re.compile(
            r'\b(' + re.escape(prefix) + r')([a-z]{3,})\b',
            re.IGNORECASE
        )
        for m in pattern.finditer(text):
            full_token = m.group(0)
            if _is_real_word(full_token):
                continue
            candidates.append((m, prefix))

    if not candidates:
        return findings

    # Batch aspell check: full tokens + remainders
    all_tokens = list({m.group(0).lower() for m, _ in candidates})
    all_remainders = list({m.group(2).lower() for m, _ in candidates})
    unknown_tokens = _aspell_check_batch(all_tokens)
    unknown_remainders = _aspell_check_batch(all_remainders)

    for m, prefix in candidates:
        full_token = m.group(0)
        remainder = m.group(2)

        # Gate 1: if aspell recognizes the fused form, it's a real word — skip
        if full_token.lower() not in unknown_tokens:
            continue

        # Gate 2: the remainder should be a real word for this to be a fusion
        if remainder.lower() in unknown_remainders:
            continue

        # Gate 3: if the full token starts with uppercase and looks like a
        # proper noun (biblical name), skip it — names like Orpah, Assir,
        # Sostratus, Orion are not fused compounds
        if full_token[0].isupper() and remainder[0].islower():
            continue  # e.g. "Ingathering" — prefix capitalized, remainder lower
        if full_token[0].isupper() and full_token not in unknown_tokens:
            continue  # aspell knows the capitalized form

        suggestion = f"{m.group(1)} {remainder}"
        findings.append(Finding(
            file=file_str, line_num=line_num, anchor=anchor,
            code=code,
            message=f"{label}: '{full_token}' → '{suggestion}'",
            original=full_token, suggested=suggestion,
            auto_fixable=False,
            context=text,
        ))

    return findings


def analyze_line_regex(text: str, anchor: str, file_str: str,
                       line_num: int) -> tuple[str, list[Finding]]:
    """Run regex-based checks (P1-P5, P7, P8) on a single verse line.
    Returns (fixed_text, findings)."""
    findings: list[Finding] = []
    fixed = text

    # P1: Missing space after punctuation
    for m in RE_MISSING_SPACE.finditer(text):
        punct, letter = m.group(1), m.group(2)
        orig = f"{punct}{letter}"
        sugg = f"{punct} {letter}"
        findings.append(Finding(
            file=file_str, line_num=line_num, anchor=anchor,
            code="P1", message=f"Missing space after '{punct}': '{orig}' → '{sugg}'",
            original=orig, suggested=sugg, auto_fixable=True, context=text,
        ))
    fixed = RE_MISSING_SPACE.sub(r'\1 \2', fixed)

    for m in RE_MISSING_SPACE_PERIOD.finditer(text):
        letter = m.group(2)
        orig = f".{letter}"
        sugg = f". {letter}"
        findings.append(Finding(
            file=file_str, line_num=line_num, anchor=anchor,
            code="P1", message=f"Missing space after '.': '{orig}' → '{sugg}'",
            original=orig, suggested=sugg, auto_fixable=True, context=text,
        ))
    fixed = RE_MISSING_SPACE_PERIOD.sub(r'\1 \2', fixed)

    # P2: Space before punctuation
    for m in RE_SPACE_BEFORE_PUNCT.finditer(fixed):
        punct = m.group(1)
        findings.append(Finding(
            file=file_str, line_num=line_num, anchor=anchor,
            code="P2", message=f"Space before '{punct}'",
            original=f" {punct}", suggested=punct,
            auto_fixable=True, context=text,
        ))
    fixed = RE_SPACE_BEFORE_PUNCT.sub(r'\1', fixed)
    fixed = RE_SPACE_BEFORE_POSSESSIVE.sub(r"\1", fixed)

    # P3: Double words
    for m in RE_DOUBLE_WORD.finditer(fixed):
        word = m.group(1)
        findings.append(Finding(
            file=file_str, line_num=line_num, anchor=anchor,
            code="P3", message=f"Double word: '{word} {word}'",
            original=f"{word} {word}", suggested=word,
            auto_fixable=True, context=text,
        ))
    fixed = RE_DOUBLE_WORD.sub(r'\1', fixed)

    # P5: Multiple consecutive spaces
    if RE_MULTI_SPACE.search(fixed):
        findings.append(Finding(
            file=file_str, line_num=line_num, anchor=anchor,
            code="P5", message="Multiple consecutive spaces",
            original="(multiple spaces)", suggested="(single space)",
            auto_fixable=True, context=text,
        ))
    fixed = RE_MULTI_SPACE.sub(' ', fixed)

    # P4: Fused preposition+word (review only)
    findings.extend(_check_fused_compounds(
        text, anchor, file_str, line_num,
        _PREPOSITIONS, "P4", "Fused preposition"
    ))

    # P8: Fused conjunction+word (review only)
    findings.extend(_check_fused_compounds(
        text, anchor, file_str, line_num,
        _CONJUNCTIONS, "P8", "Fused conjunction"
    ))

    # P7: Unbalanced quotes (report only)
    single_count = len(RE_SINGLE_QUOTE.findall(text))
    double_count = len(RE_DOUBLE_QUOTE.findall(text))
    if double_count % 2 != 0:
        findings.append(Finding(
            file=file_str, line_num=line_num, anchor=anchor,
            code="P7", message=f"Unbalanced double quotes (count={double_count})",
            original="", suggested="",
            auto_fixable=False, context=text,
        ))

    return fixed, findings


def analyze_file_spell(filepath: Path,
                       allowlist: set[str]) -> list[Finding]:
    """Run aspell-based spell check (P6) on a file."""
    findings = []
    if not _aspell_available():
        return findings

    lines = filepath.read_text(encoding="utf-8").splitlines()
    in_frontmatter = False
    verses: list[tuple[int, str, str]] = []  # (line_num, anchor, text)

    for i, line in enumerate(lines, 1):
        if RE_FRONTMATTER.match(line):
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter or RE_HEADING.match(line):
            continue
        m = RE_ANCHOR.match(line)
        if m:
            verses.append((i, m.group(1), m.group(2)))

    # Batch all words for aspell
    all_words: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for line_num, anchor, text in verses:
        words = re.findall(r"[A-Za-z']+", text)
        for w in words:
            if len(w) >= 2 and w not in allowlist and w.lower() not in allowlist:
                all_words[w].append((line_num, anchor))

    if not all_words:
        return findings

    unknown = _aspell_check_batch(list(all_words.keys()))

    for word in sorted(unknown):
        if word in allowlist or word.lower() in allowlist:
            continue
        for line_num, anchor in all_words[word]:
            findings.append(Finding(
                file=str(filepath), line_num=line_num, anchor=anchor,
                code="P6", message=f"Unknown word: '{word}'",
                original=word, suggested="",
                auto_fixable=False, context="",
            ))

    return findings


# ── File processing ─────────────────────────────────────────────────────────

def process_file(filepath: Path, passes: list[str],
                 apply_fixes: bool,
                 allowlist: set[str]) -> tuple[list[Finding], dict]:
    """Process a single file through specified passes.
    Returns (findings, stats)."""
    all_findings: list[Finding] = []
    stats = {"lines_checked": 0, "lines_fixed": 0, "findings": 0}
    file_str = str(filepath)

    lines = filepath.read_text(encoding="utf-8").splitlines()
    fixed_lines = []
    in_frontmatter = False
    frontmatter_done = False

    if "regex" in passes:
        for i, line in enumerate(lines, 1):
            # Handle frontmatter
            if line.strip() == "---":
                if not frontmatter_done:
                    in_frontmatter = not in_frontmatter
                    if not in_frontmatter:
                        frontmatter_done = True
                fixed_lines.append(line)
                continue

            if in_frontmatter or RE_HEADING.match(line):
                fixed_lines.append(line)
                continue

            m = RE_ANCHOR.match(line)
            if not m:
                fixed_lines.append(line)
                continue

            anchor = m.group(1)
            text = m.group(2)
            stats["lines_checked"] += 1

            fixed_text, findings = analyze_line_regex(
                text, anchor, file_str, i
            )

            if findings:
                all_findings.extend(findings)
                stats["findings"] += len(findings)

            if fixed_text != text:
                stats["lines_fixed"] += 1
                if apply_fixes:
                    fixed_lines.append(f"{anchor} {fixed_text}")
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)

        if apply_fixes and stats["lines_fixed"] > 0:
            filepath.write_text("\n".join(fixed_lines) + "\n", encoding="utf-8")

    if "spell" in passes:
        spell_findings = analyze_file_spell(filepath, allowlist)
        all_findings.extend(spell_findings)
        stats["findings"] += len(spell_findings)

    return all_findings, stats


# ── Reporting ───────────────────────────────────────────────────────────────

def build_report(all_findings: list[Finding], all_stats: dict,
                 scope: str, applied: bool) -> dict:
    """Build a structured JSON report."""
    by_code: dict[str, int] = defaultdict(int)
    by_file: dict[str, int] = defaultdict(int)
    auto_fixable = 0
    review_needed = 0

    for f in all_findings:
        by_code[f.code] += 1
        by_file[f.file] += 1
        if f.auto_fixable:
            auto_fixable += 1
        else:
            review_needed += 1

    return {
        "generated": str(date.today()),
        "scope": scope,
        "applied": applied,
        "summary": {
            "total_findings": len(all_findings),
            "auto_fixable": auto_fixable,
            "review_needed": review_needed,
            "files_checked": all_stats.get("files_checked", 0),
            "lines_checked": all_stats.get("lines_checked", 0),
            "lines_fixed": all_stats.get("lines_fixed", 0),
        },
        "by_category": dict(sorted(by_code.items())),
        "by_file": dict(sorted(by_file.items())),
        "findings": [f.to_dict() for f in all_findings],
    }


def build_memo(report: dict) -> str:
    """Build an Ezra-audit-compatible memo from the report."""
    today = date.today().isoformat()
    s = report["summary"]
    lines = [
        f"# Proofread Report — {today}\n",
        "\n",
        "## Summary\n",
        f"- Scope: {report['scope']}\n",
        f"- Applied: {report['applied']}\n",
        f"- Files checked: {s['files_checked']}\n",
        f"- Lines checked: {s['lines_checked']}\n",
        f"- Total findings: {s['total_findings']}\n",
        f"- Auto-fixable: {s['auto_fixable']}\n",
        f"- Review needed: {s['review_needed']}\n",
        f"- Lines fixed: {s['lines_fixed']}\n",
        "\n",
        "## By Category\n",
        "\n",
        "| Code | Count | Description |\n",
        "|------|-------|-------------|\n",
    ]
    code_desc = {
        "P1": "Missing space after punctuation",
        "P2": "Space before punctuation",
        "P3": "Double word",
        "P4": "Fused preposition+word",
        "P5": "Multiple consecutive spaces",
        "P6": "Spelling (aspell)",
        "P7": "Unbalanced quotes",
        "P8": "Fused conjunction+word",
    }
    for code, count in sorted(report["by_category"].items()):
        desc = code_desc.get(code, "Unknown")
        lines.append(f"| {code} | {count} | {desc} |\n")

    if report["findings"]:
        lines.extend([
            "\n",
            "## Sample Findings (first 50)\n",
            "\n",
            "| Anchor | Code | Message |\n",
            "|--------|------|---------|\n",
        ])
        for f in report["findings"][:50]:
            msg = f["message"].replace("|", "\\|")
            lines.append(f"| {f['anchor']} | {f['code']} | {msg} |\n")
        if len(report["findings"]) > 50:
            lines.append(f"\n*...and {len(report['findings']) - 50} more findings.*\n")

    return "".join(lines)


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Multi-pass proofreader for Orthodox Phronema canon files."
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--file", type=Path, help="Single file to proofread")
    target.add_argument("--scope", choices=["all", "canon", "staging"],
                        help="Scope: all, canon, or staging")

    parser.add_argument("--include-staging", action="store_true",
                        help="Include staging footnotes/articles (with --scope all)")
    parser.add_argument("--pass", dest="passes", action="append",
                        choices=["regex", "spell", "all"],
                        help="Which passes to run (default: all)")
    parser.add_argument("--apply", action="store_true",
                        help="Apply auto-fixable corrections in place")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Report only, no file changes (default)")
    parser.add_argument("--report-dir", type=Path, default=REPORTS_DIR,
                        help="Directory for JSON reports")
    parser.add_argument("--memo", action="store_true",
                        help="Also write an Ezra audit memo to memos/")

    args = parser.parse_args()

    # Determine passes
    if not args.passes or "all" in args.passes:
        passes = ["regex", "spell"]
    else:
        passes = args.passes

    if args.apply:
        args.dry_run = False

    # Discover files
    files = discover_files(
        scope=args.scope or "canon",
        include_staging=args.include_staging,
        single_file=args.file,
    )

    if not files:
        print("No files found to proofread.", file=sys.stderr)
        sys.exit(1)

    print(f"Proofreading {len(files)} files (passes: {', '.join(passes)})",
          file=sys.stderr)

    # Load allowlist for spell pass
    allowlist = _load_biblical_allowlist()

    all_findings: list[Finding] = []
    total_stats = {"files_checked": 0, "lines_checked": 0, "lines_fixed": 0}

    for filepath in files:
        findings, stats = process_file(
            filepath, passes,
            apply_fixes=args.apply,
            allowlist=allowlist,
        )
        all_findings.extend(findings)
        total_stats["files_checked"] += 1
        total_stats["lines_checked"] += stats["lines_checked"]
        total_stats["lines_fixed"] += stats["lines_fixed"]

        if findings:
            auto = sum(1 for f in findings if f.auto_fixable)
            review = len(findings) - auto
            print(f"  {filepath.name}: {len(findings)} findings "
                  f"({auto} auto, {review} review)", file=sys.stderr)

    # Build report
    report = build_report(
        all_findings, total_stats,
        scope=args.scope or str(args.file),
        applied=args.apply,
    )

    # Write report
    args.report_dir.mkdir(parents=True, exist_ok=True)
    report_path = args.report_dir / f"proofread_{date.today().isoformat()}.json"
    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"\nReport: {report_path}", file=sys.stderr)

    # Write memo if requested
    if args.memo:
        memo_text = build_memo(report)
        memo_path = MEMOS_DIR / f"proofread_report_{date.today().isoformat()}.md"
        memo_path.write_text(memo_text, encoding="utf-8")
        print(f"Memo: {memo_path}", file=sys.stderr)

    # Print summary
    s = report["summary"]
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"  Files checked:    {s['files_checked']}", file=sys.stderr)
    print(f"  Lines checked:    {s['lines_checked']}", file=sys.stderr)
    print(f"  Total findings:   {s['total_findings']}", file=sys.stderr)
    print(f"  Auto-fixable:     {s['auto_fixable']}", file=sys.stderr)
    print(f"  Review needed:    {s['review_needed']}", file=sys.stderr)
    if args.apply:
        print(f"  Lines fixed:      {s['lines_fixed']}", file=sys.stderr)
    else:
        print(f"  (dry-run — no changes applied)", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    # Exit code: 0 if no findings, 1 if findings exist
    sys.exit(0 if s["total_findings"] == 0 else 1)


if __name__ == "__main__":
    main()
