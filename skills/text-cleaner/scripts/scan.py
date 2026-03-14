#!/usr/bin/env python3
"""
scan.py — Generalized deep fused-token scanner for text extraction artifacts.

Refactored from canon-proofreader/scripts/deep_scan.py, now profile-driven
to work on any text corpus with configurable detection rules.

Deep scanning targets error patterns:
  D1  Fused single-letter footnote markers (a+word, b+word, c+word, etc.)
  D2  Fused article "a" before any word (not just known biblical targets)
  D3  Residual OCR kerning splits ("J ESUS", "Dav id", "L ORD")
  D4  Stray footnote markers (isolated a/b/c letters mid-verse)
  D5  Fused prepositions/conjunctions + word (broader than fix_articles.py)
  D6  Missing article "a" (contextual — where "a" was stripped as footnote marker)

Usage:
    python3 scan.py --file path/to/file.md --profile canon
    python3 scan.py --dir path/to/dir/ --profile default
    python3 scan.py --dir path/to/dir/ --profile canon --json
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

# ── Regex patterns ──────────────────────────────────────────────────────────
RE_FRONTMATTER = re.compile(r'^---\s*$')


# ── Profile Configuration ───────────────────────────────────────────────────

@dataclass
class Profile:
    """Configuration profile for text scanning."""
    name: str = "default"
    description: str = ""

    # Line format: "anchor" (BOOK.CH:VS text), "plain" (every line), "numbered" (paragraphs)
    line_format: str = "anchor"

    # Regex to extract anchors from structured lines
    anchor_regex: str = r'^([A-Z0-9]+\.\d+:\d+)\s+(.*)'

    # Regex patterns for protected zones (never scan these lines)
    protected_zones: list[str] = field(default_factory=list)

    # Path to domain-specific allowlist (relative to repo root)
    allowlist_path: Optional[str] = None

    # Prefixes to check for fused compounds (default: ["a"])
    fused_prefixes: list[str] = field(default_factory=lambda: ["a"])

    # Prepositions to check for D5 fused compounds
    prepositions: list[str] = field(default_factory=lambda: [
        "of", "in", "to", "for", "with", "from", "on", "by", "at", "as",
        "into", "upon", "over", "under", "after", "before", "between",
        "through", "about", "against", "among", "within", "without",
        "toward", "towards", "around", "beyond", "during", "until",
        "behind", "beside", "beneath", "above", "across", "along",
    ])

    # Conjunctions to check for D5 fused compounds
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
    """Check if aspell is available."""
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


def _aspell_known(word: str) -> bool:
    """Return True if aspell accepts the word."""
    if not word or not _aspell_available():
        return False
    proc = subprocess.run(
        ["aspell", "list", "--lang=en"],
        input=f"{word}\n",
        capture_output=True, text=True, check=False,
    )
    return proc.stdout.strip() == ""


def _load_allowlist(profile: Profile) -> set[str]:
    """Load allowlist from profile path or return empty set."""
    if not profile.allowlist_path:
        return set()
    allowlist_path = _REPO / profile.allowlist_path
    if allowlist_path.exists():
        return set(w.lower() for w in allowlist_path.read_text(encoding="utf-8").splitlines())
    return set()


def _make_false_positive_set(profile: Profile) -> set[str]:
    """Build a set of known safe words from profile."""
    return set(w.lower() for w in profile.false_positives)


# ── Scanning functions ──────────────────────────────────────────────────────

def scan_fused_markers(
    text: str,
    anchor: str,
    profile: Profile,
    safe_words: set[str],
) -> list[dict]:
    """Scan verse text for fused single-letter footnote markers (D1).

    Pattern: look for words where removing the first letter (from fused_prefixes)
    produces a valid English word, but the full form is NOT a valid word.
    """
    findings = []

    # Pattern: look for words where first letter is a fused prefix
    pattern = r'\b([a-z]\w{2,})\b'
    words_in_verse = re.findall(pattern, text)
    if not words_in_verse:
        return findings

    # Quick batch: check all words at once
    unknown = _aspell_check_batch(words_in_verse)

    for word in words_in_verse:
        if word not in unknown:
            continue  # aspell knows this word — it's fine
        if word.lower() in safe_words:
            continue

        first_letter = word[0]
        remainder = word[1:]

        # Only check prefixes specified in profile
        if first_letter not in profile.fused_prefixes:
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


def scan_fused_article_a(text: str, anchor: str, safe_words: set[str]) -> list[dict]:
    """Scan for fused article 'a' + word patterns that aspell doesn't catch (D2).

    Pattern: lowercase 'a' directly fused to a word that starts with a capital letter.
    These are almost certainly article + proper noun.
    """
    findings = []

    # Look for patterns like "aHook", "aCenturion" (lowercase a + Capital word)
    for m in re.finditer(r'\ba([A-Z][a-z]{2,})\b', text):
        word = m.group(0)
        if word.lower() in safe_words:
            continue
        remainder = m.group(1)
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
    """Scan for OCR kerning splits (space inserted mid-word) (D3).

    Common patterns from Docling/OSB: "J ESUS", "Dav id", "L ORD", etc.
    """
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


def scan_fused_common_words(
    text: str,
    anchor: str,
    profile: Profile,
    safe_words: set[str],
) -> list[dict]:
    """Scan for fused prepositions/conjunctions + word (D5).

    Patterns: prepositions and conjunctions fused to following words.
    """
    findings = []

    # Build patterns from profile prepositions and conjunctions
    all_common = profile.prepositions + profile.conjunctions
    all_common_lower = [w.lower() for w in all_common]

    # Build regex patterns: each common word + common follow-ups
    for common_word in profile.prepositions + profile.conjunctions:
        # Build a pattern: common_word + (other common word or article)
        follow_ups = ["the", "his", "her", "its", "their", "my", "your", "our",
                      "this", "that", "these", "those", "God", "whom", "which",
                      "all", "man", "men", "one", "he", "she", "it", "they",
                      "we", "you", "me", "us", "when", "then", "said"]

        pattern_str = rf'\b({re.escape(common_word)})(' + '|'.join(follow_ups) + r')\b'
        for m in re.finditer(pattern_str, text, re.IGNORECASE):
            full = m.group(0)
            if full.lower() in safe_words:
                continue

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


def scan_text(
    text: str,
    anchor: str,
    profile: Profile,
    safe_words: set[str],
) -> list[dict]:
    """Run all scans on a single line of text."""
    findings = []
    findings.extend(scan_fused_markers(text, anchor, profile, safe_words))
    findings.extend(scan_fused_article_a(text, anchor, safe_words))
    findings.extend(scan_kerning_splits(text, anchor))
    findings.extend(scan_fused_common_words(text, anchor, profile, safe_words))
    return findings


def scan_file(filepath: Path, profile: Profile, safe_words: set[str]) -> list[dict]:
    """Deep-scan a single file. Returns all findings."""
    lines = filepath.read_text(encoding="utf-8").splitlines()
    all_findings = []
    in_frontmatter = False
    frontmatter_done = False

    for line in lines:
        # Handle frontmatter
        if line.strip() == "---":
            if not frontmatter_done:
                in_frontmatter = not in_frontmatter
                if not in_frontmatter:
                    frontmatter_done = True
            continue

        # Skip protected lines
        if in_frontmatter or profile.is_protected_line(line):
            continue

        # Extract anchor and text (or just use text for plain lines)
        anchor_text = profile.extract_anchor(line)
        if anchor_text:
            anchor, text = anchor_text
        elif profile.line_format == "plain":
            anchor = filepath.name
            text = line
        else:
            continue

        # Run all scans
        all_findings.extend(scan_text(text, anchor, profile, safe_words))

    return all_findings


def discover_files(
    file_path: Optional[Path] = None,
    dir_path: Optional[Path] = None,
) -> list[Path]:
    """Discover files to scan."""
    if file_path:
        return [file_path]
    elif dir_path:
        if dir_path.is_dir():
            return sorted(dir_path.glob("**/*.md"))
    return []


def main():
    parser = argparse.ArgumentParser(
        description="Generalized deep fused-token scanner for extracted text"
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--file", type=Path, help="Single file to scan")
    target.add_argument("--dir", type=Path, help="Directory to scan (recursive)")

    parser.add_argument(
        "--profile", default="default",
        help="Profile name (without .yaml extension)"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="JSON output instead of human-readable"
    )
    args = parser.parse_args()

    # Load profile
    profile = load_profile(args.profile)
    safe_words = _make_false_positive_set(profile)

    # Discover files
    files = discover_files(
        file_path=args.file,
        dir_path=args.dir,
    )

    if not files:
        print("No files found to scan.", file=sys.stderr)
        sys.exit(1)

    # Scan all files
    all_findings = []
    for filepath in files:
        findings = scan_file(filepath, profile, safe_words)
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

        print(f"\n{'='*70}", file=sys.stderr)
        print(f"  Total findings: {len(all_findings)} (profile: {profile.name})",
              file=sys.stderr)
        for t in sorted(by_type.keys()):
            items = by_type[t]
            print(f"  {t}: {len(items)}", file=sys.stderr)
        print(f"{'='*70}\n", file=sys.stderr)

        # Print all findings
        for f in all_findings:
            print(
                f"{f['anchor']:15s} [{f['type']}] {f['token']:20s} "
                f"→ {f['suggestion']:20s}  ({f['note']})"
            )


if __name__ == "__main__":
    main()
