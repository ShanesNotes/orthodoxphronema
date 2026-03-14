# Noah Phronema Ingestion Experiment

> Experimental foundation document. Sandbox-only unless later adopted by a numbered
> memo.

**Version:** 2.1  
**Date:** 2026-03-14  
**Status:** Active experimental baseline + autoresearch framework  
**Audience:** Human, Ark, Ezra, Noah runtime implementers

## Summary

This experiment exposes a local downstream agent to the Orthodox Phronema Archive one
pericope at a time and studies what scriptural synthesis emerges from repeated,
read-only encounter with the canon.

The archive remains the sole scripture authority. Noah never writes back into the
repo. The live runtime begins by syncing a local clone with `git pull`, then resolves
the next pericope from the official Noah queue, then copies that scripture session into
the agent's own Obsidian vault so the vault grows as a local seed of scripture.

This experiment now also adopts the control pattern of Karpathy's `autoresearch`:

- a human-authored goal file
- one agent-editable candidate surface
- a fixed evaluation budget
- a numeric score gate
- keep/discard candidate promotion

In Noah's adaptation, the optimize loop lives entirely downstream and may change only
the local prompt/scoring profile. It never edits canon, queue generation, packet
export, or the local scripture mirror contract.

## Non-Negotiable Invariants

1. `canon/` remains immutable: YAML frontmatter plus one verse per line with frozen
   anchors only.
2. Noah is a read-only consumer of the repo.
3. Journals, local state, metrics, and connection traces live in the downstream agent
   environment, not in repo runtime state.
4. Any future repo import of findings is manual, curated, and separately ratified.

## Research Questions

1. What scriptural connections emerge from pericope-only input with no enrichment?
2. After Phase 3 matures, does optional graph context increase scriptural saturation
   without changing the archive substrate?
3. How do we evaluate journal quality at scale without importing judge-model bias?

## Tracks

### Track A: Baseline And Grounded Optimization

- Input: one pericope session at a time from the official Noah queue
- Context: scripture plus journaling prompt only
- Output: local scripture note, local journal note, optional local connection traces
- Goal: measure native synthesis from pure scripture exposure
- Optimization target: `grounded_reflection_score`
- Rule: graph usage density is logged but is not the optimized objective in this track

### Track B: Future Graph-Aware Variant

- Input: same pericope session plus optional future backlink/graph sidecars
- Status: deferred until the Phase 3 graph contract is operationally ready
- Goal: optimize `phronema_activation_score`
- Rule: graph and wikilink density may become the proxy objective only after the same
  grounding gates still pass

## Three Operating Layers

### 1. Live Daily Reading Loop

The live runtime is intentionally small. Its first action is always repo sync.

1. Update the local repo mirror via `git pull`
2. Read local downstream state
3. Open `metadata/agent_ingestion/noah/session_queue.jsonl`
4. Resolve the next pericope session after sync
5. Materialize that session into the agent vault
6. Launch the local runner against the source note and prompt note
7. Advance only local state after completion

The runtime must not invent a second traversal manifest. The queue remains the
authoritative reading order.

### 2. Frozen Baseline Window

The first `14` sessions form the out-of-the-box baseline.

- They are read live in normal order.
- Their packet ids are frozen into an evaluation manifest after capture.
- No prompt/scoring optimization is allowed during this baseline window.
- The frozen manifest becomes the first replay set for offline autoresearch.

### 3. Offline Autoresearch Loop

After the baseline window, autoresearch runs against the frozen replay set rather than
consuming future live sessions.

- Human writes `program.md`
- Agent edits only `candidate_profile.yaml`
- Fixed runner evaluates the candidate against the frozen manifest
- Hard gates must pass first
- If score improves, the candidate becomes the next local `active_profile.yaml`
- If score does not improve, the candidate is discarded

This preserves the contemplative live cadence while still allowing nightly prompt and
scoring evolution.

## Scripture Seed In The Vault

Each session should grow the downstream Obsidian vault in three places:

