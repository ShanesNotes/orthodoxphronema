"""pdf_verify.py — pdftotext-based ground truth verifier for OSB extraction.

When validation flags missing verses, embedded content, or absorbed text,
this tool extracts raw text from the source PDF pages via pdftotext and
searches for the verse content. This is the programmatic equivalent of
"flipping to the page" to check what's actually there.

Usage (CLI):
    python3 pipeline/tools/pdf_verify.py --book GEN --anchor GEN.25:34
    python3 pipeline/tools/pdf_verify.py --book GEN --page 150
    python3 pipeline/tools/pdf_verify.py --book GEN --pages 150-155
    python3 pipeline/tools/pdf_verify.py --book GEN --chapter 25

Usage (library):
    from pipeline.tools.pdf_verify import extract_page_text, verify_anchor, verify_gaps
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
import pipeline.common.paths as _paths
from pipeline.common.pdf_source import (
    extract_pdf_text,
    estimate_chapter_page_range,
    load_chapter_verse_counts,
    load_page_ranges,
)
from pipeline.common.types import CheckResult, ValidationResult

PDF_PATH = _paths.PDF_PATH


def search_in_text(text: str, pattern: str, context: int = 80) -> list[str]:
    """Search for a pattern in extracted text, returning context lines."""
    hits = []
    for m in re.finditer(pattern, text, re.IGNORECASE):
        start = max(0, m.start() - context)
        end = min(len(text), m.end() + context)
        snippet = text[start:end].replace("\n", " ").strip()
        hits.append(snippet)
    return hits


def _estimate_page_for_chapter(
    book_code: str,
    chapter: int,
    page_ranges: dict | None = None,
    cvc: dict[int, int] | None = None,
) -> tuple[int, int]:
    return estimate_chapter_page_range(
        book_code,
        chapter,
        page_ranges=page_ranges,
        cvc=cvc,
    )


def verify_anchor(
    book_code: str,
    chapter: int,
    verse: int,
    brenton_path: Path | None = None,
) -> dict:
    """Verify a specific anchor against the source PDF.

    Returns a dict with:
        - found: bool — whether verse text was found
        - page_range: (start, end) pages checked
        - snippets: list of matching text snippets
        - brenton_text: Brenton reference text (if available)
    """
    page_start, page_end = _estimate_page_for_chapter(book_code, chapter)
    raw_text = extract_pdf_text(
        page_start,
        page_end,
        PDF_PATH,
        cache_key=f"{book_code}_chapter_verify",
    )

    # Search for verse number in context
    # Pattern: the verse number preceded by whitespace or start-of-line
    pattern = rf'(?:^|\s){verse}\s+[A-Z]'
    snippets = search_in_text(raw_text, pattern)

    # Also try Brenton keywords if available
    brenton_text = ""
    brenton_keywords = []
    if brenton_path is None:
        brenton_path = _paths.BRENTON_DIR / f"{book_code}.json"
    if brenton_path.exists():
        try:
            with open(brenton_path, encoding="utf-8") as f:
                brenton_data = json.load(f)
            ch_str = str(chapter)
            if ch_str in brenton_data.get("chapters", {}):
                verses_list = brenton_data["chapters"][ch_str].get("verses", [])
                idx = verse - 1
                if 0 <= idx < len(verses_list):
                    brenton_text = verses_list[idx]
                    # Extract significant words for searching
                    brenton_keywords = [
                        w for w in re.findall(r'[a-z]+', brenton_text.lower())
                        if len(w) >= 5
                    ]
        except Exception:
            pass

    # Search for Brenton keywords in PDF text
    keyword_hits = 0
    if brenton_keywords:
        pdf_lower = raw_text.lower()
        keyword_hits = sum(1 for kw in brenton_keywords if kw in pdf_lower)

    # Conservative: "found" requires verse number match in PDF.
    # Keyword matches are supporting evidence but not sufficient alone
    # (common words can match across a wide page range).
    return {
        "anchor": f"{book_code}.{chapter}:{verse}",
        "found": len(snippets) > 0,
        "keyword_evidence": keyword_hits >= 3 and len(brenton_keywords) > 0,
        "page_range": (page_start, page_end),
        "snippets": snippets[:5],
        "brenton_text": brenton_text,
        "brenton_keyword_hits": keyword_hits,
        "brenton_keywords_total": len(brenton_keywords),
    }


def verify_gaps(
    book_code: str,
    v4_source: CheckResult | ValidationResult | list[str],
) -> list[dict]:
    """Verify all V4 gap anchors against the source PDF."""
    results = []

    if isinstance(v4_source, ValidationResult):
        check = v4_source.check("V4")
        gap_anchors = check.data.get("missing_anchors", []) if check else []
    elif isinstance(v4_source, CheckResult):
        gap_anchors = v4_source.data.get("missing_anchors", [])
    else:
        re_v4 = re.compile(r'V4\s+Missing verses in ch\.(\d+): jumps from (\d+) to (\d+)')
        gap_anchors = []
        for warning in v4_source:
            match = re_v4.match(warning)
            if not match:
                continue
            ch = int(match.group(1))
            gap_from = int(match.group(2))
            gap_to = int(match.group(3))
            gap_anchors.extend(f"{book_code}.{ch}:{v}" for v in range(gap_from + 1, gap_to))

    for anchor in gap_anchors:
        match = re.match(r'([A-Z0-9]+)\.(\d+):(\d+)', anchor)
        if not match:
            continue
        ch, v = int(match.group(2)), int(match.group(3))
        results.append(verify_anchor(book_code, ch, v))

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify OSB PDF content via pdftotext."
    )
    parser.add_argument("--book", required=True, help="Book code (e.g. GEN)")
    parser.add_argument("--anchor", help="Specific anchor (e.g. GEN.25:34)")
    parser.add_argument("--chapter", type=int, help="Chapter number to extract")
    parser.add_argument("--page", type=int, help="Single page to extract")
    parser.add_argument("--pages", help="Page range (e.g. 150-155)")
    parser.add_argument("--search", help="Search pattern in extracted text")
    args = parser.parse_args()

    book_code = args.book.upper()

    if args.anchor:
        # Parse anchor
        m = re.match(r'([A-Z0-9]+)\.(\d+):(\d+)', args.anchor.upper())
        if not m:
            print(f"Invalid anchor format: {args.anchor}", file=sys.stderr)
            sys.exit(1)
        ch, v = int(m.group(2)), int(m.group(3))
        result = verify_anchor(book_code, ch, v)
        print(f"\nVerifying: {result['anchor']}")
        print(f"Pages checked: {result['page_range'][0]}-{result['page_range'][1]}")
        found_str = "YES (verse number match)" if result["found"] else "NO"
        if result.get("keyword_evidence") and not result["found"]:
            found_str += " (but Brenton keywords suggest content nearby)"
        print(f"Found in PDF: {found_str}")
        if result["snippets"]:
            print(f"\nSnippets ({len(result['snippets'])}):")
            for s in result["snippets"]:
                print(f"  ...{s}...")
        if result["brenton_text"]:
            print(f"\nBrenton reference: {result['brenton_text'][:120]}")
            print(f"Keyword matches in PDF: {result['brenton_keyword_hits']}"
                  f"/{result['brenton_keywords_total']}")

    elif args.chapter:
        page_start, page_end = _estimate_page_for_chapter(book_code, args.chapter)
        print(f"\nEstimated pages for {book_code} ch.{args.chapter}: {page_start}-{page_end}")
        text = extract_pdf_text(page_start, page_end, PDF_PATH)
        if args.search:
            hits = search_in_text(text, args.search)
            print(f"Search '{args.search}': {len(hits)} hit(s)")
            for h in hits[:10]:
                print(f"  ...{h}...")
        else:
            # Print first 2000 chars
            print(text[:2000])

    elif args.page or args.pages:
        if args.pages:
            parts = args.pages.split("-")
            p_start, p_end = int(parts[0]), int(parts[1])
        else:
            p_start = p_end = args.page
        text = extract_pdf_text(p_start, p_end, PDF_PATH)
        if args.search:
            hits = search_in_text(text, args.search)
            print(f"Search '{args.search}': {len(hits)} hit(s)")
            for h in hits[:10]:
                print(f"  ...{h}...")
        else:
            print(text[:3000])

    else:
        print("Specify --anchor, --chapter, --page, or --pages", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
