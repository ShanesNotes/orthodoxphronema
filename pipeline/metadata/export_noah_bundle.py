"""
export_noah_bundle.py — Export Noah ingestion bundles for a downstream Obsidian vault.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from pipeline.common.frontmatter import parse_frontmatter
from pipeline.common.patterns import RE_ANCHOR_FULL
from pipeline.metadata import build_noah_queue as queue_mod


def _load_jsonl(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def _anchor_key(anchor: str) -> tuple[str, int, int]:
    book, rest = anchor.split(".", 1)
    chapter, verse = rest.split(":", 1)
    return book, int(chapter), int(verse)


def _in_range(anchor: str, start_anchor: str, end_anchor: str) -> bool:
    return _anchor_key(start_anchor) <= _anchor_key(anchor) <= _anchor_key(end_anchor)


def _read_scripture_range(canon_path: Path, start_anchor: str, end_anchor: str) -> str:
    lines = canon_path.read_text(encoding="utf-8").splitlines()
    _, body_start = parse_frontmatter(lines)
    selected: list[str] = []
    for line in lines[body_start:]:
        match = RE_ANCHOR_FULL.match(line)
        if not match:
            continue
        anchor = f"{match.group(1)}.{int(match.group(2))}:{int(match.group(3))}"
        if _in_range(anchor, start_anchor, end_anchor):
            selected.append(line.strip())
    return "\n".join(selected)


def _yaml_frontmatter(row: dict) -> str:
    fields = [
        ("session_id", row["session_id"]),
        ("book_code", row["book_code"]),
        ("canon_position", row["canon_position"]),
        ("pericope_title", row["pericope_title"]),
        ("start_anchor", row["start_anchor"]),
        ("end_anchor", row["end_anchor"]),
        ("source_canon_path", row["source_canon_path"]),
        ("writeback_policy", row["writeback_policy"]),
        ("queue_version", row["queue_version"]),
        ("prompt_template_id", row["prompt_template_id"]),
    ]
    body = ["---"]
    for key, value in fields:
        body.append(f'{key}: "{value}"' if isinstance(value, str) else f"{key}: {value}")
    body.append("---")
    return "\n".join(body)


def _build_prompt_text(row: dict) -> str:
    return "\n".join(
        [
            _yaml_frontmatter(row),
            "",
            f"# Prompt: {row['pericope_title']}",
            "",
            "Respond only to the source passage paired with this prompt.",
            "Keep observations visibly grounded in quoted phrases or verse anchors.",
            "Creative and exploratory thoughts are welcome, but do not import outside commentary in this version.",
            "",
            "## Literal scene",
            "State plainly what happens in the text and what the passage is doing on its own terms.",
            "",
            "## Patterns",
            "Note repetitions, contrasts, images, relations, boundaries, or movements that stand out.",
            "",
            "## Tension or surprise",
            "Name what feels unresolved, startling, paradoxical, or newly charged.",
            "",
            "## Interior response",
            "Describe what draws your attention, what resists you, and what lingers after reading.",
            "",
            "## Question / prayer",
            "Write one open question and one short prayer or intention arising from this passage.",
            "",
        ]
    )


def _build_journal_text(row: dict) -> str:
    return "\n".join(
        [
            _yaml_frontmatter(row),
            "",
            f"# Journal: {row['pericope_title']}",
            "",
            "## Literal scene",
            "",
            "## Patterns",
            "",
            "## Tension or surprise",
            "",
            "## Interior response",
            "",
            "## Question / prayer",
            "",
        ]
    )


def _build_source_text(row: dict, scripture_text: str) -> str:
    return "\n".join(
        [
            _yaml_frontmatter(row),
            "",
            f"# Source: {row['pericope_title']}",
            "",
            scripture_text,
            "",
        ]
    )


def export_bundle(
    queue_path: Path,
    start_session: int,
    count: int,
    out_dir: Path,
) -> Path:
    rows = _load_jsonl(queue_path)
    if start_session < 1:
        raise ValueError("start_session must be >= 1")
    if count < 1:
        raise ValueError("count must be >= 1")

    start_idx = start_session - 1
    selected = rows[start_idx:start_idx + count]
    if not selected:
        raise ValueError("No sessions found for the requested slice")

    bundle_id = f"{selected[0]['session_id']}__{selected[-1]['session_id']}"
    bundle_dir = out_dir / bundle_id
    bundle_dir.mkdir(parents=True, exist_ok=True)

    session_ids: list[str] = []
    for idx, row in enumerate(selected, start=1):
        canon_path = queue_mod.REPO_ROOT / row["source_canon_path"]
        scripture_text = _read_scripture_range(canon_path, row["start_anchor"], row["end_anchor"])
        prefix = f"{idx:02d}_{row['session_id']}"
        (bundle_dir / f"{prefix}_source.md").write_text(
            _build_source_text(row, scripture_text),
            encoding="utf-8",
        )
        (bundle_dir / f"{prefix}_prompt.md").write_text(
            _build_prompt_text(row),
            encoding="utf-8",
        )
        (bundle_dir / f"{prefix}_journal.md").write_text(
            _build_journal_text(row),
            encoding="utf-8",
        )
        session_ids.append(row["session_id"])

    bundle_payload = {
        "bundle_id": bundle_id,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "session_count": len(selected),
        "session_ids": session_ids,
        "writeback_policy": queue_mod.WRITEBACK_POLICY,
        "prompt_template_id": queue_mod.PROMPT_TEMPLATE_ID,
        "queue_version": selected[0]["queue_version"],
    }
    (bundle_dir / "00_bundle.json").write_text(
        json.dumps(bundle_payload, indent=2) + "\n",
        encoding="utf-8",
    )
    return bundle_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a Noah ingestion bundle.")
    parser.add_argument("--queue", type=Path, default=queue_mod.DEFAULT_OUT_DIR / "session_queue.jsonl")
    parser.add_argument("--book", default="GEN", help="Book code to build queue for if missing (default: GEN)")
    parser.add_argument("--start-session", type=int, required=True)
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    queue_path = args.queue
    if not queue_path.exists():
        queue_path = queue_mod.build_queue(args.book, out_dir=queue_path.parent)
    bundle_dir = export_bundle(queue_path, args.start_session, args.count, args.out_dir)
    print(bundle_dir)


if __name__ == "__main__":
    main()
