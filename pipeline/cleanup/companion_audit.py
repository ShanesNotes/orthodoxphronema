"""
companion_audit.py — Non-mutating batch audit for all companion files.

Checks footnotes, articles, and footnote-marker files across the entire
76-book canon for:
  1. Frontmatter compliance against schemas/notes_frontmatter.json
  2. Fused section headers in footnotes
  3. Marker/footnote anchor alignment
  4. Marker JSON format (dict vs bare-list)
  5. Article status (exists / empty-sentinel / has-content)
  6. Missing files

Writes JSON report to reports/companion_audit.json (configurable via --report).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

# ── repo-root bootstrap (standard pipeline pattern) ─────────────────────────
import sys as _sys
from pathlib import Path as _Path

_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists():
    _R = _R.parent
if str(_R) not in _sys.path:
    _sys.path.insert(0, str(_R))

from pipeline.common.paths import STAGING_ROOT, REGISTRY_PATH, REPORTS_ROOT
from pipeline.common.registry import load_registry, book_testament

# ── Schema constants ─────────────────────────────────────────────────────────

REQUIRED_FRONTMATTER = {"book_code", "content_type", "source", "parse_date", "status"}
VALID_CONTENT_TYPES = {"footnotes", "study_notes", "book_introduction", "article", "appendix"}
VALID_STATUSES = {"staging", "validated", "promoted"}
SOURCE_PATTERN = re.compile(r"^OSB-v[0-9]+$")

# ── Regex patterns ───────────────────────────────────────────────────────────

RE_FUSED_HEADER = re.compile(r"[^\n]### \d+:\d+")
RE_FOOTNOTE_ANCHOR = re.compile(r"\(anchor: ([A-Z0-9]+\.\d+:\d+)\)")

# ── Frontmatter parser ──────────────────────────────────────────────────────


def _parse_yaml_frontmatter(text: str) -> dict | None:
    """Minimal YAML frontmatter parser (avoids pyyaml dependency).

    Handles the subset of YAML used in our companion files: simple key: value
    pairs, quoted strings, null literals, and bracket lists.
    """
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end].strip()
    result: dict = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        colon = line.find(":")
        if colon == -1:
            continue
        key = line[:colon].strip()
        val = line[colon + 1:].strip()
        # Strip quotes
        if len(val) >= 2 and val[0] in ('"', "'") and val[-1] == val[0]:
            val = val[1:-1]
        if val == "null":
            val = None
        result[key] = val
    return result


# ── Per-file checks ─────────────────────────────────────────────────────────


def _check_frontmatter(text: str, expected_content_type: str | None = None) -> list[str]:
    """Validate frontmatter fields. Returns list of issue strings."""
    issues: list[str] = []
    fm = _parse_yaml_frontmatter(text)
    if fm is None:
        issues.append("missing YAML frontmatter block")
        return issues

    # Required fields
    for field in REQUIRED_FRONTMATTER:
        if field not in fm or fm[field] is None:
            issues.append(f"missing required field: {field}")

    # content_type enum
    ct = fm.get("content_type")
    if ct is not None and ct not in VALID_CONTENT_TYPES:
        issues.append(f"invalid content_type: {ct!r}")

    # source pattern
    src = fm.get("source")
    if src is not None and not SOURCE_PATTERN.match(src):
        issues.append(f"invalid source format: {src!r}")

    # status enum
    st = fm.get("status")
    if st is not None and st not in VALID_STATUSES:
        issues.append(f"invalid status: {st!r}")

    return issues


def _count_fused_headers(text: str) -> int:
    """Count lines with fused section headers (text immediately before ### N:N)."""
    return len(RE_FUSED_HEADER.findall(text))


def _extract_footnote_anchors(text: str) -> set[str]:
    """Extract all (anchor: BOOK.CH:V) references from footnotes markdown."""
    return set(RE_FOOTNOTE_ANCHOR.findall(text))


def _load_marker_anchors(path: Path) -> tuple[str, set[str], int]:
    """Load marker file, return (format, anchor_set, count).

    format is 'dict' if top-level is object with 'markers' key,
    'list' if top-level is a bare JSON array.
    """
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        anchors = {m.get("anchor", "") for m in data if isinstance(m, dict)}
        return "list", anchors, len(data)
    elif isinstance(data, dict):
        markers = data.get("markers", [])
        anchors = {m.get("anchor", "") for m in markers if isinstance(m, dict)}
        return "dict", anchors, len(markers)
    else:
        return "unknown", set(), 0


def _article_status(path: Path) -> tuple[bool, bool]:
    """Return (exists, is_empty_sentinel)."""
    if not path.exists():
        return False, False
    text = path.read_text(encoding="utf-8")
    # Empty sentinel pattern: file with only frontmatter + sentinel line
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            body = text[end + 4:].strip()
    # Check for empty-sentinel markers
    if not body or body.startswith("*(No ") or body.startswith("*(Empty"):
        return True, True
    return True, False


# ── Main audit loop ─────────────────────────────────────────────────────────


def run_audit() -> dict:
    """Run audit across all books and return the full report dict."""
    registry = load_registry()
    books = registry["books"]

    report_books: dict[str, dict] = {}
    summary = {
        "total_books": len(books),
        "footnotes_files": 0,
        "articles_files": 0,
        "marker_files": 0,
        "frontmatter_issues": 0,
        "fused_headers": 0,
        "marker_alignment_pass": 0,
        "marker_alignment_fail": 0,
        "marker_format_dict": 0,
        "marker_format_list": 0,
        "empty_articles": 0,
        "missing_articles": 0,
    }

    for book in books:
        code = book["code"]
        testament = book.get("testament", book_testament(registry, code) or "OT")
        base = STAGING_ROOT / testament

        fn_path = base / f"{code}_footnotes.md"
        art_path = base / f"{code}_articles.md"
        mkr_path = base / f"{code}_footnote_markers.json"

        book_report: dict = {}

        # ── Footnotes ────────────────────────────────────────────────────
        fn_entry: dict = {"exists": fn_path.exists()}
        if fn_path.exists():
            summary["footnotes_files"] += 1
            fn_text = fn_path.read_text(encoding="utf-8")
            fm_issues = _check_frontmatter(fn_text, expected_content_type="footnotes")
            fn_entry["frontmatter_issues"] = fm_issues
            summary["frontmatter_issues"] += len(fm_issues)

            fused = _count_fused_headers(fn_text)
            fn_entry["fused_header_count"] = fused
            summary["fused_headers"] += fused

            fn_anchors = _extract_footnote_anchors(fn_text)
            fn_entry["anchor_count"] = len(fn_anchors)
        else:
            fn_entry["frontmatter_issues"] = ["file missing"]
            fn_entry["fused_header_count"] = 0
            fn_entry["anchor_count"] = 0
            fn_anchors = set()

        book_report["footnotes"] = fn_entry

        # ── Articles ─────────────────────────────────────────────────────
        art_exists, art_empty = _article_status(art_path)
        art_entry: dict = {"exists": art_exists, "empty": art_empty}
        if art_exists:
            summary["articles_files"] += 1
            art_text = art_path.read_text(encoding="utf-8")
            art_fm_issues = _check_frontmatter(art_text, expected_content_type="article")
            art_entry["frontmatter_issues"] = art_fm_issues
            summary["frontmatter_issues"] += len(art_fm_issues)
            if art_empty:
                summary["empty_articles"] += 1
        else:
            art_entry["frontmatter_issues"] = []
            summary["missing_articles"] += 1

        book_report["articles"] = art_entry

        # ── Markers ──────────────────────────────────────────────────────
        mkr_entry: dict = {"exists": mkr_path.exists()}
        if mkr_path.exists():
            summary["marker_files"] += 1
            try:
                fmt, mkr_anchors, mkr_count = _load_marker_anchors(mkr_path)
            except (json.JSONDecodeError, KeyError) as exc:
                mkr_entry["format"] = "error"
                mkr_entry["error"] = str(exc)
                mkr_entry["marker_count"] = 0
                mkr_entry["alignment"] = "fail"
                mkr_entry["markers_only"] = 0
                mkr_entry["footnotes_only"] = 0
                summary["marker_alignment_fail"] += 1
                book_report["markers"] = mkr_entry
                report_books[code] = book_report
                continue

            mkr_entry["format"] = fmt
            mkr_entry["marker_count"] = mkr_count

            if fmt == "dict":
                summary["marker_format_dict"] += 1
            elif fmt == "list":
                summary["marker_format_list"] += 1

            # Alignment check
            markers_only = mkr_anchors - fn_anchors
            footnotes_only = fn_anchors - mkr_anchors
            aligned = len(markers_only) == 0 and len(footnotes_only) == 0
            mkr_entry["alignment"] = "pass" if aligned else "fail"
            mkr_entry["markers_only"] = len(markers_only)
            mkr_entry["footnotes_only"] = len(footnotes_only)

            if aligned:
                summary["marker_alignment_pass"] += 1
            else:
                summary["marker_alignment_fail"] += 1
        else:
            mkr_entry["format"] = None
            mkr_entry["marker_count"] = 0
            mkr_entry["alignment"] = "fail"
            mkr_entry["markers_only"] = 0
            mkr_entry["footnotes_only"] = 0
            summary["marker_alignment_fail"] += 1

        book_report["markers"] = mkr_entry
        report_books[code] = book_report

    return {
        "audit_date": str(date.today()),
        "summary": summary,
        "books": report_books,
    }


def print_summary(report: dict) -> None:
    """Print a human-readable summary to stdout."""
    s = report["summary"]
    print(f"Companion Audit — {report['audit_date']}")
    print(f"{'=' * 50}")
    print(f"Total books:             {s['total_books']}")
    print(f"Footnotes files:         {s['footnotes_files']}")
    print(f"Articles files:          {s['articles_files']}  (empty: {s['empty_articles']}, missing: {s['missing_articles']})")
    print(f"Marker files:            {s['marker_files']}  (dict: {s['marker_format_dict']}, list: {s['marker_format_list']})")
    print(f"Frontmatter issues:      {s['frontmatter_issues']}")
    print(f"Fused section headers:   {s['fused_headers']}")
    print(f"Marker alignment pass:   {s['marker_alignment_pass']}")
    print(f"Marker alignment fail:   {s['marker_alignment_fail']}")

    # Detail: books with issues
    books_with_fm = []
    books_with_fused = []
    books_with_align_fail = []
    for code, b in report["books"].items():
        fn_issues = b.get("footnotes", {}).get("frontmatter_issues", [])
        art_issues = b.get("articles", {}).get("frontmatter_issues", [])
        if fn_issues or art_issues:
            books_with_fm.append(code)
        if b.get("footnotes", {}).get("fused_header_count", 0) > 0:
            books_with_fused.append(code)
        if b.get("markers", {}).get("alignment") == "fail":
            books_with_align_fail.append(code)

    if books_with_fm:
        print(f"\nBooks with frontmatter issues ({len(books_with_fm)}):")
        for code in books_with_fm:
            b = report["books"][code]
            fn_issues = b.get("footnotes", {}).get("frontmatter_issues", [])
            art_issues = b.get("articles", {}).get("frontmatter_issues", [])
            parts = []
            if fn_issues:
                parts.append(f"footnotes: {fn_issues}")
            if art_issues:
                parts.append(f"articles: {art_issues}")
            print(f"  {code}: {'; '.join(parts)}")

    if books_with_fused:
        print(f"\nBooks with fused headers ({len(books_with_fused)}):")
        for code in books_with_fused:
            n = report["books"][code]["footnotes"]["fused_header_count"]
            print(f"  {code}: {n} fused header(s)")

    if books_with_align_fail:
        print(f"\nBooks with marker alignment failures ({len(books_with_align_fail)}):")
        for code in books_with_align_fail:
            m = report["books"][code]["markers"]
            if not m.get("exists"):
                print(f"  {code}: markers file missing")
            elif m.get("format") == "error":
                print(f"  {code}: JSON error — {m.get('error', '?')}")
            else:
                print(f"  {code}: markers_only={m['markers_only']}  footnotes_only={m['footnotes_only']}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Non-mutating batch audit for all companion files (footnotes, articles, markers)."
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=REPORTS_ROOT / "companion_audit.json",
        help="Path to write JSON report (default: reports/companion_audit.json)",
    )
    args = parser.parse_args()

    report = run_audit()

    # Ensure output directory exists
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Report written to {args.report}\n")
    print_summary(report)


if __name__ == "__main__":
    main()
