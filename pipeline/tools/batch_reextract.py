"""
batch_reextract.py — Recover truncated verses via targeted Docling re-extraction.

For each truncation candidate, extracts a page range from the OSB PDF,
searches for the verse's search key, and captures the full verse text.

Usage:
    python3 pipeline/tools/batch_reextract.py --book EXO
    python3 pipeline/tools/batch_reextract.py --book LEV
    python3 pipeline/tools/batch_reextract.py --book EXO --apply
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import sys as _sys; from pathlib import Path as _Path
_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists(): _R = _R.parent
if str(_R) not in _sys.path: _sys.path.insert(0, str(_R))
from pipeline.common.paths import REPO_ROOT, PDF_PATH

# Truncation targets: (anchor, page_start, page_end)
TARGETS = {
    "EXO": [
        ("EXO.1:1",   189, 195),
        ("EXO.3:1",   193, 200),
        ("EXO.9:1",   213, 220),
        ("EXO.9:24",  216, 222),
        ("EXO.11:1",  223, 230),
        ("EXO.15:25", 236, 242),
        ("EXO.17:1",  241, 248),
        ("EXO.18:1",  245, 252),
        ("EXO.18:2",  245, 252),
        ("EXO.27:20", 270, 276),
        ("EXO.33:1",  285, 292),
        ("EXO.34:13", 288, 294),
        ("EXO.35:1",  290, 296),
        ("EXO.35:31", 292, 298),
    ],
    "LEV": [
        ("LEV.10:1",  325, 335),
        ("LEV.14:21", 340, 348),
        ("LEV.16:1",  348, 356),
        ("LEV.17:8",  355, 362),
        ("LEV.21:1",  365, 375),
        # Also try to recover residual missing verses
        ("LEV.8:18",  315, 325),
        ("LEV.8:19",  315, 325),
        ("LEV.8:20",  315, 325),
        ("LEV.8:21",  315, 325),
        ("LEV.21:2",  365, 375),
        ("LEV.21:3",  365, 375),
    ],
}

from pipeline.common.patterns import RE_FOOTNOTE_MARKERS as RE_FOOTNOTE, RE_SPACED_CAPS

# Verse boundary: digits followed by uppercase or opening punct
RE_VERSE_BOUNDARY = re.compile(
    r'([†ω]*)\s*(\d+)'
    r'(?:'
    r'\s+(?=[A-Z\'"\u201c\u2018])'
    r'|'
    r'\s*(?=[(\[\'"\u201c\u2018][A-Za-z])'
    r')'
)


def normalize_text(t: str) -> str:
    """Normalize Docling text: strip tabs, collapse whitespace."""
    return re.sub(r'\s+', ' ', t.replace('\t', ' ')).strip()


def extract_page_range(page_start: int, page_end: int) -> str:
    """Extract text from PDF page range using Docling."""
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    pipeline_options.do_table_structure = False

    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )

    result = converter.convert(str(PDF_PATH), page_range=(page_start, page_end))
    doc = result.document

    parts = []
    for item in doc.iterate_items():
        elem = item[0] if isinstance(item, tuple) else item
        etype = type(elem).__name__
        if etype == "PictureItem":
            continue
        text = getattr(elem, "text", "") or ""
        text = normalize_text(text)
        if not text:
            continue
        # Skip spaced-caps study article headers
        if etype == "SectionHeaderItem" and RE_SPACED_CAPS.match(text):
            continue
        parts.append(text)

    return " ".join(parts)


def find_verse_text(full_text: str, book_code: str, chapter: int, verse: int) -> str | None:
    """
    Find the full text for a specific verse in extracted text.
    Searches for the verse number boundary and captures text until the next verse.
    """
    # Build patterns for this specific verse
    # Strategy: find all verse-number boundaries, locate our target, capture text to next boundary

    # First, find all verse boundaries in the text
    boundaries = []
    for m in RE_VERSE_BOUNDARY.finditer(full_text):
        vnum = int(m.group(2))
        boundaries.append((m.start(), m.end(), vnum))

    if not boundaries:
        return None

    # Look for our target verse number
    # For chapter-first verses (verse 1), also look for chapter number as lead-in
    target_hits = []
    for i, (start, end, vnum) in enumerate(boundaries):
        if vnum == verse:
            # Get text from this boundary to the next
            if i + 1 < len(boundaries):
                next_start = boundaries[i + 1][0]
            else:
                next_start = len(full_text)

            verse_text = full_text[end:next_start].strip()
            # Strip footnote markers
            verse_text = RE_FOOTNOTE.sub('', verse_text).strip()
            # Clean up extra spaces
            verse_text = re.sub(r'\s+', ' ', verse_text)

            if len(verse_text) > 10:  # Minimum viable verse
                target_hits.append(verse_text)

    if not target_hits:
        return None

    # Return the longest hit (most complete)
    return max(target_hits, key=len)


def load_current_verses(book_code: str) -> dict[str, tuple[int, str]]:
    """Load current verse texts from staged file. Returns {anchor: (line_num, text)}."""
    testament = "OT"  # Both EXO and LEV are OT
    staged = REPO_ROOT / "staging" / "validated" / testament / f"{book_code}.md"
    verses = {}
    with open(staged, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.rstrip('\n')
            if line.startswith(f"{book_code}."):
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    anchor = parts[0]
                    text = parts[1]
                    verses[anchor] = (i, text)
    return verses


def apply_recovery(book_code: str, recoveries: dict[str, str]) -> int:
    """Apply recovered verse texts to staged file. Returns count of applied fixes."""
    testament = "OT"
    staged = REPO_ROOT / "staging" / "validated" / testament / f"{book_code}.md"

    content = staged.read_text(encoding="utf-8")
    lines = content.split('\n')
    applied = 0

    for anchor, new_text in recoveries.items():
        for i, line in enumerate(lines):
            if line.startswith(f"{anchor} "):
                old_text = line.split(' ', 1)[1] if ' ' in line else ''
                # Only apply if new text is longer (more complete)
                if len(new_text) > len(old_text):
                    lines[i] = f"{anchor} {new_text}"
                    applied += 1
                    print(f"  [apply] {anchor}: {len(old_text)} -> {len(new_text)} chars")
                else:
                    print(f"  [skip]  {anchor}: existing ({len(old_text)}) >= recovered ({len(new_text)})")
                break

    if applied:
        staged.write_text('\n'.join(lines), encoding="utf-8")

    return applied


def main():
    parser = argparse.ArgumentParser(description="Batch re-extract truncated verses")
    parser.add_argument("--book", required=True, help="Book code (EXO or LEV)")
    parser.add_argument("--apply", action="store_true", help="Apply recovered text to staged file")
    args = parser.parse_args()

    book_code = args.book.upper()
    if book_code not in TARGETS:
        print(f"ERROR: No targets defined for {book_code}", file=sys.stderr)
        sys.exit(1)

    targets = TARGETS[book_code]
    current_verses = load_current_verses(book_code)

    # Group targets by page range to minimize Docling calls
    range_cache: dict[tuple[int, int], str] = {}
    recoveries: dict[str, str] = {}
    not_recovered: list[str] = []

    for anchor, pg_start, pg_end in targets:
        parts = anchor.split('.')
        chapter = int(parts[1].split(':')[0])
        verse = int(parts[1].split(':')[1])

        cache_key = (pg_start, pg_end)
        if cache_key not in range_cache:
            print(f"\n[docling] Extracting pages {pg_start}-{pg_end} ...")
            try:
                range_cache[cache_key] = extract_page_range(pg_start, pg_end)
                print(f"[docling] Got {len(range_cache[cache_key])} chars of text")
            except Exception as e:
                print(f"[docling] FAILED: {e}")
                range_cache[cache_key] = ""

        full_text = range_cache[cache_key]
        if not full_text:
            not_recovered.append(anchor)
            continue

        # Try to find the verse in extracted text
        recovered = find_verse_text(full_text, book_code, chapter, verse)

        if recovered:
            current = current_verses.get(anchor)
            current_text = current[1] if current else ""
            current_len = len(current_text)

            if len(recovered) > current_len:
                recoveries[anchor] = recovered
                print(f"  [OK]    {anchor}: recovered {len(recovered)} chars (was {current_len})")
            elif current:
                print(f"  [SAME]  {anchor}: recovered ({len(recovered)}) <= existing ({current_len})")
            else:
                # Verse was missing entirely (residual) — any recovery is good
                recoveries[anchor] = recovered
                print(f"  [NEW]   {anchor}: recovered {len(recovered)} chars (was missing)")
        else:
            not_recovered.append(anchor)
            print(f"  [MISS]  {anchor}: not found in pages {pg_start}-{pg_end}")

    # Also try search-key approach for missed verses
    if not_recovered:
        print(f"\n[info] {len(not_recovered)} verse(s) not recovered via boundary search.")
        print("       Attempting search-key fallback ...")

        still_missing = []
        for anchor in not_recovered:
            current = current_verses.get(anchor)
            if not current:
                still_missing.append(anchor)
                continue

            current_text = current[1]
            # Use last 40 chars as search key
            search_key = current_text[-40:] if len(current_text) > 40 else current_text
            # Escape regex special chars
            search_key_escaped = re.escape(search_key)

            # Find in any cached range
            target_entry = [(a, s, e) for a, s, e in targets if a == anchor][0]
            cache_key = (target_entry[1], target_entry[2])
            full_text = range_cache.get(cache_key, "")

            if not full_text:
                still_missing.append(anchor)
                continue

            m = re.search(search_key_escaped, full_text)
            if m:
                # Found the search key — now grab text from the verse start
                # Look backward from match to find the verse number
                pre_text = full_text[:m.start()]
                # Find the last verse boundary before our match
                last_boundary = None
                for bm in RE_VERSE_BOUNDARY.finditer(pre_text):
                    last_boundary = bm

                if last_boundary:
                    # Grab from after the verse number to the next boundary
                    verse_start = last_boundary.end()
                    post_text = full_text[verse_start:]
                    # Find next verse boundary
                    next_b = RE_VERSE_BOUNDARY.search(post_text[1:])  # skip first char
                    if next_b:
                        verse_text = post_text[:next_b.start() + 1].strip()
                    else:
                        verse_text = post_text.strip()

                    verse_text = RE_FOOTNOTE.sub('', verse_text).strip()
                    verse_text = re.sub(r'\s+', ' ', verse_text)

                    if len(verse_text) > len(current_text):
                        recoveries[anchor] = verse_text
                        print(f"  [KEY]   {anchor}: recovered {len(verse_text)} chars via search key")
                    else:
                        still_missing.append(anchor)
                        print(f"  [SHORT] {anchor}: search-key result ({len(verse_text)}) <= existing ({len(current_text)})")
                else:
                    still_missing.append(anchor)
            else:
                still_missing.append(anchor)
                print(f"  [MISS]  {anchor}: search key not found in extracted text")

        not_recovered = still_missing

    # Summary
    print(f"\n{'='*60}")
    print(f"[summary] {book_code}: {len(recoveries)} recovered, {len(not_recovered)} not recovered")
    if not_recovered:
        print(f"  Not recovered: {', '.join(not_recovered)}")

    # Apply if requested
    if args.apply and recoveries:
        print(f"\n[apply] Applying {len(recoveries)} recoveries to staged file ...")
        applied = apply_recovery(book_code, recoveries)
        print(f"[apply] Applied {applied} fixes")
    elif recoveries and not args.apply:
        print("\n[info] Run with --apply to write recovered text to staged file")

    # Output recoveries as JSON for review
    output = {
        "book": book_code,
        "recovered": {k: v for k, v in recoveries.items()},
        "not_recovered": not_recovered,
    }
    output_path = REPO_ROOT / "reports" / f"{book_code}_reextraction_results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n[output] Results written to {output_path}")


if __name__ == "__main__":
    main()
