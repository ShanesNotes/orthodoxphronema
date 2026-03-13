# Codex Ark Handoff Packet - 2026-03-12

**Author:** `Codex`  
**Type:** `external_handoff_packet`  
**Status:** `advisory`  
**Audience:** `Ark`  
**Protocol:** non-governing external artifact under `AGENTS.md`

## Objective

Resume core engineering tomorrow with one clean lane at a time, without spending time rediscovering the current drift picture.

## Current Truth

- OT is effectively complete at `49/49` promoted books, but OT lock still depends on the existing `EST` / `V7` governance packet.
- NT is broad but not stable: dashboard shows `27` staged NT books with `15` still `extracting`, `6` `editorially_clean`, and `6` `promotion_ready`.
- The live engineering risk is not phase ambiguity. It is contract drift in three concentrated code areas.
- Full test baseline at time of packet:
  - `pytest -q` -> `27 failed, 294 passed`
  - `pytest tests/test_promote_gate.py -q` -> `13 failed, 9 passed`
  - `pytest tests/test_verse_split.py -q` -> `8 failed, 12 passed`
  - `pytest tests/test_common.py -q` -> `6 failed, 34 passed`

## Recommended Lane Order

### Lane 1: Promotion gate repair

Why first:
- highest-risk mismatch with documented workflow
- sits on the canon-promotion boundary
- failure cluster is clean and bounded

Core surfaces:
- [promote.py](/home/ark/orthodoxphronema/pipeline/promote/promote.py)
- [gates.py](/home/ark/orthodoxphronema/pipeline/promote/gates.py)
- [test_promote_gate.py](/home/ark/orthodoxphronema/tests/test_promote_gate.py)

Known symptoms:
- live promote path does not delegate to the gate module
- unresolved editorial candidates do not block
- stale dossiers do not block
- sidecar field normalization drift is not enforced
- absorbed-content blocking is not enforced
- taxonomy-based ratification is not enforced beyond `osb_*`
- dossier schema is missing fields expected by tests

Exit condition:
- `pytest tests/test_promote_gate.py -q` is green

### Lane 2: Parser typed-record migration

Why second:
- parser work is active and important, but the seam is implementation-local
- this is best treated as one coherent migration, not ad hoc fixes

Core surfaces:
- [osb_extract.py](/home/ark/orthodoxphronema/pipeline/parse/osb_extract.py)
- [types.py](/home/ark/orthodoxphronema/pipeline/common/types.py)
- [test_verse_split.py](/home/ark/orthodoxphronema/tests/test_verse_split.py)

Known symptoms:
- `VerseRecord` exists, but `osb_extract.py` still subscripts verses like dicts
- marker traces expected by tests are richer than current parser output
- output serialization still assumes older marker payload shape

Exit condition:
- `pytest tests/test_verse_split.py -q` is green

### Lane 3: Common-layer compatibility cleanup

Why third:
- important but lower-risk than promotion and parser boundaries
- likely a compatibility and contract-clarification pass, not fresh architecture

Core surfaces:
- [registry.py](/home/ark/orthodoxphronema/pipeline/common/registry.py)
- [frontmatter.py](/home/ark/orthodoxphronema/pipeline/common/frontmatter.py)
- [text.py](/home/ark/orthodoxphronema/pipeline/common/text.py)
- [patterns.py](/home/ark/orthodoxphronema/pipeline/common/patterns.py)
- [test_common.py](/home/ark/orthodoxphronema/tests/test_common.py)

Known symptoms:
- helper APIs and tests disagree on missing-book behavior, page-range shape, frontmatter helpers, staged discovery helpers, and expected word lists

Exit condition:
- `pytest tests/test_common.py -q` is green

## Evidence Already Prepared

Use these artifacts first:

- [CODEX_PROJECT_DEEP_DIVE_20260312.md](/home/ark/orthodoxphronema/research/CODEX_PROJECT_DEEP_DIVE_20260312.md)
- [CODEX_DEEP_DIVE_FINDINGS_20260312.json](/home/ark/orthodoxphronema/research/CODEX_DEEP_DIVE_FINDINGS_20260312.json)
- [CODEX_TEST_FAILURE_TAXONOMY_20260312.json](/home/ark/orthodoxphronema/research/CODEX_TEST_FAILURE_TAXONOMY_20260312.json)
- [CODEX_OPTIMIZATION_EXECUTION_PLAN_20260312.md](/home/ark/orthodoxphronema/research/CODEX_OPTIMIZATION_EXECUTION_PLAN_20260312.md)
- [CODEX_OPTIMIZATION_TASK_MATRIX_20260312.json](/home/ark/orthodoxphronema/research/CODEX_OPTIMIZATION_TASK_MATRIX_20260312.json)

Photius evidence is now available at:

- [99_structural_drift_evidence_packet.md](/home/ark/orthodoxphronema/memos/99_structural_drift_evidence_packet.md)

That packet already bundles:
- promotion-gate mismatch evidence
- parser typed-record migration evidence
- common-layer contract census

## Implementation Guidance

- Take only one core lane at a time.
- Do not combine promote, parser, and common cleanup into one mixed patch set.
- After each lane, run the targeted test cluster before any broad suite run.
- Treat the promote lane as the governing boundary repair, not just a test cleanup.

## Recommended Verification Order

1. `pytest tests/test_promote_gate.py -q`
2. `pytest tests/test_verse_split.py -q`
3. `pytest tests/test_common.py -q`
4. `pytest -q`

## What Not To Spend Time On First

- nested `AGENTS.md` rollout
- skills authoring
- MCP configuration beyond docs lookup
- broad workflow redesign
- repo cleanup unrelated to the three drift clusters

Those are worth doing later, but only after code contracts stabilize.
