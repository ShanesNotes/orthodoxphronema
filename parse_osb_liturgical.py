#!/usr/bin/env python3
"""
Parser for Orthodox Study Bible "This passage is read at" liturgical cross-references.

The source file contains verse-range → liturgical occasion mappings in two patterns:
1. Early entries (Genesis through some OT books): implicit book references like "1:1-3 This passage..."
2. Later entries: explicit book references like "Gen 17:1", "Mt 10:32", "Heb 11:9"

Outputs structured JSON to reference/liturgical-crossrefs.json
"""

import re
import json
from pathlib import Path
from typing import Optional, List, Tuple, Dict

# 3-letter book codes used in the repo
BOOK_CODES = {
    # OT
    'Gen': 'GEN', 'Genesis': 'GEN',
    'Ex': 'EXO', 'Exod': 'EXO', 'Exodus': 'EXO',
    'Lev': 'LEV', 'Levit': 'LEV', 'Leviticus': 'LEV',
    'Num': 'NUM', 'Numbers': 'NUM',
    'Deut': 'DEU', 'Deuteronomy': 'DEU',
    'Josh': 'JOS', 'Joshua': 'JOS',
    'Jdg': 'JDG', 'Judges': 'JDG',
    'Ruth': 'RUT',
    '1Sam': '1SA', '1 Sam': '1SA', '1 Samuel': '1SA',
    '2Sam': '2SA', '2 Sam': '2SA', '2 Samuel': '2SA',
    '1Kgs': '1KI', '1 Kgs': '1KI', '1 Kings': '1KI', '3Kingd': '1KI',
    '2Kgs': '2KI', '2 Kgs': '2KI', '2 Kings': '2KI', '4Kingd': '2KI',
    '1Chr': '1CH', '1 Chr': '1CH', '1 Chronicles': '1CH',
    '2Chr': '2CH', '2 Chr': '2CH', '2 Chronicles': '2CH',
    '1Es': '1ES', '1 Es': '1ES',
    'Ezra': 'EZR', 'Ezr': 'EZR',
    'Neh': 'NEH', 'Nehemiah': 'NEH',
    'Tob': 'TOB', 'Tobit': 'TOB',
    'Jdt': 'JDT', 'Judith': 'JDT',
    'Est': 'EST', 'Esth': 'EST', 'Esther': 'EST',
    '1Macc': '1MA', '1 Macc': '1MA',
    '2Macc': '2MA', '2 Macc': '2MA',
    '3Macc': '3MA', '3 Macc': '3MA',
    'Ps': 'PSA', 'Psalm': 'PSA', 'Psalms': 'PSA',
    'Job': 'JOB',
    'Prov': 'PRO', 'Proverbs': 'PRO',
    'Eccl': 'ECC', 'Ecclesiastes': 'ECC',
    'Song': 'SNG', 'Song of Songs': 'SNG',
    'Wis': 'WIS', 'Wisdom': 'WIS',
    'Sir': 'SIR', 'Sirach': 'SIR',
    'Hos': 'HOS', 'Hosea': 'HOS',
    'Joel': 'JOL',
    'Amos': 'AMO',
    'Obad': 'OBA', 'Obadiah': 'OBA',
    'Jonah': 'JON',
    'Mic': 'MIC', 'Micah': 'MIC',
    'Nah': 'NAH', 'Nahum': 'NAH',
    'Hab': 'HAB', 'Habakkuk': 'HAB',
    'Zeph': 'ZEP', 'Zephaniah': 'ZEP',
    'Hag': 'HAG', 'Haggai': 'HAG',
    'Zech': 'ZEC', 'Zechariah': 'ZEC',
    'Mal': 'MAL', 'Malachi': 'MAL',
    'Is': 'ISA', 'Isa': 'ISA', 'Isaiah': 'ISA',
    'Jer': 'JER', 'Jeremiah': 'JER',
    'Bar': 'BAR', 'Baruch': 'BAR',
    'Lam': 'LAM', 'Lamentations': 'LAM',
    'LJe': 'LJE',
    'Ezek': 'EZK', 'Ezekiel': 'EZK',
    'Dan': 'DAN', 'Daniel': 'DAN',
    # NT
    'Mat': 'MAT', 'Mt': 'MAT', 'Matt': 'MAT', 'Matthew': 'MAT',
    'Mk': 'MRK', 'Mark': 'MRK', 'Mar': 'MRK',
    'Lk': 'LUK', 'Luke': 'LUK', 'Luk': 'LUK',
    'Jn': 'JOH', 'John': 'JOH', 'Joh': 'JOH',
    'Acts': 'ACT', 'Act': 'ACT',
    'Rom': 'ROM', 'Romans': 'ROM',
    '1Cor': '1CO', '1 Cor': '1CO', '1 Corinthians': '1CO',
    '2Cor': '2CO', '2 Cor': '2CO', '2 Corinthians': '2CO',
    'Gal': 'GAL', 'Galatians': 'GAL',
    'Eph': 'EPH', 'Ephesians': 'EPH',
    'Phil': 'PHP', 'Philippians': 'PHP', 'Phlp': 'PHP',
    'Col': 'COL', 'Colossians': 'COL',
    '1Th': '1TH', '1 Th': '1TH', '1 Thessalonians': '1TH',
    '2Th': '2TH', '2 Th': '2TH', '2 Thessalonians': '2TH',
    '1Tim': '1TI', '1 Tim': '1TI', '1 Timothy': '1TI',
    '2Tim': '2TI', '2 Tim': '2TI', '2 Timothy': '2TI',
    'Tit': 'TIT', 'Titus': 'TIT',
    'Phlm': 'PHM', 'Philemon': 'PHM',
    'Heb': 'HEB', 'Hebrews': 'HEB',
    'Jas': 'JAS', 'James': 'JAS',
    '1Pet': '1PE', '1 Pet': '1PE', '1 Peter': '1PE',
    '2Pet': '2PE', '2 Pet': '2PE', '2 Peter': '2PE',
    '1Jn': '1JN', '1 Jn': '1JN', '1 John': '1JN',
    '2Jn': '2JN', '2 Jn': '2JN', '2 John': '2JN',
    '3Jn': '3JN', '3 Jn': '3JN', '3 John': '3JN',
    'Jude': 'JUD',
    'Rev': 'REV', 'Revelation': 'REV',
}

