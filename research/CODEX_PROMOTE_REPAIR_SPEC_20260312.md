# Codex Promote Repair Spec - 2026-03-12

**Author:** `Codex`  
**Type:** `external_repair_spec`  
**Status:** `advisory`  
**Audience:** `Ark`  
**Scope:** `pipeline/promote/promote.py` alignment with `pipeline/promote/gates.py` and `tests/test_promote_gate.py`

## Goal

Make the live promotion path in [promote.py](/home/ark/orthodoxphronema/pipeline/promote/promote.py) behaviorally match the composed gate contract in [gates.py](/home/ark/orthodoxphronema/pipeline/promote/gates.py) and restore the expected dossier schema validated by [test_promote_gate.py](/home/ark/orthodoxphronema/tests/test_promote_gate.py).

## Current Mismatch

The repo currently has two promotion models:

- a composed gate layer in [gates.py](/home/ark/orthodoxphronema/pipeline/promote/gates.py)
- an inline, simplified gate flow in [promote.py](/home/ark/orthodoxphronema/pipeline/promote/promote.py)

The tests target the richer contract. The live code currently follows the simpler one.

## Required Behavioral Changes

### 1. Make `promote.py` call the gate module instead of reimplementing it

Target behavior:
- `promote_book()` should run the gate checks in one explicit sequence using the gate helpers.

Recommended sequence:
1. validation error gate
2. editorial candidates gate
3. dossier freshness gate
4. sidecar field-normalization gate
5. V4 coverage gate
6. absorbed-content gate
7. ratification gate
8. completeness gate

Reason:
- this collapses the current contract drift instead of copying more logic into `promote.py`

### 2. Load and pass the correct support inputs for gates

`promote.py` currently loads:
- staged file
- residual sidecar
- warnings

It also needs to load:
- editorial candidates path for D1
- prior dossier path for D2
- residual taxonomy / per-entry ratification class set for D5

Concrete requirement:
- use `RESIDUAL_CLASSES` and the existing taxonomy helper path to build the `ratified_classes` set
- pass the staged body checksum into freshness
- keep `dry_run` behavior exempt from freshness blocking

### 3. Tighten ratification behavior to match taxonomy, not only `osb_*`

Current bug:
- [promote.py](/home/ark/orthodoxphronema/pipeline/promote/promote.py) only enforces per-entry ratification for classifications starting with `osb_`

Required behavior:
- per-entry ratification must follow the taxonomy in `residual_classes.json`
- non-empty residual sidecars require top-level `ratified_by: human`
- non-empty residual sidecars with missing `ratified_date` must block

Test targets:
- `TestPerEntryRatification.test_taxonomy_required_entry_ratification_blocks_non_osb_class`
- `TestHumanRatificationGate.test_ratified_by_ark_blocks`
- `TestHumanRatificationGate.test_ratified_by_null_blocks`

### 4. Restore D1-D4 blocking behavior fully

Required restored blocks:
- editorial candidates `total_candidates > 0`
- stale dossier checksum on non-dry-run promote
- residual entries using `class` instead of `classification`
- absorbed/fused content descriptions

Test targets:
- `TestEditorialCandidatesGate.test_editorial_candidates_nonzero_blocks`
- `TestDossierFreshness.test_stale_dossier_blocks_promote`
- `TestSidecarFieldNormalization.test_class_field_blocks`
- `TestAbsorbedContentGate.*`

### 5. Expand dossier generation to match the tested evidence contract

Add these top-level dossier fields:
- `allow_incomplete`
- `staged_path`
- `residuals_path`
- `editorial_candidates_path`

Keep these existing fields:
- `book_code`
- `testament`
- `timestamp`
- `registry_version`
- `body_checksum`
- `validation`
- `residuals_sidecar`
- `decision`

Recommended additions:
- serialize paths as strings
- write `None` when a sidecar path does not exist

### 6. Preserve check statuses beyond the current `PASS/WARN/FAIL` folding

Current bug:
- `generate_dossier()` infers status only from errors and warnings, so informational or skipped checks cannot survive into the dossier shape.

Required behavior:
- dossier `validation` entries must preserve richer check states, including `INFO` and `SKIP`

Practical implementation choice:
- stop deriving validation solely from message prefixes
- instead use structured validation results if available from the validator seam

If full structured validator output is not already exposed:
- add the minimal bridge needed in `promote.py` to carry per-check statuses into dossier generation without broad validator redesign

Test targets:
- `TestDossierSchema.test_dossier_preserves_warn_and_skip_statuses`
- `TestDossierSchema.test_generate_dossier_does_not_fold_v10_into_v1`

### 7. Extend dossier check coverage through `V10`

Current bug:
- `generate_dossier()` only materializes `V1` through `V9`

Required behavior:
- include `V10` in the dossier validation map
- do not let `V10` messages affect `V1`

## Recommended Edit Shape

### Inside `promote.py`

- import gate helpers from [gates.py](/home/ark/orthodoxphronema/pipeline/promote/gates.py)
- import residual-class taxonomy helper from the common layer
- isolate dossier-path and sidecar-path discovery early
- centralize dossier writing through one helper that always has:
  - `allow_incomplete`
  - staged path
  - sidecar paths
  - structured validation statuses

### Avoid

- do not duplicate gate logic from `gates.py` again
- do not broaden this lane into validator redesign beyond what dossier status preservation strictly needs

## Acceptance Criteria

Targeted:
- `pytest tests/test_promote_gate.py -q` passes

Regression:
- `pytest -q` should reduce the total suite failure count by `13`

Behavioral:
- promote dry-run still works
- non-dry-run freshness blocking works
- dossier writes still occur on all exit paths

## Sequencing

This lane should be completed before:
- parser typed-record migration
- common helper cleanup

Reason:
- it is the only active drift cluster directly touching the canon-promotion boundary
