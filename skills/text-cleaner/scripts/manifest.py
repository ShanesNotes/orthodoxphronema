#!/usr/bin/env python3
"""
manifest.py — Generate batch work manifests from footnote review dashboard.

Reads the footnote review dashboard.json and produces an ordered work manifest
for batch scan/detect/fix cycles with clean.py.

Usage:
    python3 manifest.py --dashboard reports/footnote_review/dashboard.json
    python3 manifest.py --dashboard reports/footnote_review/dashboard.json --output manifest.json
    python3 manifest.py --dashboard reports/footnote_review/dashboard.json --status review_required
    python3 manifest.py --dashboard reports/footnote_review/dashboard.json --missing structural_clean
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ── Repo discovery ──────────────────────────────────────────────────────────
_THIS = Path(__file__).resolve().parent
_REPO = _THIS
while _REPO != _REPO.parent and not (_REPO / "pipeline" / "__init__.py").exists():
    _REPO = _REPO.parent

# Content surface → directory mapping
SURFACE_DIRS = {
    "staging": {
        "footnotes": _REPO / "staging" / "validated",
        "articles": _REPO / "staging" / "validated",
    },
    "study": {
        "footnotes": _REPO / "study" / "footnotes",
        "articles": _REPO / "study" / "articles",
    },
}


def load_dashboard(path: Path) -> dict:
    """Load and validate dashboard JSON."""
    if not path.exists():
        print(f"Error: dashboard not found: {path}", file=sys.stderr)
        sys.exit(1)
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_file_path(book: dict) -> Path | None:
    """Resolve the footnote file path for a book entry."""
    code = book["book_code"]
    testament = book.get("testament", "OT")
    surface = book.get("content_surface", "study")

    surface_map = SURFACE_DIRS.get(surface, SURFACE_DIRS["study"])
    base_dir = surface_map["footnotes"] / testament
    footnote_file = base_dir / f"{code}_footnotes.md"

    if footnote_file.exists():
        return footnote_file
    return None


def generate_manifest(
    dashboard: dict,
    status_filter: str | None = None,
    missing_check: str | None = None,
) -> list[dict]:
    """Generate ordered work manifest from dashboard.

    Args:
        dashboard: Parsed dashboard.json
        status_filter: Only include books with this status (e.g. "review_required")
        missing_check: Only include books missing this component check
    """
    manifest = []

    for book in dashboard.get("books", []):
        # Apply status filter
        if status_filter and book.get("status") != status_filter:
            continue

        # Apply missing-check filter
        if missing_check:
            component = book.get("component_status", {})
            if component.get(missing_check, False):
                continue  # Already has this check — skip

        file_path = resolve_file_path(book)
        if not file_path:
            continue

        pending_checks = []
        for check, passed in book.get("component_status", {}).items():
            if not passed:
                pending_checks.append(check)

        manifest.append({
            "book_code": book["book_code"],
            "testament": book.get("testament", "OT"),
            "position": book.get("position", 0),
            "status": book.get("status", "unknown"),
            "file_path": str(file_path),
            "pending_checks": pending_checks,
            "structure_issues": book.get("structure_issue_count", 0),
            "footnote_issues": book.get("footnote_issue_count", 0),
        })

    # Sort by biblical position
    manifest.sort(key=lambda b: b["position"])
    return manifest


def main():
    parser = argparse.ArgumentParser(
        description="Generate batch work manifest from footnote review dashboard."
    )
    parser.add_argument(
        "--dashboard", type=Path, required=True,
        help="Path to dashboard.json"
    )
    parser.add_argument(
        "--output", type=Path,
        help="Output path for manifest JSON (default: stdout)"
    )
    parser.add_argument(
        "--status", default=None,
        help="Filter by book status (e.g., review_required, complete)"
    )
    parser.add_argument(
        "--missing", default=None,
        help="Filter by missing component check (e.g., structural_clean)"
    )

    args = parser.parse_args()

    dashboard = load_dashboard(args.dashboard)
    manifest = generate_manifest(
        dashboard,
        status_filter=args.status,
        missing_check=args.missing,
    )

    result = {
        "generated_from": str(args.dashboard),
        "dashboard_date": dashboard.get("generated", "unknown"),
        "filters": {
            "status": args.status,
            "missing_check": args.missing,
        },
        "book_count": len(manifest),
        "books": manifest,
    }

    output_text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output_text, encoding="utf-8")
        print(f"Manifest: {args.output} ({len(manifest)} books)", file=sys.stderr)
    else:
        print(output_text)

    # Summary to stderr
    if manifest:
        by_status = {}
        for book in manifest:
            s = book["status"]
            by_status[s] = by_status.get(s, 0) + 1
        print(f"\nManifest summary: {len(manifest)} books", file=sys.stderr)
        for s, count in sorted(by_status.items()):
            print(f"  {s}: {count}", file=sys.stderr)
    else:
        print("No books matched the given filters.", file=sys.stderr)


if __name__ == "__main__":
    main()
