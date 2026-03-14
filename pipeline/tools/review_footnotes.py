"""
review_footnotes.py — Canonical-order footnote review driver.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys

from pipeline.cleanup.verify_footnotes import build_verification_result
from pipeline.common.frontmatter import parse_frontmatter
from pipeline.common.paths import REPORTS_ROOT, REPO_ROOT, STAGING_ROOT, STUDY_FOOTNOTES
from pipeline.common.registry import load_registry
from pipeline.reference.reference_aliases import canonical_biblical_code, load_reference_aliases
from pipeline.reference.wikilinks import audit_path, registry_dimensions

DEFAULT_REPORT_DIR = REPORTS_ROOT / "footnote_review"
TEXT_CLEANER = REPO_ROOT / "skills" / "text-cleaner" / "scripts" / "clean.py"

HEADING_RE = re.compile(r"^###\s+(?P<chapter>\d+:\d+(?:-\d+)?)\s*$")
ANCHOR_MARKER_RE = re.compile(r"^\*\(anchor:\s+([A-Z0-9]+\.\d+:\d+)\)\*$")
INLINE_HEADING_SPILL_RE = re.compile(r"^\d+:\d+(?:-\d+)?\s+")
DANGLING_RANGE_RE = re.compile(r"^-\d+")
PAREN_TOKEN_RE = re.compile(r"\((?P<token>[A-Za-z][A-Za-z.]{1,30})\)")
SAINT_RE = re.compile(r"\bSt\.\s+[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,2}\b")
MIDLINE_REF_SPILL_RE = re.compile(r"\.\s+\d+:\d+(?:-\d+)?\s+")
SOURCE_SECTIONS = (
    ("patristic", "patristic_future"),
    ("apostolic", "apostolic_future"),
    ("liturgical_creedal", "liturgical_creedal_future"),
)


def ordered_books(
    registry: dict,
    *,
    book: str | None = None,
    start_book: str | None = None,
    end_book: str | None = None,
) -> list[dict]:
    books = sorted(registry.get("books", []), key=lambda item: item["position"])
    if book:
        return [item for item in books if item["code"] == book]

    start_idx = 0
    end_idx = len(books) - 1
    if start_book:
        start_idx = next(i for i, item in enumerate(books) if item["code"] == start_book)
    if end_book:
        end_idx = next(i for i, item in enumerate(books) if item["code"] == end_book)
    if start_idx > end_idx:
        return []
    return books[start_idx : end_idx + 1]


def footnotes_path(book_meta: dict) -> Path:
    study_path = STUDY_FOOTNOTES / book_meta["testament"] / f"{book_meta['code']}_footnotes.md"
    if study_path.exists():
        return study_path
    return STAGING_ROOT / book_meta["testament"] / f"{book_meta['code']}_footnotes.md"


def run_text_cleaner(path: Path, report_dir: Path, profile: str = "patristic") -> dict:
    report_dir.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [
            sys.executable,
            str(TEXT_CLEANER),
            "--file",
            str(path),
            "--profile",
            profile,
            "--dry-run",
            "--json",
            "--report-dir",
            str(report_dir),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {
            "status": "tool_error",
            "returncode": proc.returncode,
            "stderr_tail": proc.stderr.splitlines()[-20:],
            "summary": {
                "total_findings": 0,
                "auto_fixable": 0,
                "review_needed": 0,
                "files_checked": 0,
                "lines_checked": 0,
                "lines_fixed": 0,
            },
            "by_category": {},
        }
    return {
        "status": "ok" if proc.returncode in (0, 1) else "tool_error",
        "returncode": proc.returncode,
        "summary": payload.get("summary", {}),
        "by_category": payload.get("by_category", {}),
        "stderr_tail": proc.stderr.splitlines()[-20:],
    }


def audit_structure(book_code: str, path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    _, body_start = parse_frontmatter(lines)
    findings: list[dict] = []
    pending_heading: tuple[int, str] | None = None
    previous_nonblank: str | None = None

    for idx in range(body_start, len(lines)):
        line_no = idx + 1
        raw = lines[idx]
        stripped = raw.strip()
        if not stripped:
            continue
        if stripped == "## Footnotes":
            continue

        heading_match = HEADING_RE.match(stripped)
        if heading_match:
            pending_heading = (line_no, heading_match.group("chapter"))
            continue

        anchor_match = ANCHOR_MARKER_RE.match(stripped)
        if anchor_match:
            if pending_heading is None:
                findings.append(
                    {
                        "type": "orphan_anchor_marker",
                        "line_number": line_no,
                        "raw_text": stripped,
                    }
                )
            else:
                heading_line, heading_ref = pending_heading
                anchor_ref = anchor_match.group(1).split(".", 1)[1]
                if anchor_ref != heading_ref.split("-", 1)[0]:
                    findings.append(
                        {
                            "type": "heading_anchor_mismatch",
                            "line_number": line_no,
                            "raw_text": stripped,
                            "heading_line": heading_line,
                            "heading_ref": heading_ref,
                            "anchor_ref": anchor_ref,
                        }
                    )
                pending_heading = None
            continue

        if pending_heading is not None:
            heading_line, heading_ref = pending_heading
            findings.append(
                {
                    "type": "missing_anchor_after_heading",
                    "line_number": line_no,
                    "raw_text": stripped,
                    "heading_line": heading_line,
                    "heading_ref": heading_ref,
                }
            )
            pending_heading = None

        if MIDLINE_REF_SPILL_RE.search(stripped):
            findings.append(
                {
                    "type": "midline_reference_spill",
                    "line_number": line_no,
                    "raw_text": stripped,
                }
            )

        if DANGLING_RANGE_RE.match(stripped):
            findings.append(
                {
                    "type": "dangling_range_continuation",
                    "line_number": line_no,
                    "raw_text": stripped,
                }
            )
        elif INLINE_HEADING_SPILL_RE.match(stripped) and previous_nonblank:
            previous_tokens = previous_nonblank.rstrip(".,;:)]}").split()
            if previous_tokens and canonical_biblical_code(previous_tokens[-1]) is not None:
                findings.append(
                    {
                        "type": "broken_reference_split",
                        "line_number": line_no,
                        "raw_text": stripped,
                        "previous_line_tail": previous_nonblank[-120:],
                    }
                )
        previous_nonblank = stripped

    if pending_heading is not None:
        findings.append(
            {
                "type": "heading_without_anchor",
                "line_number": pending_heading[0],
                "raw_text": pending_heading[1],
            }
        )

    return {
        "issue_count": len(findings),
        "findings": findings[:100],
        "truncated": len(findings) > 100,
    }


def build_source_patterns() -> dict[str, list[tuple[str, str, re.Pattern[str]]]]:
    data = load_reference_aliases()
    patterns: dict[str, list[tuple[str, str, re.Pattern[str]]]] = {}
    for report_key, section_key in SOURCE_SECTIONS:
        section_patterns: list[tuple[str, str, re.Pattern[str]]] = []
        for entry in data.get(section_key, []):
            for alias in sorted(entry.get("aliases", []), key=len, reverse=True):
                section_patterns.append(
                    (
                        entry["canonical"],
                        alias,
                        re.compile(rf"(?<![\w]){re.escape(alias)}(?![\w])", re.IGNORECASE),
                    )
                )
        patterns[report_key] = section_patterns
    return patterns


PATTERN_CACHE = build_source_patterns()
KNOWN_SOURCE_TOKENS = {
    report_key: {alias.lower() for _, alias, _ in patterns}
    for report_key, patterns in PATTERN_CACHE.items()
}


def audit_source_entities(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    _, body_start = parse_frontmatter(lines)
    tiers: dict[str, dict] = {
        report_key: {
            "matched_entities_count": 0,
            "matched_entities": [],
            "entity_counts": {},
            "unresolved_candidates_count": 0,
            "unresolved_candidates": [],
            "explicit_citation_snippets": [],
        }
        for report_key, _ in SOURCE_SECTIONS
    }
    matches_by_tier: dict[str, list[dict]] = {report_key: [] for report_key, _ in SOURCE_SECTIONS}
    unresolved_by_tier: dict[str, list[dict]] = {report_key: [] for report_key, _ in SOURCE_SECTIONS}
    snippets_by_tier: dict[str, list[dict]] = {report_key: [] for report_key, _ in SOURCE_SECTIONS}
    seen_matches: dict[str, set[tuple[int, str, str]]] = {
        report_key: set() for report_key, _ in SOURCE_SECTIONS
    }
    seen_unresolved: dict[str, set[tuple[int, str]]] = {
        report_key: set() for report_key, _ in SOURCE_SECTIONS
    }
    counts_by_tier: dict[str, Counter] = {report_key: Counter() for report_key, _ in SOURCE_SECTIONS}

    for idx in range(body_start, len(lines)):
        line_no = idx + 1
        line = lines[idx]
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("*(anchor:"):
            continue

        occupied: list[tuple[int, int]] = []
        line_has_signal = False
        for report_key, patterns in PATTERN_CACHE.items():
            for canonical, alias, pattern in patterns:
                for match in pattern.finditer(line):
                    key = (line_no, canonical, alias)
                    if key in seen_matches[report_key]:
                        continue
                    seen_matches[report_key].add(key)
                    counts_by_tier[report_key][canonical] += 1
                    occupied.append(match.span())
                    matches_by_tier[report_key].append(
                        {
                            "line_number": line_no,
                            "entity": canonical,
                            "matched_alias": alias,
                            "context": stripped[:240],
                        }
                    )
                    line_has_signal = True

        def overlaps(span: tuple[int, int]) -> bool:
            start, end = span
            return any(not (end <= seen_start or start >= seen_end) for seen_start, seen_end in occupied)

        for match in PAREN_TOKEN_RE.finditer(line):
            token = match.group("token").strip(".,;:)")
            if overlaps(match.span()):
                continue
            if canonical_biblical_code(token) is not None:
                continue
            if not (
                any(ch.isupper() for ch in token[1:])
                or (token[0].isupper() and token[1:].islower())
            ):
                continue
            classified = False
            for report_key, known_tokens in KNOWN_SOURCE_TOKENS.items():
                if token.lower() in known_tokens:
                    classified = True
                    break
                key = (line_no, token)
                if key in seen_unresolved[report_key]:
                    continue
                if report_key == "liturgical_creedal":
                    should_track = token in {"Creed", "CanonAnd"}
                elif report_key == "apostolic":
                    should_track = False
                else:
                    should_track = (
                        any(ch.isupper() for ch in token[1:])
                        and not token.endswith("Service")
                    )
                if should_track:
                    seen_unresolved[report_key].add(key)
                    unresolved_by_tier[report_key].append(
                        {
                            "line_number": line_no,
                            "token": token,
                            "context": stripped[:240],
                        }
                    )
                    line_has_signal = True
            if classified:
                continue

        for match in SAINT_RE.finditer(line):
            token = match.group(0)
            if overlaps(match.span()):
                continue
            known_tier = next(
                (
                    report_key
                    for report_key, known_tokens in KNOWN_SOURCE_TOKENS.items()
                    if token.lower() in known_tokens
                ),
                None,
            )
            if known_tier is not None:
                continue
            report_key = "apostolic" if any(name in token for name in ("Paul", "Peter")) else "patristic"
            key = (line_no, token)
            if key in seen_unresolved[report_key]:
                continue
            seen_unresolved[report_key].add(key)
            unresolved_by_tier[report_key].append(
                {
                    "line_number": line_no,
                    "token": token,
                    "context": stripped[:240],
                }
            )
            line_has_signal = True

        if line_has_signal:
            for paren_match in re.finditer(r"\(([^)]{2,120})\)", line):
                snippet = paren_match.group(1).strip()
                if canonical_biblical_code(snippet) is not None:
                    continue
                tier_key = None
                lowered = snippet.lower()
                if lowered in KNOWN_SOURCE_TOKENS["liturgical_creedal"]:
                    tier_key = "liturgical_creedal"
                elif lowered in KNOWN_SOURCE_TOKENS["patristic"]:
                    tier_key = "patristic"
                elif lowered in KNOWN_SOURCE_TOKENS["apostolic"]:
                    tier_key = "apostolic"
                if tier_key is None or len(snippets_by_tier[tier_key]) >= 50:
                    continue
                snippets_by_tier[tier_key].append(
                    {
                        "line_number": line_no,
                        "snippet": snippet,
                    }
                )

    for report_key, _ in SOURCE_SECTIONS:
        tiers[report_key] = {
            "matched_entities_count": len(matches_by_tier[report_key]),
            "matched_entities": matches_by_tier[report_key][:100],
            "entity_counts": dict(sorted(counts_by_tier[report_key].items())),
            "unresolved_candidates_count": len(unresolved_by_tier[report_key]),
            "unresolved_candidates": unresolved_by_tier[report_key][:100],
            "explicit_citation_snippets": snippets_by_tier[report_key][:50],
        }
    return tiers


def build_book_report(book_meta: dict, report_dir: Path, dimensions: dict[str, dict[int, int]]) -> dict:
    path = footnotes_path(book_meta)
    exists = path.exists()
    if not exists:
        return {
            "book_code": book_meta["code"],
            "position": book_meta["position"],
            "testament": book_meta["testament"],
            "status": "missing",
            "footnotes_path": str(path),
        }

    cleaner = run_text_cleaner(path, report_dir / "_text_cleaner_raw")
    structure = audit_structure(book_meta["code"], path)
    verification = build_verification_result(book_meta["code"])
    wikilinks = audit_path(path, dimensions)
    source_entities = audit_source_entities(path)

    component_status = {
        "mechanical_clean": cleaner["summary"].get("auto_fixable", 0) == 0 and cleaner["status"] == "ok",
        "structural_clean": structure["issue_count"] == 0,
        "marker_alignment_pass": verification.get("issue_count", 1) == 0,
        "wikilinks_verified": wikilinks["convertible_refs"] == 0,
        "patristic_entity_verified": source_entities["patristic"]["unresolved_candidates_count"] == 0,
        "apostolic_entity_verified": source_entities["apostolic"]["unresolved_candidates_count"] == 0,
        "liturgical_creedal_verified": source_entities["liturgical_creedal"]["unresolved_candidates_count"] == 0,
    }
    overall_status = "complete" if all(component_status.values()) else "review_required"

    return {
        "book_code": book_meta["code"],
        "position": book_meta["position"],
        "testament": book_meta["testament"],
        "status": overall_status,
        "content_surface": "study" if str(path).startswith(str(STUDY_FOOTNOTES)) else "staging",
        "verification_surface": "staging",
        "footnotes_path": str(path),
        "component_status": component_status,
        "mechanical": {
            "tool_status": cleaner["status"],
            "summary": cleaner["summary"],
            "by_category": cleaner["by_category"],
        },
        "structure": structure,
        "footnote_verification": verification,
        "wikilinks": {
            "total_refs": wikilinks["total_refs"],
            "convertible_refs": wikilinks["convertible_refs"],
            "already_linked_refs": wikilinks["already_linked_refs"],
            "unresolved_refs": wikilinks["unresolved_refs"],
            "unresolved_examples": wikilinks["unresolved_examples"][:20],
        },
        "source_entities": source_entities,
        "patristics": source_entities["patristic"],
    }


def write_reports(reports: list[dict], report_dir: Path) -> dict:
    report_dir.mkdir(parents=True, exist_ok=True)
    counts = Counter(report["status"] for report in reports)
    component_counts = Counter()
    books = []
    for report in reports:
        component_counts.update(
            key for key, passed in report.get("component_status", {}).items() if passed
        )
        books.append(
            {
                "book_code": report["book_code"],
                "position": report["position"],
                "testament": report["testament"],
                "status": report["status"],
                "content_surface": report.get("content_surface"),
                "component_status": report.get("component_status", {}),
                "structure_issue_count": report.get("structure", {}).get("issue_count", 0),
                "wikilink_unresolved_refs": report.get("wikilinks", {}).get("unresolved_refs", 0),
                "patristic_unresolved_candidates": report.get("patristics", {}).get("unresolved_candidates_count", 0),
                "apostolic_unresolved_candidates": report.get("source_entities", {}).get("apostolic", {}).get("unresolved_candidates_count", 0),
                "liturgical_creedal_unresolved_candidates": report.get("source_entities", {}).get("liturgical_creedal", {}).get("unresolved_candidates_count", 0),
                "footnote_issue_count": report.get("footnote_verification", {}).get("issue_count", 0),
            }
        )
        book_report = report_dir / f"{report['book_code']}.json"
        book_report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    ordered_books = sorted(books, key=lambda item: item["position"])
    waves = []
    for wave_start in range(0, len(ordered_books), 5):
        chunk = ordered_books[wave_start : wave_start + 5]
        waves.append(
            {
                "wave": wave_start // 5 + 1,
                "start_book": chunk[0]["book_code"],
                "end_book": chunk[-1]["book_code"],
                "book_count": len(chunk),
                "complete_books": sum(1 for item in chunk if item["status"] == "complete"),
                "structural_clean_books": sum(
                    1 for item in chunk if item["component_status"].get("structural_clean")
                ),
                "marker_alignment_books": sum(
                    1 for item in chunk if item["component_status"].get("marker_alignment_pass")
                ),
                "patristic_verified_books": sum(
                    1 for item in chunk if item["component_status"].get("patristic_entity_verified")
                ),
                "apostolic_verified_books": sum(
                    1 for item in chunk if item["component_status"].get("apostolic_entity_verified")
                ),
                "liturgical_creedal_verified_books": sum(
                    1
                    for item in chunk
                    if item["component_status"].get("liturgical_creedal_verified")
                ),
            }
        )

    dashboard = {
        "generated": __import__("datetime").date.today().isoformat(),
        "book_count": len(reports),
        "status_counts": dict(sorted(counts.items())),
        "component_pass_counts": dict(sorted(component_counts.items())),
        "waves": waves,
        "books": books,
    }
    (report_dir / "dashboard.json").write_text(json.dumps(dashboard, indent=2) + "\n", encoding="utf-8")
    return dashboard


def main() -> int:
    parser = argparse.ArgumentParser(description="Canonical-order footnote review driver.")
    parser.add_argument("--book")
    parser.add_argument("--start-book")
    parser.add_argument("--end-book")
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    args = parser.parse_args()

    registry = load_registry()
    books = ordered_books(
        registry,
        book=args.book,
        start_book=args.start_book,
        end_book=args.end_book,
    )
    if not books:
        raise SystemExit("No books matched the requested range.")

    dimensions = registry_dimensions()
    reports = [build_book_report(book_meta, args.report_dir, dimensions) for book_meta in books]
    dashboard = write_reports(reports, args.report_dir)
    print(json.dumps(dashboard, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
