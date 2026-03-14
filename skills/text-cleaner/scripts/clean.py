#!/usr/bin/env python3
"""
clean.py — Generalized multi-pass text extraction cleaner for Orthodox Phronema.

Refactored from canon-proofreader to support profile-driven configuration.
Detects extraction artifacts (fused words, punctuation spacing, etc.) across
any text corpus using configurable profiles.

Error categories (P1–P8, same as proofread.py):
  P1  Missing space after punctuation   (auto-fix)
  P2  Space before punctuation           (auto-fix)
  P3  Double/repeated words              (auto-fix)
  P4  Fused preposition+word compounds   (review)
  P5  Multiple consecutive spaces        (auto-fix)
  P6  Spelling errors (aspell)           (review)
  P7  Unbalanced quotes                  (report only)
  P8  Fused conjunction+word             (review)

Usage:
    python3 clean.py --file path/to/file.md --profile canon --dry-run
    python3 clean.py --dir path/to/dir/ --profile default --apply
    python3 clean.py --dir path/to/dir/ --profile canon --json
    python3 clean.py --file path/to/file.md --scope canon
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    yaml = None

# ── Repo discovery ──────────────────────────────────────────────────────────
_THIS = Path(__file__).resolve().parent
_REPO = _THIS
while _REPO != _REPO.parent and not (_REPO / "pipeline" / "__init__.py").exists():
    _REPO = _REPO.parent

SKILLS_DIR = _REPO / "skills" / "text-cleaner"
PROFILES_DIR = SKILLS_DIR / "profiles"
REPORTS_DIR = _REPO / "reports" / "text-cleaner"
MEMOS_DIR = _REPO / "memos"

# Built-in scope mappings (scope -> directory mapping)
SCOPE_MAPPINGS = {
    "canon": _REPO / "canon",
    "canon_ot": _REPO / "canon" / "OT",
    "canon_nt": _REPO / "canon" / "NT",
    "staging": _REPO / "staging" / "validated",
    "staging_ot": _REPO / "staging" / "validated" / "OT",
    "staging_nt": _REPO / "staging" / "validated" / "NT",
}

# ── Regex patterns ──────────────────────────────────────────────────────────
RE_FRONTMATTER = re.compile(r'^---\s*$')
RE_HEADING = re.compile(r'^#{1,4}\s')

# P1: Missing space after punctuation
RE_MISSING_SPACE = re.compile(
    r'(?<![A-Z0-9])(?<!\d)'
    r'([,;:!?])'
    r'([A-Za-z])'
)
RE_MISSING_SPACE_PERIOD = re.compile(
    r'(?<!\.)(?<![A-Z])'
    r'(\.)(?!\.)'
    r'([A-Z])'
)

# P2: Space before punctuation
RE_SPACE_BEFORE_PUNCT = re.compile(r' ([,\.;:!?\)\]\}])')
RE_SPACE_BEFORE_POSSESSIVE = re.compile(r" ('s)\b")

# P3: Double words
RE_DOUBLE_WORD = re.compile(r'\b(\w{2,})\s+\1\b', re.IGNORECASE)

# P5: Multiple consecutive spaces
RE_MULTI_SPACE = re.compile(r'  +')

# P7: Quote counting
RE_SINGLE_QUOTE = re.compile(r"[''']")
RE_DOUBLE_QUOTE = re.compile(r'["""]')

# Cache for aspell-checked words
_ENGLISH_WORDS_CACHE: set[str] | None = None


# ── Profile Configuration ───────────────────────────────────────────────────

