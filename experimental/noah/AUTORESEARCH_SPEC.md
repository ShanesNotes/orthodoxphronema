# Noah Autoresearch Spec

> Experimental downstream optimization contract inspired by Karpathy's
> `autoresearch`. Sandbox-only unless later adopted by a numbered memo.

## Purpose

Operationalize a Karpathy-style optimize-measure-keep/discard loop for Noah without
touching the archive substrate or the live Noah packet contract.

This loop exists to improve Noah's local prompt/scoring profile over time while
preserving:

- immutable canon
- queue-driven pericope delivery
- `git pull` first live runtime behavior
- local `bible/` scripture mirroring

## Karpathy Pattern, Translated

Keep the original control ideas, but map them into Noah-safe surfaces:

- `program.md`: human-owned statement of goal, constraints, and active track
- `candidate_profile.yaml`: single agent-editable surface
- fixed runner: unchanged evaluation harness
- fixed budget: same evaluation manifest and same time cap for every candidate
- score gate: numeric keep/discard decision
- promotion: update only the local active profile if the candidate wins

The agent does not edit runtime code, queue generation, or repo packet logic in v1.

## Operating Model

### Live Reading Loop

- consumes the next queue session after `git pull`
- writes `bible/`, `prompts/`, and `journal/`
- uses the current local `active_profile.yaml`

### Offline Optimization Loop

- runs on a frozen evaluation manifest
- does not advance the live reading schedule
- may run nightly while Noah continues reading one session per day

## Baseline Freeze

Before optimization begins:

- collect the first `14` live Noah sessions
- freeze them into `evaluation_manifest.json`
- keep their packets and journals as the baseline replay set

The baseline set should be created from the first 14 rows of the official Noah queue
once those sessions have actually been read and journaled.

## Mutable Versus Fixed Surfaces

### Mutable In V1

- prompt text or prompt template references
- scoring weights
- scoring thresholds
- evaluator toggles inside the candidate profile

### Fixed In V1

- queue semantics
- bundle/session contract
- local `bible/` mirror pathing
- journal note pathing
- archive source paths
- runtime wrapper semantics

## Candidate Evaluation Contract

Each candidate run must:

1. read `program.md`
2. load `candidate_profile.yaml`
3. replay the frozen evaluation manifest
4. generate or rescore outputs under the candidate profile
5. compute hard-gate results
6. compute the track-appropriate score
7. append a row to `experiment_log.jsonl`
8. promote the candidate only if it beats the current active profile and passes gates

## Track Objectives

### Track A

Optimize `grounded_reflection_score`.

Hard gates:

- anchor syntax validity
- required section completeness
- no unsupported external sourcing
- grounding threshold met

Score components:

- anchor coverage
- lexical grounding
- section completeness
- bounded novelty

### Track B

Optimize `phronema_activation_score`.

Track B may begin only when ancillary graph inputs are available as validated read-only
sidecars.

It retains all Track A gates and adds:

- valid unique cross-anchor density
- ancillary-link precision
- graph usage density / wikilink density that survives downstream validation

This is where graph and wikilink usage become the experimental proxy for phronema
activation.

## Promotion Contract

Nightly promotion is automatic inside the downstream sandbox only.

A candidate becomes the next `active_profile.yaml` only if:

- hard gates pass
- the score beats the current active profile on the same manifest
- the manifest version and track match

If any of those fail, discard the candidate.

## Files To Maintain

- `program.md`
- `candidate_profile.yaml`
- `active_profile.yaml`
- `evaluation_manifest.json`
- `experiment_log.jsonl`

Recommended local sandbox layout:

```text
/path/to/noah-autoresearch/
  program.md
  candidate_profile.yaml
  active_profile.yaml
  evaluation_manifest.json
  experiment_log.jsonl
  runs/
    2026-03-14T230000Z/
      scorecard.json
      candidate_profile.yaml
      outputs/
```

## Default Budgets

- per-candidate wall-clock cap: `10 minutes`
- baseline manifest size: `14 sessions`
- one live Noah session per day remains unchanged

These defaults may be tuned later, but the keep/discard comparison must always use the
same budget on both incumbent and candidate.
