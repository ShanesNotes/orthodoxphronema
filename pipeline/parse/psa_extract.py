"""
psa_extract.py — Sequential pdftotext extractor for Psalms and other poetry books.

This preserves Photius's direct-pdftotext state-machine approach while pulling the
reusable logic into shared helpers so other poetry / wisdom books can reuse it
without cloning the whole script.
"""

from __future__ import annotations

import argparse
import sys as _sys
import json
from datetime import date
from pathlib import Path

_R = Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists():
    _R = _R.parent
if str(_R) not in _sys.path:
    _sys.path.insert(0, str(_R))

from pipeline.common.paths import PDF_PATH
from pipeline.common.pdf_source import extract_pdf_text, load_page_ranges
from pipeline.common.poetry import (
    DEFAULT_POETRY_SPLIT_WORD_PAIRS,
    PoetryExtractionConfig,
    extract_poetry_lines,
)
from pipeline.common.registry import book_meta, load_registry

REPO_ROOT = Path(__file__).parent.parent.parent
STAGING = REPO_ROOT / "staging" / "raw"
DEFAULT_PAGE_START = 1739
DEFAULT_PAGE_END = 1914


def resolve_page_range(book_code: str, page_start: int | None, page_end: int | None) -> tuple[int, int]:
    """Resolve extraction page ranges from explicit args first, then registry defaults."""
    if page_start is not None and page_end is not None:
        return page_start, page_end
    if (page_start is None) != (page_end is None):
        raise ValueError("--page-start and --page-end must be provided together")

    page_ranges = load_page_ranges()
    text_range = page_ranges.get(book_code, {}).get("text", [])
    if len(text_range) >= 2:
        return int(text_range[0]), int(text_range[1])

    return DEFAULT_PAGE_START, DEFAULT_PAGE_END


def resolve_book_defaults(book_code: str) -> dict[str, str | int]:
    """Resolve book frontmatter defaults from registry metadata when available."""
    try:
        meta = book_meta(load_registry(), book_code)
    except ValueError:
        meta = None
    if meta is None:
        return {
            "book_name": book_code,
            "testament": "OT",
            "canon_position": 24,
        }

    return {
        "book_name": meta.get("name", book_code),
        "testament": meta.get("testament", "OT"),
        "canon_position": int(meta.get("position", 24)),
    }


def build_config(args: argparse.Namespace, chapter_starts: dict[int, list[str]] = None) -> PoetryExtractionConfig:
    """Build a configurable poetry extractor while keeping Psalms defaults."""
    header_prefixes = tuple(args.header_prefix or ("Psalm",))
    header_regexes = tuple(args.header_regex or ())
    bootstrap_phrases = tuple(args.bootstrap_phrase or ("Blessed is the man",))
    return PoetryExtractionConfig(
        book_code=args.book_code,
        chapter_header_prefixes=header_prefixes,
        chapter_header_regexes=header_regexes,
        first_chapter_bootstrap_phrases=bootstrap_phrases,
        split_word_pairs=DEFAULT_POETRY_SPLIT_WORD_PAIRS,
        chapter_start_phrases=chapter_starts,
    )


def extract_poetry_book(
    config: PoetryExtractionConfig,
    start_page: int,
    end_page: int,
    *,
    layout: bool = False,
) -> str:
    """Extract raw PDF text and run the shared sequential poetry state machine."""
    print(f"[poetry] Extracting PDF pages {start_page}-{end_page} for {config.book_code}...")
    text = extract_pdf_text(
        start_page,
        end_page,
        PDF_PATH,
        layout=layout,
        cache_key=f"{config.book_code.lower()}_poetry",
    )
    return extract_poetry_lines(text.splitlines(), config)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sequential pdftotext extractor for poetry / wisdom books."
    )
    parser.add_argument("--book-code", default="PSA", help="Book code to emit (default: PSA)")
    parser.add_argument("--book-name", help="Book name for frontmatter. If omitted, use registry metadata.")
    parser.add_argument(
        "--page-start",
        type=int,
        help="Start page in OSB PDF. If omitted, use registry page_ranges for the book.",
    )
    parser.add_argument(
        "--page-end",
        type=int,
        help="End page in OSB PDF. If omitted, use registry page_ranges for the book.",
    )
    parser.add_argument(
        "--header-prefix",
        action="append",
        help="Chapter header prefix to detect, repeatable (example: Psalm, Proverbs, Sirach)",
    )
    parser.add_argument(
        "--header-regex",
        action="append",
        help="Additional header regex with chapter in group 1 or named group 'chapter'",
    )
    parser.add_argument(
        "--bootstrap-phrase",
        action="append",
        help="Phrase that bootstraps chapter 1 when the first header is absent",
    )
    parser.add_argument(
        "--layout",
        action="store_true",
        help="Use pdftotext -layout output instead of plain sequential text",
    )
    parser.add_argument(
        "--out-path",
        type=Path,
        help="Optional output path. Defaults to staging/raw/<BOOK>.md",
    )
    parser.add_argument(
        "--chapter-starts",
        type=Path,
        help="Path to JSON manifest of chapter starting phrases",
    )
    args = parser.parse_args()

    # Load chapter starts if provided
    chapter_starts = None
    if args.chapter_starts and args.chapter_starts.exists():
        with open(args.chapter_starts) as f:
            manifest = json.load(f)
            if args.book_code in manifest:
                # Convert string keys to int and wrap in list if necessary
                chapter_starts = {}
                for k, v in manifest[args.book_code].items():
                    chapter_starts[int(k)] = [v] if isinstance(v, str) else v

    config = build_config(args, chapter_starts)
    page_start, page_end = resolve_page_range(args.book_code, args.page_start, args.page_end)
    book_defaults = resolve_book_defaults(args.book_code)
    book_name = args.book_name or str(book_defaults["book_name"])
    testament = str(book_defaults["testament"])
    canon_position = int(book_defaults["canon_position"])
    text = extract_poetry_book(
        config,
        page_start,
        page_end,
        layout=args.layout,
    )

    out_path = args.out_path or (STAGING / f"{args.book_code}.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    frontmatter = f"""---
book_code: {args.book_code}
book_name: "{book_name}"
testament: {testament}
canon_position: {canon_position}
source: "OSB-v1"
parse_date: "{date.today()}"
status: raw
---
"""
    out_path.write_text(frontmatter + text, encoding="utf-8")
    print(f"[poetry] Written to {out_path}")


if __name__ == "__main__":
    main()
