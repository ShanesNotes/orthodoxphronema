"""
DEPRECATED: This script is superseded by skills/text-cleaner (P4/P8 + D5 detection).
Archived copy at pipeline/archive/historical_cleanup/fix_omissions.py.
Kept in place for backward compatibility with existing test imports.

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
  R7  Brenton-assisted fused compound detection (only with --reference brenton)

Usage:
    python3 fix_omissions.py staging/validated/OT/GEN.md                               # dry-run
    python3 fix_omissions.py staging/validated/OT/GEN.md --in-place                   # overwrite
    python3 fix_omissions.py staging/validated/OT/GEN.md --in-place --reference brenton  # + R7
    python3 fix_omissions.py staging/validated/OT/GEN.md --report                     # memo only
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
import sys as _sys; from pathlib import Path as _Path
_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists(): _R = _R.parent
if str(_R) not in _sys.path: _sys.path.insert(0, str(_R))
from pipeline.common.paths import REPO_ROOT, BRENTON_DIR as _BRENTON_DIR
from pipeline.common.patterns import SHORT_PREFIXES as _SHORT_PREFIXES

ALLOWLIST_DIR = Path(__file__).parent / "allowlists"
_DEFAULT_BRENTON_DIR = _BRENTON_DIR


def _load_normalize_module():
    """Lazy-load the shared normalize_reference_text module."""
    from pipeline.reference import normalize_reference_text
    return normalize_reference_text


# ---------------------------------------------------------------------------
# Regex constants (rule-independent)
# ---------------------------------------------------------------------------
RE_FUSED_POSSESSIVE = re.compile(r"('s)([a-z])")
RE_SPACE_BEFORE_PUNCT = re.compile(r" ([.,;:!?])")
RE_SPACE_BEFORE_POSSESSIVE = re.compile(r" ('s)\b")
RE_VERSE_LINE = re.compile(r'^([A-Z0-9]+\.\d+:\d+) (.+)')
RE_DROP_CAP = re.compile(r'^[a-z]')
RE_ANCHOR_PARTS = re.compile(r'^([A-Z0-9]+)\.(\d+):(\d+)$')


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
# Cleanup engine (R1–R6)
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


# ---------------------------------------------------------------------------
# R7: Brenton-assisted fused compound detection
# ---------------------------------------------------------------------------

def run_brenton_pass(
    verse_pairs: list[tuple[str, str]],   # [(anchor, text), ...]
    brenton_index: dict,
    norm,
    stats: dict,
    r7_report: list[dict],
) -> dict[str, str]:
    """
    Scan verse tokens against Brenton tokens to find fused compounds
    not caught by R1–R4.

    Auto-apply criteria (ALL must be true):
      1. OSB token = prefix + suffix where prefix in _SHORT_PREFIXES
      2. len(suffix) >= 3
      3. Brenton has (prefix, suffix) as adjacent tokens
      4. Token similarity of full verse improves by >= 0.02 after repair
      5. No semantic substitution (exact token-level match only)

    Returns dict of anchor -> repaired_text for auto-approved repairs.
    """
    repairs: dict[str, str] = {}

    for anchor, text in verse_pairs:
        m = RE_ANCHOR_PARTS.match(anchor)
        if not m:
            continue
        chapter, verse = int(m.group(2)), int(m.group(3))
        brenton_verse = norm.get_brenton_verse(brenton_index, chapter, verse)
        if not brenton_verse:
            continue

        norm_osb = norm.normalize_for_compare(text)
        norm_bren = norm.normalize_for_compare(brenton_verse)
        base_score = norm.token_similarity(norm_osb, norm_bren)

        osb_tokens = norm.tokenize(norm_osb)
        bren_tokens = norm.tokenize(norm_bren)
        bren_bigrams = set()
        for i in range(len(bren_tokens) - 1):
            bren_bigrams.add((bren_tokens[i], bren_tokens[i + 1]))

        auto_fixes: list[tuple[str, str, str]] = []  # (fused, prefix, suffix)
        for tok in set(osb_tokens):  # deduplicate tokens
            for p in _SHORT_PREFIXES:
                if tok.startswith(p) and len(tok) > len(p) + 2:
                    suffix = tok[len(p):]
                    if len(suffix) >= 3 and (p, suffix) in bren_bigrams:
                        auto_fixes.append((tok, p, suffix))
                        break

        if not auto_fixes:
            continue

        # Apply all auto fixes to text; verify similarity improvement
        repaired_text = text
        for fused, prefix, suffix in auto_fixes:
            repaired_text = re.sub(
                r'\b' + re.escape(fused) + r'\b',
                prefix + " " + suffix,
                repaired_text
            )

        norm_repaired = norm.normalize_for_compare(repaired_text)
        new_score = norm.token_similarity(norm_repaired, norm_bren)

        if new_score - base_score >= 0.02:
            repairs[anchor] = repaired_text
            stats["R7"] = stats.get("R7", 0) + len(auto_fixes)
            stats["_lines_changed"] = stats.get("_lines_changed", 0) + 1
            for fused, prefix, suffix in auto_fixes:
                r7_report.append({
                    "anchor": anchor,
                    "fused": fused,
                    "repair": f"{prefix} {suffix}",
                    "score_before": round(base_score, 4),
                    "score_after": round(new_score, 4),
                    "classification": "auto_applied",
                })
        else:
            # Score didn't improve enough — report but don't apply
            for fused, prefix, suffix in auto_fixes:
                r7_report.append({
                    "anchor": anchor,
                    "fused": fused,
                    "repair": f"{prefix} {suffix}",
                    "score_before": round(base_score, 4),
                    "score_after": round(new_score, 4),
                    "classification": "ambiguous_no_improve",
                })

    return repairs


def apply_r7_repairs(lines: list[str], repairs: dict[str, str]) -> list[str]:
    """Apply R7 repairs to the line list (operates on post-R1–R5 lines)."""
    result = []
    for line in lines:
        m = RE_VERSE_LINE.match(line.rstrip("\n"))
        if m and m.group(1) in repairs:
            anchor = m.group(1)
            result.append(f"{anchor} {repairs[anchor]}\n")
        else:
            result.append(line)
    return result


# ---------------------------------------------------------------------------
# Diff collection
# ---------------------------------------------------------------------------

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
               diff_samples: list[str], in_place: bool,
               r7_report: list[dict] | None = None) -> str:
    today = date.today().isoformat()
    lines_changed = stats.get("_lines_changed", 0)
    mode_label = "in-place" if in_place else "dry-run"
    r7_count = stats.get("R7", 0)
    brenton_mode = r7_report is not None

    memo_lines = [
        f"# {book_name} Cleanup Report — {today}\n",
        "\n",
        "## Summary\n",
        f"- Input: `{input_path}`\n",
        f"- Mode: **{mode_label}**\n",
        f"- Brenton reference: {'enabled (R7)' if brenton_mode else 'disabled'}\n",
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
        f"| R7 | Brenton-assisted fused compound splits | {r7_count} |\n",
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
        "first letter was not captured by Docling. Run dropcap_verify.py for\n",
        "Brenton-backed classification.\n",
        "\n",
        "| Anchor | Text (first 50 chars) |\n",
        "|--------|-----------------------|\n",
    ])
    for entry in drop_cap_report:
        memo_lines.append(f"| {entry} |\n")

    # R7 report section
    if r7_report:
        auto_applied = [r for r in r7_report if r["classification"] == "auto_applied"]
        ambiguous = [r for r in r7_report if r["classification"] != "auto_applied"]

        memo_lines.extend([
            "\n",
            "## Brenton-Assisted Repairs (R7)\n",
            "\n",
            f"Auto-applied: {len(auto_applied)}  |  Ambiguous (not applied): {len(ambiguous)}\n",
            "\n",
        ])

        if auto_applied:
            memo_lines.extend([
                "### Auto-Applied Splits\n",
                "\n",
                "| Anchor | Fused | Repair | Score Δ |\n",
                "|--------|-------|--------|--------|\n",
            ])
            for r in auto_applied:
                delta = round(r["score_after"] - r["score_before"], 4)
                memo_lines.append(
                    f"| {r['anchor']} | `{r['fused']}` | `{r['repair']}` | +{delta} |\n"
                )

        if ambiguous:
            memo_lines.extend([
                "\n",
                "### Ambiguous — Not Applied (score did not improve)\n",
                "\n",
                "| Anchor | Fused | Repair | Score Δ |\n",
                "|--------|-------|--------|--------|\n",
            ])
            for r in ambiguous:
                delta = round(r["score_after"] - r["score_before"], 4)
                memo_lines.append(
                    f"| {r['anchor']} | `{r['fused']}` | `{r['repair']}` | {delta:+.4f} |\n"
                )

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
    parser.add_argument(
        "--reference", metavar="SOURCE",
        help="Auxiliary reference source for R7 (currently: 'brenton')"
    )
    parser.add_argument(
        "--brenton-dir", type=Path, default=_DEFAULT_BRENTON_DIR,
        help=f"Directory containing Brenton JSON index files (default: {_DEFAULT_BRENTON_DIR})"
    )
    args = parser.parse_args()

    input_path = args.path
    if not input_path.exists():
        print(f"File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    use_brenton = args.reference and args.reference.lower() == "brenton"

    book_code = input_path.stem
    file_text = input_path.read_text(encoding="utf-8")
    book_name = extract_book_name(file_text, book_code)

    # Load allowlists
    fused_set, word_splits, hyphen_splits = load_allowlists(book_code)
    re_fused = build_fused_article_regex(fused_set)

    original_lines = file_text.splitlines(keepends=True)
    stats: dict[str, int] = {}
    drop_cap_report: list[str] = []

    # R1–R6 pass
    cleaned_lines = []
    for line in original_lines:
        cleaned = apply_cleanup(
            line.rstrip("\n"), stats, drop_cap_report,
            re_fused, word_splits, hyphen_splits
        )
        cleaned_lines.append(cleaned + "\n")

    # R7: Brenton-assisted pass (optional)
    r7_report: list[dict] | None = None
    if use_brenton:
        r7_report = []
        try:
            norm = _load_normalize_module()
            brenton_index = norm.load_brenton_index(book_code, args.brenton_dir)
            if brenton_index is None:
                print(
                    f"WARNING: No Brenton index for {book_code} at {args.brenton_dir}. "
                    "Run index_brenton.py first. Skipping R7.",
                    file=sys.stderr
                )
            else:
                # Build verse pairs from post-R1–R5 lines
                verse_pairs: list[tuple[str, str]] = []
                for line in cleaned_lines:
                    m = RE_VERSE_LINE.match(line.rstrip("\n"))
                    if m:
                        verse_pairs.append((m.group(1), m.group(2)))

                r7_repairs = run_brenton_pass(
                    verse_pairs, brenton_index, norm, stats, r7_report
                )
                if r7_repairs:
                    cleaned_lines = apply_r7_repairs(cleaned_lines, r7_repairs)
        except Exception as e:
            print(f"WARNING: R7 Brenton pass failed: {e}", file=sys.stderr)

    # Diff samples
    diff_samples = collect_diffs(
        [l.rstrip("\n") for l in original_lines],
        [l.rstrip("\n") for l in cleaned_lines]
    )

    # Build memo
    memo_text = build_memo(
        book_code, book_name, input_path,
        stats, drop_cap_report, diff_samples, args.in_place,
        r7_report=r7_report
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
    if use_brenton:
        r7_auto = len([r for r in (r7_report or []) if r["classification"] == "auto_applied"])
        r7_ambig = len([r for r in (r7_report or []) if r["classification"] != "auto_applied"])
        print(f"  R7: {stats.get('R7', 0)} auto-applied, {r7_ambig} ambiguous", file=sys.stderr)
    print(f"  Total lines changed: {lines_changed}", file=sys.stderr)


if __name__ == "__main__":
    main()
