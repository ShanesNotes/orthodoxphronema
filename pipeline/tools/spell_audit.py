"""
spell_audit.py — Aspell-based spelling audit for canon/staged book files.

Usage:
    python3 pipeline/tools/spell_audit.py --dir canon/OT
    python3 pipeline/tools/spell_audit.py --file canon/OT/GEN.md
    python3 pipeline/tools/spell_audit.py --build-allowlist --dir canon/OT --output schemas/biblical_names.txt
    python3 pipeline/tools/spell_audit.py --dir canon/OT --allowlist schemas/biblical_names.txt --output-json reports/spell_audit.json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

RE_ANCHOR = re.compile(r'^([A-Z0-9]+\.\d+:\d+)\s+(.*)')
RE_FRONTMATTER = re.compile(r'^---\s*$')
RE_HEADING = re.compile(r'^#{1,4}\s')

# Biblical order for sorting
_BIBLICAL_ORDER = [
    "GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT",
    "1SA", "2SA", "1KI", "2KI", "1CH", "2CH", "EZR", "NEH",
    "EST", "JOB", "PSA", "PRO", "ECC", "SNG", "ISA", "JER",
    "LAM", "EZK", "DAN", "HOS", "JOL", "AMO", "OBA", "JON",
    "MIC", "NAH", "HAB", "ZEP", "HAG", "ZEC", "MAL",
    "TOB", "JDT", "WIS", "SIR", "BAR", "LJE", "1ES", "1MA", "2MA", "3MA",
    "MAT", "MRK", "LUK", "JOH", "ACT", "ROM", "1CO", "2CO",
    "GAL", "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI",
    "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JN", "2JN",
    "3JN", "JUD", "REV",
]
_BIBLICAL_ORDER_MAP = {code: i for i, code in enumerate(_BIBLICAL_ORDER)}


def extract_verse_text(path: Path) -> list[tuple[str, str]]:
    """Extract (anchor, verse_text) pairs from a canon/staged file."""
    lines = path.read_text(encoding="utf-8").splitlines()
    in_frontmatter = False
    results = []
    for line in lines:
        if RE_FRONTMATTER.match(line):
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue
        if RE_HEADING.match(line):
            continue
        m = RE_ANCHOR.match(line)
        if m:
            results.append((m.group(1), m.group(2)))
    return results


def aspell_check(text: str) -> set[str]:
    """Run aspell and return set of unknown words."""
    result = subprocess.run(
        ["aspell", "list", "--lang=en"],
        input=text, capture_output=True, text=True
    )
    return set(result.stdout.strip().splitlines()) if result.stdout.strip() else set()


def audit_book(path: Path, allowlist: set[str] | None = None) -> dict:
    """Audit a single book file for spelling errors."""
    verses = extract_verse_text(path)
    if not verses:
        return {"book": path.stem, "total_suspects": 0, "suspects": []}

    # Build word-to-anchor mapping
    word_anchors: dict[str, list[tuple[str, str]]] = {}  # word -> [(anchor, context)]
    all_text_parts = []
    for anchor, text in verses:
        all_text_parts.append(text)
        words = re.findall(r"[A-Za-z']+", text)
        for w in words:
            if w not in word_anchors:
                word_anchors[w] = []
            # Keep only first 3 occurrences to limit output
            if len(word_anchors[w]) < 3:
                # Trim context to ~60 chars around the word
                idx = text.find(w)
                start = max(0, idx - 25)
                end = min(len(text), idx + len(w) + 25)
                ctx = text[start:end]
                if start > 0:
                    ctx = "..." + ctx
                if end < len(text):
                    ctx = ctx + "..."
                word_anchors[w].append((anchor, ctx))

    # Run aspell on all text at once
    all_text = "\n".join(all_text_parts)
    unknown = aspell_check(all_text)

    # Filter
    if allowlist:
        unknown -= allowlist

    # Build suspects
    suspects = []
    for word in sorted(unknown):
        if word in word_anchors:
            for anchor, context in word_anchors[word]:
                suspects.append({
                    "anchor": anchor,
                    "word": word,
                    "context": context,
                })

    return {
        "book": path.stem,
        "total_suspects": len(unknown),
        "suspects": suspects,
    }


def build_allowlist(paths: list[Path]) -> set[str]:
    """Extract all capitalized words that aspell flags, for manual review."""
    all_caps_words = set()
    for path in paths:
        verses = extract_verse_text(path)
        for _, text in verses:
            # Find capitalized words (proper nouns)
            words = re.findall(r"\b[A-Z][a-z]+(?:'[a-z]+)?\b", text)
            all_caps_words.update(words)

    # Filter through aspell to find which ones it doesn't know
    if not all_caps_words:
        return set()
    unknown = aspell_check("\n".join(all_caps_words))
    return unknown


def discover_books(dir_path: Path) -> list[Path]:
    """Find .md book files in a directory, sorted in biblical order."""
    paths = sorted(dir_path.glob("*.md"),
                   key=lambda p: _BIBLICAL_ORDER_MAP.get(p.stem.upper(), 999))
    return [p for p in paths if not any(
        p.stem.endswith(s) for s in ("_notes", "_editorial_candidates", "_footnote_markers")
    )]


def main():
    parser = argparse.ArgumentParser(description="Spell audit for canon book files.")
    parser.add_argument("--file", metavar="FILE", help="Single book file to audit.")
    parser.add_argument("--dir", metavar="DIR", help="Directory of book files to audit.")
    parser.add_argument("--allowlist", metavar="FILE", help="Path to biblical names allowlist.")
    parser.add_argument("--build-allowlist", action="store_true",
                        help="Build allowlist from capitalized words in the files.")
    parser.add_argument("--output", metavar="FILE", help="Output file for allowlist (with --build-allowlist).")
    parser.add_argument("--output-json", metavar="FILE", help="Write JSON audit report.")
    args = parser.parse_args()

    if args.build_allowlist:
        if not args.dir:
            print("--build-allowlist requires --dir", file=sys.stderr)
            sys.exit(1)
        paths = discover_books(Path(args.dir))
        allowlist = build_allowlist(paths)
        sorted_words = sorted(allowlist, key=str.lower)
        if args.output:
            Path(args.output).write_text("\n".join(sorted_words) + "\n", encoding="utf-8")
            print(f"Allowlist written: {args.output} ({len(sorted_words)} words)")
        else:
            for w in sorted_words:
                print(w)
        return

    # Load allowlist if provided
    allowlist = None
    if args.allowlist:
        al_path = Path(args.allowlist)
        if al_path.exists():
            allowlist = set(al_path.read_text(encoding="utf-8").splitlines())

    # Discover files
    if args.file:
        paths = [Path(args.file)]
    elif args.dir:
        paths = discover_books(Path(args.dir))
    else:
        print("Specify --file or --dir", file=sys.stderr)
        sys.exit(1)

    results = []
    for path in paths:
        r = audit_book(path, allowlist)
        results.append(r)
        status = f"{r['total_suspects']} suspects" if r['total_suspects'] else "clean"
        print(f"{r['book']:4s} | {status}")

    # Summary
    total = sum(r["total_suspects"] for r in results)
    print(f"\nTotal: {len(results)} books, {total} spelling suspects")

    if args.output_json:
        out = Path(args.output_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump({"books": results}, f, indent=2)
        print(f"JSON report: {out}")


if __name__ == "__main__":
    main()
