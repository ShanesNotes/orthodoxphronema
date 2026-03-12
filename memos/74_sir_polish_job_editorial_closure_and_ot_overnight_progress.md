# Memo 74 — SIR Polish, JOB Editorial Closure, And OT Overnight Progress

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `SIR / JOB / OT closeout`
**Workstream:** `ot-closeout`  
**Phase:** `1`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- Memo 72 reset OT closeout around `PRO`, `SIR`, `JOB`, and `PSA`.
- Memo 73 packaged `PRO` and `SIR` for residual ratification, but `SIR` still had obvious visible OCR residue.
- `JOB` still had four unresolved chapter-open editorial candidates, which kept it in a text-repair lane instead of a residual-triage lane.

## Objective
- Remove the visible OCR residue blocking `SIR` from a practical promotion posture.
- Resolve `JOB`'s active editorial candidates with OSB-PDF-backed fixes.
- Refresh OT closeout state so the remaining overnight lane is residual triage and PSA recovery, not stale editorial debt.

## Files / Artifacts
- `staging/validated/OT/SIR.md`
- `staging/validated/OT/JOB.md`
- `staging/validated/OT/JOB_editorial_candidates.json`
- `pipeline/promote/promote.py`
- `tests/test_promote_gate.py`
- `reports/SIR_promotion_dossier.json`
- `reports/JOB_promotion_dossier.json`
- `reports/book_status_dashboard.json`

## Findings Or Changes
- `SIR`
  - Cleared the broad, deterministic OCR-spacing family in staged text.
  - Representative fixes included `day s -> days`, `aby ss -> abyss`, `lam p -> lamp`, `rem ov es -> removes`, `harm ony -> harmony`, `lifesty le -> lifestyle`, and similar split-word residue across the book.
  - Post-fix dry-run preview is materially cleaner and no longer opens with obvious corruption.
- `JOB`
  - Resolved all four active chapter-open editorial candidates directly in `JOB.md`:
    - `JOB.1:1` `here` -> `There`
    - `JOB.2:1` `hen` -> `Then`
    - `JOB.3:1` `fter` -> `After`
    - `JOB.12:1` `ut` -> `Then`
  - Updated `JOB_editorial_candidates.json` so no active editorial candidates remain.
  - `JOB` is now in residual-triage mode only:
    - dashboard status: `editorially_clean`
    - decision: `dry-run`
    - remaining issue surface: live `V4` / `V7` / `V10` residual tail
- Promotion/dossier seam
  - Fixed a real bug in `pipeline/promote/promote.py`: `V10` warnings were being misclassified as `V1` in generated dossiers because of naive `startswith("V1")` matching.
  - Added a focused regression in `tests/test_promote_gate.py` to prevent `V10` from folding into `V1` again.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Polish `SIR` in place rather than defer | The residue was deterministic and promotion-visible | A broad replacement sweep could overcorrect if not bounded | Revert `SIR.md` and reapply only verified substitutions |
| Mark `JOB` editorial candidates resolved and zero the active count | Dashboard and downstream gates treat `total_candidates` as the live blocker count | Historical candidate history is now carried as resolved entries, not as active count | Reconstruct count from resolved entries if a historical audit needs it |
| Fix dossier check-name matching now | It was actively misrouting `JOB` by making `V10` look like `V1` | Existing broader promote-gate tests remain out of sync with current codebase expectations | Revert the local helper if a wider dossier schema rewrite happens later |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `SIR` validator | `warn` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/SIR.md` (`V7` overcount only) |
| `SIR` dry-run | `warn` | `python3 pipeline/promote/promote.py --book SIR --dry-run --allow-incomplete` |
| `JOB` validator after editorial fixes | `warn` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/JOB.md` |
| `JOB` dry-run after editorial fixes | `warn` | `python3 pipeline/promote/promote.py --book JOB --dry-run --allow-incomplete` |
| Dashboard refresh | `pass` | `python3 pipeline/tools/generate_book_status_dashboard.py` |
| Dossier bug regression | `pass` | `pytest tests/test_promote_gate.py -q -k does_not_fold_v10_into_v1` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `staging/validated/OT/SIR.md`, `staging/validated/OT/JOB.md`, `staging/validated/OT/JOB_editorial_candidates.json`, `pipeline/promote/promote.py`, `tests/test_promote_gate.py`, memo/board surfaces |
| `Verification run` | `done` | `SIR` and `JOB` validator + dry-run, dashboard refresh, focused regression test |
| `Artifacts refreshed` | `done` | `reports/SIR_promotion_dossier.json`, `reports/JOB_promotion_dossier.json`, `reports/book_status_dashboard.json` |
| `Remaining known drift` | `present` | `PRO` / `SIR` still await human residual ratification; `JOB` still has residual V4/V7/V10 tail; `PSA` remains blocked |
| `Next owner` | `ezra / human / photius` | Ezra packages `JOB` residual triage next; Human ratifies `PRO`/`SIR`; Photius continues `PSA` recovery |

## Requested Next Action
- Human:
  - Ratify `PRO` residual posture now.
  - Ratify `SIR` residual posture now that the visible polish pass is complete.
- Ezra:
  - Build the `JOB` residual triage packet next.
- Photius:
  - Continue `PSA` verse-2/title recovery.

## Handoff
**To:** `human / ezra / photius`  
**Ask:** `Treat Packet A as PRO + SIR pending ratification. Treat JOB as residual-triage only from here. Keep PSA separate.`
