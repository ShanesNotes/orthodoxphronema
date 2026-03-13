# Memo 75 — JOB Residual Triage Packet

**Author:** `ezra`  
**Type:** `audit`  
**Status:** `in_review`  
**Scope:** `JOB residual triage`
**Workstream:** `ot-closeout`  
**Phase:** `1`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- Memo 74 cleared `JOB`'s chapter-open editorial blockers and moved the book into residual-triage mode.
- `JOB` now dry-runs cleanly enough for dossier generation, but it still carries:
  - `43` unratified residual sidecar entries
  - live validator warnings on `V4`, `V7`, and `V10`
- The goal here is not to guess missing text. It is to reduce tomorrow's decision surface to a bounded residual packet.

## Objective
- Group `JOB` residuals by meaningful chapter clusters.
- Distinguish between:
  - residuals that appear to be historical docling-exception provenance
  - live gap groups still visible in the validator
  - ambiguous cross-page or source-layer cases
- Recommend whether `JOB` should be ratified now or held for one more focused repair pass.

## Files / Artifacts
- `staging/validated/OT/JOB.md`
- `staging/validated/OT/JOB_residuals.json`
- `reports/JOB_promotion_dossier.json`
- `reports/book_status_dashboard.json`

## Findings Or Changes
- Current `JOB` state after editorial closure:
  - dashboard status: `editorially_clean`
  - decision: `dry-run`
  - validator warnings: `V4`, `V7`, and `V10` only
- Residual sidecar shape:
  - total residuals: `43`
  - all are currently `docling_issue`
  - all remain unratified
- Heaviest residual clusters:
  - ch.23 = `9`
  - ch.15 = `6`
  - ch.18 = `3`
  - ch.17 / ch.19 / ch.24 / ch.36 / ch.39 = `2` or fewer each
- Live validator gap groups are smaller than the residual sidecar:
  - `17:2`
  - `18:2`
  - `19:4`
  - `23:7-9`
  - `23:13-15`
  - `24:2`
  - `36:30`
  - `39:1`
- Source-proof notes:
  - `JOB.24:24` family is definitely present in the PDF text layer (`his innards are full of stiff fat` search hit).
  - `JOB.17:2`, `JOB.18:2`, `JOB.19:4`, and `JOB.36:30` were not found by `pdf_edge_case_check.py` in the PDF text layer.
  - `JOB.23:13-15` and `JOB.24:2` produced noisy page-pair context rather than clean direct confirmation.
- Judgment:
  - `JOB` is no longer blocked by editorial cleanup.
  - The remaining problem is a bounded residual/risk question, but the live `V4` / `V10` tail is still concrete enough that I do **not** recommend immediate promotion tonight.
  - Best next step is one more focused recovery pass on the seven live gap groups, then a ratification ask if the tail remains.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Keep `JOB` out of Packet A | `PRO` and `SIR` are already cleaner governance-closeout books | Delays OT completion by one packet | Recombine later if `JOB` tail collapses quickly |
| Treat `JOB` as a bounded residual-recovery pass, not a broad parser lane | Only seven live gap groups remain | A too-broad cleanup pass could introduce new drift | Restrict work to the current validator gap groups |
| Do not ratify `JOB` tonight | Evidence is mixed on multiple live gaps | Human could ratify an avoidable impurity | Revisit after one more focused PDF-backed pass |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `JOB` validator after editorial fixes | `warn` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/JOB.md` |
| `JOB` dry-run after editorial fixes | `warn` | `python3 pipeline/promote/promote.py --book JOB --dry-run --allow-incomplete` |
| Residual cluster extraction | `pass` | `python3` chapter-count summary over `JOB_residuals.json` |
| PDF edge-case spot-check | `warn` | `python3 pipeline/validate/pdf_edge_case_check.py staging/validated/OT/JOB.md` |
| `JOB.24` text presence | `pass` | `python3 pipeline/tools/pdf_verify.py --book JOB --pages 1993-1995 --search "his innards are full of stiff fat"` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `memos/75_job_residual_triage_packet.md`, board/index surfaces |
| `Verification run` | `done` | validator, dry-run, edge-case check, and representative PDF search |
| `Artifacts refreshed` | `done` | `reports/JOB_promotion_dossier.json`, `reports/book_status_dashboard.json` already reflect post-fix state |
| `Remaining known drift` | `present` | `JOB` still has live `V4` / `V7` / `V10` warnings |
| `Next owner` | `ezra` | Do one more focused `JOB` recovery pass on the seven live gap groups |

## Requested Next Action
- Ezra:
  - attempt one last bounded recovery pass on `JOB.17`, `18`, `19`, `23`, `24`, `36`, and `39`
  - if the tail does not shrink materially, convert this memo into a human ratification ask

## Handoff
**To:** `ezra / human`  
**Ask:** `Do not promote JOB yet. Either reduce the seven live gap groups one more step, or bring this packet to Human as an explicit residual-risk decision.`
