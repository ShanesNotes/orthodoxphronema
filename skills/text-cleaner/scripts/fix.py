#!/usr/bin/env python3
"""
fix.py — Generalized curated fused-token fixer for text extraction artifacts.

Refactored from canon-proofreader/scripts/fix_fused_markers.py, now profile-driven
and replacement-map-driven to support any text corpus.

A "fused token" is a word artifact from OCR/extraction where a footnote marker
(like 'a', 'b', 'c') merged with the following word. This tool applies a curated
replacement map to fix these tokens.

Replacement maps are JSON files organized by replacement strategy:
  - strip: Remove the prefix (verbs, function words, determiner contexts)
  - article: Insert "a " before the word (nouns, adjectives before nouns)
  - context: Replace multi-word patterns (e.g., "along time" → "a long time")

Usage:
    # Apply fixes using a curated replacement map
    python3 fix.py --dir path/to/corpus/ --map replacements.json --profile canon
    python3 fix.py --dir path/to/corpus/ --map replacements.json --dry-run
    python3 fix.py --file path/to/file.md --map replacements.json

    # Generate a draft map from scan output
    python3 fix.py --generate-map scan_output.json --output draft_map.json

    # Auto-discover map from profile
    python3 fix.py --dir path/to/corpus/ --profile canon
"""
from __future__ import annotations

import argparse
import json
import re
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

# ── Profile Configuration ───────────────────────────────────────────────────


@dataclass
class Profile:
    """Configuration profile for text fixing."""
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

    # Prepositions to check for fused compounds
    prepositions: list[str] = field(default_factory=lambda: [
        "of", "in", "to", "for", "with", "from", "on", "by", "at", "as",
        "into", "upon", "over", "under", "after", "before", "between",
        "through", "about", "against", "among", "within", "without",
        "toward", "towards", "around", "beyond", "during", "until",
        "behind", "beside", "beneath", "above", "across", "along",
    ])

    # Conjunctions to check for fused compounds
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


@dataclass
class ReplacementMap:
    """Curated replacement map loaded from JSON."""
    strip: dict[str, str] = field(default_factory=dict)  # Remove prefix
    article: dict[str, str] = field(default_factory=dict)  # Insert "a "
    context: list[dict] = field(default_factory=list)  # Multi-word patterns: [{"pattern": ..., "replacement": ...}]

    @classmethod
    def from_json(cls, path: Path) -> ReplacementMap:
        """Load replacement map from JSON file."""
        if not path.exists():
            raise FileNotFoundError(f"Replacement map not found: {path}")

        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            strip=data.get("strip", {}),
            article=data.get("article", {}),
            context=data.get("context", []),
        )

    def to_json(self, path: Path) -> None:
        """Write replacement map to JSON file."""
        data = {
            "strip": self.strip,
            "article": self.article,
            "context": self.context,
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


# ── Profile Loading ──────────────────────────────────────────────────────────

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
                    prepositions=data.get("prepositions") or [],
                    conjunctions=data.get("conjunctions") or [],
                    false_positives=data.get("false_positives", []),
                )
        except Exception as e:
            print(f"Warning: Failed to load profile {profile_name}: {e}", file=sys.stderr)

    # Return default profile
    return Profile(name=profile_name)


def discover_map_path(profile_name: str) -> Optional[Path]:
    """Auto-discover replacement map from profile name."""
    map_path = PROFILES_DIR / f"{profile_name}_replacements.json"
    return map_path if map_path.exists() else None


# ── Token Fixing ────────────────────────────────────────────────────────────

def fix_file(
    filepath: Path,
    replacements: ReplacementMap,
    profile: Profile,
    dry_run: bool = False,
) -> list[dict]:
    """
    Fix all fused tokens in a single file using replacement map.
    Returns list of fixes applied.
    """
    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()
    fixes = []
    new_lines = []

    for line in lines:
        # Skip protected zones
        if profile.is_protected_line(line):
            new_lines.append(line)
            continue

        original = line
        anchor = None
        verse_text = line

        # Extract anchor if applicable
        if profile.anchor_regex:
            result = profile.extract_anchor(line)
            if result:
                anchor, verse_text = result

        # Apply strip replacements (word boundary matching)
        for token, replacement in replacements.strip.items():
            pattern = re.compile(r'\b' + re.escape(token) + r'\b')
            if pattern.search(verse_text):
                verse_text = pattern.sub(replacement, verse_text)
                fixes.append({
                    "anchor": anchor or "",
                    "token": token,
                    "strategy": "strip",
                    "replacement": replacement,
                })

        # Apply article replacements (word boundary matching)
        for token, replacement in replacements.article.items():
            pattern = re.compile(r'\b' + re.escape(token) + r'\b')
            if pattern.search(verse_text):
                verse_text = pattern.sub(replacement, verse_text)
                fixes.append({
                    "anchor": anchor or "",
                    "token": token,
                    "strategy": "article",
                    "replacement": replacement,
                })

        # Apply context-sensitive replacements
        for ctx_entry in replacements.context:
            ctx_pattern = re.compile(ctx_entry["pattern"])
            if ctx_pattern.search(verse_text):
                verse_text = ctx_pattern.sub(ctx_entry["replacement"], verse_text)
                fixes.append({
                    "anchor": anchor or "",
                    "token": ctx_entry["pattern"],
                    "strategy": "context",
                    "replacement": ctx_entry["replacement"],
                })

        # Reconstruct line with anchor if applicable
        if anchor:
            new_line = f"{anchor} {verse_text}"
        else:
            new_line = verse_text

        if new_line != original:
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    # Write file if not dry run
    if fixes and not dry_run:
        new_text = "\n".join(new_lines)
        if text.endswith("\n"):
            new_text += "\n"
        filepath.write_text(new_text, encoding="utf-8")

    return fixes


