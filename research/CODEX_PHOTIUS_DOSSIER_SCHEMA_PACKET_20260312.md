# Codex Photius Dossier Schema Packet - 2026-03-12

**Author:** `Codex`  
**Type:** `external_delegation_packet`  
**Status:** `ready`  
**Audience:** `Photius`  
**Protocol:** non-governing external artifact under `AGENTS.md`

## Role

Operate as `Photius` under `AGENTS.md` and `GEMINI.md`.

This is a bounded evidence-packaging lane only.

## Hard Constraints

- Do not edit `canon/`
- Do not edit `pipeline/promote/`
- Do not edit `pipeline/parse/`
- Do not edit `pipeline/validate/`
- Do not edit `schemas/`
- Do not perform implementation work
- You may write only bounded evidence artifacts in `memos/` or `reports/`

## Mission

Package the exact dossier-schema delta Ark needs for the `promote.py` repair lane, without making code changes.

## Read

- [promote.py](/home/ark/orthodoxphronema/pipeline/promote/promote.py)
- [gates.py](/home/ark/orthodoxphronema/pipeline/promote/gates.py)
- [test_promote_gate.py](/home/ark/orthodoxphronema/tests/test_promote_gate.py)
- representative real dossier files in [`reports/`](/home/ark/orthodoxphronema/reports)

Recommended real dossier sample:
- `2JN_promotion_dossier.json`
- `EST_promotion_dossier.json`
- `WIS_promotion_dossier.json`
- one NT blocked dossier such as `MAT_promotion_dossier.json`

## Output

Produce one durable artifact that contains:

### 1. Dossier field matrix

For each expected dossier field, show:
- field name
- current source in `promote.py`, if any
- whether tests require it
- whether real dossiers currently include it
- recommended status: keep, add, or reshape

### 2. Validation status matrix

For `V1` through `V10`, show:
- whether current dossier generation can represent its status correctly
- whether tests expect `PASS`, `WARN`, `FAIL`, `INFO`, or `SKIP`
- any current misclassification path

### 3. Exit-path matrix

For each exit path:
- validation error block
- editorial block
- freshness block
- ratification block
- completeness block
- dry-run success
- promote success

Show whether dossier writing currently happens and whether the dossier shape is complete enough for that exit path.

## Requirements

- findings first
- exact file references
- exact test references
- exact representative dossier file references
- distinguish observed fact from inference
- no implementation changes

## Verification

Run and cite:
- `pytest tests/test_promote_gate.py -q`

## Completion Requirement

Create one durable memo or report and include:
- `Files read`
- `Verification run`
- `Artifacts refreshed`
- `Remaining known drift`
- `Next owner`

## Success Condition

Ark should be able to use your packet as the exact schema/evidence appendix for the first repair lane in `promote.py`.
