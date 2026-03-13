# NT Warning Reduction: EPH, MAT, HEB — 2026-03-12

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `nt staged warning reduction / heading density / local verse-boundary repair`
**Workstream:** `canon-hygiene`  
**Phase:** `4`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- After Memo `108`, the live NT warning-reduction lane had shifted away from `JOH`, `LUK`, and `REV` and back to the wider warning books named on the ops board.
- Current validator truth showed `EPH` and `HEB` were down to `V8` heading-density warnings only, while `MAT` still carried both heading-density noise and a residual overcount.

## Objective
- Reduce or eliminate the remaining warnings in `EPH`, `MAT`, and `HEB` using bounded staged-file edits only.
- Prefer exact local repairs over broad stylistic cleanup.
- Preserve companion extraction work and avoid any canon mutation or dossier churn in this lane.

## Files / Artifacts
- `staging/validated/NT/EPH.md`
- `staging/validated/NT/MAT.md`
- `staging/validated/NT/HEB.md`

## Findings Or Changes
- `EPH`
  - Collapsed over-segmented heading clusters at the opening Trinitarian section, the mid-chapter doxology boundary, the light/will section in chapter 5, and the armor-of-God section in chapter 6.
  - Result: `EPH` now passes validation cleanly with no remaining warnings.
- `HEB`
  - Removed one redundant section break in chapter 7 by merging `The Rules of the Priestly Orders` into the immediately preceding Melchizedek heading.
  - Result: `HEB` now passes validation cleanly with no remaining warnings.
- `MAT`
  - Converted sixteen pure parenthetical cross-reference stubs at chapter tails from fake verse lines into non-verse reference lines.
  - Repaired a real source-backed verse-boundary defect at the end of chapter 27 by splitting embedded `MAT.27:56` out of `MAT.27:55`, confirmed via `pdf_edge_case_check.py`.
  - Result: `MAT` now passes all structural checks; only the broad `V8` heading-density warning remains.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Remove only pure parenthetical fake verses in `MAT` | They were causing false verse overcounts without carrying scripture text | Some editorial navigation value is reduced | Reintroduce them later as non-verse metadata if needed |
| Keep `MAT` heading-density reduction bounded | The remaining `V8` warning is broad but not structurally corrupt | `MAT` still carries one warning after the lane | Revisit as a dedicated heading-curation pass if it becomes promotion-critical |
| Solve `EPH` / `HEB` through heading consolidation only | Their warning profile was already narrow and did not justify verse edits | Some editorial granularity is reduced | Restore individual headings from git if later review wants them back |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `EPH` validation | `pass` | `python3 pipeline/validate/validate_canon.py staging/validated/NT/EPH.md` |
| `HEB` validation | `pass` | `python3 pipeline/validate/validate_canon.py staging/validated/NT/HEB.md` |
| `MAT` validation | `pass_with_warnings` | `python3 pipeline/validate/validate_canon.py staging/validated/NT/MAT.md` |
| `MAT` source spot-check | `pass` | `python3 pipeline/validate/pdf_edge_case_check.py staging/validated/NT/MAT.md` confirmed `MAT.27:56` split |
| Full suite | `pass` | `pytest -q` -> `327 passed` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `EPH.md`, `MAT.md`, `HEB.md` |
| `Verification run` | `done` | targeted validator runs, `MAT` PDF edge-case spot-check, full suite |
| `Artifacts refreshed` | `deferred` | no dossier/dashboard refresh; staged warning-reduction only |
| `Remaining known drift` | `present` | `MAT` still carries one broad `V8` heading-density warning; `PSA_footnote_markers.json` remains a separate systemic blocker; dossiers for changed staged books are stale until a later refresh lane |
| `Next owner` | `ezra` | update dispatch surfaces so the NT lane no longer overstates `EPH` / `HEB` as active warning books |

## Requested Next Action
- Re-rank the NT live-warning lane around `MAT` plus any other books that still emit real structural warnings, rather than carrying `EPH` and `HEB` forward as if unchanged.

## Handoff
**To:** `ezra`  
**Ask:** `Refresh the ops/board surfaces to show that `EPH` and `HEB` are closed and `MAT` is down to one residual `V8` warning.`
