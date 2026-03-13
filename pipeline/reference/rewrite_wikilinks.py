"""
rewrite_wikilinks.py — Rewrite bare staged-companion references into wikilinks.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline.common.paths import REPORTS_ROOT, STAGING_ROOT
from pipeline.reference.wikilinks import discover_target_paths, registry_dimensions, rewrite_path, write_json_report

DEFAULT_REPORT = REPORTS_ROOT / "wikilink_rewrite_report.json"


def build_rewrite_report(paths: list[Path], in_place: bool) -> dict:
    dimensions = registry_dimensions()
    files = [rewrite_path(path, dimensions, in_place=in_place) for path in paths]
    return {
        "file_count": len(files),
        "changed_files": sum(1 for item in files if item["changed"]),
        "converted_refs": sum(item["converted_refs"] for item in files),
        "files": files,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Rewrite staged companion references into wikilinks.")
    parser.add_argument("roots", nargs="*", type=Path, default=[STAGING_ROOT])
    parser.add_argument("--book")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    if args.dry_run == args.in_place:
        parser.error("choose exactly one of --dry-run or --in-place")

    paths = discover_target_paths(args.roots, book_code=args.book)
    payload = build_rewrite_report(paths, in_place=args.in_place)
    write_json_report(payload, args.report)
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
