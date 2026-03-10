"""
purity_audit.py — Non-mutating purity scan for staged canon files.

This consolidates editorial candidate discovery for:
  - chapter-opening drop-cap / first-letter omissions
  - split-word residue
  - existing fused-article candidates

Default behavior is report-only. It can optionally merge findings into the
existing BOOK_editorial_candidates.json sidecar so the dashboard and promotion
gates continue to use one editorial queue.
"""

from __future__ import annotations

import argparse
from datetime import date
import json
import re
import sys
from pathlib import Path

import sys as _sys
from pathlib import Path as _Path

_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists():
    _R = _R.parent
if str(_R) not in _sys.path:
    _sys.path.insert(0, str(_R))

from pipeline.cleanup.dropcap_verify import classify_dropcap, _load_normalize
from pipeline.cleanup.fix_articles import (
    build_editorial_report as build_fused_article_report,
    load_brenton_index as load_article_brenton_index,
    merge_editorial_report,
    process_file as process_fused_articles,
)
from pipeline.common.patterns import KNOWN_SPLIT_JOIN_WORDS, RE_ANCHOR, RE_CHAPTER_HDR

RE_SPLIT_SUFFIX = re.compile(
    r"(?<=[a-z])(ov|ev|iv|erv|alv|elv|olv|eav|av|arv|ilv) ([a-z])"
)
RE_LOWER_TOKEN = re.compile(r"\b[a-z]{1,10}\b")
PURITY_CATEGORIES = {"chapter_open_dropcap", "split_word_residue", "fused_article_explicit"}


def _sanitize_scan_text(text: str) -> str:
    """Ignore human review graffiti such as *** while preserving the verse text."""
    return text.replace("***", "").strip()


def _build_report(
    book_code: str,
    filepath: Path,
    candidates: list[dict],
    notes: list[str],
) -> dict:
    by_category: dict[str, int] = {}
    report_candidates: list[dict] = []
    for cand in candidates:
        category = cand["category"]
        by_category[category] = by_category.get(category, 0) + 1
        report_candidates.append(cand)

    return {
        "book": book_code,
        "file": str(filepath),
        "generated": str(date.today()),
        "total_candidates": len(report_candidates),
        "by_category": by_category,
        "candidates": report_candidates,
        "notes": notes,
    }


def scan_chapter_open_dropcaps(
    filepath: Path,
    *,
    brenton_index: dict[str, str] | None = None,
    norm=None,
) -> list[dict]:
    """Find lowercase chapter-opening verse-1 lines after chapter headings."""
    lines = filepath.read_text(encoding="utf-8").splitlines()
    candidates: list[dict] = []

    for i, line in enumerate(lines[:-1]):
        if not RE_CHAPTER_HDR.match(line):
            continue

        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j >= len(lines):
            continue

        verse_line = lines[j]
        anchor_match = RE_ANCHOR.match(verse_line)
        if not anchor_match:
            continue

        book_code = anchor_match.group(1)
        chapter_s = anchor_match.group(2)
        verse_s = anchor_match.group(3)
        anchor = f"{book_code}.{chapter_s}:{verse_s}"
        if verse_s != "1":
            continue

        text = _sanitize_scan_text(verse_line[anchor_match.end():])
        if not text or not text[0].islower():
            continue

        result = classify_dropcap(
            anchor,
            text,
            int(chapter_s),
            int(verse_s),
            brenton_index,
            norm,
        )
        if result is None:
            continue

        confidence = 0.95 if result["classification"] == "confirmed_auto" else 0.70
        residual = result.get("residual") or text[:60]
        token = residual.split()[0] if residual.split() else residual
        source_hint = result.get("source", "heuristic")
        if result.get("classification"):
            source_hint = f"{source_hint}:{result['classification']}"

        candidates.append(
            {
                "line": j + 1,
                "anchor": anchor,
                "category": "chapter_open_dropcap",
                "token": token,
                "confidence": confidence,
                "source_hint": source_hint,
                "manual_status": "pending",
                "replacement": result.get("proposed_repair"),
            }
        )

    return candidates


