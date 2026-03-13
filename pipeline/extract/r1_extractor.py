"""
r1_extractor.py — Narrow R1 extraction seed for future-layer metadata.
"""
from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from pipeline.common.paths import METADATA_ROOT, REGISTRY_PATH, REPO_ROOT
from pipeline.common.registry import chapter_verse_counts, load_registry
from pipeline.extract.models import ReferenceRecord
from pipeline.reference.wikilinks import find_reference_instances, iter_text_blocks

R1_OUTPUT_DIR = METADATA_ROOT / "r1_output"

def _registry_dimensions(path: Path | str = REGISTRY_PATH) -> dict[str, dict[int, int]]:
    registry = load_registry(path)
    dims: dict[str, dict[int, int]] = {}
    for book in registry.get("books", []):
        cvc = chapter_verse_counts(registry, book["code"])
        if cvc:
            dims[book["code"]] = cvc
    return dims


def _relative_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def extract_references_from_path(
    path: Path | str,
    dimensions: dict[str, dict[int, int]] | None = None,
) -> list[ReferenceRecord]:
    dimensions = dimensions or _registry_dimensions()
    path = Path(path)
    records: list[ReferenceRecord] = []
    source_file = _relative_path(path)

    for block_lines, context in iter_text_blocks(path):
        for line_no, line in block_lines:
            for instance in find_reference_instances(line, dimensions):
                for anchor_id in instance.anchor_ids:
                    records.append(
                        ReferenceRecord(
                            source_file=source_file,
                            line_number=line_no,
                            raw_match=instance.raw_text,
                            anchor_id=anchor_id,
                            reference_type=instance.reference_type,
                            context=context,
                        )
                    )

    return sorted(
        records,
        key=lambda rec: (rec.anchor_id, rec.line_number, rec.raw_match),
    )


def extract_references_from_paths(paths: Iterable[Path | str]) -> list[ReferenceRecord]:
    dimensions = _registry_dimensions()
    results: list[ReferenceRecord] = []
    for path in paths:
        results.extend(extract_references_from_path(path, dimensions))
    return sorted(
        results,
        key=lambda rec: (rec.anchor_id, rec.line_number, rec.raw_match),
    )


def write_jsonl(records: Iterable[ReferenceRecord], out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(
        records,
        key=lambda rec: (rec.anchor_id, rec.line_number, rec.raw_match),
    )
    lines = [record.to_json() for record in ordered]
    payload = "\n".join(lines)
    if payload:
        payload += "\n"
    out_path.write_text(payload, encoding="utf-8")
    return out_path


def write_book_output(book_code: str, paths: Iterable[Path | str]) -> Path:
    out_path = R1_OUTPUT_DIR / f"{book_code}.jsonl"
    return write_jsonl(extract_references_from_paths(paths), out_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract narrow R1 JSONL from Markdown sources.")
    parser.add_argument("book_code", help="Book code for output naming, e.g. GEN")
    parser.add_argument("paths", nargs="+", type=Path, help="Markdown files to scan")
    args = parser.parse_args()

    out = write_book_output(args.book_code, args.paths)
    print(out)
