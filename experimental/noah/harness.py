#!/usr/bin/env python3
"""Noah ingestion harness — feeds one chapter per day to a Claude agent.

Reads noah_manifest.json, extracts the chapter text from the canon file,
builds the prompt, invokes Claude, and saves the response as a vault entry.

Usage:
    # Run today's portion (reads/advances state from noah_state.json):
    python3 experimental/noah/harness.py

    # Run a specific day:
    python3 experimental/noah/harness.py --day 42

    # Dry run (extract + print, no API call):
    python3 experimental/noah/harness.py --dry-run

    # Use a specific model:
    python3 experimental/noah/harness.py --model claude-sonnet-4-6

Environment:
    ANTHROPIC_API_KEY  — required for API invocation
    NOAH_VAULT_DIR     — vault location (default: ~/noah-vault)
    NOAH_ARCHIVE_DIR   — archive repo root (default: auto-detect from script location)
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ARCHIVE = SCRIPT_DIR.parents[1]
DEFAULT_VAULT = Path.home() / "noah-vault"
STATE_FILE = SCRIPT_DIR / "noah_state.json"
MANIFEST_FILE = SCRIPT_DIR / "noah_manifest.json"
SYSTEM_PROMPT_FILE = SCRIPT_DIR / "noah_system_prompt.md"


def load_manifest():
    if not MANIFEST_FILE.exists():
        print(f"Manifest not found at {MANIFEST_FILE}")
        print("Run: python3 experimental/noah/manifest_generator.py")
        sys.exit(1)
    with open(MANIFEST_FILE) as f:
        return json.load(f)


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_completed_day": 0}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def extract_chapter(canon_file: Path, book_code: str, chapter: int) -> str:
    """Extract a single chapter's text from a canon markdown file.

    Returns the chapter text including any narrative headings (### lines)
    that fall within the chapter boundaries.
    """
    if not canon_file.exists():
        raise FileNotFoundError(f"Canon file not found: {canon_file}")

    content = canon_file.read_text()
    lines = content.split("\n")

    # Find the start of the target chapter
    chapter_header = f"## Chapter {chapter}"
    start_idx = None
    for i, line in enumerate(lines):
        if line.strip() == chapter_header:
            start_idx = i
            break

    if start_idx is None:
        raise ValueError(f"Chapter header '{chapter_header}' not found in {canon_file}")

    # Find the end: next ## Chapter header or end of file
    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        if lines[i].strip().startswith("## Chapter "):
            end_idx = i
            break

    # Extract and clean
    chapter_lines = lines[start_idx:end_idx]

    # Strip trailing blank lines
    while chapter_lines and not chapter_lines[-1].strip():
        chapter_lines.pop()

    return "\n".join(chapter_lines)


def build_prompt(portion: dict, chapter_text: str, vault_dir: Path) -> str:
    """Build the user prompt for Noah's daily reading."""
    day = portion["day"]
    book = portion["book_name"]
    code = portion["book_code"]
    ch = portion["chapter"]
    total_ch = portion["total_chapters"]
    testament = portion["testament"]
    deut = portion["deuterocanonical"]
    position = portion["canon_position"]

    testament_label = "Old Testament" if testament == "OT" else "New Testament"
    deut_note = " (deuterocanonical)" if deut else ""

    prompt = f"""# Day {day} — {book} Chapter {ch}

**Book:** {book}{deut_note}
**Chapter:** {ch} of {total_ch}
**Testament:** {testament_label}
**Canon Position:** {position} of 76

---

{chapter_text}

---

Your vault is at `{vault_dir}/`. You may read any of your previous journal entries.
Today's entry should be saved to `{vault_dir}/daily/{portion['entry_filename']}`.
"""
    return prompt


def load_system_prompt() -> str:
    if not SYSTEM_PROMPT_FILE.exists():
        raise FileNotFoundError(f"System prompt not found: {SYSTEM_PROMPT_FILE}")
    return SYSTEM_PROMPT_FILE.read_text()


def invoke_noah(system_prompt: str, user_prompt: str, vault_dir: Path,
                model: str, archive_dir: Path) -> str:
    """Invoke Noah via the Claude CLI (claude-code).

    Noah gets tool access to its vault directory for reading previous entries.
    """
    # Build the full prompt with system context
    full_prompt = user_prompt

    cmd = [
        "claude",
        "--print",
        "--model", model,
        "--system-prompt", system_prompt,
        "--allowedTools", "Read,Glob,Grep,Write,Bash",
        "--max-turns", "10",
        "--prompt", full_prompt,
    ]

    env = os.environ.copy()

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env,
        timeout=600,  # 10 minute timeout
    )

    if result.returncode != 0:
        print(f"Claude CLI error (exit {result.returncode}):", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"Claude invocation failed with exit code {result.returncode}")

    return result.stdout


