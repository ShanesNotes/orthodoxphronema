"""
audit_wikilinks.py — Audit staged companion files for wikilink conversion readiness.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline.common.paths import REPORTS_ROOT, STAGING_ROOT
from pipeline.reference.wikilinks import audit_path, discover_target_paths, registry_dimensions, write_json_report

DEFAULT_REPORT = REPORTS_ROOT / "wikilink_audit.json"


def build_audit(paths: list[Path]) -> dict:
    dimensions = registry_dimensions()
    files = [audit_path(path, dimensions) for path in paths]
    return {
        "file_count": len(files),
        "total_refs": sum(item["total_refs"] for item in files),
        "convertible_refs": sum(item["convertible_refs"] for item in files),
        "already_linked_refs": sum(item["already_linked_refs"] for item in files),
        "unresolved_refs": sum(item["unresolved_refs"] for item in files),
        "files": files,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit staged companion files for wikilink rollout.")
    parser.add_argument("roots", nargs="*", type=Path, default=[STAGING_ROOT])
    parser.add_argument("--book")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    paths = discover_target_paths(args.roots, book_code=args.book)
    payload = build_audit(paths)
    write_json_report(payload, args.report)
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
