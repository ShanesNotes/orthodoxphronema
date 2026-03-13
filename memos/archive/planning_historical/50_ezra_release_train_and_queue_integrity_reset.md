# Memo 50 — Ezra Release Train And Queue Integrity Reset

**Author:** `ezra`
**Type:** `workflow`
**Status:** `implemented`
**Scope:** `release train / queue integrity / audit batching`

## Context
- Ezra's new delivery-ops lane depends on `reports/book_status_dashboard.json` as the live machine-readable source of truth.
- Since `memos/ezra_ops_board.md` was first seeded, Photius landed Memo 48 and moved `NUM`, `DEU`, and `TOB` into `promotion_ready`.
- The live queue therefore drifted from repo truth and needed a reset before Ezra could add value through sequencing and release-readiness work.

## Objective
- Reconcile the human-readable queue with the current dashboard.
- Establish a small release train for the current `promotion_ready` set.
- Turn "many ready books" into small explicit audit batches.

## Files / Artifacts
- `memos/50_ezra_release_train_and_queue_integrity_reset.md`
- `memos/ezra_ops_board.md`
- `reports/book_status_dashboard.json`

## Findings Or Changes
- Queue integrity issue found and normalized:
  - live dashboard now reports `promotion_ready: 13`
  - live dashboard now reports `editorially_clean: 4`
  - the prior ops board still showed `promotion_ready: 10` and `editorially_clean: 6`
- Ezra release train is now defined in 3 small audit batches:
  - **Batch A — cleanest near-term candidates:** `RUT`, `1ES`, `EXO`, `JOS`
  - **Batch B — historical books with resolved staging work:** `1KI`, `2KI`, `1CH`, `2CH`
  - **Batch C — dry-run but still closer to recent cleanup / resolved exceptions:** `EZR`, `JDT`, `NUM`, `DEU`, `TOB`
- Batch A was chosen because it is the lowest-friction combination for Ezra:
  - `RUT` and `1ES` have `V7 PASS`
  - `EXO` already has human-ratified residual state at the sidecar level
  - `JOS` remains dry-run and should be checked early because it has a `V7 WARN` but no live residual sidecar
- Ezra should audit one batch at a time and end each memo with:
  - `promote`
  - `hold`
  - `needs_photius_cleanup`
  - `needs_ark_decision`

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Reconcile the ops board immediately when dashboard truth changes | Ezra's coordination value collapses if the queue drifts from generated state | Frequent updates may feel operationally noisy | Reduce refresh frequency if drift becomes rare |
| Split `promotion_ready` books into 3 audit batches | Small batches are easier to review and easier for Human/Ark to act on | Some books may wait longer for audit | Rebalance the batches if one becomes blocked |
| Start with Batch A | It offers the best near-term chance of converting ready state into promote/hold decisions quickly | Another batch might contain a higher strategic priority | Reorder if Human or Ark changes release priority |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Dashboard currently reports `promotion_ready: 13` | `pass` | `reports/book_status_dashboard.json` |
| Dashboard currently reports `editorially_clean: 4` | `pass` | `reports/book_status_dashboard.json` |
| Memo 48 explains the shift of `NUM`, `DEU`, and `TOB` into `promotion_ready` | `pass` | `memos/48_photius_stabilization_run_num_deu_tob.md` |
| All 13 release-train books currently show dossier `decision: "dry-run"` | `pass` | `reports/*_promotion_dossier.json` for the Batch A-C books |

## Open Questions
- Should Ezra keep the release train strictly in this order, or should Ark/Human be allowed to jump a batch for strategic reasons?
- Should a future release train split OT substrate and deuterocanon into separate audit streams?

## Requested Next Action
- Ezra: audit Batch A first and land a findings-first memo.
- Ark: use the batch framing to avoid dispersing effort across too many near-ready books at once.
- Human: treat the release train as the default sequence unless a specific book becomes urgent.

## Handoff
**To:** `human`  
**Ask:** `Use Batch A/B/C as the current release train so audits, promotions, and cleanup requests stop competing for attention.`

## Notes
- This memo is a queue reset, not a reclassification of canon quality.
- The release train is intentionally operational, not theological or canonical in significance.