# Define the canonical order of OT books (used to determine which book implicit references belong to)
OT_BOOK_ORDER = [
    'GEN', 'EXO', 'LEV', 'NUM', 'DEU', 'JOS', 'JDG', 'RUT',
    '1SA', '2SA', '1KI', '2KI', '1CH', '2CH', '1ES', 'EZR', 'NEH',
    'TOB', 'JDT', 'EST', '1MA', '2MA', '3MA',
    'PSA', 'JOB', 'PRO', 'ECC', 'SNG', 'WIS', 'SIR',
    'HOS', 'JOL', 'AMO', 'OBA', 'JON', 'MIC', 'NAH', 'HAB', 'ZEP', 'HAG', 'ZEC', 'MAL',
    'ISA', 'JER', 'BAR', 'LAM', 'LJE', 'EZK', 'DAN',
]


def normalize_book_name(book_str: str) -> Optional[str]:
    """Convert various book name formats to 3-letter code."""
    book_str = book_str.strip()
    if book_str in BOOK_CODES:
        return BOOK_CODES[book_str]
    return None


def parse_verse_reference(ref_str: str, current_book: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
    """
    Parse a verse reference string and return (book_code, verse_range).

    If the reference starts with a book name, extract it.
    If it's implicit (no book), use current_book.

    Examples:
        "Gen 17:1, 2, 4–8" → ("GEN", "17:1, 2, 4-8")
        "1:1-3" → (current_book, "1:1-3")
        "Mt 10:32, 33" → ("MAT", "10:32, 33")
    """
    ref_str = ref_str.strip()

    # Try to detect explicit book reference at the start
    words = ref_str.split()
    if len(words) > 0:
        potential_book = words[0].rstrip(',:;')
        normalized = normalize_book_name(potential_book)
        if normalized:
            # Extract the verse part (everything after the book name)
            verse_part = ' '.join(words[1:])
            # Clean up the verse part
            verse_part = verse_part.split(':')[0] if ':' in verse_part else verse_part
            return (normalized, verse_part.strip())

    # No explicit book found; use current_book
    if current_book:
        return (current_book, ref_str)
    else:
        return (None, ref_str)


def parse_occasions(occasion_text: str) -> List[str]:
    """Extract occasion text. May span multiple lines."""
    # Normalize whitespace and clean up
    text = ' '.join(occasion_text.split())
    # Remove trailing punctuation if present
    text = text.rstrip('.,;')
    return [text] if text else []


def parse_file(filepath: str) -> List[Dict]:
    """Parse the OSB liturgical cross-references file."""
    entries = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove form feed characters
    content = content.replace('\x0c', '')
    lines = content.split('\n')

    current_book = 'GEN'  # Start with Genesis
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Check for explicit book references (e.g., "Gen 17:1, 2, 4–8...")
        # This pattern: "BookName verse_numbers: Occasion text..."
        # The challenge: verses may contain colons (e.g., "13:1–3")
        # Solution: match the last colon followed by capitalized text as separator
        match_explicit = re.match(
            r'^([A-Za-z0-9]+)\s+(.*?):\s*([A-Z].+)$',
            line
        )

        if match_explicit:
            book_prefix = match_explicit.group(1)
            verse_part = match_explicit.group(2).strip()
            occasion_start = match_explicit.group(3).strip()

            # Try to parse the book name
            normalized_book = normalize_book_name(book_prefix)

            if normalized_book:
                # This is an explicit book reference
                current_book = normalized_book
                book_code = normalized_book

                # Collect occasion text (may span multiple lines)
                occasion_lines = [occasion_start] if occasion_start else []
                i += 1
                while i < len(lines):
                    next_line = lines[i].strip()
                    if not next_line:
                        i += 1
                        break
                    # Check if next line starts a new entry (explicit or implicit)
                    if re.match(r'^[A-Za-z0-9]+\s+[0-9]', next_line) or re.match(r'^[0-9]+:[0-9]', next_line):
                        break
                    occasion_lines.append(next_line)
                    i += 1

                occasion_text = ' '.join(occasion_lines)
                occasions = parse_occasions(occasion_text)

                if occasions and verse_part:
                    reference = f"{book_code} {verse_part}"
                    entries.append({
                        'reference': reference,
                        'occasions': occasions,
                        'needs_review': False
                    })
                continue

        # Try to match implicit book references (no book prefix, just verse range)
        # Pattern: "1:1-3 This passage is read..."
        match_implicit = re.match(
            r'^([0-9:,–\-;\s]+?)\s+(.+)',
            line
        )

        if match_implicit:
            verse_part = match_implicit.group(1).strip()
            occasion_text = match_implicit.group(2).strip()

            # Make sure verse_part looks like a verse range (has : or is all digits)
            if ':' in verse_part or (verse_part and verse_part[0].isdigit()):
                # Collect multi-line occasion text
                occasion_lines = [occasion_text] if occasion_text else []
                i += 1
                while i < len(lines):
                    next_line = lines[i].strip()
                    if not next_line:
                        i += 1
                        break
                    # Check if next line starts a new entry
                    if re.match(r'^[A-Za-z0-9]+\s+[0-9]', next_line) or re.match(r'^[0-9]+:[0-9]', next_line):
                        break
                    occasion_lines.append(next_line)
                    i += 1

                occasion_text = ' '.join(occasion_lines)
                occasions = parse_occasions(occasion_text)

                if occasions:
                    reference = f"{current_book} {verse_part}"
                    entries.append({
                        'reference': reference,
                        'occasions': occasions,
                        'needs_review': True  # Mark implicit book assignments for review
                    })
                continue

        # If we can't parse this line, skip it
        i += 1

    return entries


def main():
    source_file = '/tmp/osb_readat_full.txt'
    output_file = Path('/home/ark/orthodoxphronema/reference/liturgical-crossrefs.json')

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Parse the file
    entries = parse_file(source_file)

    # Create JSON structure
    data = {
        'meta': {
            'source': 'Orthodox Study Bible',
            'description': 'Liturgical cross-references: scripture passages and their liturgical occasions',
            'extracted': '2026-03-14',
            'count': len(entries)
        },
        'entries': entries
    }

    # Write to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Parsed {len(entries)} entries")
    print(f"Wrote to {output_file}")

    # Print summary
    books_with_entries = {}
    for entry in entries:
        book = entry['reference'].split()[0]
        books_with_entries[book] = books_with_entries.get(book, 0) + 1

    print(f"\nEntries by book:")
    for book in OT_BOOK_ORDER + ['MAT', 'MRK', 'LUK', 'JOH', 'ACT', 'ROM', '1CO', '2CO', 'GAL', 'EPH', 'PHP', 'COL', '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 'HEB', 'JAS', '1PE', '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV']:
        if book in books_with_entries:
            print(f"  {book}: {books_with_entries[book]}")


if __name__ == '__main__':
    main()