- `bible/<BOOK>/<SESSION_ID>.md`
- `prompts/<BOOK>/<SESSION_ID>.md`
- `journal/YYYY-MM-DD_<SESSION_ID>.md`

The `bible/` folder is the local mirrored scripture witness. It lets the vault blossom
gradually with the same pericope source text Noah is reading while preserving repo
purity.

Rules:

- copy the session source note into `bible/`
- preserve YAML provenance fields from the packet
- do not annotate scripture inline
- use local note links such as `[[bible/GEN/GEN.P001]]`
- use archive-native anchor links such as `[[GEN.2:7]]`
- never invent a custom link prefix

## Repo-Owned Versus Environment-Owned

### Repo-Owned

- canon text
- Noah queue at `metadata/agent_ingestion/noah/session_queue.jsonl`
- per-session packet/export shape
- prompt template ids and packet metadata
- experimental documentation and schemas

### Environment-Owned

- local repo mirror / clone
- local runner and invocation method
- local vault
- local state file
- local journals
- local connection traces and evaluator outputs
- `program.md`
- `candidate_profile.yaml`
- `active_profile.yaml`
- `evaluation_manifest.json`
- `experiment_log.jsonl`

## Evaluation And Optimization

### Hard Gates

Every candidate must fail closed on:

- invalid or malformed archive anchor syntax
- missing required journal sections
- unsupported external sourcing
- grounding score below threshold

### Track A Score

`grounded_reflection_score` should combine:

- anchor validity and usable anchor coverage
- lexical grounding to the source packet
- section completeness
- bounded novelty / non-repetition

### Track B Score

`phronema_activation_score` should add:

- valid unique cross-anchor density
- ancillary-link precision
- graph and wikilink usage density that survives downstream validation

Graph usage density is therefore a later proxy for phronema activation, not a standalone
baseline metric.

### Promotion Rule

Nightly auto-promotion is allowed only inside the downstream sandbox:

- hard gates pass
- candidate score exceeds the current active profile on the frozen evaluation manifest
- promotion updates only the local `active_profile.yaml`

No repo files change as part of the nightly loop.

## Modular Runtime Vocabulary

Active experiment docs should use neutral labels:

- `runtime_profile`
- `runner_interface`
- `local_model_identifier`
- `evaluation_profile`
- `experiment_profile`

Concrete hardware, GPU, service-manager, or model examples may appear only as examples
or legacy prototypes, not as the active experiment contract.

## Minimal Local State Template

```yaml
agent: Noah
queue_version: noah-queue-v1
repo_root: /path/to/orthodoxphronema
vault_root: /path/to/noah-vault
runtime_profile: local_readonly_v1
active_profile: /path/to/noah-autoresearch/active_profile.yaml
last_completed_session: GEN.P014
next_session: GEN.P015
last_run_at: 2026-03-14T06:00:00Z
```

## Optional Local Connection Trace Template

```json
{
  "date": "YYYY-MM-DD",
  "track": "A",
  "model": "{local_model_identifier}",
  "input_session": "GEN.P001",
  "generated_anchors": [
    {
      "source_anchor": "GEN.1:1",
      "target_anchor": "JOH.1:1",
      "context_snippet": "In the beginning"
    }
  ],
  "metrics": {
    "anchor_validity_score": 1.0,
    "novelty_entropy": 0.45
  }
}
```

## Current Practical Path

For implementation and testing:

- use the official Noah queue and packet outputs
- start with pericope sessions, not chapter manifests
- start each live run with `git pull`
- mirror the source packet into `bible/`
- freeze the first 14 sessions before any optimization
- run autoresearch only on prompt/scoring profiles, never on archive interfaces

The current practical runtime runbook is:

- `experimental/noah/MINIMAL_RUNTIME_RUNBOOK.md`

The current practical autoresearch runbook is:

- `experimental/noah/AUTORESEARCH_SPEC.md`

Legacy chapter-based and machine-specific prototype files remain useful as historical
reference only. They are not the active path.