def scan_split_word_residue(filepath: Path) -> list[dict]:
    """Find live split-word residue using the same core V11 patterns."""
    lines = filepath.read_text(encoding="utf-8").splitlines()
    candidates: list[dict] = []

    for line_number, line in enumerate(lines, 1):
        anchor_match = RE_ANCHOR.match(line)
        if not anchor_match:
            continue
        anchor = anchor_match.group(1)
        text = _sanitize_scan_text(line[anchor_match.end():])
        seen_contexts: set[str] = set()

        for match in RE_SPLIT_SUFFIX.finditer(text):
            word_start = text.rfind(" ", 0, match.start()) + 1
            if word_start < match.start() and text[word_start].isupper():
                continue
            context = text[max(0, match.start() - 8):match.end() + 8].strip()
            if context in seen_contexts:
                continue
            seen_contexts.add(context)
            candidates.append(
                {
                    "line": line_number,
                    "anchor": anchor,
                    "category": "split_word_residue",
                    "token": context,
                    "confidence": 0.85,
                    "source_hint": "v11_suffix_regex",
                    "manual_status": "pending",
                    "replacement": context.replace(" ", "", 1),
                }
            )

        token_matches = list(RE_LOWER_TOKEN.finditer(text))
        for left_match, right_match in zip(token_matches, token_matches[1:]):
            if left_match.end() + 1 != right_match.start():
                continue
            left = left_match.group(0)
            right = right_match.group(0)
            joined = f"{left}{right}"
            if joined not in KNOWN_SPLIT_JOIN_WORDS:
                continue
            context = text[max(0, left_match.start() - 8):right_match.end() + 8].strip()
            if context in seen_contexts:
                continue
            seen_contexts.add(context)
            candidates.append(
                {
                    "line": line_number,
                    "anchor": anchor,
                    "category": "split_word_residue",
                    "token": context,
                    "confidence": 0.90,
                    "source_hint": "known_split_join_words",
                    "manual_status": "pending",
                    "replacement": joined,
                }
            )

    return candidates


def run_purity_audit(
    filepath: Path,
    *,
    include_fused_articles: bool = True,
    fused_article_min_confidence: float = 0.75,
    use_brenton: bool = False,
) -> dict:
    """Build a merged editorial-candidate report for purity issues."""
    book_code = filepath.stem.split("_")[0]
    brenton_index = None
    norm = None

    if use_brenton:
        try:
            norm = _load_normalize()
        except Exception:
            norm = None
        brenton_index = load_article_brenton_index(book_code)

    chapter_candidates = scan_chapter_open_dropcaps(
        filepath,
        brenton_index=brenton_index,
        norm=norm,
    )
    split_candidates = scan_split_word_residue(filepath)
    purity_report = _build_report(
        book_code,
        filepath,
        chapter_candidates + split_candidates,
        notes=[
            "Purity audit from purity_audit.py",
            "Chapter-opening drop-cap suspects and split-word residue should block promotion until resolved or ratified",
            "Inline *** review markers were ignored during detection",
        ],
    )

    if not include_fused_articles:
        return purity_report

    fused_brenton = brenton_index if use_brenton else None
    _, fused_candidates = process_fused_articles(
        filepath,
        fused_brenton,
        threshold=0.70,
        apply_fixes=False,
    )
    fused_report = build_fused_article_report(
        book_code,
        filepath,
        fused_candidates,
        min_confidence=fused_article_min_confidence,
    )
    return merge_editorial_report(fused_report, purity_report)


def replace_owned_categories(existing: dict | None, owned_categories: set[str]) -> dict | None:
    """Drop stale purity-audit categories before merging refreshed scan results."""
    if not existing:
        return None

    cleaned = dict(existing)
    kept_candidates = [
        candidate
        for candidate in existing.get("candidates", [])
        if candidate.get("category") not in owned_categories
    ]
    cleaned["candidates"] = kept_candidates
    cleaned["total_candidates"] = len(kept_candidates)

    by_category: dict[str, int] = {}
    for item in kept_candidates:
        category = item.get("category", "unknown")
        by_category[category] = by_category.get(category, 0) + 1
    cleaned["by_category"] = by_category
    return cleaned


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Non-mutating purity audit for chapter-open truncation and conjoined-word residue."
    )
    parser.add_argument("file", type=Path, help="Staged canon .md file")
    parser.add_argument(
        "--editorial-report",
        action="store_true",
        help="Print merged BOOK_editorial_candidates-style JSON report",
    )
    parser.add_argument(
        "--editorial-out",
        type=Path,
        help="Write or merge findings into BOOK_editorial_candidates.json",
    )
    parser.add_argument(
        "--reference",
        choices=["brenton"],
        help="Use Brenton for drop-cap / fused-article confirmation when available",
    )
    parser.add_argument(
        "--skip-fused-articles",
        action="store_true",
        help="Exclude fused-article candidates from the purity report",
    )
    parser.add_argument(
        "--fused-min-confidence",
        type=float,
        default=0.75,
        help="Minimum confidence for fused-article editorial candidates (default: 0.75)",
    )
    args = parser.parse_args()

    if not args.file.exists():
        print(f"ERROR: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    report = run_purity_audit(
        args.file,
        include_fused_articles=not args.skip_fused_articles,
        fused_article_min_confidence=args.fused_min_confidence,
        use_brenton=args.reference == "brenton",
    )

    if args.editorial_out:
        existing = None
        if args.editorial_out.exists():
            existing = json.loads(args.editorial_out.read_text(encoding="utf-8"))
            existing = replace_owned_categories(
                existing,
                set(PURITY_CATEGORIES if not args.skip_fused_articles else {"chapter_open_dropcap", "split_word_residue"}),
            )
        merged = merge_editorial_report(existing, report)
        args.editorial_out.write_text(
            json.dumps(merged, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    if args.editorial_report or not args.editorial_out:
        print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
