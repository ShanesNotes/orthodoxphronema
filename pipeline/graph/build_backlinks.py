"""
build_backlinks.py — Build Layer 2 backlink shards from R1 JSONL output.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path

from pipeline.common.paths import METADATA_ROOT, REGISTRY_PATH
from pipeline.common.registry import book_testament, load_registry
from pipeline.extract.models import ReferenceRecord

BACKLINKS_ROOT = METADATA_ROOT / "anchor_backlinks"
GENERATOR_VERSION = "phase3-backlinks-v1"


def detect_domain(source_file: str) -> str:
    normalized = source_file.replace("\\", "/").lstrip("./")
    if normalized.startswith("phronema/liturgics/") or normalized.startswith("phronema/liturgical/"):
        return "liturgical"
    if normalized.startswith("phronema/patristics/") or normalized.startswith("phronema/patristic/"):
        return "patristic"
    if normalized.startswith(("phronema/study/", "articles/", "notes/", "staging/validated/")):
        return "study"
    raise ValueError(f"unable to infer domain for source_file {source_file!r}")


def anchor_filename(anchor_id: str) -> str:
    book_code, remainder = anchor_id.split(".", 1)
    chapter, verse = remainder.split(":", 1)
    return f"{book_code}.{chapter}-{verse}.json"


def canon_uri(anchor_id: str, registry: dict) -> str:
    book_code = anchor_id.split(".", 1)[0]
    testament = book_testament(registry, book_code)
    if testament is None:
        raise ValueError(f"unknown book code in registry: {book_code}")
    return f"canon/{testament}/{book_code}.md#{anchor_id}"


def load_records(paths: list[Path]) -> list[ReferenceRecord]:
    records: list[ReferenceRecord] = []
    for path in paths:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            payload = json.loads(line)
            record = ReferenceRecord(**payload)
            record.validate()
            records.append(record)
    return sorted(records, key=lambda item: (item.anchor_id, item.source_file, item.line_number, item.raw_match))


def build_backlink_index(records: list[ReferenceRecord], registry: dict) -> dict[str, dict[str, dict]]:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    by_domain: dict[str, dict[str, dict]] = defaultdict(dict)
    for record in records:
        domain = detect_domain(record.source_file)
        payload = by_domain[domain].setdefault(
            record.anchor_id,
            {
                "anchor_id": record.anchor_id,
                "canon_uri": canon_uri(record.anchor_id, registry),
                "text_tradition": "LXX",
                "generated_at": generated_at,
                "generator_version": GENERATOR_VERSION,
                "links": [],
            },
        )
        payload["links"].append(
            {
                "source_file": record.source_file,
                "line_number": record.line_number,
                "raw_match": record.raw_match,
                "reference_type": record.reference_type,
                "context": record.context,
            }
        )

    for domain_payload in by_domain.values():
        for anchor_payload in domain_payload.values():
            anchor_payload["links"].sort(
                key=lambda item: (item["source_file"], item["line_number"], item["raw_match"])
            )
    return by_domain


def write_backlinks(backlinks: dict[str, dict[str, dict]], output_root: Path = BACKLINKS_ROOT) -> list[Path]:
    written: list[Path] = []
    for domain, anchors in backlinks.items():
        for anchor_id, payload in sorted(anchors.items()):
            out_path = output_root / domain / anchor_filename(anchor_id)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            written.append(out_path)
    return written


def build_from_paths(
    input_paths: list[Path],
    output_root: Path = BACKLINKS_ROOT,
    registry_path: Path = REGISTRY_PATH,
) -> list[Path]:
    registry = load_registry(registry_path)
    records = load_records(input_paths)
    backlinks = build_backlink_index(records, registry)
    return write_backlinks(backlinks, output_root=output_root)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build backlink shards from R1 JSONL files.")
    parser.add_argument("paths", nargs="+", type=Path, help="One or more R1 JSONL paths")
    parser.add_argument("--output-root", type=Path, default=BACKLINKS_ROOT)
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()

    written = build_from_paths(args.paths, output_root=args.output_root, registry_path=args.registry)
    print(json.dumps([str(path) for path in written], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
