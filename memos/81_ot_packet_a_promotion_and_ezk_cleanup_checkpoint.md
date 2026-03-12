# Memo 81 — OT Packet A Promotion And EZK Cleanup Checkpoint

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `in_review`  
**Scope:** `ot packet a promotion / ezk cleanup / queue reset`  
**Workstream:** `ot-closeout`  
**Phase:** `1`  
**Supersedes:** `memos/73_pro_sir_residual_ratification_packet.md`, `memos/79_ot_overnight_execution_pro_sir_job_nt_audit.md`  
**Superseded by:** `none`

## Context
- The OT continuation plan prioritized `PRO + SIR` as Packet A, then `JOB`, then `PSA`, with promoted-canon cleanup beginning as capacity opened.
- Direct execution revealed two important live truths:
  - `PRO` and `SIR` were ready to promote from their current staged files.
  - `JOB` had drifted away from the bounded Memo 79 shape and is not currently a ratification-only book.
- The first promoted-canon cleanup target (`EZK`) had a source-backed missing block in `41:5-12`.

## Objective
- Promote Packet A (`PRO`, `SIR`) from current staged truth.
- Refresh the live OT queue after promotion.
- Land the first promoted-canon cleanup win by repairing and re-promoting `EZK`.

## Files / Artifacts
- `canon/OT/PRO.md`
- `canon/OT/SIR.md`
- `canon/OT/EZK.md`
- `staging/validated/OT/EZK.md`
- `reports/PRO_promotion_dossier.json`
- `reports/SIR_promotion_dossier.json`
- `reports/EZK_promotion_dossier.json`
- `reports/book_status_dashboard.json`
- `memos/ezra_ops_board.md`

## Findings Or Changes
### Packet A promotion
- Promoted `PRO` from the current staged file.
  - result: `PRO` is now `promoted / promoted / FRESH`
- Promoted `SIR` from the current staged file with `--allow-incomplete`.
  - result: `SIR` is now `promoted / promoted / FRESH`
  - remaining validator posture in promoted canon: `V7` overcount only

### `JOB` queue correction
- Re-checking `JOB` during execution showed the staged file is materially worse than the bounded Memo 79 state.
- Current `JOB` validator truth:
  - `29` residual missing anchors
  - `V7` gap of `25`
  - multiple new `V10` absorbed-content hints
- Judgment:
  - `JOB` is not ready for Packet B promotion
  - `JOB` must be re-triaged as an active OT repair lane, not a ratification-only lane

### `EZK` promoted-canon cleanup
- `pdf_edge_case_check.py` confirmed that `EZK.41:5-12` exists in the OSB text layer and was missing from the staged/promoted path.
- Added `EZK.41:5-12` back into `staging/validated/OT/EZK.md`.
- Validation result after fix:
  - `V4` cleared
  - only `V7` overcount remains (`1268 / 1265`)
- Re-promoted `EZK` so canon now matches the repaired staged file.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Promote `PRO` and `SIR` now | Both books were clean enough to promote from current staged truth | Residual governance debate remains historical rather than blocking | Re-promote from later staged truth if needed |
| Remove `JOB` from the ratification-only lane | Live staged truth no longer matches Memo 79 | Continuing to treat it as Packet B would hide a real regression | Re-triage from current validator output |
| Start promoted-canon cleanup immediately with `EZK` | The omission was source-backed and repairable now | Could widen canon-hygiene scope too early | Keep packet small and evidence-backed |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `PRO` promotion | `pass` | `python3 pipeline/promote/promote.py --book PRO` |
| `SIR` promotion | `pass` | `python3 pipeline/promote/promote.py --book SIR --allow-incomplete` |
| `JOB` current state recheck | `warn` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/JOB.md` |
| `EZK` source proof | `pass` | `python3 pipeline/validate/pdf_edge_case_check.py staging/validated/OT/EZK.md` |
| `EZK` staged validation after repair | `warn` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/EZK.md` |
| `EZK` re-promotion | `pass` | `python3 pipeline/promote/promote.py --book EZK --allow-incomplete` |
| dashboard refresh | `pass` | `python3 pipeline/tools/generate_book_status_dashboard.py` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | promoted `PRO`, `SIR`, repaired/re-promoted `EZK`, refreshed reports, ops board, this memo |
| `Verification run` | `done` | promotion commands, `JOB` validator recheck, `EZK` edge-case + validator checks |
| `Artifacts refreshed` | `done` | `*_promotion_dossier.json` for `PRO`, `SIR`, `EZK`; `reports/book_status_dashboard.json` |
| `Remaining known drift` | `present` | `JOB` regressed; `PSA` remains isolated; `EST` still needs promoted-canon disposition |
| `Next owner` | `ezra / photius / ark` | Ezra for OT queue reset and `JOB` re-triage, Photius for `PSA`, Ark stays on NT |

## Requested Next Action
- Ezra:
  - reclassify `JOB` as the primary OT holdout repair lane
  - continue promoted-canon cleanup with `EST` once `JOB` is re-triaged
- Photius:
  - continue `PSA` only
- Ark:
  - stay on NT stabilization unless `JOB` exposes a true parser/schema issue

## Handoff
**To:** `human / ark / photius / ezra`  
**Ask:** `Packet A is complete. The remaining OT holdouts are now JOB and PSA. Treat JOB as an active repair book again, and treat EZK as the first completed promoted-canon cleanup win.`