@dataclass
class Profile:
    """Configuration profile for text cleaning."""
    name: str = "default"
    description: str = ""

    # Line format: "anchor" (BOOK.CH:VS text), "plain" (every line), "numbered" (paragraphs)
    line_format: str = "anchor"

    # Regex to extract anchors from structured lines
    anchor_regex: str = r'^([A-Z0-9]+\.\d+:\d+)\s+(.*)'

    # Regex patterns for protected zones (never process these lines)
    protected_zones: list[str] = field(default_factory=list)

    # Path to domain-specific allowlist (relative to repo root)
    allowlist_path: Optional[str] = None

    # Prefixes to check for fused compounds (default: ["a"])
    fused_prefixes: list[str] = field(default_factory=lambda: ["a"])

    # Prepositions to check for P4 fused compounds
    prepositions: list[str] = field(default_factory=lambda: [
        "of", "in", "to", "for", "with", "from", "on", "by", "at", "as",
        "into", "upon", "over", "under", "after", "before", "between",
        "through", "about", "against", "among", "within", "without",
        "toward", "towards", "around", "beyond", "during", "until",
        "behind", "beside", "beneath", "above", "across", "along",
    ])

    # Conjunctions to check for P8 fused compounds
    conjunctions: list[str] = field(default_factory=lambda: [
        "and", "but", "or", "nor", "for", "yet", "so",
        "that", "when", "while", "where", "which", "because",
        "although", "though", "since", "unless", "whether",
        "if", "then", "than",
    ])

    # Known safe words (no fusion)
    false_positives: list[str] = field(default_factory=list)

    # Compiled regex patterns
    _compiled_protected: list[re.Pattern] = field(default_factory=list, init=False)
    _compiled_anchor: Optional[re.Pattern] = field(default=None, init=False)

    def __post_init__(self):
        """Compile regex patterns."""
        self._compiled_protected = [
            re.compile(zone) for zone in self.protected_zones
        ]
        if self.anchor_regex:
            self._compiled_anchor = re.compile(self.anchor_regex)

    def is_protected_line(self, line: str) -> bool:
        """Check if a line matches any protected zone pattern."""
        return any(p.match(line) for p in self._compiled_protected)

    def extract_anchor(self, line: str) -> tuple[str, str] | None:
        """Extract anchor and text from a line. Returns (anchor, text) or None."""
        if not self._compiled_anchor:
            return None
        m = self._compiled_anchor.match(line)
        if m:
            return (m.group(1), m.group(2))
        return None


def load_profile(profile_name: str) -> Profile:
    """Load a profile from YAML or return defaults."""
    profile_path = PROFILES_DIR / f"{profile_name}.yaml"

    if profile_path.exists() and yaml:
        try:
            data = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
            if data:
                return Profile(
                    name=data.get("name", profile_name),
                    description=data.get("description", ""),
                    line_format=data.get("line_format", "anchor"),
                    anchor_regex=data.get("anchor_regex", ""),
                    protected_zones=data.get("protected_zones", [
                        r'^---\s*$', r'^#{1,4}\s'
                    ]),
                    allowlist_path=data.get("allowlist"),
                    fused_prefixes=data.get("fused_prefixes", ["a"]),
                    prepositions=data.get("prepositions") or [
                        "of", "in", "to", "for", "with", "from", "on", "by", "at", "as",
                        "into", "upon", "over", "under", "after", "before", "between",
                        "through", "about", "against", "among", "within", "without",
                        "toward", "towards", "around", "beyond", "during", "until",
                        "behind", "beside", "beneath", "above", "across", "along",
                    ],
                    conjunctions=data.get("conjunctions") or [
                        "and", "but", "or", "nor", "for", "yet", "so",
                        "that", "when", "while", "where", "which", "because",
                        "although", "though", "since", "unless", "whether",
                        "if", "then", "than",
                    ],
                    false_positives=data.get("false_positives") or [],
                )
        except Exception as e:
            print(f"Warning: could not load profile {profile_path}: {e}",
                  file=sys.stderr)

    # Fall back to defaults
    return Profile(name=profile_name)


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


def _load_allowlist(profile: Profile) -> set[str]:
    """Load allowlist from profile path or return empty set."""
    if not profile.allowlist_path:
        return set()
    allowlist_path = _REPO / profile.allowlist_path
    if allowlist_path.exists():
        return set(allowlist_path.read_text(encoding="utf-8").splitlines())
    return set()


def _make_false_positive_set(profile: Profile) -> set[str]:
    """Build a set of known safe words from profile."""
    return set(w.lower() for w in profile.false_positives)


# ── File discovery ──────────────────────────────────────────────────────────

