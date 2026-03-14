# Noah Minimal Runtime Runbook

> Active experimental runtime path. Sandbox-only unless later adopted by a numbered
> memo.

## Core Shape

- Repo remains the source of truth.
- Noah is a downstream consumer only.
- The runtime starts with `git pull`.
- The official Noah queue defines ordered pericope sessions.
- The local vault accumulates a mirrored `bible/` scripture seed plus prompts and
  journals.
- If autoresearch is enabled, the live runtime reads the current local
  `active_profile.yaml` but does not participate in candidate scoring itself.

No repo writeback. No canon mutation. No companion enrichment in v1.

## Official Repo Inputs

- Queue:
  - `metadata/agent_ingestion/noah/session_queue.jsonl`
- Bundle generator:
  - `pipeline/metadata/export_noah_bundle.py`
- Packet shape:
  - one `source.md`
  - one `prompt.md`
  - one `journal.md`

The queue is the authoritative ordered walk. Do not use the older chapter manifest as
the primary traversal source.

## Recommended Local Layout

```text
/path/to/runtime/
  orthodoxphronema/
  noah-vault/
    bible/
      GEN/
        GEN.P001.md
        GEN.P002.md
    prompts/
      GEN/
        GEN.P001.md
    journal/
      2026-03-14_GEN.P001.md
    themes/
    questions/
    noah_state.yaml
```

## What Gets Written To The Vault

Each session should create or refresh three local files:

1. `bible/<BOOK>/<SESSION_ID>.md`
- copy the repo-generated session source note into the vault
- keep YAML provenance intact
- this is Noah's local scripture witness
- do not annotate scripture inline

2. `prompts/<BOOK>/<SESSION_ID>.md`
- copy the repo-generated prompt note into the vault

3. `journal/YYYY-MM-DD_<SESSION_ID>.md`
- create from the repo-generated journal scaffold if missing
- this is where Noah writes

The `bible/` mirror is local-only and derivative. It should never be treated as
authoritative scripture.

## Linking Rules

- Journal entries should link to the local scripture note:
  - `[[bible/GEN/GEN.P001]]`
- Reflections that mention exact scripture anchors should use archive-native syntax:
  - `[[GEN.2:7]]`
  - `[[GEN.2:18]]`
- Do not invent a custom prefix like `[[archive:GEN.2:7]]`.

This keeps Noah's vault compatible with the archive's actual wikilink contract.

## Local State

Keep progress local to the runtime environment:

```yaml
agent: Noah
queue_version: noah-queue-v1
repo_root: /path/to/orthodoxphronema
vault_root: /path/to/noah-vault
runtime_profile: local_readonly_v1
local_model_identifier: example-local-model
last_completed_session: GEN.P001
next_session: GEN.P002
last_run_at: 2026-03-14T06:00:00Z
```

Do not centralize Noah progress in repo metadata yet.

If autoresearch is enabled, keep the active prompt/scoring profile in a separate local
sandbox and treat it as an input to the runtime, not as repo state.

## Minimal Runtime Responsibilities

The wrapper should do only this:

1. `git -C <repo_root> pull`
2. read `<vault_root>/noah_state.yaml`
3. open `metadata/agent_ingestion/noah/session_queue.jsonl`
4. resolve the next session id after sync
5. export or copy the corresponding session bundle into a temp/runtime location
6. copy:
   - `*_source.md` -> `vault/bible/<BOOK>/<SESSION_ID>.md`
   - `*_prompt.md` -> `vault/prompts/<BOOK>/<SESSION_ID>.md`
   - `*_journal.md` -> `vault/journal/YYYY-MM-DD_<SESSION_ID>.md` if missing
7. launch the local runner with:
   - source note path
   - prompt note path
   - journal output path
8. after completion, advance `last_completed_session` and `next_session`

That is the whole runtime.

## Minimal Invocation Pattern

On the repo side, queue and bundle generation already exist:

```bash
python3 pipeline/metadata/build_noah_queue.py --book GEN
python3 pipeline/metadata/export_noah_bundle.py \
  --book GEN \
  --start-session 1 \
  --count 1 \
  --out-dir metadata/agent_ingestion/noah/bundles
```

The runtime can either:

- call the exporter for the next session on demand, or
- directly read the already-generated queue and consume the existing output shape

Recommended: call the exporter or consume its packet shape, not the older chapter
harness.

## Autoresearch Boundary

If Karpathy-style autoresearch is enabled:

- freeze the first 14 live sessions before any optimization
- run candidate evaluation on the frozen manifest, not on future live sessions
- allow mutation only of the local prompt/scoring profile
- keep nightly promotion local to the downstream sandbox

See:

- `experimental/noah/AUTORESEARCH_SPEC.md`
- `experimental/noah/AUTORESEARCH_PROGRAM_TEMPLATE.md`
- `experimental/noah/CANDIDATE_PROFILE_TEMPLATE.yaml`

## Prompt Philosophy

The current prompt contract is intentionally simple and grounded:

- `Literal scene`
- `Patterns`
- `Tension or surprise`
- `Interior response`
- `Question / prayer`

Creative thought is allowed, but Noah should stay visibly anchored to the given text and
not import outside commentary in v1.

## Legacy Prototype Status

These remain useful as sandbox history, but are not the active path:

- `experimental/noah/harness.py`
- `experimental/noah/manifest_generator.py`
- `experimental/noah/noah_manifest.json`
- `experimental/noah/noah_system_prompt.md`
- `experimental/noah/noah.service`
- `experimental/noah/noah.timer`

Their common limitations are:

- chapter-first traversal rather than queue-driven pericope traversal
- concrete machine/service assumptions
- runner-specific behavior in the active contract

## Tomorrow Checklist

1. Clone or pull `orthodoxphronema` into the local runtime environment.
2. Confirm `metadata/agent_ingestion/noah/session_queue.jsonl` exists.
3. Create `vault/{bible,prompts,journal,themes,questions}`.
4. Create `vault/noah_state.yaml`.
5. Materialize `GEN.P001`.
6. Verify these three files exist locally:
   - `bible/GEN/GEN.P001.md`
   - `prompts/GEN/GEN.P001.md`
   - `journal/YYYY-MM-DD_GEN.P001.md`
7. Launch Noah against the prompt and source.
8. After completion, advance local state to `GEN.P002`.

## Distilled Decision

Use the simple `git pull` consumer model, but anchor it to the official pericope queue
and packet contract instead of the older chapter manifest.

That gives you:

- minimal moving parts
- official ordering
- local scripture accumulation in the vault
- clean separation between archive purity and Noah's lived reading trail
