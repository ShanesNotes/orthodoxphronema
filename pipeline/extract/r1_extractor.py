"""
r1_extractor.py — Narrow R1 extraction seed for future-layer metadata.
"""
from __future__ import annotations

from collections.abc import Iterable
import json
from pathlib import Path
import re

from pipeline.common.frontmatter import parse_frontmatter
from pipeline.common.paths import METADATA_ROOT, REGISTRY_PATH, REPO_ROOT
from pipeline.common.registry import chapter_verse_counts, load_registry
from pipeline.extract.models import ReferenceRecord
from pipeline.reference.reference_aliases import canonical_biblical_code

R1_OUTPUT_DIR = METADATA_ROOT / "r1_output"

FROZEN_RE = re.compile(r"\[\[([A-Za-z0-9]{1,8})\.(\d+):(\d+)\]\]")
BARE_RE = re.compile(
    r"(?<!\[\[)(?P<book>[1-4]?[A-Za-z]{1,8})\s+(?P<chapter>\d+):(?P<verse>\d+)(?:-\d+)?"
)

def _registry_dimensions(path: Path | str = REGISTRY_PATH) -> dict[str, dict[int, int]]:
    registry = load_registry(path)
    dims: dict[str, dict[int, int]] = {}
    for book in registry.get("books", []):
        cvc = chapter_verse_counts(registry, book["code"])
        if cvc:
            dims[book["code"]] = cvc
    return dims


def _normalize_book_token(token: str) -> str | None:
    cleaned = token.strip().rstrip(".,;:)]}")
    return canonical_biblical_code(cleaned)


def normalize_anchor_id(
    book_token: str,
    chapter_text: str,
    verse_text: str,
    dimensions: dict[str, dict[int, int]] | None = None,
) -> str | None:
    dimensions = dimensions or _registry_dimensions()
    book_code = _normalize_book_token(book_token)
    if book_code is None:
        return None
    chapter = int(chapter_text)
    verse = int(verse_text)
    cvc = dimensions.get(book_code)
    if cvc is None:
        return None
    if chapter not in cvc or verse < 1 or verse > cvc[chapter]:
        return None
    return f"{book_code}.{chapter}:{verse}"


def _relative_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def _iter_text_blocks(path: Path) -> Iterable[tuple[list[tuple[int, str]], str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    _, body_start = parse_frontmatter(lines)
    current: list[tuple[int, str]] = []
    in_code_fence = False

    def flush() -> tuple[list[tuple[int, str]], str] | None:
        nonlocal current
        if not current:
            return None
        context = " ".join(text.strip() for _, text in current if text.strip()).strip()
        block = current
        current = []
        if not context:
            return None
        return block, context

    for idx in range(body_start, len(lines)):
        line_no = idx + 1
        line = lines[idx]
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            payload = flush()
            if payload:
                yield payload
            continue
        if in_code_fence:
            continue
        if not stripped:
            payload = flush()
            if payload:
                yield payload
            continue
        if stripped.startswith("#") or stripped.startswith("*(anchor:"):
            payload = flush()
            if payload:
                yield payload
            continue

        current.append((line_no, line))

    payload = flush()
    if payload:
        yield payload


def extract_references_from_path(
    path: Path | str,
    dimensions: dict[str, dict[int, int]] | None = None,
) -> list[ReferenceRecord]:
    dimensions = dimensions or _registry_dimensions()
    path = Path(path)
    records: list[ReferenceRecord] = []
    source_file = _relative_path(path)

    for block_lines, context in _iter_text_blocks(path):
        for line_no, line in block_lines:
            frozen_spans: list[tuple[int, int]] = []
            for match in FROZEN_RE.finditer(line):
                anchor_id = normalize_anchor_id(
                    match.group(1),
                    match.group(2),
                    match.group(3),
                    dimensions,
                )
                if anchor_id is None:
                    continue
                records.append(
                    ReferenceRecord(
                        source_file=source_file,
                        line_number=line_no,
                        raw_match=match.group(0),
                        anchor_id=anchor_id,
                        reference_type="frozen",
                        context=context,
                    )
                )
                frozen_spans.append(match.span())

            masked = list(line)
            for start, end in frozen_spans:
                for i in range(start, end):
                    masked[i] = " "
            masked_line = "".join(masked)

            for match in BARE_RE.finditer(masked_line):
                anchor_id = normalize_anchor_id(
                    match.group("book"),
                    match.group("chapter"),
                    match.group("verse"),
                    dimensions,
                )
                if anchor_id is None:
                    continue
                records.append(
                    ReferenceRecord(
                        source_file=source_file,
                        line_number=line_no,
                        raw_match=match.group(0),
                        anchor_id=anchor_id,
                        reference_type="bare",
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