def discover_files(
    file_path: Optional[Path] = None,
    dir_path: Optional[Path] = None,
    scope: Optional[str] = None,
) -> list[Path]:
    """Discover files to process."""
    if file_path:
        return [file_path]

    if dir_path:
        if dir_path.is_file():
            return [dir_path]
        if dir_path.is_dir():
            return sorted(dir_path.glob("*.md"))
        return []

    if scope:
        if scope in SCOPE_MAPPINGS:
            scope_dir = SCOPE_MAPPINGS[scope]
            if scope_dir.exists():
                return sorted(scope_dir.rglob("*.md"))

    return []


# ── Core analysis ───────────────────────────────────────────────────────────

class Finding:
    """A single cleaning finding."""
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


def _check_fused_compounds(
    text: str,
    anchor: str,
    file_str: str,
    line_num: int,
    prefixes: list[str],
    code: str,
    label: str,
    false_positives: set[str],
) -> list[Finding]:
    """Check for fused prefix+word patterns using aspell-gated detection."""
    findings = []

    candidates: list[tuple[re.Match, str]] = []
    for prefix in prefixes:
        pattern = re.compile(
            r'\b(' + re.escape(prefix) + r')([a-z]{3,})\b',
            re.IGNORECASE
        )
        for m in pattern.finditer(text):
            full_token = m.group(0)
            if full_token.lower() in false_positives:
                continue
            candidates.append((m, prefix))

    if not candidates:
        return findings

    # Batch aspell check
    all_tokens = list({m.group(0).lower() for m, _ in candidates})
    all_remainders = list({m.group(2).lower() for m, _ in candidates})
    unknown_tokens = _aspell_check_batch(all_tokens)
    unknown_remainders = _aspell_check_batch(all_remainders)

    for m, prefix in candidates:
        full_token = m.group(0)
        remainder = m.group(2)

        # Gate 1: if aspell recognizes the full token, skip it
        if full_token.lower() not in unknown_tokens:
            continue

        # Gate 2: the remainder should be recognized
        if remainder.lower() in unknown_remainders:
            continue

        # Gate 3: skip apparent proper nouns
        if full_token[0].isupper() and remainder[0].islower():
            continue
        if full_token[0].isupper() and full_token not in unknown_tokens:
            continue

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


def analyze_line_regex(
    text: str,
    anchor: str,
    file_str: str,
    line_num: int,
    profile: Profile,
    false_positives: set[str],
) -> tuple[str, list[Finding]]:
    """Run regex-based checks (P1-P5, P7, P8) on a single line."""
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

    # P4: Fused preposition+word
    findings.extend(_check_fused_compounds(
        text, anchor, file_str, line_num,
        profile.prepositions, "P4", "Fused preposition",
        false_positives,
    ))

    # P8: Fused conjunction+word
    findings.extend(_check_fused_compounds(
        text, anchor, file_str, line_num,
        profile.conjunctions, "P8", "Fused conjunction",
        false_positives,
    ))

    # P7: Unbalanced quotes
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


def analyze_file_spell(
    filepath: Path,
    profile: Profile,
    allowlist: set[str],
) -> list[Finding]:
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
        if in_frontmatter or RE_HEADING.match(line) or profile.is_protected_line(line):
            continue

        if profile.line_format == "anchor":
            result = profile.extract_anchor(line)
            if result:
                anchor, text = result
                verses.append((i, anchor, text))
        else:
            # Plain line format: treat entire line as content
            verses.append((i, "", line))

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


