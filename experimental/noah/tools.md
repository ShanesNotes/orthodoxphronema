# Noah Tools Catalog

Tools available to the Noah runtime, organized by access layer.

---

## Archive Tools (read-only)

These are provided by the Orthodox Phronema Archive. Noah may read but never write to them.

| Tool | Purpose |
|------|---------|
| `session_queue.jsonl` | Pre-built session queue consumed one entry at a time. Each entry specifies a passage, anchor set, and optional theme constraint. |
| `export_noah_bundle.py` | Generates a self-contained bundle (scripture text + footnotes + articles) for a given session entry. Noah receives the bundle output, never calls the script directly. |
| `canon/` | Canonical scripture text (one verse per line, wikilink syntax). Source of truth for all passage reads. |
| `schemas/anchor_registry.json` | Master registry of valid anchor IDs. Used to validate that Noah's citations reference real anchors. |

## Vault Tools (local read-write)

Noah's own workspace. All persistent state lives here.

| Tool | Purpose |
|------|---------|
| `noah_state.yaml` | Session counter, current queue position, last-run timestamp. Written at session end. |
| `bible/` | Personal scripture notes, keyed by book and chapter. Noah writes here during reflection. |
| `journal/` | Dated session journals. One file per session, append-only within a session. |
| `themes/` | Theme files that accumulate cross-session observations. Noah creates and extends these over time. |
| `questions/` | Unresolved questions Noah wants to return to. Each file is a single question with context. |

## Evaluation Tools

Used by the evaluation harness, not by Noah directly.

| Tool | Purpose |
|------|---------|
| `evaluator.py` | Scores a completed session against grounding, citation, and restraint criteria. |
| `autoresearch_runner.py` | Orchestrates multi-session runs and aggregates evaluation results. |

## External Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| Python | >= 3.11 | Runtime for pipeline scripts and evaluation harness. |
| PyYAML | any | Read/write `noah_state.yaml` and candidate profiles. |
| Git | any | Version control for vault contents between sessions. |

## Open-Source Research Tools

Optional tools that extend Noah's environment for development and analysis.

| Tool | Purpose |
|------|---------|
| Obsidian | Vault management and manual inspection of Noah's output. Not used at runtime. |
| DuckDB | Optional graph queries across session journals and theme files. |
| ripgrep | Fast anchor search across canon and vault files. |
| jq | JSONL processing for session queue manipulation and evaluation output. |
