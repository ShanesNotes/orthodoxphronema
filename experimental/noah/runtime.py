#!/usr/bin/env python3
"""
runtime.py — Pericope-based Noah runtime harness.

Follows MINIMAL_RUNTIME_RUNBOOK.md exactly:
1. git pull in repo
2. Read noah_state.yaml from vault
3. Open session_queue.jsonl
4. Resolve next session
5. Extract pericope text from canon using start/end anchors
6. Copy source -> bible/{BOOK}/{SESSION_ID}.md
7. Generate prompt -> prompts/{BOOK}/{SESSION_ID}.md
8. Create journal scaffold -> journal/{DATE}_{SESSION_ID}.md
9. Invoke agent (model-neutral CLI, --model flag)
10. Advance state

No pipeline/ imports — reads JSONL and canon as data.

CLI: python3 runtime.py --repo /path --vault /path [--model X] [--dry-run] [--session ID]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

QUEUE_REL_PATH = "metadata/agent_ingestion/noah/session_queue.jsonl"
SYSTEM_PROMPT_REL = "experimental/noah/noah_system_prompt.md"
RE_ANCHOR_LINE = re.compile(r"^([A-Z0-9]+)\.(\d+):(\d+)\s")


def _load_state(vault: Path) -> dict:
    state_path = vault / "noah_state.yaml"
    if not state_path.exists():
        return {}
    return yaml.safe_load(state_path.read_text(encoding="utf-8")) or {}


def _save_state(vault: Path, state: dict) -> None:
    (vault / "noah_state.yaml").write_text(
        yaml.dump(state, default_flow_style=False, sort_keys=False),
        encoding="utf-8",
    )


def _load_queue(repo: Path) -> list[dict]:
    path = repo / QUEUE_REL_PATH
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _resolve_next_session(queue: list[dict], state: dict, override: str | None) -> dict | None:
    if override:
        for row in queue:
            if row["session_id"] == override:
                return row
        return None
    last = state.get("last_completed_session")
    if last is None:
        return queue[0] if queue else None
    for row in queue:
        if row["session_id"] == last:
            nxt = row.get("next_session_id")
            if nxt is None:
                return None  # end of queue
            for r in queue:
                if r["session_id"] == nxt:
                    return r
    return None


def _anchor_key(anchor: str) -> tuple[str, int, int]:
    book, rest = anchor.split(".", 1)
    ch, v = rest.split(":", 1)
    return book, int(ch), int(v)


def _in_range(anchor: str, start: str, end: str) -> bool:
    return _anchor_key(start) <= _anchor_key(anchor) <= _anchor_key(end)


def _extract_source(repo: Path, row: dict) -> str:
    """Read the canon file and extract the pericope text range."""
    canon_path = repo / row["source_canon_path"]
    lines = canon_path.read_text(encoding="utf-8").splitlines()
    selected: list[str] = []
    for line in lines:
        m = RE_ANCHOR_LINE.match(line)
        if not m:
            continue
        anchor = f"{m.group(1)}.{int(m.group(2))}:{int(m.group(3))}"
        if _in_range(anchor, row["start_anchor"], row["end_anchor"]):
            selected.append(line.strip())
    return "\n".join(selected)


def _build_source_md(row: dict, text: str) -> str:
    return f"""---
session_id: "{row['session_id']}"
book_code: "{row['book_code']}"
pericope_title: "{row['pericope_title']}"
start_anchor: "{row['start_anchor']}"
end_anchor: "{row['end_anchor']}"
writeback_policy: "{row['writeback_policy']}"
---

# Source: {row['pericope_title']}

{text}
"""


def _build_prompt_md(row: dict) -> str:
    return f"""---
session_id: "{row['session_id']}"
book_code: "{row['book_code']}"
pericope_title: "{row['pericope_title']}"
---

# Prompt: {row['pericope_title']}

Respond only to the source passage paired with this prompt.
Keep observations visibly grounded in quoted phrases or verse anchors.
Creative and exploratory thoughts are welcome, but do not import outside commentary in this version.

## Literal scene
State plainly what happens in the text and what the passage is doing on its own terms.

## Patterns
Note repetitions, contrasts, images, relations, boundaries, or movements that stand out.

## Tension or surprise
Name what feels unresolved, startling, paradoxical, or newly charged.

## Interior response
Describe what draws your attention, what resists you, and what lingers after reading.