def process_file(
    filepath: Path,
    profile: Profile,
    passes: list[str],
    apply_fixes: bool,
    allowlist: set[str],
) -> tuple[list[Finding], dict]:
    """Process a single file through specified passes."""
    all_findings: list[Finding] = []
    stats = {"lines_checked": 0, "lines_fixed": 0, "findings": 0}
    file_str = str(filepath)

    false_positives = _make_false_positive_set(profile)

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

            if in_frontmatter or RE_HEADING.match(line) or profile.is_protected_line(line):
                fixed_lines.append(line)
                continue

            if profile.line_format == "anchor":
                result = profile.extract_anchor(line)
                if not result:
                    fixed_lines.append(line)
                    continue
                anchor, text = result
            else:
                # Plain line format
                if not line.strip():
                    fixed_lines.append(line)
                    continue
                anchor = ""
                text = line

            stats["lines_checked"] += 1

            fixed_text, findings = analyze_line_regex(
                text, anchor, file_str, i, profile, false_positives
            )

            if findings:
                all_findings.extend(findings)
                stats["findings"] += len(findings)

            if fixed_text != text:
                stats["lines_fixed"] += 1
                if apply_fixes:
                    if profile.line_format == "anchor" and anchor:
                        fixed_lines.append(f"{anchor} {fixed_text}")
                    else:
                        fixed_lines.append(fixed_text)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)

        if apply_fixes and stats["lines_fixed"] > 0:
            filepath.write_text("\n".join(fixed_lines) + "\n", encoding="utf-8")

    if "spell" in passes:
        spell_findings = analyze_file_spell(filepath, profile, allowlist)
        all_findings.extend(spell_findings)
        stats["findings"] += len(spell_findings)

    return all_findings, stats


# ── Reporting ───────────────────────────────────────────────────────────────

def build_report(
    all_findings: list[Finding],
    all_stats: dict,
    profile_name: str,
    applied: bool,
    output_format: str,
) -> dict:
    """Build a structured report."""
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
        "profile": profile_name,
        "format": output_format,
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


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generalized multi-pass text extraction cleaner."
    )

    # Target selection
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--file", type=Path, help="Single file to process")
    target.add_argument("--dir", type=Path, help="Directory to process")
    target.add_argument("--scope", choices=list(SCOPE_MAPPINGS.keys()),
                        help="Predefined scope (e.g., canon, staging)")

    # Profile and processing options
    parser.add_argument("--profile", default="default",
                        help="Profile name (default: default)")
    parser.add_argument("--pass", dest="passes", action="append",
                        choices=["regex", "spell", "all"],
                        help="Which passes to run (default: all)")
    parser.add_argument("--apply", action="store_true",
                        help="Apply auto-fixable corrections in place")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Report only, no file changes (default)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON (machine-readable)")
    parser.add_argument("--report-dir", type=Path, default=REPORTS_DIR,
                        help="Directory for JSON reports")

    args = parser.parse_args()

    # Load profile
    profile = load_profile(args.profile)
    print(f"Profile: {profile.name}", file=sys.stderr)

    # Determine passes
    if not args.passes or "all" in args.passes:
        passes = ["regex", "spell"]
    else:
        passes = args.passes

    if args.apply:
        args.dry_run = False

    # Discover files
    files = discover_files(
        file_path=args.file,
        dir_path=args.dir,
        scope=args.scope,
    )

    if not files:
        print("No files found to process.", file=sys.stderr)
        sys.exit(1)

    print(f"Processing {len(files)} files (passes: {', '.join(passes)})",
          file=sys.stderr)

    # Load allowlist
    allowlist = _load_allowlist(profile)

    all_findings: list[Finding] = []
    total_stats = {"files_checked": 0, "lines_checked": 0, "lines_fixed": 0}

    for filepath in files:
        findings, stats = process_file(
            filepath, profile, passes,
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
    output_format = "json" if args.json else "text"
    report = build_report(
        all_findings, total_stats,
        profile_name=args.profile,
        applied=args.apply,
        output_format=output_format,
    )

    # Output report
    if args.json:
        # JSON output to stdout
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        # Human-readable summary to stderr
        s = report["summary"]
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"  Profile:          {args.profile}", file=sys.stderr)
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

    # Write report file
    args.report_dir.mkdir(parents=True, exist_ok=True)
    report_path = args.report_dir / f"clean_{args.profile}_{date.today().isoformat()}.json"
    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Report: {report_path}", file=sys.stderr)

    # Exit code: 0 if no findings, 1 if findings exist
    sys.exit(0 if s["total_findings"] == 0 else 1)


if __name__ == "__main__":
    main()
