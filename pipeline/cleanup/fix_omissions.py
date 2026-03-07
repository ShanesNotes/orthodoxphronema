"""
fix_omissions.py — Non-destructive cleanup for staged canon files.

Reads a staged canon .md, applies bounded allowlist-only transforms,
and either reports changes (--dry-run/--report) or applies them (--in-place).

Rules:
  R1  Split fused article compounds ("afirmament" -> "a firmament")
  R2  Split fused possessives ("God'simage" -> "God's image")
  R3  Rejoin word-split artifacts ("y ou" -> "you", "wiv es" -> "wives")
  R4  Rejoin hyphen-split line breaks ("Egyp-tian" -> "Egyptian")
  R5  Fix trailing space before punctuation ("body ." -> "body.")
  R6  Detect drop-cap omissions (verse starts lowercase) — REPORT ONLY, no auto-fix

Usage:
    python3 fix_omissions.py staging/validated/OT/GEN.md             # dry-run (default)
    python3 fix_omissions.py staging/validated/OT/GEN.md --in-place  # overwrite file + memo
    python3 fix_omissions.py staging/validated/OT/GEN.md --report    # memo only, no file change
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import yaml
from pathlib import Path
from datetime import date

# ---------------------------------------------------------------------------
# Repo layout
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent.parent
ALLOWLIST_DIR = Path(__file__).parent / "allowlists"

# ---------------------------------------------------------------------------
# Regex constants (rule-independent)
# ---------------------------------------------------------------------------
RE_FUSED_POSSESSIVE = re.compile(r"('s)([a-z])")
RE_SPACE_BEFORE_PUNCT = re.compile(r" ([.,;:!?])")
RE_SPACE_BEFORE_POSSESSIVE = re.compile(r" ('s)\b")
RE_VERSE_LINE = re.compile(r'^([A-Z0-9]+\.\d+:\d+) (.+)')
RE_DROP_CAP = re.compile(r'^[a-z]')


# ---------------------------------------------------------------------------
# Allowlist loading
# ---------------------------------------------------------------------------

# Inline defaults — used when no external allowlist file exists
_DEFAULT_FUSED_ARTICLES: list[str] = []
_DEFAULT_WORD_SPLITS: list[tuple[str, str]] = []
_DEFAULT_HYPHEN_SPLITS: list[tuple[str, str]] = []


def load_allowlists(book_code: str) -> tuple[set[str], list[tuple[str, str]], list[tuple[str, str]]]:
    """Load per-book allowlists from JSON, falling back to inline defaults."""
    path = ALLOWLIST_DIR / f"{book_code}.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        fused = set(data.get("fused_articles", []))
        word_splits = [tuple(p) for p in data.get("word_splits", [])]
        # Sort longest-first so compound entries like "alawgiv er" match before
        # their substring components like "giv e"
        word_splits.sort(key=lambda p: len(p[0]), reverse=True)
        hyphen_splits = [tuple(p) for p in data.get("hyphen_splits", [])]
        return fused, word_splits, hyphen_splits
    return set(_DEFAULT_FUSED_ARTICLES), list(_DEFAULT_WORD_SPLITS), list(_DEFAULT_HYPHEN_SPLITS)


def build_fused_article_regex(allowlist: set[str]) -> re.Pattern | None:
    if not allowlist:
        return None
    return re.compile(
        r'\b(' + '|'.join(sorted(allowlist, key=len, reverse=True)) + r')\b'
    )


# ---------------------------------------------------------------------------
# Book name from frontmatter or filename
# ---------------------------------------------------------------------------

def extract_book_name(text: str, book_code: str) -> str:
    """Try to read book_name from YAML frontmatter; fall back to book_code."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            try:
                fm = yaml.safe_load(text[4:end])
                if isinstance(fm, dict) and "book_name" in fm:
                    return fm["book_name"]
            except Exception:
                pass
    return book_code


# ---------------------------------------------------------------------------
# Cleanup engine
# ---------------------------------------------------------------------------

def fix_fused_article(m: re.Match) -> str:
    return "a " + m.group(1)[1:]


