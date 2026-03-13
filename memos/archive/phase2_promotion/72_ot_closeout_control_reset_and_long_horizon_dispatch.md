# Memo 72 — OT Closeout Control Reset And Long-Horizon Dispatch

**Author:** `ezra`  
**Type:** `workflow`  
**Status:** `implemented`  
**Scope:** `ot closeout / promotion sequencing`
**Workstream:** `ot-closeout`  
**Phase:** `1`  
**Supersedes:** `71`  
**Superseded by:** `none`

## Context
- Memo 71 correctly identified the four OT holdouts, but parts of its operational picture are now stale.
- `PRO` is no longer a structural recovery problem: `PRO.31` exists, validation passes, and dry-run promotion is clean.
- `JOB` remains the only OT holdout with live editorial candidates plus validator gaps.
- `PSA` is not a generic cleanup book; its warnings are dominated by a systematic verse-2/title absorption pattern.
- `memos/ezra_ops_board.md` was still describing an older release train and could not safely drive tomorrow's work.

## Objective
- Reset OT closeout around live repo truth.
- Separate governance-closeout books from real text-repair books.
- Keep Ark on NT extraction by default while OT finish work proceeds under Ezra sequencing and Photius recovery.

## Files / Artifacts
- `reports/book_status_dashboard.json`
- `reports/PRO_promotion_dossier.json`
- `memos/71_ot_closeout_overnight_dispatch.md`
- `memos/ezra_ops_board.md`
- `PROJECT_BOARD.md`

## Findings Or Changes
- `PRO` now belongs in a ratification-first lane:
  - `validate_canon.py` passes all structural checks.
  - `promote.py --book PRO --dry-run --allow-incomplete` succeeds and writes a fresh dossier.
  - Remaining work is governance packaging of the `130` unratified residuals, not more extraction.
- `SIR` belongs in a ratification-plus-light-polish lane:
  - It is structurally clean and already dry-runs.
  - The remaining risk is visible residue and unratified residual posture, not chapter/anchor repair.
- `JOB` remains the only OT book needing real source-backed text closure:
  - `4` editorial candidates remain live.
  - Validator still reports `12` residual missing-anchor warnings and `3` absorbed-content hints.
- `PSA` is a dedicated systematic recovery lane:
  - Validator reports `61` residual missing anchors, mostly repeated `1 -> 3` and `2 -> 4` chapter-opening patterns.
  - This should be worked as verse-2/title recovery, not as broad cleanup.
- OT promotion order is now:
  1. `PRO` + `SIR`
  2. `JOB`
  3. `PSA`

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Supersede Memo 71 with this reset | Memo 71's `PRO` assumptions are stale | Team may continue routing by stale memo | Revert to dashboard + dossier truth only |
| Treat `PRO` as governance-closeout only | Structural and dry-run surfaces are already clean | Residual packet may under-explain chapter clusters | Expand packet evidence without reopening extraction |
| Keep `JOB` as the only OT text-repair priority | It is the only holdout with live editorial candidates and unresolved validator gaps | May consume more PDF verification time than expected | Defer unresolved tails to ratification packet |
| Isolate `PSA` as a long-horizon program | Its failure mode is systematic and distinct from normal cleanup | Broad recovery effort could sprawl | Keep recovery batched by repeated pattern families |
| Keep Ark on NT extraction unless OT escalates | OT can proceed without pulling Ark back into routine closeout | Canon promotion timing may wait on Ark checkpoint windows | Queue packets for the next Ark promotion window |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Dashboard OT holdout count | `pass` | `reports/book_status_dashboard.json` shows `45` promoted, `4` OT holdouts |
| `PRO` structural state | `pass` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/PRO.md` |
| `PRO` promotion readiness | `pass` | `python3 pipeline/promote/promote.py --book PRO --dry-run --allow-incomplete` |
| `JOB` current warning surface | `warn` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/JOB.md` |
| `PSA` current warning surface | `warn` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/PSA.md` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `memos/71_ot_closeout_overnight_dispatch.md`, `memos/72_ot_closeout_control_reset_and_long_horizon_dispatch.md`, `memos/ezra_ops_board.md`, `PROJECT_BOARD.md`, `memos/INDEX.md` |
| `Verification run` | `done` | Dashboard read, `PRO` dry-run, `JOB`/`PSA` validator runs |
| `Artifacts refreshed` | `done` | Memo and board surfaces updated to current OT state |
| `Remaining known drift` | `present` | `reports/book_status_dashboard.json` is current; old narrative drift remains only in historical memos |
| `Next owner` | `ezra` | Build `PRO` / `SIR` ratification packets, then close `JOB`; `photius` stays on `PSA` |

## Open Questions
- Whether `SIR` needs one more visible-text polish pass before Human sees the ratification packet.
- Whether any `JOB` editorial candidate remains ambiguous after direct PDF verification.

## Requested Next Action
- Use this memo, not Memo 71, as the OT closeout dispatch.
- Keep Ark on NT extraction unless `JOB` or `PSA` surfaces a parser/schema issue or a canon-write checkpoint is ready.

## Handoff
**To:** `ezra / photius / ark`  
**Ask:** `Ezra owns PRO/SIR/JOB closeout sequencing; Photius owns PSA systematic recovery; Ark stays on NT unless OT escalates.`
