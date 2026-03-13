# Memo 29 — Workflow Dashboard And Promotion Gate Follow-Up

**Author:** `ezra`
**Type:** `audit`
**Status:** `active`
**Date:** `2026-03-08`
**Scope:** `workflow surfaces / promotion semantics / immediate execution order`

## Context
- Human asked Ezra to implement the previously approved stabilization/process plan.
- This pass was limited to non-canon workflow/tooling improvements, not scripture edits.
- Goal: reduce memo drift, make status visible in generated artifacts, and tighten promotion semantics around residual policy.

## What Ezra Implemented

### 1. Taxonomy-driven per-entry ratification
- Updated [`pipeline/promote/promote.py`](/home/ark/orthodoxphronema/pipeline/promote/promote.py) so per-entry ratification is driven by [`schemas/residual_classes.json`](/home/ark/orthodoxphronema/schemas/residual_classes.json), not by hardcoded `osb_*` prefix logic.
- Result:
  - promotion policy now follows the declared residual taxonomy
  - future policy-sensitive residual classes can be added without another gate rewrite

### 2. Generated book-status dashboard
- Added [`pipeline/tools/generate_book_status_dashboard.py`](/home/ark/orthodoxphronema/pipeline/tools/generate_book_status_dashboard.py).
- Generated live artifact: [`reports/book_status_dashboard.json`](/home/ark/orthodoxphronema/reports/book_status_dashboard.json)
- Dashboard fields summarize:
  - status ladder position
  - validation statuses (`V1–V9`)
  - editorial candidate counts
  - residual counts / ratification state
  - promotion dossier decision/checksum

### 3. Test coverage for the new workflow layer
- Extended [`tests/test_promote_gate.py`](/home/ark/orthodoxphronema/tests/test_promote_gate.py)
- Added [`tests/test_book_status_dashboard.py`](/home/ark/orthodoxphronema/tests/test_book_status_dashboard.py)
- Verified:
  - `python3 -m pytest tests/ -q` -> `24 passed`
  - `python3 -m py_compile pipeline/promote/promote.py pipeline/tools/generate_book_status_dashboard.py`

## Current Live State

From [`reports/book_status_dashboard.json`](/home/ark/orthodoxphronema/reports/book_status_dashboard.json):

| Book | Status | Why |
|---|---|---|
| `GEN` | `promotion_ready` | validation structurally passable, 0 editorial candidates, residuals ratified |
| `EXO` | `structurally_passable` | 14 editorial candidates remain |
| `LEV` | `structurally_passable` | 5 editorial candidates remain; residual sidecar not ratified |

This is the cleanest current planning surface in the repo. Use it instead of inferring state from multiple daily memos.

## Interpretation
- `GEN` is the only active book that currently clears the new workflow ladder into `promotion_ready`.
- `EXO` is no longer ambiguous at workflow level: it is not promotion-ready because the editorial candidate sidecar still reports unresolved truncation debt.
- `LEV` is also clearly below promotion-ready because both editorial debt and ratification debt remain.

## Recommended Next Steps For Ark

### Priority 1 — Close `GEN`
- Re-read [`reports/GEN_promotion_dossier.json`](/home/ark/orthodoxphronema/reports/GEN_promotion_dossier.json) and [`staging/validated/OT/GEN_residuals.json`](/home/ark/orthodoxphronema/staging/validated/OT/GEN_residuals.json) against the new dashboard framing.
- If no new concern appears, prepare the final `GEN` promotion run from the same staged artifact already represented in the dossier/dashboard.
- After promotion, regenerate the dashboard so `GEN` moves from `promotion_ready` to `promoted`.

### Priority 2 — Close `EXO` editorial debt before debating promotion
- Treat [`staging/validated/OT/EXO_editorial_candidates.json`](/home/ark/orthodoxphronema/staging/validated/OT/EXO_editorial_candidates.json) as the concrete queue.
- Resolve the 14 truncation candidates first.
- Only revisit the CVC / versification discussion after the visible editorial debt is closed.

### Priority 3 — Finish `LEV` stabilization
- Resolve the 5 truncation candidates in [`staging/validated/OT/LEV_editorial_candidates.json`](/home/ark/orthodoxphronema/staging/validated/OT/LEV_editorial_candidates.json).
- Then review and ratify or refine [`staging/validated/OT/LEV_residuals.json`](/home/ark/orthodoxphronema/staging/validated/OT/LEV_residuals.json).
- Do not move `LEV` into promotion discussion while it is still both editorially open and unratified.

## Process Recommendation
- Keep the dashboard as the primary live planning artifact.
- Keep memos for rationale and major decisions, but do not let memos become the only place current state is visible.
- Suggested near-term operating rule:
  - regenerate the dashboard after any validation/promote-affecting change
  - reference dashboard state in status memos instead of restating counts manually

## Suggested Next Engineering Step
- Wire dashboard generation into a standard post-validation or post-promotion step so it stays fresh automatically.
- If Ark wants a higher-confidence workflow gate next, the best next move is not another memo; it is a formal pre-promotion editorial check that fails when `BOOK_editorial_candidates.json` is non-empty.

## Handoff
**To:** `ark`
**Ask:** Use the dashboard as the live status surface, promote `GEN` only if the current staged artifact still matches the represented dossier, and keep `EXO`/`LEV` in stabilization until their editorial candidate sidecars are cleared.