def apply_cleanup(line: str, stats: dict[str, int], drop_cap_report: list[str],
                  re_fused: re.Pattern | None,
                  word_splits: list[tuple[str, str]],
                  hyphen_splits: list[tuple[str, str]]) -> str:
    """Apply R1-R5 transforms to a single line. R6 is detect-only."""
    original = line

    if line.startswith('---') or line.startswith('#'):
        return line

    m = RE_VERSE_LINE.match(line)
    if not m:
        return line

    anchor = m.group(1)
    text = m.group(2)

    # R6: detect drop-cap (before any fixes)
    if RE_DROP_CAP.match(text):
        drop_cap_report.append(f"{anchor} | `{text[:50]}...`")

    # R1: fused articles
    if re_fused:
        new_text = re_fused.sub(fix_fused_article, text)
        if new_text != text:
            stats["R1"] = stats.get("R1", 0) + len(re_fused.findall(text))
            text = new_text

    # R2: fused possessives
    new_text = RE_FUSED_POSSESSIVE.sub(lambda m: m.group(1) + " " + m.group(2), text)
    if new_text != text:
        stats["R2"] = stats.get("R2", 0) + len(RE_FUSED_POSSESSIVE.findall(text))
        text = new_text

    # R3: word splits
    for wrong, right in word_splits:
        if wrong in text:
            count = text.count(wrong)
            text = text.replace(wrong, right)
            stats["R3"] = stats.get("R3", 0) + count

    # R4: hyphen splits
    for wrong, right in hyphen_splits:
        if wrong in text:
            count = text.count(wrong)
            text = text.replace(wrong, right)
            stats["R4"] = stats.get("R4", 0) + count

    # R5: space before punctuation and space before possessive 's
    new_text = RE_SPACE_BEFORE_PUNCT.sub(r'\1', text)
    new_text = RE_SPACE_BEFORE_POSSESSIVE.sub(r"\1", new_text)
    if new_text != text:
        stats["R5"] = stats.get("R5", 0) + (len(text) - len(new_text))
        text = new_text

    result = f"{anchor} {text}"
    if result != original:
        stats["_lines_changed"] = stats.get("_lines_changed", 0) + 1

    return result


def collect_diffs(original_lines: list[str], cleaned_lines: list[str],
                  first_n: int = 20, last_n: int = 20) -> list[str]:
    """Collect before/after diff samples from verse lines only."""
    diffs: list[tuple[int, str, str]] = []
    for i, (o, c) in enumerate(zip(original_lines, cleaned_lines)):
        if o != c:
            diffs.append((i + 1, o.rstrip(), c.rstrip()))

    samples = []
    if len(diffs) <= first_n + last_n:
        selected = diffs
    else:
        selected = diffs[:first_n] + diffs[-last_n:]

    for lineno, before, after in selected:
        samples.append(f"L{lineno}:")
        samples.append(f"  - `{before}`")
        samples.append(f"  + `{after}`")
        samples.append("")
    return samples


# ---------------------------------------------------------------------------
# Memo generation
# ---------------------------------------------------------------------------

