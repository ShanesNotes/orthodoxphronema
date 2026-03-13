"""
build_future_seed.py — Build the first future-layer vertical slice from canon + companions.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess

from pipeline.common.frontmatter import parse_frontmatter
from pipeline.common.paths import CANON_ROOT, METADATA_ROOT, REPO_ROOT, STAGING_ROOT
from pipeline.common.patterns import RE_ANCHOR_FULL
from pipeline.common.registry import book_meta, book_testament, load_registry
from pipeline.extract.r1_extractor import extract_references_from_paths, write_book_output
from pipeline.metadata import generate_pericope_index as pericope_mod

DEFAULT_BOOK_CODE = "GEN"
DEFAULT_PERICOPE_TITLE = "The Garden of Eden"
DEFAULT_START_ANCHOR = "GEN.2:7"
DEFAULT_END_ANCHOR = "GEN.2:24"
DEFAULT_COMPANION_BASE = STAGING_ROOT
EMBEDDING_DOCS_DIR = METADATA_ROOT / "embedding_documents"
GENERATOR_VERSION = "future-seed-v1"

RE_FOOTNOTE_ANCHOR = re.compile(r"^\*\(anchor:\s*([A-Z0-9]+\.\d+:\d+)\)\*\s*$")


def _source_timestamp_iso(*paths: Path) -> str:
    existing = [path for path in paths if path.exists()]
    if not existing:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    latest_mtime = max(path.stat().st_mtime for path in existing)
    return datetime.fromtimestamp(latest_mtime, timezone.utc).replace(microsecond=0).isoformat()


def _relative_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def _git_commit_hash() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None


def resolve_paths(book_code: str, companion_base: Path = DEFAULT_COMPANION_BASE) -> dict[str, Path]:
    registry = load_registry()
    testament = book_testament(registry, book_code)
    if testament is None:
        raise ValueError(f"Unknown book code: {book_code}")
    canon_path = CANON_ROOT / testament / f"{book_code}.md"
    footnotes_path = companion_base / testament / f"{book_code}_footnotes.md"
    articles_path = companion_base / testament / f"{book_code}_articles.md"
    return {
        "canon": canon_path,
        "footnotes": footnotes_path,
        "articles": articles_path,
    }


def _anchor_key(anchor: str) -> tuple[str, int, int]:
    book, rest = anchor.split(".", 1)
    chapter, verse = rest.split(":", 1)
    return book, int(chapter), int(verse)


def _in_anchor_range(anchor: str, start_anchor: str, end_anchor: str) -> bool:
    return _anchor_key(start_anchor) <= _anchor_key(anchor) <= _anchor_key(end_anchor)


def _load_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    fm, _ = parse_frontmatter(lines)
    return fm


def _read_scripture_range(canon_path: Path, start_anchor: str, end_anchor: str) -> str:
    lines = canon_path.read_text(encoding="utf-8").splitlines()
    _, body_start = parse_frontmatter(lines)
    selected: list[str] = []
    for line in lines[body_start:]:
        match = RE_ANCHOR_FULL.match(line)
        if not match:
            continue
        anchor = f"{match.group(1)}.{int(match.group(2))}:{int(match.group(3))}"
        if _in_anchor_range(anchor, start_anchor, end_anchor):
            selected.append(line.strip())
    return "\n".join(selected)


def parse_footnotes(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    _, body_start = parse_frontmatter(lines)
    results: list[dict] = []
    current: dict | None = None
    body_lines: list[str] = []

    def flush() -> None:
        nonlocal current, body_lines
        if current is None:
            return
        current["text"] = " ".join(part.strip() for part in body_lines if part.strip()).strip()
        current["end_line"] = current["end_line"] or current["start_line"]
        results.append(current)
        current = None
        body_lines = []

    for idx in range(body_start, len(lines)):
        line_no = idx + 1
        stripped = lines[idx].strip()
        anchor_match = RE_FOOTNOTE_ANCHOR.match(stripped)
        if stripped.startswith("### "):
            flush()
            continue
        if anchor_match:
            flush()
            current = {
                "anchor": anchor_match.group(1),
                "start_line": line_no + 1,
                "end_line": None,
                "text": "",
            }
            continue
        if current is not None:
            if stripped:
                body_lines.append(lines[idx])
                current["end_line"] = line_no
            elif body_lines:
                body_lines.append("")

    flush()
    return results


def build_cross_ref_candidates(
    extracted_records: list,
    note_blocks: list[dict],
    start_anchor: str,
    end_anchor: str,
    footnotes_source_file: str,
) -> list[str]:
    note_ranges = [
        (block["start_line"], block["end_line"])
        for block in note_blocks
        if _in_anchor_range(block["anchor"], start_anchor, end_anchor)
    ]
    candidates = {
        record.anchor_id
        for record in extracted_records
        for start_line, end_line in note_ranges
        if record.source_file == footnotes_source_file and start_line <= record.line_number <= end_line
    }
    return sorted(candidates)


def build_embedding_document(
    book_code: str,
    pericope_title: str,
    start_anchor: str,
    end_anchor: str,
    canon_path: Path,
    footnotes_path: Path,
    articles_path: Path,
    extracted_records: list,
) -> dict:
    generated_at = _source_timestamp_iso(canon_path, footnotes_path, articles_path)
    note_blocks = parse_footnotes(footnotes_path)
    footnotes_source_file = _relative_path(footnotes_path)
    in_range_notes = [
        {
            "anchor": block["anchor"],
            "text": block["text"],
        }
        for block in note_blocks
        if block["text"] and _in_anchor_range(block["anchor"], start_anchor, end_anchor)
    ]
    canon_fm = _load_frontmatter(canon_path)
    footnotes_fm = _load_frontmatter(footnotes_path)
    articles_fm = _load_frontmatter(articles_path) if articles_path.exists() else {}

    return {
        "document_id": f"{book_code}.{start_anchor.split('.', 1)[1]}-{end_anchor.split(':', 1)[1]}",
        "book_code": book_code,
        "pericope_title": pericope_title,
        "start_anchor": start_anchor,
        "end_anchor": end_anchor,
        "scripture_text": _read_scripture_range(canon_path, start_anchor, end_anchor),
        "footnotes": in_range_notes,
        "cross_ref_candidates": build_cross_ref_candidates(
            extracted_records,
            note_blocks,
            start_anchor,
            end_anchor,
            footnotes_source_file,
        ),
        "liturgical_context": None,
        "alt_versification": None,
        "embedding_status": "footnotes_ready" if in_range_notes else "pending",
        "provenance": {
            "canon_source": _relative_path(canon_path),
            "companion_sources": [
                _relative_path(footnotes_path),
                _relative_path(articles_path),
            ],
            "anchor_range": [start_anchor, end_anchor],
            "generator_version": GENERATOR_VERSION,
            "generated_at": generated_at,
            "git_commit_hash": _git_commit_hash(),
            "source_dates": {
                "canon_parse_date": canon_fm.get("parse_date"),
                "canon_promote_date": canon_fm.get("promote_date"),
                "footnotes_parse_date": footnotes_fm.get("parse_date"),
                "articles_parse_date": articles_fm.get("parse_date"),
            },
        },
    }


def enrich_pericope_payload(
    payload: dict,
    pericope_title: str,
    start_anchor: str,
    end_anchor: str,
    footnotes_path: Path,
    articles_path: Path,
    extracted_records: list,
) -> dict:
    generated_at = _source_timestamp_iso(footnotes_path, articles_path)
    enriched = deepcopy(payload)
    note_blocks = parse_footnotes(footnotes_path)
    footnotes_source_file = _relative_path(footnotes_path)
    note_anchors = [
        block["anchor"]
        for block in note_blocks
        if block["text"] and _in_anchor_range(block["anchor"], start_anchor, end_anchor)
    ]
    cross_refs = build_cross_ref_candidates(
        extracted_records,
        note_blocks,
        start_anchor,
        end_anchor,
        footnotes_source_file,
    )
    for pericope in enriched["pericopes"]:
        if pericope["title"] != pericope_title:
            continue
        pericope["notes_anchors"] = note_anchors
        pericope["source_companions"] = [
            _relative_path(footnotes_path),
            _relative_path(articles_path),
        ]
        pericope["cross_ref_candidates"] = cross_refs
        pericope["liturgical_context"] = None
        pericope["alt_versification"] = None
        pericope["embedding_status"] = "footnotes_ready" if note_anchors else "pending"
        pericope["provenance"] = {
            "canon_source": payload["generated_from"],
            "companion_sources": [
                _relative_path(footnotes_path),
                _relative_path(articles_path),
            ],
            "anchor_range": [start_anchor, end_anchor],
            "generator_version": GENERATOR_VERSION,
            "generated_at": generated_at,
            "git_commit_hash": _git_commit_hash(),
        }
        break
    return enriched


def write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def write_jsonl(path: Path, records: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(record, ensure_ascii=True, sort_keys=True) for record in records]
    payload = "\n".join(lines)
    if payload:
        payload += "\n"
    path.write_text(payload, encoding="utf-8")
    return path


def build_seed(
    book_code: str = DEFAULT_BOOK_CODE,
    pericope_title: str = DEFAULT_PERICOPE_TITLE,
    start_anchor: str = DEFAULT_START_ANCHOR,
    end_anchor: str = DEFAULT_END_ANCHOR,
    companion_base: Path = DEFAULT_COMPANION_BASE,
    pericope_out_dir: Path | None = None,
    embedding_out_dir: Path = EMBEDDING_DOCS_DIR,
    r1_out_dir: Path | None = None,
) -> dict[str, Path]:
    paths = resolve_paths(book_code, companion_base)
    pericope_out_dir = pericope_out_dir or pericope_mod.DEFAULT_OUT_DIR
    r1_out_dir = r1_out_dir or (METADATA_ROOT / "r1_output")

    source_paths = [path for path in (paths["footnotes"], paths["articles"]) if path.exists()]
    extracted = extract_references_from_paths(source_paths)
    if r1_out_dir == METADATA_ROOT / "r1_output":
        r1_path = write_book_output(book_code, source_paths)
    else:
        r1_path = write_jsonl(
            r1_out_dir / f"{book_code}.jsonl",
            [record.to_dict() for record in extracted],
        )

    pericope_payload = pericope_mod.extract_pericopes(paths["canon"])
    enriched_payload = enrich_pericope_payload(
        pericope_payload,
        pericope_title,
        start_anchor,
        end_anchor,
        paths["footnotes"],
        paths["articles"],
        extracted,
    )
    pericope_path = write_json(pericope_out_dir / f"{book_code}.json", enriched_payload)

    embedding_doc = build_embedding_document(
        book_code,
        pericope_title,
        start_anchor,
        end_anchor,
        paths["canon"],
        paths["footnotes"],
        paths["articles"],
        extracted,
    )
    embedding_path = write_jsonl(embedding_out_dir / f"{book_code}.jsonl", [embedding_doc])

    return {
        "pericope_index": pericope_path,
        "r1_output": r1_path,
        "embedding_documents": embedding_path,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Build the future-layer vertical seed.")
    parser.add_argument("--book-code", default=DEFAULT_BOOK_CODE)
    parser.add_argument("--pericope-title", default=DEFAULT_PERICOPE_TITLE)
    parser.add_argument("--start-anchor", default=DEFAULT_START_ANCHOR)
    parser.add_argument("--end-anchor", default=DEFAULT_END_ANCHOR)
    parser.add_argument(
        "--companion-base",
        type=Path,
        default=DEFAULT_COMPANION_BASE,
        help=f"Base directory for companion files (default: {DEFAULT_COMPANION_BASE})",
    )
    parser.add_argument("--pericope-out-dir", type=Path, default=pericope_mod.DEFAULT_OUT_DIR)
    parser.add_argument("--r1-out-dir", type=Path, default=METADATA_ROOT / "r1_output")
    parser.add_argument("--embedding-out-dir", type=Path, default=EMBEDDING_DOCS_DIR)
    args = parser.parse_args()

    outputs = build_seed(
        book_code=args.book_code,
        pericope_title=args.pericope_title,
        start_anchor=args.start_anchor,
        end_anchor=args.end_anchor,
        companion_base=args.companion_base,
        pericope_out_dir=args.pericope_out_dir,
        embedding_out_dir=args.embedding_out_dir,
        r1_out_dir=args.r1_out_dir,
    )
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