def fix_directory(
    dirpath: Path,
    replacements: ReplacementMap,
    profile: Profile,
    dry_run: bool = False,
    pattern: str = "*.md",
) -> dict:
    """
    Fix all markdown files in a directory.
    Returns summary dict with stats.
    """
    if not dirpath.is_dir():
        raise ValueError(f"Not a directory: {dirpath}")

    files = sorted(dirpath.rglob(pattern))
    total_files = 0
    total_fixes = 0
    file_results = {}

    for filepath in files:
        fixes = fix_file(filepath, replacements, profile, dry_run=dry_run)
        if fixes:
            total_files += 1
            total_fixes += len(fixes)
            file_results[str(filepath)] = fixes

    return {
        "total_files": total_files,
        "total_fixes": total_fixes,
        "file_results": file_results,
    }


# ── Map Generation from Scan Output ──────────────────────────────────────────

def classify_token_heuristic(token: str, base_word: str) -> str:
    """
    Heuristic classification of a fused token.
    Returns "strip" or "article".

    Rules:
      - If base_word ends in: -ed, -ing, -s (3rd person), -er, -ly → likely "strip" (verb/adverb)
      - If base_word ends in: -tion, -ness, -ment, vowel → likely "article" (noun)
      - Otherwise: prefer "article" (conservative default)
    """
    word = base_word.lower()

    # Verb indicators
    verb_patterns = [
        r'ed$',      # past tense: asked, answered
        r'ing$',     # gerund: blessing, maintaining
        r's$',       # 3rd person: desires, brings
        r'r$',       # agent: remember, believer
    ]

    for pattern in verb_patterns:
        if re.search(pattern, word):
            return "strip"

    # Noun/adjective indicators
    noun_patterns = [
        r'tion$',    # abstraction, dissension
        r'ness$',    # righteousness
        r'ment$',    # judgment, government
    ]

    for pattern in noun_patterns:
        if re.search(pattern, word):
            return "article"

    # Default: if common function words or prepositions, strip
    function_words = {
        "about", "away", "both", "daily", "except", "nor", "out",
        "throughout", "until", "and", "but", "or", "yet", "so",
    }

    if word in function_words:
        return "strip"

    # Conservative default for ambiguous cases: article (safer to add "a" than strip)
    return "article"


def generate_map_from_scan(scan_json_path: Path) -> ReplacementMap:
    """
    Generate a draft replacement map from scan.py JSON output.

    Expects scan output with structure like:
    {
      "findings": [
        {"token": "atook", "anchor": "...", "verse": "..."},
        ...
      ]
    }
    """
    if not scan_json_path.exists():
        raise FileNotFoundError(f"Scan output not found: {scan_json_path}")

    scan_data = json.loads(scan_json_path.read_text(encoding="utf-8"))
    findings = scan_data.get("findings", [])

    map_obj = ReplacementMap()
    seen = set()

    for finding in findings:
        token = finding.get("token")
        if not token or token in seen:
            continue
        seen.add(token)

        # Extract base word (remove leading 'a', 'b', 'c', 'd')
        if token and token[0] in "abcd" and len(token) > 1:
            base_word = token[1:]
        else:
            base_word = token

        # Classify heuristically
        strategy = classify_token_heuristic(token, base_word)

        if strategy == "strip":
            map_obj.strip[token] = base_word
        else:  # article
            map_obj.article[token] = f"a {base_word}"

    return map_obj


