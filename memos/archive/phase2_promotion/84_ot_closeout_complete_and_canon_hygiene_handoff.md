# Memo 84 — OT Closeout Complete And Canon Hygiene Handoff

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `in_review`  
**Scope:** `ot closeout complete / job promotion / next-lane handoff`  
**Workstream:** `ot-closeout`  
**Phase:** `1`  
**Supersedes:** `memos/83_psa_promotion_and_job_narrowed_residual_checkpoint.md`  
**Superseded by:** `none`

## Context
- Memo 83 closed `PSA` and narrowed `JOB` to the chapter 23 seam plus global completeness drift.
- Further `JOB` source probes showed the chapter 23 seam was recoverable from the OSB PDF text layer.
- After that recovery, `JOB` no longer had verse-sequence gaps; the only remaining warning was a global `V7` overcount against the current registry.

## Objective
- Finish the OT canon promotion lane.
- Refresh the repo truth so OT no longer appears as an open release train.
- Hand the next Ezra lane forward to promoted-canon hygiene.

## Files / Artifacts
- `staging/validated/OT/JOB.md`
- `canon/OT/JOB.md`
- `reports/JOB_promotion_dossier.json`
- `reports/book_status_dashboard.json`
- `memos/ezra_ops_board.md`
- `PROJECT_BOARD.md`
- `memos/INDEX.md`

## Findings Or Changes
### `JOB` chapter 23 recovery
- Replaced the contaminated `JOB.23` seam with source-backed text from the OSB PDF text layer:
  - `JOB.23:4-17`
- Cleaned the immediate `JOB.24:3-11` OCR joins that had become more visible after the seam repair.

### `JOB` result
- Validator posture after the pass:
  - `V1` `PASS`
  - `V2` `PASS`
  - `V3` `PASS`
  - `V4` `PASS`
  - `V8` `PASS`
  - `V9` `PASS`
  - only `V7 WARN` remains: `1084 / 1082` verses, net overcount `2`
- Promoted `JOB` into `canon/OT/JOB.md`.
- Refreshed `reports/JOB_promotion_dossier.json`.

### OT closeout state
- All OT books are now promoted:
  - `49 / 49`
- OT no longer has a holdout lane.
- The next live Ezra OT lane is promoted-canon hygiene, not OT promotion.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Promote `JOB` with the remaining `V7` overcount | There are no remaining sequence gaps; the only live issue is versification drift against the registry | Registry/source mismatch remains to be normalized later | Re-promote from later staged truth after any registry or purity correction |
| Mark OT closeout complete | All 49 OT books now have canon artifacts and fresh dossiers | Could hide promoted-canon cleanup debt if read as “perfect canon” | Keep canon-hygiene as the next active Ezra lane |
| Move Ezra to canon hygiene next | OT promotion is done; highest leverage is now promoted-canon cleanup | NT stabilization still competes for attention | Keep Ark on NT while Ezra handles OT canon hygiene |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `JOB` staged validation after final pass | `warn` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/JOB.md` |
| `JOB` promotion | `pass` | `python3 pipeline/promote/promote.py --book JOB --allow-incomplete` |
| dashboard refresh | `pass` | `python3 pipeline/tools/generate_book_status_dashboard.py` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | final `JOB` staged repair, promoted `JOB`, refreshed dashboard/boards, this memo |
| `Verification run` | `done` | `JOB` validator + promotion, dashboard regeneration |
| `Artifacts refreshed` | `done` | `reports/JOB_promotion_dossier.json`, `reports/book_status_dashboard.json`, coordination surfaces |
| `Remaining known drift` | `present` | promoted canon still carries warning and purity debt; `JOB` still has a `V7` overcount vs registry |
| `Next owner` | `ezra / ark / human` | Ezra for OT canon hygiene, Ark for NT stabilization, Human for future canon-hygiene judgments as needed |

## Requested Next Action
- Ezra:
  - move from OT promotion to promoted-canon hygiene
  - start with the warning-heavy canon books already surfaced on the ops board
- Ark:
  - stay on NT stabilization
- Human:
  - treat OT promotion as complete; future OT asks are canon-hygiene and residual-policy decisions, not missing-book promotion

## Handoff
**To:** `human / ark / ezra`  
**Ask:** `OT promotion is complete at 49/49. The next OT lane is promoted-canon hygiene, not holdout recovery.`
