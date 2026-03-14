"""
build_noah_queue.py — Build a read-only Noah ingestion queue from canon pericopes.

Supports single-book mode (--book GEN) and full-canon mode (--all-books).
Full-canon mode links pericopes across all 76 books in canonical position order.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from pipeline.common.paths import METADATA_ROOT, REPO_ROOT, canon_filepath
from pipeline.common.registry import book_meta, book_testament, load_registry
from pipeline.metadata import generate_pericope_index as pericope_mod

QUEUE_VERSION = "noah-queue-v2"
PROMPT_TEMPLATE_ID = "noah_journal_v1"
WRITEBACK_POLICY = "read_only"
DEFAULT_OUT_DIR = METADATA_ROOT / "agent_ingestion" / "noah"


def _timestamp_for(*paths: Path) -> str:
    existing = [path for path in paths if path.exists()]
    latest = max(path.stat().st_mtime for path in existing) if existing else None
    if latest is None:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return datetime.fromtimestamp(latest, timezone.utc).replace(microsecond=0).isoformat()


def _relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def _pericope_index_path(book_code: str, pericope_out_dir: Path) -> Path:
    return pericope_out_dir / f"{book_code}.json"


def ensure_pericope_index(book_code: str, pericope_out_dir: Path = pericope_mod.DEFAULT_OUT_DIR) -> Path:
    registry = load_registry()
    testament = book_testament(registry, book_code)
    if testament is None:
        raise ValueError(f"Unknown book code: {book_code}")
    out_path = _pericope_index_path(book_code, pericope_out_dir)
    if out_path.exists():
        return out_path
    canon_path = canon_filepath(testament, book_code)
    return pericope_mod.write_pericope_index(canon_path, pericope_out_dir)


def load_pericope_payload(book_code: str, pericope_out_dir: Path = pericope_mod.DEFAULT_OUT_DIR) -> dict:
    path = ensure_pericope_index(book_code, pericope_out_dir)
    return json.loads(path.read_text(encoding="utf-8"))


def build_queue_rows(book_code: str, pericope_out_dir: Path = pericope_mod.DEFAULT_OUT_DIR) -> list[dict]:
    registry = load_registry()
    meta = book_meta(registry, book_code)
    testament = meta["testament"]
    canon_path = canon_filepath(testament, book_code)
    pericope_path = ensure_pericope_index(book_code, pericope_out_dir)
    payload = load_pericope_payload(book_code, pericope_out_dir)
    generated_at = _timestamp_for(canon_path, pericope_path)

    rows: list[dict] = []
    pericopes = payload.get("pericopes", [])
    for idx, pericope in enumerate(pericopes, start=1):
        rows.append(
            {
                "session_id": f"{book_code}.P{idx:03d}",
                "book_code": book_code,
                "canon_position": meta["position"],
                "pericope_index": idx,
                "pericope_title": pericope["title"],
                "start_anchor": pericope["start_anchor"],
                "end_anchor": pericope["end_anchor"],
                "verse_count": pericope.get("verse_count"),
                "chapter_range": pericope.get("chapter_range"),
                "source_canon_path": _relative(canon_path),
                "generated_from": _relative(pericope_path),
                "previous_session_id": None,
                "next_session_id": None,
                "global_session_index": None,
                "queue_version": QUEUE_VERSION,
                "generated_at": generated_at,
                "writeback_policy": WRITEBACK_POLICY,
                "prompt_template_id": PROMPT_TEMPLATE_ID,
            }
        )

    # Intra-book linking
    for idx, row in enumerate(rows):
        if idx > 0:
            row["previous_session_id"] = rows[idx - 1]["session_id"]
        if idx + 1 < len(rows):
            row["next_session_id"] = rows[idx + 1]["session_id"]
    return rows


def build_all_books_rows(pericope_out_dir: Path = pericope_mod.DEFAULT_OUT_DIR) -> list[dict]:
    """Build queue rows for all 76 books in canonical position order with cross-book linking."""
    registry = load_registry()
    books = sorted(registry["books"], key=lambda b: b["position"])

    all_rows: list[dict] = []
    for book in books:
        rows = build_queue_rows(book["code"], pericope_out_dir)
        all_rows.extend(rows)

    # Cross-book linking + global index
    for idx, row in enumerate(all_rows):
        row["global_session_index"] = idx + 1
        if idx > 0:
            row["previous_session_id"] = all_rows[idx - 1]["session_id"]
        if idx + 1 < len(all_rows):
            row["next_session_id"] = all_rows[idx + 1]["session_id"]

    return all_rows


def write_queue(rows: list[dict], out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = "\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n"
    out_path.write_text(payload, encoding="utf-8")
    return out_path


def build_queue(
    book_code: str,
    out_dir: Path = DEFAULT_OUT_DIR,
    pericope_out_dir: Path = pericope_mod.DEFAULT_OUT_DIR,
) -> Path:
    rows = build_queue_rows(book_code, pericope_out_dir)
    return write_queue(rows, out_dir / "session_queue.jsonl")


def build_full_canon_queue(
    out_dir: Path = DEFAULT_OUT_DIR,
    pericope_out_dir: Path = pericope_mod.DEFAULT_OUT_DIR,
) -> Path:
    rows = build_all_books_rows(pericope_out_dir)
    return write_queue(rows, out_dir / "session_queue.jsonl")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Noah ingestion queue from canon pericopes.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--book", default=None, help="Book code to build (e.g. GEN)")
    group.add_argument("--all-books", action="store_true", help="Build full-canon queue (all 76 books)")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--pericope-out-dir", type=Path, default=pericope_mod.DEFAULT_OUT_DIR)
    args = parser.parse_args()

    if args.all_books:
        out_path = build_full_canon_queue(out_dir=args.out_dir, pericope_out_dir=args.pericope_out_dir)
    else:
        book = args.book or "GEN"
        out_path = build_queue(book, out_dir=args.out_dir, pericope_out_dir=args.pericope_out_dir)
    print(out_path)


if __name__ == "__main__":
    main()
