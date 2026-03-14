#!/usr/bin/env python3
"""
autoresearch_runner.py — Offline optimization loop per AUTORESEARCH_SPEC.md.

Karpathy-style optimize-measure-keep/discard loop:
1. Read program.md + load candidate_profile.yaml
2. Replay frozen evaluation_manifest.json sessions
3. Generate journal under candidate prompt template
4. Score via evaluator
5. Aggregate scores across manifest
6. If gates pass AND score beats active profile -> promote to active_profile.yaml
7. Append to experiment_log.jsonl

10-minute wall-clock cap per candidate. Runs in downstream sandbox, never touches archive.

CLI: python3 autoresearch_runner.py --sandbox /path [--repo /path] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

# Allow import from same directory
import sys
sys.path.insert(0, str(Path(__file__).parent))

from evaluator import Scorecard, evaluate

WALL_CLOCK_CAP_SECONDS = 600  # 10 minutes


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_manifest(sandbox: Path) -> list[dict]:
    """Load the frozen evaluation manifest."""
    return json.loads((sandbox / "evaluation_manifest.json").read_text(encoding="utf-8"))


def load_profile(path: Path) -> dict:
    """Load a YAML profile (candidate or active)."""
    return _load_yaml(path)


def replay_session(
    sandbox: Path,
    session: dict,
    profile: dict,
    repo: Path | None = None,
) -> tuple[str, str, int]:
    """Replay a single manifest session. Returns (journal_text, source_text, verse_count).

    In v1 this reads pre-existing journals from the baseline directory.
    Future versions will invoke the agent to generate under the candidate profile.
    """
    sid = session["session_id"]
    baseline_dir = sandbox / "baseline"

    # Read the baseline journal
    journal_path = baseline_dir / f"{sid}_journal.md"
    if not journal_path.exists():
        return "", "", 0
    journal_text = journal_path.read_text(encoding="utf-8")

    # Read the source
    source_path = baseline_dir / f"{sid}_source.md"
    source_text = source_path.read_text(encoding="utf-8") if source_path.exists() else ""

    verse_count = session.get("verse_count", 0) or 0
    return journal_text, source_text, verse_count


def score_candidate(
    sandbox: Path,
    manifest: list[dict],
    profile: dict,
    repo: Path | None = None,
) -> tuple[list[Scorecard], dict]:
    """Run all manifest sessions, score each, return (scorecards, aggregate)."""
    weights = profile.get("scoring", {}).get("weights", None)
    threshold = (
        profile.get("scoring", {})
        .get("hard_gates", {})
        .get("minimum_grounding_score", 0.70)
    )

    scorecards: list[Scorecard] = []
    for session in manifest:
        journal_text, source_text, verse_count = replay_session(
            sandbox, session, profile, repo
        )
        if not journal_text:
            continue
        card = evaluate(
            journal_text, source_text, verse_count,
            weights=weights, grounding_threshold=threshold,
        )
        scorecards.append(card)

    if not scorecards:
        return scorecards, {"mean_composite": 0.0, "gates_pass_rate": 0.0, "n": 0}

    aggregate = {
        "mean_composite": sum(c.weighted_composite for c in scorecards) / len(scorecards),
        "gates_pass_rate": sum(1 for c in scorecards if c.all_gates_passed) / len(scorecards),
        "n": len(scorecards),
    }
    return scorecards, aggregate


def should_promote(candidate_agg: dict, active_agg: dict) -> bool:
    """Promote candidate only if gates pass rate is 1.0 AND score beats active."""
    if candidate_agg["gates_pass_rate"] < 1.0:
        return False
    if candidate_agg["n"] == 0:
        return False
    return candidate_agg["mean_composite"] > active_agg.get("mean_composite", 0.0)


def promote(sandbox: Path, profile: dict) -> None:
    """Copy candidate_profile.yaml to active_profile.yaml."""
    candidate_path = sandbox / "candidate_profile.yaml"
    active_path = sandbox / "active_profile.yaml"
    shutil.copy2(candidate_path, active_path)


def append_log(sandbox: Path, entry: dict) -> None:
    """Append to experiment_log.jsonl."""
    log_path = sandbox / "experiment_log.jsonl"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")


def run_candidate(
    sandbox: Path,
    repo: Path | None = None,
    dry_run: bool = False,
) -> dict:
    """Execute one candidate evaluation cycle. Returns the log entry."""
    sandbox = sandbox.resolve()
    start_time = time.monotonic()

    print(f"[autoresearch] sandbox: {sandbox}")
    print(f"[autoresearch] wall-clock cap: {WALL_CLOCK_CAP_SECONDS}s")

    # Load inputs
    manifest = load_manifest(sandbox)
    candidate = load_profile(sandbox / "candidate_profile.yaml")
    active = load_profile(sandbox / "active_profile.yaml") if (sandbox / "active_profile.yaml").exists() else {}

    print(f"[autoresearch] manifest: {len(manifest)} sessions")
    print(f"[autoresearch] candidate: {candidate.get('profile_id', 'unknown')}")

    # Score candidate
    scorecards, candidate_agg = score_candidate(sandbox, manifest, candidate, repo)

    elapsed = time.monotonic() - start_time
    if elapsed > WALL_CLOCK_CAP_SECONDS:
        print(f"[autoresearch] TIMEOUT after {elapsed:.1f}s — discarding candidate")
        candidate_agg["timed_out"] = True

    print(f"[autoresearch] candidate score: {candidate_agg['mean_composite']:.4f}")
    print(f"[autoresearch] gates pass rate: {candidate_agg['gates_pass_rate']:.2f}")

    # Score active for comparison
    if active:
        _, active_agg = score_candidate(sandbox, manifest, active, repo)
        print(f"[autoresearch] active score: {active_agg['mean_composite']:.4f}")
    else:
        active_agg = {"mean_composite": 0.0, "gates_pass_rate": 0.0, "n": 0}
        print("[autoresearch] no active profile — candidate is first")

    # Decide
    promoted = should_promote(candidate_agg, active_agg) and not candidate_agg.get("timed_out")

    if promoted and not dry_run:
        promote(sandbox, candidate)
        print("[autoresearch] PROMOTED candidate to active_profile.yaml")
    elif promoted:
        print("[autoresearch] [dry-run] would promote candidate")
    else:
        print("[autoresearch] DISCARDED candidate")

    # Log entry
    log_entry = {
        "timestamp": _timestamp(),
        "profile_id": candidate.get("profile_id", "unknown"),
        "track": candidate.get("track", "A"),
        "manifest_size": len(manifest),
        "scored_sessions": candidate_agg["n"],
        "candidate_score": round(candidate_agg["mean_composite"], 4),
        "candidate_gates_pass_rate": round(candidate_agg["gates_pass_rate"], 4),
        "active_score": round(active_agg.get("mean_composite", 0.0), 4),
        "promoted": promoted,
        "elapsed_seconds": round(elapsed, 1),
        "timed_out": candidate_agg.get("timed_out", False),
    }

    if not dry_run:
        append_log(sandbox, log_entry)

    # Save scorecards
    run_dir = sandbox / "runs" / _timestamp().replace(":", "")
    if not dry_run:
        run_dir.mkdir(parents=True, exist_ok=True)
        for i, card in enumerate(scorecards):
            (run_dir / f"scorecard_{i:03d}.json").write_text(card.to_json(), encoding="utf-8")
        shutil.copy2(sandbox / "candidate_profile.yaml", run_dir / "candidate_profile.yaml")

    return log_entry


def freeze_baseline(
    sandbox: Path,
    queue_path: Path,
    vault_journal_dir: Path,
    vault_bible_dir: Path,
    count: int = 14,
) -> None:
    """Freeze first N live sessions into evaluation_manifest.json and baseline/.

    Call this after the first 14 sessions have been completed.
    """
    rows = _load_jsonl(queue_path)[:count]
    baseline_dir = sandbox / "baseline"
    baseline_dir.mkdir(parents=True, exist_ok=True)

    manifest_entries: list[dict] = []
    for row in rows:
        sid = row["session_id"]
        book = row["book_code"]

        # Copy journal
        # Look for journal with any date prefix
        found_journal = False
        for jp in vault_journal_dir.glob(f"*_{sid}.md"):
            shutil.copy2(jp, baseline_dir / f"{sid}_journal.md")
            found_journal = True
            break

        # Copy source
        source = vault_bible_dir / book / f"{sid}.md"
        if source.exists():
            shutil.copy2(source, baseline_dir / f"{sid}_source.md")

        if found_journal:
            manifest_entries.append({
                "session_id": sid,
                "book_code": book,
                "verse_count": row.get("verse_count"),
                "start_anchor": row.get("start_anchor"),
                "end_anchor": row.get("end_anchor"),
            })

    (sandbox / "evaluation_manifest.json").write_text(
        json.dumps(manifest_entries, indent=2) + "\n", encoding="utf-8"
    )
    print(f"[baseline] froze {len(manifest_entries)} sessions to {sandbox}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Noah autoresearch candidate runner.")
    sub = parser.add_subparsers(dest="command")

    run_p = sub.add_parser("run", help="Run a candidate evaluation cycle")
    run_p.add_argument("--sandbox", type=Path, required=True)
    run_p.add_argument("--repo", type=Path, default=None)
    run_p.add_argument("--dry-run", action="store_true")

    freeze_p = sub.add_parser("freeze", help="Freeze baseline from live sessions")
    freeze_p.add_argument("--sandbox", type=Path, required=True)
    freeze_p.add_argument("--queue", type=Path, required=True)
    freeze_p.add_argument("--vault-journal", type=Path, required=True)
    freeze_p.add_argument("--vault-bible", type=Path, required=True)
    freeze_p.add_argument("--count", type=int, default=14)

    args = parser.parse_args()

    if args.command == "run":
        run_candidate(args.sandbox, repo=args.repo, dry_run=args.dry_run)
    elif args.command == "freeze":
        freeze_baseline(args.sandbox, args.queue, args.vault_journal, args.vault_bible, args.count)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
