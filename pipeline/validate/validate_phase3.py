"""
validate_phase3.py — Validate Layer 2 backlink shards before graph regeneration.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re

from pipeline.common.paths import CANON_ROOT, METADATA_ROOT, REGISTRY_PATH, REPORTS_ROOT, canon_filepath
from pipeline.common.patterns import RE_ANCHOR_FULL
from pipeline.common.registry import book_testament, chapter_verse_counts, load_registry

BACKLINKS_ROOT = METADATA_ROOT / "anchor_backlinks"
DEFAULT_REPORT = REPORTS_ROOT / "phase3_validation_report.json"
_BACKLINK_FILE_RE = re.compile(r"^([A-Z0-9]{2,4})\.(\d+)-(\d+)\.json$")


def valid_anchor_ids(registry: dict) -> set[str]:
    anchors: set[str] = set()
    for book in registry.get("books", []):
        cvc = chapter_verse_counts(registry, book["code"])
        if not cvc:
            continue
        for chapter, verse_count in cvc.items():
            for verse in range(1, verse_count + 1):
                anchors.add(f"{book['code']}.{chapter}:{verse}")
    return anchors


def discover_backlink_files(backlinks_root: Path = BACKLINKS_ROOT) -> list[Path]:
    return sorted(backlinks_root.glob("*/*.json"))


def anchor_from_filename(path: Path) -> str | None:
    match = _BACKLINK_FILE_RE.fullmatch(path.name)
    if not match:
        return None
    return f"{match.group(1)}.{int(match.group(2))}:{int(match.group(3))}"


def canon_anchors_for_book(book_code: str, registry: dict, canon_root: Path = CANON_ROOT) -> set[str]:
    testament = book_testament(registry, book_code)
    if testament is None:
        return set()
    path = canon_filepath(testament, book_code)
    if not path.exists():
        fallback = canon_root / testament / f"{book_code}.md"
        if fallback.exists():
            path = fallback
    if not path.exists():
        return set()
    anchors: set[str] = set()
    lines = path.read_text(encoding="utf-8").splitlines()
    for line in lines:
        match = RE_ANCHOR_FULL.match(line)
        if match:
            anchors.add(f"{match.group(1)}.{int(match.group(2))}:{int(match.group(3))}")
    return anchors


def validate_backlinks(
    backlinks_root: Path = BACKLINKS_ROOT,
    registry_path: Path = REGISTRY_PATH,
    book_code: str | None = None,
) -> dict:
    registry = load_registry(registry_path)
    known_anchors = valid_anchor_ids(registry)
    errors: list[str] = []
    warnings: list[str] = []
    high_degree: list[str] = []
    seen_anchors: set[str] = set()

    for path in discover_backlink_files(backlinks_root):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: invalid JSON ({exc})")
            continue

        anchor_id = payload.get("anchor_id")
        filename_anchor = anchor_from_filename(path)
        if filename_anchor is None:
            errors.append(f"{path}: filename does not match BOOK.CH-V.json")
        elif anchor_id != filename_anchor:
            errors.append(f"{path}: anchor_id {anchor_id!r} does not match filename {filename_anchor!r}")

        if anchor_id not in known_anchors:
            errors.append(f"{path}: dangling target anchor {anchor_id!r}")
        else:
            seen_anchors.add(anchor_id)

        book = anchor_id.split(".", 1)[0] if isinstance(anchor_id, str) and "." in anchor_id else None
        testament = book_testament(registry, book) if book else None
        expected_uri = f"canon/{testament}/{book}.md#{anchor_id}" if book and testament else None
        if payload.get("canon_uri") != expected_uri:
            errors.append(f"{path}: canon_uri mismatch for {anchor_id!r}")

        links = payload.get("links", [])
        dedup_counter = Counter(
            (
                link.get("source_file"),
                link.get("line_number"),
                link.get("raw_match"),
                link.get("reference_type"),
            )
            for link in links
        )
        duplicate_count = sum(count - 1 for count in dedup_counter.values() if count > 1)
        if duplicate_count:
            warnings.append(f"{path}: {duplicate_count} duplicate inbound link(s)")
        if len(links) > 50:
            warnings.append(f"{path}: high-degree inbound node ({len(links)} links)")
            high_degree.append(anchor_id)

    zero_degree = []
    if book_code:
        canon_anchors = canon_anchors_for_book(book_code, registry)
        zero_degree = sorted(canon_anchors - seen_anchors)
        if zero_degree:
            warnings.append(f"{book_code}: {len(zero_degree)} zero-degree anchor(s)")

    status = "FAIL" if errors else "WARN" if warnings else "PASS"
    return {
        "status": status,
        "file_count": len(discover_backlink_files(backlinks_root)),
        "errors": errors,
        "warnings": warnings,
        "high_degree_anchors": high_degree,
        "zero_degree": {
            "book_code": book_code,
            "count": len(zero_degree),
            "sample": zero_degree[:10],
        },
    }


def write_report(report: dict, path: Path = DEFAULT_REPORT) -> Path:
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Phase 3 backlink shards.")
    parser.add_argument("--backlinks-root", type=Path, default=BACKLINKS_ROOT)
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--book-code")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    report = validate_backlinks(args.backlinks_root, registry_path=args.registry, book_code=args.book_code)
    write_report(report, args.report)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