def build_memo(book_code: str, book_name: str, input_path: Path,
               stats: dict[str, int], drop_cap_report: list[str],
               diff_samples: list[str], in_place: bool) -> str:
    today = date.today().isoformat()
    lines_changed = stats.get("_lines_changed", 0)
    mode_label = "in-place" if in_place else "dry-run"

    memo_lines = [
        f"# {book_name} Cleanup Report — {today}\n",
        "\n",
        "## Summary\n",
        f"- Input: `{input_path}`\n",
        f"- Mode: **{mode_label}**\n",
        f"- Lines changed: {lines_changed}\n",
        "\n",
        "## Rules Applied\n",
        "\n",
        "| Rule | Description | Count |\n",
        "|------|-------------|-------|\n",
        f"| R1 | Split fused article compounds (allowlist) | {stats.get('R1', 0)} |\n",
        f"| R2 | Split fused possessives ('s + word) | {stats.get('R2', 0)} |\n",
        f"| R3 | Rejoin word-split artifacts (allowlist) | {stats.get('R3', 0)} |\n",
        f"| R4 | Rejoin hyphen-split line breaks (allowlist) | {stats.get('R4', 0)} |\n",
        f"| R5 | Remove trailing space before punctuation | {stats.get('R5', 0)} |\n",
        f"| R6 | Drop-cap omissions detected (NO auto-fix) | {len(drop_cap_report)} |\n",
        "\n",
        "## Before/After Examples (first 20 + last 20 changed lines)\n",
        "\n",
    ]
    memo_lines.extend(f"{s}\n" for s in diff_samples)

    memo_lines.extend([
        "\n",
        "## Unresolved: Drop-Cap Omissions (R6 — human review required)\n",
        "\n",
        "These verses begin with a lowercase letter, indicating the PDF drop-cap\n",
        "first letter was not captured by Docling. **Do not auto-infer** the missing\n",
        "letter — each must be verified against the source PDF.\n",
        "\n",
        "| Anchor | Text (first 50 chars) |\n",
        "|--------|-----------------------|\n",
    ])
    for entry in drop_cap_report:
        memo_lines.append(f"| {entry} |\n")

    return "".join(memo_lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Non-destructive cleanup for staged canon files."
    )
    parser.add_argument(
        "path", type=Path,
        help="Staged canon .md file to clean"
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run", action="store_true", default=True,
        help="Print summary to stdout, no file writes (default)"
    )
    mode.add_argument(
        "--in-place", action="store_true",
        help="Overwrite input file and write memo to memos/"
    )
    mode.add_argument(
        "--report", action="store_true",
        help="Write memo only, no file changes"
    )
    args = parser.parse_args()

    input_path = args.path
    if not input_path.exists():
        print(f"File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    book_code = input_path.stem
    file_text = input_path.read_text(encoding="utf-8")
    book_name = extract_book_name(file_text, book_code)

    # Load allowlists
    fused_set, word_splits, hyphen_splits = load_allowlists(book_code)
    re_fused = build_fused_article_regex(fused_set)

    original_lines = file_text.splitlines(keepends=True)
    stats: dict[str, int] = {}
    drop_cap_report: list[str] = []

    cleaned_lines = []
    for line in original_lines:
        cleaned = apply_cleanup(
            line.rstrip("\n"), stats, drop_cap_report,
            re_fused, word_splits, hyphen_splits
        )
        cleaned_lines.append(cleaned + "\n")

    # Diff samples
    diff_samples = collect_diffs(
        [l.rstrip("\n") for l in original_lines],
        [l.rstrip("\n") for l in cleaned_lines]
    )

    # Build memo
    memo_text = build_memo(
        book_code, book_name, input_path,
        stats, drop_cap_report, diff_samples, args.in_place
    )

    memo_path = REPO_ROOT / "memos" / f"08_{book_code.lower()}_cleanup_report.md"

    if args.in_place:
        input_path.write_text("".join(cleaned_lines), encoding="utf-8")
        memo_path.write_text(memo_text, encoding="utf-8")
        print(f"Wrote: {input_path} (in-place)")
        print(f"Wrote: {memo_path}")
    elif args.report:
        memo_path.write_text(memo_text, encoding="utf-8")
        print(f"Wrote: {memo_path}")
    else:
        # dry-run: output cleaned content to stdout
        sys.stdout.write("".join(cleaned_lines))

    # Summary to stderr (visible in all modes)
    lines_changed = stats.get("_lines_changed", 0)
    print(f"\n--- Cleanup Summary ({book_name} / {book_code}) ---", file=sys.stderr)
    for rule in ["R1", "R2", "R3", "R4", "R5"]:
        print(f"  {rule}: {stats.get(rule, 0)} fixes", file=sys.stderr)
    print(f"  R6: {len(drop_cap_report)} drop-cap suspects (report only)", file=sys.stderr)
    print(f"  Total lines changed: {lines_changed}", file=sys.stderr)


if __name__ == "__main__":
    main()
