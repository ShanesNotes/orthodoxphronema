"""
pdf_edge_case_check.py - OSB PDF text-layer spot-check for residual V4 gaps.

Purpose:
    When a staged book has a relatively small number of unresolved missing
    anchors, surface source-text windows from the OSB PDF so an LLM or human
    can classify the remaining gaps before broadening parser heuristics.

Usage:
    python3 pipeline/validate/pdf_edge_case_check.py staging/validated/OT/GEN.md
    python3 pipeline/validate/pdf_edge_case_check.py staging/validated/OT/GEN.md --limit 5
    python3 pipeline/validate/pdf_edge_case_check.py staging/validated/OT/GEN.md --json-out reports/GEN_pdf_edge_cases.json
    python3 pipeline/validate/pdf_edge_case_check.py staging/validated/OT/GEN.md --render-dir /tmp/gen_pdf_pages
    python3 pipeline/validate/pdf_edge_case_check.py staging/validated/OT/GEN.md --max-gaps 100
    python3 pipeline/validate/pdf_edge_case_check.py staging/validated/OT/GEN.md --force
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
PDF_PATH = REPO_ROOT / "src.texts" / "the_orthodox_study_bible.pdf"
REGISTRY = REPO_ROOT / "schemas" / "anchor_registry.json"
CACHE_DIR = Path("/tmp/orthodoxphronema_pdf_cache")

RE_ANCHOR = re.compile(r"^([A-Z0-9]+)\.(\d+):(\d+)\s+(.*)$")
RE_FM_FIELD = re.compile(r"^(\w+):\s*(.+)")
RE_FOOTNOTE_MARKERS = re.compile(r"[†ω]+")


@dataclass
class GapCase:
    book_code: str
    chapter: int
    prev_verse: int
    next_verse: int
    missing_verses: list[int]
    prev_lineno: int
    next_lineno: int
    prev_text: str
    next_text: str


@dataclass(frozen=True)
class PdfPage:
    absolute_page: int
    book_page: int
    normalized_text: str


@dataclass(frozen=True)
class PdfMatch:
    scope: str
    method_name: str
    max_bridge_chars: int
    snippet: str
    absolute_page_start: int
    absolute_page_end: int
    book_page_start: int
    book_page_end: int


def load_registry() -> dict:
    with open(REGISTRY, encoding="utf-8") as f:
        return json.load(f)


def parse_frontmatter(lines: list[str]) -> tuple[dict, int]:
    if not lines or lines[0].strip() != "---":
        return {}, 0

    fm: dict[str, str] = {}
    i = 1
    while i < len(lines) and lines[i].strip() != "---":
        match = RE_FM_FIELD.match(lines[i])
        if match:
            fm[match.group(1)] = match.group(2).strip().strip('"')
        i += 1
    return fm, i + 1


def collect_gap_cases(path: Path) -> tuple[str, list[GapCase]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    fm, body_start = parse_frontmatter(lines)
    book_code = fm.get("book_code", path.stem)

    verses_by_chapter: dict[int, list[tuple[int, int, str]]] = {}
    for lineno, line in enumerate(lines[body_start:], start=body_start + 1):
        match = RE_ANCHOR.match(line)
        if not match:
            continue
        _, chapter_s, verse_s, verse_text = match.groups()
        chapter = int(chapter_s)
        verse = int(verse_s)
        verses_by_chapter.setdefault(chapter, []).append((verse, lineno, verse_text))

    cases: list[GapCase] = []
    for chapter, verse_list in sorted(verses_by_chapter.items()):
        prev_verse = 0
        prev_lineno = 0
        prev_text = ""
        for verse, lineno, verse_text in verse_list:
            if verse > prev_verse + 1 and prev_verse > 0:
                missing_verses = list(range(prev_verse + 1, verse))
                cases.append(
                    GapCase(
                        book_code=book_code,
                        chapter=chapter,
                        prev_verse=prev_verse,
                        next_verse=verse,
                        missing_verses=missing_verses,
                        prev_lineno=prev_lineno,
                        next_lineno=lineno,
                        prev_text=prev_text,
                        next_text=verse_text,
                    )
                )
            prev_verse = verse
            prev_lineno = lineno
            prev_text = verse_text

    return book_code, cases


def missing_anchor_count(cases: list[GapCase]) -> int:
    return sum(len(case.missing_verses) for case in cases)


def page_range_for_book(registry: dict, book_code: str) -> tuple[int, int]:
    page_info = registry["page_ranges"][book_code]
    start_page, end_page = page_info["text"]
    return int(start_page), int(end_page)


def ensure_pdftotext() -> str:
    exe = shutil.which("pdftotext")
    if not exe:
        raise RuntimeError("pdftotext is required for PDF edge-case checks")
    return exe


def ensure_pdftoppm() -> str:
    exe = shutil.which("pdftoppm")
    if not exe:
        raise RuntimeError("pdftoppm is required for page rendering")
    return exe


def extract_book_pdf_text(book_code: str, start_page: int, end_page: int) -> str:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"{book_code}_{start_page}_{end_page}.txt"
    if not cache_path.exists():
        exe = ensure_pdftotext()
        subprocess.run(
            [
                exe,
                "-layout",
                "-f",
                str(start_page),
                "-l",
                str(end_page),
                str(PDF_PATH),
                str(cache_path),
            ],
            check=True,
        )
    return cache_path.read_text(encoding="utf-8", errors="ignore")


def is_navigation_page(text: str) -> bool:
    lower = text.lower()
    return (
        "back to table of contents" in lower
        or "chapters in " in lower
        or "verses in " in lower
    )


def normalize_search_text(text: str) -> str:
    text = RE_FOOTNOTE_MARKERS.sub("", text)
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)
    text = re.sub(r"[^A-Za-z0-9]+", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def extract_pdf_pages(raw_pdf_text: str, start_page: int) -> list[PdfPage]:
    pages = raw_pdf_text.split("\x0c")
    if pages and not pages[-1].strip():
        pages = pages[:-1]

    result: list[PdfPage] = []
    for offset, raw_page in enumerate(pages):
        normalized = ""
        if not is_navigation_page(raw_page):
            normalized = normalize_search_text(raw_page)
        result.append(
            PdfPage(
                absolute_page=start_page + offset,
                book_page=offset + 1,
                normalized_text=normalized,
            )
        )
    return result


def phrase_words(text: str) -> list[str]:
    return normalize_search_text(text).split()


def left_phrase_for_case(case: GapCase, word_count: int) -> str:
    first_missing = case.missing_verses[0]
    match = re.search(rf"(?<!\d){first_missing}(?!\d)", case.prev_text)
    source = case.prev_text[: match.start()] if match else case.prev_text
    words = phrase_words(source)
    return " ".join(words[-word_count:])


def right_phrase_for_case(case: GapCase, word_count: int) -> str:
    words = phrase_words(case.next_text)
    return " ".join(words[:word_count])


def number_token(num: int) -> str:
    return rf"(?<!\d){num}(?!\d)"


def build_sequence_pattern(
    numbers: list[int],
    max_bridge_chars: int,
    left_phrase: str = "",
    right_phrase: str = "",
) -> re.Pattern[str]:
    parts: list[str] = []
    if left_phrase:
        parts.append(re.escape(left_phrase))
    for num in numbers:
        if parts:
            parts.append(rf".{{0,{max_bridge_chars}}}?")
        parts.append(number_token(num))
    if right_phrase:
        parts.append(rf".{{0,{max_bridge_chars}}}?")
        parts.append(re.escape(right_phrase))
    return re.compile("(?s)" + "".join(parts))


def find_sequence_window(
    pdf_pages: list[PdfPage],
    case: GapCase,
    context_chars: int,
    phrase_words_count: int,
) -> PdfMatch | None:
    left_phrase = left_phrase_for_case(case, phrase_words_count)
    right_phrase = right_phrase_for_case(case, phrase_words_count)
    number_sets = [[case.prev_verse, *case.missing_verses, case.next_verse]]
    if case.prev_verse == 1:
        number_sets.append([*case.missing_verses, case.next_verse])

    methods = [
        ("full_context", left_phrase, right_phrase),
        ("left_context", left_phrase, ""),
        ("right_context", "", right_phrase),
    ]

    scopes: list[tuple[str, int, int, int, int, str]] = []
    for page in pdf_pages:
        if not page.normalized_text:
            continue
        scopes.append(
            (
                "page",
                page.absolute_page,
                page.absolute_page,
                page.book_page,
                page.book_page,
                page.normalized_text,
            )
        )

    for idx in range(len(pdf_pages) - 1):
        left_page = pdf_pages[idx]
        right_page = pdf_pages[idx + 1]
        combined = " ".join(
            part for part in (left_page.normalized_text, right_page.normalized_text) if part
        ).strip()
        if not combined:
            continue
        scopes.append(
            (
                "page_pair",
                left_page.absolute_page,
                right_page.absolute_page,
                left_page.book_page,
                right_page.book_page,
                combined,
            )
        )

    for numbers in number_sets:
        for scope, abs_start, abs_end, book_start, book_end, search_text in scopes:
            for max_bridge_chars in (240, 480, 960, 1920, 3840):
                for method_name, left_context, right_context in methods:
                    pattern = build_sequence_pattern(
                        numbers,
                        max_bridge_chars=max_bridge_chars,
                        left_phrase=left_context,
                        right_phrase=right_context,
                    )
                    match = pattern.search(search_text)
                    if not match:
                        continue
                    start = max(0, match.start() - context_chars)
                    end = min(len(search_text), match.end() + context_chars)
                    snippet = search_text[start:end].strip()
                    return PdfMatch(
                        scope=scope,
                        method_name=method_name,
                        max_bridge_chars=max_bridge_chars,
                        snippet=snippet,
                        absolute_page_start=abs_start,
                        absolute_page_end=abs_end,
                        book_page_start=book_start,
                        book_page_end=book_end,
                    )
    return None


def summarize_case(case: GapCase) -> str:
    missing = case.missing_verses
    if len(missing) == 1:
        return f"{case.book_code}.{case.chapter}:{missing[0]}"
    return f"{case.book_code}.{case.chapter}:{missing[0]}-{missing[-1]}"


def anchor_label(book_code: str, chapter: int, verse: int) -> str:
    return f"{book_code}.{chapter}:{verse}"


def page_range_label(start_page: int, end_page: int) -> str:
    if start_page == end_page:
        return str(start_page)
    return f"{start_page}-{end_page}"


def render_matched_pages(matches: list[PdfMatch], render_dir: Path) -> dict[int, str]:
    render_dir.mkdir(parents=True, exist_ok=True)
    exe = ensure_pdftoppm()
    rendered: dict[int, str] = {}
    pages_to_render = sorted(
        {
            page
            for match in matches
            for page in range(match.absolute_page_start, match.absolute_page_end + 1)
        }
    )
    for page in pages_to_render:
        output_prefix = render_dir / f"osb_page_{page}"
        candidates = sorted(render_dir.glob(f"osb_page_{page}-*.png"))
        if not candidates:
            subprocess.run(
                [
                    exe,
                    "-png",
                    "-f",
                    str(page),
                    "-l",
                    str(page),
                    str(PDF_PATH),
                    str(output_prefix),
                ],
                check=True,
            )
            candidates = sorted(render_dir.glob(f"osb_page_{page}-*.png"))
        if not candidates:
            raise RuntimeError(f"pdftoppm did not produce an image for page {page}")
        rendered[page] = str(candidates[0])
    return rendered


def build_case_record(
    case: GapCase,
    match: PdfMatch | None,
    rendered_pages: dict[int, str],
) -> dict:
    record = {
        "label": summarize_case(case),
        "book_code": case.book_code,
        "chapter": case.chapter,
        "prev_verse": case.prev_verse,
        "next_verse": case.next_verse,
        "missing_verses": case.missing_verses,
        "staged": {
            "prev_lineno": case.prev_lineno,
            "next_lineno": case.next_lineno,
            "prev_anchor": anchor_label(case.book_code, case.chapter, case.prev_verse),
            "next_anchor": anchor_label(case.book_code, case.chapter, case.next_verse),
            "prev_text": case.prev_text,
            "next_text": case.next_text,
        },
        "pdf_match": None,
    }
    if match is None:
        return record

    pages = list(range(match.absolute_page_start, match.absolute_page_end + 1))
    record["pdf_match"] = {
        "scope": match.scope,
        "method": match.method_name,
        "max_bridge_chars": match.max_bridge_chars,
        "absolute_pages": pages,
        "book_pages": list(range(match.book_page_start, match.book_page_end + 1)),
        "snippet": match.snippet,
        "rendered_pages": [rendered_pages[page] for page in pages if page in rendered_pages],
    }
    return record


def print_report(
    stage_path: Path,
    cases: list[GapCase],
    pdf_pages: list[PdfPage],
    limit: int | None,
    context_chars: int,
    phrase_words_count: int,
    render_dir: Path | None,
) -> tuple[int, list[dict]]:
    total_missing = missing_anchor_count(cases)
    print(f"PDF edge-case spot-check: {stage_path}")
    print(f"Gap groups           : {len(cases)}")
    print(f"Missing anchors      : {total_missing}")
    print(f"Context chars        : {context_chars}")
    print(f"Phrase words         : {phrase_words_count}")
    print()

    matches_found = 0
    displayed = cases if limit is None else cases[:limit]
    records: list[dict] = []
    matched_results: list[PdfMatch] = []
    match_by_label: dict[str, PdfMatch] = {}

    for case in displayed:
        result = find_sequence_window(
            pdf_pages,
            case,
            context_chars=context_chars,
            phrase_words_count=phrase_words_count,
        )
        if result is not None:
            matched_results.append(result)
            match_by_label[summarize_case(case)] = result

    rendered_pages: dict[int, str] = {}
    if render_dir is not None and matched_results:
        rendered_pages = render_matched_pages(matched_results, render_dir)

    for index, case in enumerate(displayed, start=1):
        label = summarize_case(case)
        print(f"[{index}/{len(displayed)}] {label}")
        print(
            f"  staged gap : ch.{case.chapter} {case.prev_verse} -> {case.next_verse} "
            f"(missing {case.missing_verses})"
        )
        print(
            f"  prev line  : {case.prev_lineno} | "
            f"{case.book_code}.{case.chapter}:{case.prev_verse} {case.prev_text[:160]}"
        )
        print(
            f"  next line  : {case.next_lineno} | "
            f"{case.book_code}.{case.chapter}:{case.next_verse} {case.next_text[:160]}"
        )

        result = match_by_label.get(label)
        if result is None:
            print("  pdf match  : not found")
            records.append(build_case_record(case, None, rendered_pages))
            print()
            continue

        matches_found += 1
        abs_pages = page_range_label(result.absolute_page_start, result.absolute_page_end)
        book_pages = page_range_label(result.book_page_start, result.book_page_end)
        print(
            f"  pdf match  : {result.method_name}/{result.scope} "
            f"(max_bridge={result.max_bridge_chars})"
        )
        print(f"  pdf pages  : absolute {abs_pages} | book-local {book_pages}")
        if result.absolute_page_start in rendered_pages:
            first_page = rendered_pages[result.absolute_page_start]
            print(f"  page image : {first_page}")
        print(f"  pdf text   : {result.snippet}")
        records.append(build_case_record(case, result, rendered_pages))
        print()

    print(
        f"Summary: matched {matches_found}/{len(displayed)} displayed gap groups "
        f"from the OSB PDF text layer."
    )
    if limit is not None and len(cases) > limit:
        print(f"Displayed first {limit} of {len(cases)} gap groups.")
    return (0 if matches_found == len(displayed) else 1), records


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Spot-check residual V4 gaps against the OSB PDF text layer."
    )
    parser.add_argument("path", help="Path to staged BOOK.md")
    parser.add_argument(
        "--max-gaps",
        type=int,
        default=100,
        help="Only run automatically when total missing anchors are <= this count",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Run even when the missing-anchor count exceeds --max-gaps",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only print the first N gap groups",
    )
    parser.add_argument(
        "--context-chars",
        type=int,
        default=180,
        help="Characters of PDF context to show around a matched window",
    )
    parser.add_argument(
        "--phrase-words",
        type=int,
        default=6,
        help="Words of staged-text context to use when locating a PDF window",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Write a machine-readable per-gap report to this JSON path",
    )
    parser.add_argument(
        "--render-dir",
        type=Path,
        default=None,
        help="Render matched PDF pages to this directory for visual review",
    )
    args = parser.parse_args()

    stage_path = Path(args.path)
    if not stage_path.exists():
        print(f"ERROR: file not found: {stage_path}", file=sys.stderr)
        sys.exit(1)

    book_code, cases = collect_gap_cases(stage_path)
    total_missing = missing_anchor_count(cases)
    if total_missing == 0:
        print(f"No missing anchors detected in {stage_path}.")
        sys.exit(0)

    if total_missing > args.max_gaps and not args.force:
        print(
            f"Skipped PDF edge-case check: {total_missing} missing anchors "
            f"exceeds threshold {args.max_gaps}."
        )
        print("Re-run with --force to override.")
        sys.exit(2)

    registry = load_registry()
    start_page, end_page = page_range_for_book(registry, book_code)
    raw_pdf_text = extract_book_pdf_text(book_code, start_page, end_page)
    pdf_pages = extract_pdf_pages(raw_pdf_text, start_page)
    exit_code, records = print_report(
        stage_path=stage_path,
        cases=cases,
        pdf_pages=pdf_pages,
        limit=args.limit,
        context_chars=args.context_chars,
        phrase_words_count=args.phrase_words,
        render_dir=args.render_dir,
    )
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "stage_path": str(stage_path),
            "book_code": book_code,
            "book_pdf_pages": {
                "absolute_start": start_page,
                "absolute_end": end_page,
            },
            "gap_groups": len(cases),
            "missing_anchors": total_missing,
            "displayed_cases": len(records),
            "cases": records,
        }
        args.json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Wrote JSON report: {args.json_out}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
