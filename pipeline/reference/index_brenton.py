"""
index_brenton.py — Build Brenton Septuagint reference index.

Parses all chapter files under src.texts/Brenton-Septuagint.txt/ and writes
per-book JSON index files to staging/reference/brenton/BOOK.json.

Each chapter file format:
  Line 0: Book name (e.g. "Genesis.")
  Line 1: Chapter header (e.g. "Chapter 1.")
  Lines 2+: One verse per line (positional: line 0 after header = verse 1)

Usage:
    python3 pipeline/reference/index_brenton.py               # index all books
    python3 pipeline/reference/index_brenton.py --book GEN    # single book only
    python3 pipeline/reference/index_brenton.py --book GEN EXO LEV
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
BRENTON_DIR = REPO_ROOT / "src.texts" / "Brenton-Septuagint.txt"
OUTPUT_DIR = REPO_ROOT / "staging" / "reference" / "brenton"
REGISTRY = REPO_ROOT / "schemas" / "anchor_registry.json"

# Filename pattern: eng-Brenton_{pos}_{book_code}_{chapter}_read.txt
RE_FILENAME = re.compile(r'^eng-Brenton_(\d{3})_([A-Z0-9]+)_(\d{2,3})_read\.txt$')

# Brenton book codes that differ from our registry codes
# Key = Brenton code in filename; Value = registry book code
BOOK_CODE_ALIASES: dict[str, str] = {
    "DAG": "DAN",  # Brenton "Daniel (Greek/LXX)" → our DAN
}

# Books absent from Brenton (OT-only reference; NT not present)
KNOWN_ABSENT: set[str] = {
    # NT books
    "MAT", "MRK", "LUK", "JHN", "ACT", "ROM",
    "1CO", "2CO", "GAL", "EPH", "PHP", "COL",
    "1TH", "2TH", "1TI", "2TI", "TIT", "PHM",
    "HEB", "JAS", "1PE", "2PE", "1JN", "2JN",
    "3JN", "JUD", "REV",
    # OT books without Brenton coverage
    "EST",  # Esther (only additions present in some editions)
    "NAH",  # Nahum
}


def load_registry_codes() -> set[str]:
    """Load all valid book codes from anchor_registry.json."""
    with open(REGISTRY, encoding="utf-8") as f:
        data = json.load(f)
    books = data.get("books", [])
    return {b["code"] for b in books}


def parse_chapter_file(path: Path) -> list[str]:
    """
    Parse a Brenton chapter file.
    Returns ordered list of verse texts (index 0 = verse 1).
    Skips first 2 lines (book name + chapter header) and empty lines.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    # Skip first 2 header lines
    verse_lines = lines[2:]
    # Collect non-empty lines as verses (strip trailing whitespace)
    verses = [ln.strip() for ln in verse_lines if ln.strip()]
    return verses


def build_index(book_filter: list[str] | None = None) -> dict[str, dict]:
    """
    Build per-book index from all Brenton chapter files.
    Returns dict: book_code → {chapters: {ch_str: {verses: [...], line_count: N}}}
    """
    registry_codes = load_registry_codes()
    books: dict[str, dict] = defaultdict(lambda: {"chapters": {}, "warnings": []})

    files = sorted(BRENTON_DIR.glob("eng-Brenton_*_*_*_read.txt"))
    processed = 0
    skipped = 0

    for path in files:
        m = RE_FILENAME.match(path.name)
        if not m:
            continue

        brenton_code = m.group(2)
        chapter_num = int(m.group(3))

        # Skip metadata file
        if brenton_code == "000":
            continue

        # Apply alias
        book_code = BOOK_CODE_ALIASES.get(brenton_code, brenton_code)

        # Filter by requested books
        if book_filter and book_code not in book_filter:
            continue

        # Validate against registry
        if book_code not in registry_codes and book_code not in KNOWN_ABSENT:
            books[book_code]["warnings"].append(
                f"WARNING: {brenton_code} → {book_code} not in registry"
            )

        verses = parse_chapter_file(path)
        ch_str = str(chapter_num)
        books[book_code]["chapters"][ch_str] = {
            "verses": verses,
            "line_count": len(verses),
        }
        processed += 1

    print(f"Parsed {processed} chapter files, skipped {skipped}.")
    return dict(books)


def write_book_json(book_code: str, data: dict) -> Path:
    """Write staging/reference/brenton/BOOK.json."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{book_code}.json"
    payload = {
        "book_code": book_code,
        "source": "Brenton Septuagint Translation (eBible.org, 2025)",
        "note": "Verse texts are positional — index 0 = verse 1 of each chapter.",
        "chapters": data["chapters"],
        "warnings": data.get("warnings", []),
    }
    out_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    return out_path


def summarize(book_code: str, data: dict) -> str:
    chapters = data["chapters"]
    total_verses = sum(ch["line_count"] for ch in chapters.values())
    warnings = data.get("warnings", [])
    warn_str = f"  {len(warnings)} warning(s)" if warnings else ""
    return f"  {book_code}: {len(chapters)} chapters, {total_verses} verses{warn_str}"


def main():
    parser = argparse.ArgumentParser(
        description="Build Brenton Septuagint reference index (staging/reference/brenton/)."
    )
    parser.add_argument(
        "--book", nargs="*", metavar="CODE",
        help="Book code(s) to index (e.g. GEN EXO). Default: all books."
    )
    args = parser.parse_args()

    book_filter = [b.upper() for b in args.book] if args.book else None

    if not BRENTON_DIR.exists():
        print(f"ERROR: Brenton directory not found: {BRENTON_DIR}", file=sys.stderr)
        sys.exit(1)

    print(f"Indexing Brenton files from: {BRENTON_DIR}")
    if book_filter:
        print(f"Filter: {', '.join(book_filter)}")

    all_books = build_index(book_filter)

    if not all_books:
        print("No books matched. Check --book codes.", file=sys.stderr)
        sys.exit(1)

    print(f"\nWriting {len(all_books)} book index file(s) to {OUTPUT_DIR}/")
    for book_code in sorted(all_books):
        data = all_books[book_code]
        out_path = write_book_json(book_code, data)
        print(summarize(book_code, data))
        for w in data.get("warnings", []):
            print(f"    ⚠  {w}")

    print(f"\nDone. Index files: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