def save_entry(vault_dir: Path, portion: dict, response: str):
    """Save Noah's journal entry with YAML frontmatter."""
    daily_dir = vault_dir / "daily"
    daily_dir.mkdir(parents=True, exist_ok=True)

    entry_path = daily_dir / portion["entry_filename"]

    frontmatter = f"""---
day: {portion['day']}
book: {portion['book_name']}
book_code: {portion['book_code']}
chapter: {portion['chapter']}
testament: {portion['testament']}
canon_position: {portion['canon_position']}
deuterocanonical: {str(portion['deuterocanonical']).lower()}
date: {date.today().isoformat()}
---

"""
    entry_path.write_text(frontmatter + response)
    return entry_path


def ensure_vault(vault_dir: Path):
    """Create the vault directory structure if it doesn't exist."""
    (vault_dir / "daily").mkdir(parents=True, exist_ok=True)
    (vault_dir / "themes").mkdir(exist_ok=True)
    (vault_dir / "questions").mkdir(exist_ok=True)

    index_path = vault_dir / "index.md"
    if not index_path.exists():
        index_path.write_text(
            "# Noah's Scripture Journal\n\n"
            "Sequential encounter with the Orthodox canon — 76 books, 1,344 chapters.\n\n"
            "## Structure\n"
            "- `daily/` — One entry per chapter, in canonical order\n"
            "- `themes/` — Emergent thematic notes (created by Noah)\n"
            "- `questions/` — Unresolved questions (created by Noah)\n"
        )


def main():
    parser = argparse.ArgumentParser(description="Noah ingestion harness")
    parser.add_argument("--day", type=int, help="Run a specific day (default: next)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Extract and print chapter text without invoking Claude")
    parser.add_argument("--model", default="claude-sonnet-4-6",
                        help="Model to use (default: claude-sonnet-4-6)")
    parser.add_argument("--vault", type=str, default=None,
                        help=f"Vault directory (default: {DEFAULT_VAULT})")
    parser.add_argument("--archive", type=str, default=None,
                        help=f"Archive repo root (default: {DEFAULT_ARCHIVE})")
    args = parser.parse_args()

    archive_dir = Path(args.archive) if args.archive else DEFAULT_ARCHIVE
    vault_dir = Path(args.vault) if args.vault else Path(
        os.environ.get("NOAH_VAULT_DIR", str(DEFAULT_VAULT)))

    manifest = load_manifest()
    state = load_state()

    # Determine which day to run
    if args.day is not None:
        target_day = args.day
    else:
        target_day = state["last_completed_day"] + 1

    if target_day < 1 or target_day > manifest["total_days"]:
        print(f"Day {target_day} is out of range (1-{manifest['total_days']})")
        sys.exit(1)

    portion = manifest["portions"][target_day - 1]
    assert portion["day"] == target_day

    canon_file = archive_dir / portion["canon_file"]

    print(f"Day {target_day}/{manifest['total_days']}: "
          f"{portion['book_name']} ch{portion['chapter']} "
          f"({portion['testament']})")

    # Extract chapter
    chapter_text = extract_chapter(canon_file, portion["book_code"], portion["chapter"])

    if args.dry_run:
        print("\n--- CHAPTER TEXT ---")
        print(chapter_text)
        print(f"\n--- {len(chapter_text)} chars, "
              f"{len(chapter_text.splitlines())} lines ---")
        return

    # Set up vault
    ensure_vault(vault_dir)

    # Build prompt
    system_prompt = load_system_prompt()
    user_prompt = build_prompt(portion, chapter_text, vault_dir)

    # Invoke Noah
    print(f"Invoking Noah ({args.model})...")
    response = invoke_noah(system_prompt, user_prompt, vault_dir,
                           args.model, archive_dir)

    # Save entry
    entry_path = save_entry(vault_dir, portion, response)
    print(f"Entry saved: {entry_path}")

    # Update state
    state["last_completed_day"] = target_day
    state["last_run_date"] = date.today().isoformat()
    save_state(state)
    print(f"State updated: day {target_day} complete")


if __name__ == "__main__":
    main()
