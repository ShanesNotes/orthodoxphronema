# Memo 80 — Promoted Canon Verification Audit

**Author:** `ezra`  
**Type:** `audit`  
**Status:** `in_review`  
**Scope:** `promoted canon verification`  
**Workstream:** `canon-hygiene`  
**Phase:** `1`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- Human requested a verification pass on promoted canon books with follow-through on dossiers and ops surfaces.
- The promoted OT canon set currently contains `45` books.
- The right claim boundary matters here: the repo can prove validator state, dossier freshness, and some OCR residue classes tonight, but it cannot honestly certify literal `100%` verse-by-verse source equivalence to the OSB PDF for all promoted books without a full-source audit pass.

## Objective
- Re-verify all promoted canon books against the current validator.
- Refresh promoted dossiers so the dashboard reflects current staged truth.
- Surface the books that remain non-clean in promoted canon.
- Record the difference between `fresh dossier` and `clean canon`.

## Files / Artifacts
- `canon/OT/*.md` for promoted OT books
- `reports/*_promotion_dossier.json`
- `reports/book_status_dashboard.json`
- `memos/ezra_ops_board.md`

## Findings Or Changes
### Dossier layer
- Refreshed promotion dossiers for all `45` promoted OT books via `batch_dossier.py`.
- Regenerated `reports/book_status_dashboard.json`.
- Result:
  - promoted stale dossiers before refresh: `25`
  - promoted stale dossiers after refresh: `0`

### Canon validator sweep
- Ran `run_validation()` across all `45` promoted canon books.
- Result:
  - promoted books with validator warnings or failures: `20` on the raw sweep, `19` reflected as promoted-warning books in the refreshed dashboard
  - no promoted canon book failed hard validation in a way that would demote it automatically, but many are not “clean canon”

### Highest-signal promoted canon issues
- Structural / sequence warnings still present in promoted canon:
  - `EST`: `V4`, `V7`, `V10`
  - `EZK`: `V4`, `V7`
- Completeness / versification drift warnings still present in promoted canon:
  - `GEN`, `EXO`, `NUM`, `DEU`, `JDG`, `2KI`, `1CH`, `2CH`, `EZR`, `TOB`, `JDT`, `1MA`, `3MA`, `BAR`
- Heading-density warnings still present in promoted canon:
  - `1MA`, `2MA`, `HAB`, `LJE`
- Text-purity warnings still present in promoted canon:
  - `JOS`: `V11` split-word suspect
  - `JDG`: `V11` split-word suspect

### Hand-audit residue not fully captured by validators
- Quick residue grep still surfaced visible canon issues:
  - `1MA.2:9`: `havebeen`
  - `DAN.3:37`: `havebeen`
  - `1SA` still contains a visibly corrupted merged block around `1SA.3:1` that deserves a dedicated source-backed pass
- Judgment:
  - dossier freshness is now correct
  - promoted canon is **not** yet certifiable as “100% compliant / no errors”

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Refresh all promoted dossiers now | Dashboard truth was drifting behind current staged/promoted state | Could blur canon truth with staged drift if interpreted loosely | Keep this memo explicit that freshness is not equivalence |
| Do not claim 100% source compliance | The current tooling and audit depth do not support that claim repo-wide | Human could assume canon is cleaner than it is | Run a dedicated promoted-canon source audit packet later |
| Track promoted canon cleanup as a separate lane from OT holdout promotion | These are different problems with different evidence surfaces | Without separation, backlog will thrash | Keep canon-hygiene explicitly queued on the ops board |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Promoted dossier refresh | `pass` | `python3 pipeline/tools/batch_dossier.py --book ...` |
| Dashboard regeneration | `pass` | `python3 pipeline/tools/generate_book_status_dashboard.py` |
| Promoted canon validator sweep | `warn` | `run_validation()` across all promoted canon files |
| Dossier freshness check | `warn` | `python3 pipeline/tools/check_stale_dossiers.py` |
| Canon residue grep | `warn` | `rg -n "pray er|havebeen" canon/OT/...` plus targeted scan |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | refreshed promoted dossiers, dashboard, ops board, this memo |
| `Verification run` | `done` | validator sweep, dossier refresh, dashboard regen, stale-dossier check, residue grep |
| `Artifacts refreshed` | `done` | promoted dossiers and `reports/book_status_dashboard.json` |
| `Remaining known drift` | `present` | `19` promoted books still carry validator warnings; visible residue remains in at least `1SA`, `1MA`, `DAN` |
| `Next owner` | `ezra / human / ark` | Ezra for canon-hygiene packeting, Human for prioritization, Ark only if parser/schema escalation is required |

## Requested Next Action
- Ezra:
  - build a promoted-canon cleanup packet ordered by severity:
    1. `EST`, `EZK`
    2. `JOS`, `JDG`
    3. `1SA`, `1MA`, `DAN`
- Human:
  - do not treat “fresh dossier” as “fully clean canon”
  - prioritize whether promoted-canon hygiene should come before more OT/NT frontier work

## Handoff
**To:** `human / ark / ezra`  
**Ask:** `The dossier layer is current again, but promoted canon is not yet clean enough to certify as error-free. Use this memo as the starting packet for a dedicated canon-hygiene lane instead of assuming promotion already proved source-perfect text.`
