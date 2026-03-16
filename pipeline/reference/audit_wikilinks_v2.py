"""
audit_wikilinks_v2.py — Project-wide wikilink audit with orphan detection and range validation.

Scans all Markdown files across staging/, study/, and reference/ for wikilinks,
validates every [[BOOK.CH:V]] against the anchor registry, and detects:
  1. Orphaned wikilinks (target anchor doesn't exist in registry CVC)
  2. Invalid range endpoints ([[BOOK.CH:V]]-W where W > max verse)
  3. Bare (unconverted) references
  4. Per-domain statistics

Usage:
    python3 pipeline/reference/audit_wikilinks_v2.py [--report reports/wikilink_audit_v2.json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path

from pipeline.common.frontmatter import parse_frontmatter
from pipeline.common.paths import (
    CANON_ROOT, METADATA_ROOT, REFERENCE_ROOT, REPO_ROOT, REPORTS_ROOT,
    STAGING_ROOT, STUDY_ROOT,
)
from pipeline.common.registry import chapter_verse_counts, load_registry
from pipeline.reference.reference_aliases import canonical_biblical_code
from pipeline.reference.wikilinks import BARE_RE, WIKILINK_RE, registry_dimensions

DEFAULT_REPORT = REPORTS_ROOT / "wikilink_audit_v2.json"

# Scan roots and their domain mappings
SCAN_ROOTS = [
    (STAGING_ROOT, "staging"),
    (STUDY_ROOT, "study"),
    (REFERENCE_ROOT, "reference"),
]


@dataclass
class WikilinkFinding:
    file: str
    line_number: int
    raw_text: str
    anchor: str
    finding_type: str  # "orphan", "invalid_range_end", "bare_ref", "valid"
    detail: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class FileAuditResult:
    path: str
    domain: str
    wikilink_count: int = 0
    bare_ref_count: int = 0
    orphan_count: int = 0
    invalid_range_count: int = 0
    findings: list[dict] = field(default_factory=list)


def _relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _detect_domain(path: Path) -> str:
    rel = _relative(path)
    for root, domain in SCAN_ROOTS:
        try:
            path.resolve().relative_to(root.resolve())
            return domain
        except ValueError:
            continue
    return "unknown"


def discover_markdown_files() -> list[tuple[Path, str]]:
    """Find all Markdown files in scan roots."""
    results: list[tuple[Path, str]] = []
    for root, domain in SCAN_ROOTS:
        if not root.exists():
            continue
        for md_file in sorted(root.rglob("*.md")):
            results.append((md_file, domain))
    return results


def discover_json_files() -> list[tuple[Path, str]]:
    """Find JSON files that may contain wikilinks."""
    results: list[tuple[Path, str]] = []
    for root, domain in SCAN_ROOTS:
        if not root.exists():
            continue
        for json_file in sorted(root.rglob("*.json")):
            results.append((json_file, domain))
    return results


def validate_anchor(anchor_id: str, dimensions: dict[str, dict[int, int]]) -> tuple[bool, str]:
    """Check if an anchor exists in the registry CVC."""
    parts = anchor_id.split(".", 1)
    if len(parts) != 2:
        return False, f"malformed anchor: {anchor_id}"
    book_code = parts[0]
    rest = parts[1].split(":", 1)
    if len(rest) != 2:
        return False, f"malformed anchor: {anchor_id}"
    try:
        ch = int(rest[0])
        v = int(rest[1])
    except ValueError:
        return False, f"non-numeric chapter/verse: {anchor_id}"

    cvc = dimensions.get(book_code)
    if cvc is None:
        return False, f"unknown book code: {book_code}"
    if ch not in cvc:
        return False, f"chapter {ch} not in {book_code} (max={max(cvc.keys())})"
    if v < 1 or v > cvc[ch]:
        return False, f"verse {v} out of range for {book_code}.{ch} (max={cvc[ch]})"
    return True, ""


def validate_range_end(
    book_code: str, chapter: int, end_verse: int,
    dimensions: dict[str, dict[int, int]],
) -> tuple[bool, str]:
    """Check if a range endpoint is valid."""
    cvc = dimensions.get(book_code)
    if cvc is None:
        return False, f"unknown book: {book_code}"
    if chapter not in cvc:
        return False, f"chapter {chapter} not in {book_code}"
    if end_verse < 1 or end_verse > cvc[chapter]:
        return False, f"range end {end_verse} exceeds max {cvc[chapter]} for {book_code}.{chapter}"
    return True, ""


def audit_markdown_file(
    path: Path, domain: str, dimensions: dict[str, dict[int, int]],
) -> FileAuditResult:
    """Audit a single Markdown file for wikilink issues."""
    result = FileAuditResult(path=_relative(path), domain=domain)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    try:
        _, body_start = parse_frontmatter(lines)
    except Exception:
        body_start = 0

    in_code_fence = False
    for idx in range(body_start, len(lines)):
        line = lines[idx]
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue

        line_no = idx + 1

        # Check wikilinks
        for m in WIKILINK_RE.finditer(line):
            book_token = m.group(1)
            chapter = int(m.group(2))
            verse = int(m.group(3))
            end_verse = int(m.group(4)) if m.group(4) else None

            book_code = canonical_biblical_code(book_token)
            if book_code is None:
                book_code = book_token.upper()

            anchor = f"{book_code}.{chapter}:{verse}"
            valid, detail = validate_anchor(anchor, dimensions)

            if not valid:
                result.orphan_count += 1
                result.findings.append(WikilinkFinding(
                    file=result.path, line_number=line_no,
                    raw_text=m.group(0), anchor=anchor,
                    finding_type="orphan", detail=detail,
                ).to_dict())
            else:
                result.wikilink_count += 1

            # Validate range end
            if end_verse is not None and valid:
                range_valid, range_detail = validate_range_end(
                    book_code, chapter, end_verse, dimensions,
                )
                if not range_valid:
                    result.invalid_range_count += 1
                    result.findings.append(WikilinkFinding(
                        file=result.path, line_number=line_no,
                        raw_text=m.group(0), anchor=f"{anchor}-{end_verse}",
                        finding_type="invalid_range_end", detail=range_detail,
                    ).to_dict())

        # Check bare refs
        occupied = [(m.start(), m.end()) for m in WIKILINK_RE.finditer(line)]
        for m in BARE_RE.finditer(line):
            if any(not (m.end() <= s or m.start() >= e) for s, e in occupied):
                continue
            book_code = canonical_biblical_code(m.group("book"))
            if book_code is None:
                continue
            result.bare_ref_count += 1
            if result.bare_ref_count <= 20:  # Cap findings for bare refs
                result.findings.append(WikilinkFinding(
                    file=result.path, line_number=line_no,
                    raw_text=m.group(0),
                    anchor=f"{book_code}.{m.group('chapter')}:{m.group('verse')}",
                    finding_type="bare_ref", detail="unconverted bare reference",
                ).to_dict())

    return result


def audit_json_file(
    path: Path, domain: str, dimensions: dict[str, dict[int, int]],
) -> FileAuditResult:
    """Audit a JSON file for wikilinks (scans string values)."""
    result = FileAuditResult(path=_relative(path), domain=domain)

    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return result

    # Scan raw text for wikilinks
    for line_no, line in enumerate(text.splitlines(), start=1):
        for m in WIKILINK_RE.finditer(line):
            book_token = m.group(1)
            chapter = int(m.group(2))
            verse = int(m.group(3))
            end_verse = int(m.group(4)) if m.group(4) else None

            book_code = canonical_biblical_code(book_token)
            if book_code is None:
                book_code = book_token.upper()

            anchor = f"{book_code}.{chapter}:{verse}"
            valid, detail = validate_anchor(anchor, dimensions)

            if not valid:
                result.orphan_count += 1
                result.findings.append(WikilinkFinding(
                    file=result.path, line_number=line_no,
                    raw_text=m.group(0), anchor=anchor,
                    finding_type="orphan", detail=detail,
                ).to_dict())
            else:
                result.wikilink_count += 1

            if end_verse is not None and valid:
                range_valid, range_detail = validate_range_end(
                    book_code, chapter, end_verse, dimensions,
                )
                if not range_valid:
                    result.invalid_range_count += 1
                    result.findings.append(WikilinkFinding(
                        file=result.path, line_number=line_no,
                        raw_text=m.group(0), anchor=f"{anchor}-{end_verse}",
                        finding_type="invalid_range_end", detail=range_detail,
                    ).to_dict())

    return result


def run_full_audit(report_path: Path = DEFAULT_REPORT) -> dict:
    """Run project-wide wikilink audit."""
    print("Loading registry dimensions...", file=sys.stderr)
    dimensions = registry_dimensions()
    print(f"  {len(dimensions)} books in registry", file=sys.stderr)

    print("Discovering files...", file=sys.stderr)
    md_files = discover_markdown_files()
    json_files = discover_json_files()
    print(f"  {len(md_files)} Markdown, {len(json_files)} JSON files", file=sys.stderr)

    # Audit all files
    all_results: list[FileAuditResult] = []

    print("Auditing Markdown files...", file=sys.stderr)
    for path, domain in md_files:
        result = audit_markdown_file(path, domain, dimensions)
        if result.wikilink_count > 0 or result.bare_ref_count > 0 or result.orphan_count > 0:
            all_results.append(result)

    print("Auditing JSON files...", file=sys.stderr)
    for path, domain in json_files:
        result = audit_json_file(path, domain, dimensions)
        if result.wikilink_count > 0 or result.bare_ref_count > 0 or result.orphan_count > 0:
            all_results.append(result)

    # Aggregate
    domain_stats: dict[str, dict[str, int]] = defaultdict(lambda: {
        "files": 0, "wikilinks": 0, "bare_refs": 0, "orphans": 0, "invalid_ranges": 0,
    })
    all_orphans: list[dict] = []
    all_invalid_ranges: list[dict] = []

    for r in all_results:
        ds = domain_stats[r.domain]
        ds["files"] += 1
        ds["wikilinks"] += r.wikilink_count
        ds["bare_refs"] += r.bare_ref_count
        ds["orphans"] += r.orphan_count
        ds["invalid_ranges"] += r.invalid_range_count
        for f in r.findings:
            if f["finding_type"] == "orphan":
                all_orphans.append(f)
            elif f["finding_type"] == "invalid_range_end":
                all_invalid_ranges.append(f)

    total_wikilinks = sum(ds["wikilinks"] for ds in domain_stats.values())
    total_bare = sum(ds["bare_refs"] for ds in domain_stats.values())
    total_orphans = sum(ds["orphans"] for ds in domain_stats.values())
    total_invalid = sum(ds["invalid_ranges"] for ds in domain_stats.values())

    report = {
        "audit_version": "v2",
        "total_files_scanned": len(md_files) + len(json_files),
        "total_files_with_refs": len(all_results),
        "total_wikilinks": total_wikilinks,
        "total_bare_refs": total_bare,
        "total_orphans": total_orphans,
        "total_invalid_ranges": total_invalid,
        "domain_stats": dict(domain_stats),
        "orphaned_wikilinks": all_orphans,
        "invalid_range_endpoints": all_invalid_ranges,
        "files": [
            {
                "path": r.path,
                "domain": r.domain,
                "wikilinks": r.wikilink_count,
                "bare_refs": r.bare_ref_count,
                "orphans": r.orphan_count,
                "invalid_ranges": r.invalid_range_count,
            }
            for r in sorted(all_results, key=lambda x: x.path)
        ],
    }

    # Write report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    # Print summary
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"WIKILINK AUDIT v2 — Project-wide Results", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)
    print(f"Files scanned:      {len(md_files) + len(json_files)}", file=sys.stderr)
    print(f"Files with refs:    {len(all_results)}", file=sys.stderr)
    print(f"Total wikilinks:    {total_wikilinks:,}", file=sys.stderr)
    print(f"Total bare refs:    {total_bare:,}", file=sys.stderr)
    print(f"Orphaned wikilinks: {total_orphans}", file=sys.stderr)
    print(f"Invalid ranges:     {total_invalid}", file=sys.stderr)
    print(file=sys.stderr)
    print("By domain:", file=sys.stderr)
    for domain, stats in sorted(domain_stats.items()):
        print(f"  {domain:12s}: {stats['wikilinks']:,} wikilinks, "
              f"{stats['bare_refs']:,} bare, "
              f"{stats['orphans']} orphans, "
              f"{stats['invalid_ranges']} invalid ranges", file=sys.stderr)

    if all_orphans:
        print(f"\nOrphaned wikilinks ({len(all_orphans)}):", file=sys.stderr)
        for o in all_orphans[:20]:
            print(f"  {o['file']}:{o['line_number']} — {o['raw_text']} → {o['detail']}", file=sys.stderr)
        if len(all_orphans) > 20:
            print(f"  ... and {len(all_orphans) - 20} more", file=sys.stderr)

    if all_invalid_ranges:
        print(f"\nInvalid range endpoints ({len(all_invalid_ranges)}):", file=sys.stderr)
        for ir in all_invalid_ranges[:20]:
            print(f"  {ir['file']}:{ir['line_number']} — {ir['raw_text']} → {ir['detail']}", file=sys.stderr)

    print(f"\nReport written: {report_path}", file=sys.stderr)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Project-wide wikilink audit v2.")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    report = run_full_audit(args.report)
    print(json.dumps({
        "total_wikilinks": report["total_wikilinks"],
        "total_bare_refs": report["total_bare_refs"],
        "total_orphans": report["total_orphans"],
        "total_invalid_ranges": report["total_invalid_ranges"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