## Question / prayer
Write one open question and one short prayer or intention arising from this passage.
"""


def _build_journal_md(row: dict) -> str:
    return f"""---
session_id: "{row['session_id']}"
book_code: "{row['book_code']}"
pericope_title: "{row['pericope_title']}"
date: "{datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
---

# Journal: {row['pericope_title']}

## Literal scene

## Patterns

## Tension or surprise

## Interior response

## Question / prayer
"""


def materialize_session(repo: Path, vault: Path, row: dict, dry_run: bool = False) -> dict[str, Path]:
    """Write source, prompt, and journal files to vault. Returns path dict."""
    book = row["book_code"]
    sid = row["session_id"]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    source_text = _extract_source(repo, row)

    paths = {
        "bible": vault / "bible" / book / f"{sid}.md",
        "prompt": vault / "prompts" / book / f"{sid}.md",
        "journal": vault / "journal" / f"{today}_{sid}.md",
    }

    contents = {
        "bible": _build_source_md(row, source_text),
        "prompt": _build_prompt_md(row),
        "journal": _build_journal_md(row),
    }

    for key, path in paths.items():
        if dry_run:
            print(f"  [dry-run] would write: {path}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        if key == "journal" and path.exists():
            print(f"  [skip] journal exists: {path}")
            continue
        path.write_text(contents[key], encoding="utf-8")
        print(f"  [write] {path}")

    return paths


def advance_state(vault: Path, row: dict) -> None:
    """Update noah_state.yaml after session completion."""
    state = _load_state(vault)
    state["agent"] = "Noah"
    state["queue_version"] = row.get("queue_version", "noah-queue-v2")
    state["last_completed_session"] = row["session_id"]
    state["next_session"] = row.get("next_session_id")
    state["last_run_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    _save_state(vault, state)


def run(
    repo: Path,
    vault: Path,
    model: str | None = None,
    dry_run: bool = False,
    session_override: str | None = None,
    skip_pull: bool = False,
) -> None:
    repo = repo.resolve()
    vault = vault.resolve()

    # Step 1: git pull
    if not skip_pull and not dry_run:
        print("[1] git pull")
        subprocess.run(["git", "-C", str(repo), "pull"], check=True)
    else:
        print("[1] git pull (skipped)")

    # Step 2: read state
    print("[2] reading state")
    state = _load_state(vault)

    # Step 3: open queue
    print("[3] loading queue")
    queue = _load_queue(repo)
    print(f"     {len(queue)} sessions in queue")

    # Step 4: resolve next session
    print("[4] resolving session")
    row = _resolve_next_session(queue, state, session_override)
    if row is None:
        print("     no session to run (queue complete or override not found)")
        return
    print(f"     session: {row['session_id']} — {row['pericope_title']}")

    # Steps 5-8: materialize
    print("[5-8] materializing session")
    paths = materialize_session(repo, vault, row, dry_run=dry_run)

    if dry_run:
        print("[dry-run] stopping before agent invocation")
        return

    # Step 9: invoke agent
    print("[9] invoking agent")
    if model:
        system_prompt = repo / SYSTEM_PROMPT_REL
        cmd = [
            "claude", "--model", model,
            "--system-prompt", str(system_prompt),
            "--input", str(paths["prompt"]),
            "--output", str(paths["journal"]),
        ]
        print(f"     cmd: {' '.join(cmd)}")
        # Uncomment when ready for live runs:
        # subprocess.run(cmd, check=True)
        print("     [stub] agent invocation placeholder — uncomment when model CLI is configured")
    else:
        print("     no --model specified; skipping agent invocation")

    # Step 10: advance state
    print("[10] advancing state")
    advance_state(vault, row)
    print(f"     done. next: {row.get('next_session_id', 'END')}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Noah pericope runtime harness.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--repo", type=Path, required=True, help="Path to orthodoxphronema repo")
    parser.add_argument("--vault", type=Path, required=True, help="Path to Noah vault directory")
    parser.add_argument("--model", default=None, help="Model identifier for agent invocation")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing files")
    parser.add_argument("--session", default=None, help="Override: run a specific session ID")
    parser.add_argument("--skip-pull", action="store_true", help="Skip git pull step")
    args = parser.parse_args()

    run(
        repo=args.repo,
        vault=args.vault,
        model=args.model,
        dry_run=args.dry_run,
        session_override=args.session,
        skip_pull=args.skip_pull,
    )


if __name__ == "__main__":
    main()
