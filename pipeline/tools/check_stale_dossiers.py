"""
check_stale_dossiers.py — Detect stale promotion dossiers.

Computes current body checksums of staged files and compares against
the checksums recorded in promotion dossiers.

Usage:
    python3 pipeline/tools/check_stale_dossiers.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import sys as _sys; from pathlib import Path as _Path
_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists(): _R = _R.parent
if str(_R) not in _sys.path: _sys.path.insert(0, str(_R))
from pipeline.common.paths import STAGING_ROOT, REPORTS_ROOT
from pipeline.common.text import sha256_hex
from pipeline.common.frontmatter import split_frontmatter
from pipeline.tools.generate_book_status_dashboard import (
    build_dashboard,
    dossier_freshness_status,
    dossier_refresh_priority,
)


def split_body(text: str) -> str:
    """Return body text after frontmatter (everything after closing ---)."""
    _, body = split_frontmatter(text)
    return body


def find_staged_file(code: str) -> Path | None:
    """Find the staged .md file for a book code."""
    for testament in ("OT", "NT"):
        path = STAGING_ROOT / testament / f"{code}.md"
        if path.exists():
            return path
    return None


def main():
    dossier_files = sorted(REPORTS_ROOT.glob("*_promotion_dossier.json"))

    if not dossier_files:
        print("No promotion dossiers found.")
        sys.exit(0)

    stale_count = 0
    dashboard_books = {
        entry["book_code"]: entry for entry in build_dashboard()["books"]
    }
    results = []

    for dossier_path in dossier_files:
        code = dossier_path.stem.replace("_promotion_dossier", "")

        with open(dossier_path, encoding="utf-8") as f:
            dossier = json.load(f)

        staged_path = find_staged_file(code)

        if staged_path is None:
            status = "NO_STAGED_FILE"
            book_entry = dashboard_books.get(code, {})
            priority = dossier_refresh_priority(
                status,
                book_entry.get("status", "extracting"),
                book_entry.get("decision"),
            )
            results.append((code, status, priority, "", "", book_entry.get("status", "")))
            continue

        text = staged_path.read_text(encoding="utf-8")
        body = split_body(text)
        current_checksum = sha256_hex(body)

        status = dossier_freshness_status(dossier, staged_path, current_checksum)
        if status == "STALE":
            stale_count += 1
        elif status in {"NO_CHECKSUM", "NO_STAGED_FILE", "NO_STAGED_CHECKSUM"}:
            stale_count += 1

        book_entry = dashboard_books.get(code, {})
        priority = dossier_refresh_priority(
            status,
            book_entry.get("status", "extracting"),
            book_entry.get("decision"),
        )
        recorded_checksum = dossier.get("body_checksum", "")
        results.append(
            (
                code,
                status,
                priority,
                book_entry.get("status", ""),
                recorded_checksum[:16],
                current_checksum[:16],
            )
        )

    # Print table
    header = (
        f"{'BOOK':4s} | {'Status':14s} | {'Priority':8s} | {'Queue':19s} | "
        f"{'Dossier':>16s} | {'Current':>16s}"
    )
    print(f"\nDossier Freshness Check ({len(results)} dossiers)")
    print("=" * len(header))
    print(header)
    print("-" * len(header))

    for code, status, priority, queue_status, rec, cur in results:
        print(
            f"{code:4s} | {status:14s} | {priority:8s} | {queue_status:19.19s} | "
            f"{rec:>16s} | {cur:>16s}"
        )

    print("=" * len(header))

    fresh = sum(1 for _, s, _, _, _, _ in results if s == "FRESH")
    high = sum(1 for _, _, p, _, _, _ in results if p == "high")
    print(f"Fresh: {fresh}, Stale: {stale_count}, High-priority refresh: {high}, Total: {len(results)}")

    sys.exit(1 if stale_count > 0 else 0)


if __name__ == "__main__":
    main()