# ── Main CLI ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Fix fused tokens in extracted text using curated replacement maps.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Apply fixes with explicit map
  python3 fix.py --dir canon/ --map profiles/canon_replacements.json --profile canon

  # Auto-discover map from profile
  python3 fix.py --dir canon/ --profile canon

  # Dry run to see what would change
  python3 fix.py --file canon/OT/Genesis.md --profile canon --dry-run

  # Generate draft map from scan output
  python3 fix.py --generate-map scan_output.json --output draft_map.json
        """
    )

    parser.add_argument(
        "--file",
        type=Path,
        help="Single file to fix"
    )
    parser.add_argument(
        "--dir",
        type=Path,
        help="Directory to fix (recursive *.md discovery)"
    )
    parser.add_argument(
        "--map",
        type=Path,
        help="Path to replacement map JSON file"
    )
    parser.add_argument(
        "--profile",
        default="default",
        help="Profile name to load (default: 'default')"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show fixes without applying them"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--generate-map",
        type=Path,
        help="Generate draft map from scan.py JSON output"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output path for generated map (use with --generate-map)"
    )

    args = parser.parse_args()

    # ── Generate map mode ──
    if args.generate_map:
        print(f"Generating draft map from {args.generate_map}...", file=sys.stderr)
        try:
            draft_map = generate_map_from_scan(args.generate_map)
            output_path = args.output or Path("draft_replacements.json")
            draft_map.to_json(output_path)
            print(
                f"✓ Generated draft map with {len(draft_map.strip)} strip tokens "
                f"and {len(draft_map.article)} article tokens.",
                file=sys.stderr
            )
            print(f"✓ Saved to {output_path}", file=sys.stderr)
            print("\nReview the map and adjust classifications before using:", file=sys.stderr)
            print(f"  python3 fix.py --dir corpus/ --map {output_path} --profile canon", file=sys.stderr)
        except Exception as e:
            print(f"Error generating map: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # ── Validate inputs for fix mode ──
    if not args.file and not args.dir:
        parser.print_help()
        sys.exit(1)

    # Load profile
    profile = load_profile(args.profile)
    print(f"Loaded profile: {profile.name}", file=sys.stderr)

    # Load or discover replacement map
    map_path = args.map
    if not map_path:
        map_path = discover_map_path(args.profile)
        if map_path:
            print(f"Auto-discovered map: {map_path}", file=sys.stderr)

    if not map_path:
        print(
            f"Error: No replacement map found. Specify --map or use "
            f"--generate-map to create one.",
            file=sys.stderr
        )
        sys.exit(1)

    try:
        replacements = ReplacementMap.from_json(map_path)
        print(
            f"Loaded map with {len(replacements.strip)} strip, "
            f"{len(replacements.article)} article, {len(replacements.context)} context rules",
            file=sys.stderr
        )
    except Exception as e:
        print(f"Error loading map: {e}", file=sys.stderr)
        sys.exit(1)

    # ── Apply fixes ──
    try:
        if args.file:
            fixes = fix_file(args.file, replacements, profile, dry_run=args.dry_run)
            results = {
                "mode": "single_file",
                "total_fixes": len(fixes),
                "fixes": fixes,
            }
        else:  # args.dir
            results_dict = fix_directory(args.dir, replacements, profile, dry_run=args.dry_run)
            results = {
                "mode": "directory",
                "total_files": results_dict["total_files"],
                "total_fixes": results_dict["total_fixes"],
                "files": results_dict["file_results"],
            }

        if args.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            # Human-readable output
            if args.file:
                print(f"\n{args.file.name}: {len(fixes)} fixes", file=sys.stderr)
                for f in fixes:
                    action = "→" if not args.dry_run else "would →"
                    anchor_str = f"{f['anchor']:15s}" if f["anchor"] else "(plain)"
                    print(
                        f"  {anchor_str} {f['token']:25s} {action} {f['replacement']:20s} ({f['strategy']})",
                        file=sys.stderr
                    )
            else:
                print(f"\n{'='*70}", file=sys.stderr)
                print(f"  Files changed: {results['total_files']}", file=sys.stderr)
                print(f"  Total fixes: {results['total_fixes']}" +
                      (" (dry run)" if args.dry_run else ""), file=sys.stderr)
                print(f"{'='*70}", file=sys.stderr)

                # Summarize by file if not too many
                if results['total_files'] <= 20:
                    for filepath, file_fixes in results['files'].items():
                        print(f"\n{Path(filepath).name}: {len(file_fixes)} fixes", file=sys.stderr)
                        for f in file_fixes[:5]:  # Show first 5
                            anchor_str = f"{f['anchor']:15s}" if f["anchor"] else "(plain)"
                            print(
                                f"  {anchor_str} {f['token']:25s} → {f['replacement']:20s} ({f['strategy']})",
                                file=sys.stderr
                            )
                        if len(file_fixes) > 5:
                            print(f"  ... and {len(file_fixes) - 5} more", file=sys.stderr)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
