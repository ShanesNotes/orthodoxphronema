# Noah Downstream Ingestion Contract — 2026-03-13

**Author:** `ezra`
**Type:** `implementation`
**Status:** `implemented`
**Scope:** `downstream agent packets / noah pilot / obsidian export contract`
**Workstream:** `future-layers`
**Phase:** `4`
**Supersedes:** `none`
**Superseded by:** `none`

## Context

Ark created `experimental/` documentation for Noah as an OpenClaw-based downstream consumer on a separate SER5 machine. That surfaced the right idea, but it was still provisional and described a whole-book + enrichment flow that no longer matches the chosen Noah model.

The official Noah direction is:
- downstream-only, read-only consumer
- pericope sessions, not whole-book meals
- scripture plus journaling prompt only in v1
- Genesis-first pilot
- Obsidian vault remains external and non-authoritative

## Contract

- `experimental/` is sandbox only. It may hold drafts, but it is not a governing surface.
- Official Noah artifacts live under `metadata/agent_ingestion/noah/`.
- The archive emits two derived Noah surfaces:
  - `session_queue.jsonl` — deterministic pericope session ordering
  - exported bundle directories — Obsidian-friendly `source.md`, `prompt.md`, and `journal.md` files
- Noah does not write back into `canon/`, `staging/`, or repo-managed metadata.

## Implementation

- Added `pipeline/metadata/build_noah_queue.py`
  - builds a Genesis-first session queue from canon + pericope headings
  - auto-generates missing pericope indexes
- Added `pipeline/metadata/export_noah_bundle.py`
  - exports one or many consecutive sessions as a delivery bundle
  - treats “daily” as a bundle label only, so multiple sessions per day are supported
- Added `tests/test_noah_ingestion.py`
  - queue order / chaining
  - bundle export structure
  - prompt/journal section contract

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | Noah generators, docs, tests, this memo |
| `Verification run` | `done` | Genesis queue build, Genesis first-bundle export, `pytest -q tests/test_noah_ingestion.py`, `pytest -q`, coordination check `PASS` |
| `Artifacts refreshed` | `done` | `metadata/agent_ingestion/noah/session_queue.jsonl`, first Genesis bundle, `reports/coordination_state.json` |
| `Remaining known drift` | `present` | `experimental/` still contains earlier whole-book draft docs, but they are now explicitly sandbox-only |
| `Next owner` | `ezra` | verify Genesis queue/bundle output and then route Noah pilot usage notes |
