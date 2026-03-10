# Memo 57 — Daily Plan Reset: Structural Holds and Promotion Harvest

**Author:** `ezra`  
**Type:** `workflow`  
**Status:** `implemented`  
**Scope:** `daily queue / release train / structural triage`

## Context
- [memos/48_minor_prophets_complete_and_session_status.md](/home/ark/orthodoxphronema/memos/48_minor_prophets_complete_and_session_status.md) expanded the same-day release pool with 9 promotion-ready Minor Prophets and 3 blocked books.
- [memos/54_footnote_alignment_report_1es_1ki.md](/home/ark/orthodoxphronema/memos/54_footnote_alignment_report_1es_1ki.md) changed the truth for `1ES` and `1KI`: `1ES` is footnote-aligned; `1KI` is structurally unsound.
- [memos/55_memo54_audit_and_structured_validation_followthrough.md](/home/ark/orthodoxphronema/memos/55_memo54_audit_and_structured_validation_followthrough.md) closed the Memo 54 refactor seam work, so generic validator/tool refactor is no longer the highest-value lane today.
- [memos/56_batch_a_footnote_audit_and_jos_structural_warning.md](/home/ark/orthodoxphronema/memos/56_batch_a_footnote_audit_and_jos_structural_warning.md) escalated `JOS` into the same structural-reset class as `1KI`.

## Objective
- Normalize the daily queue to current repo truth.
- Prioritize structural integrity over nominal dashboard readiness.
- Harvest low-risk promotion progress from books that are actually clean.
- Keep long-horizon work visible without letting it displace the release train.

## Files / Artifacts
- [reports/book_status_dashboard.json](/home/ark/orthodoxphronema/reports/book_status_dashboard.json)
- [reports/RUT_promotion_dossier.json](/home/ark/orthodoxphronema/reports/RUT_promotion_dossier.json)
- [reports/1ES_promotion_dossier.json](/home/ark/orthodoxphronema/reports/1ES_promotion_dossier.json)
- [reports/JOS_promotion_dossier.json](/home/ark/orthodoxphronema/reports/JOS_promotion_dossier.json)
- [reports/1KI_promotion_dossier.json](/home/ark/orthodoxphronema/reports/1KI_promotion_dossier.json)
- [memos/ezra_ops_board.md](/home/ark/orthodoxphronema/memos/ezra_ops_board.md)

## Findings Or Changes
- Live dashboard truth is `promoted: 2`, `promotion_ready: 20`, `editorially_clean: 12`, `extracting: 42`. The previous ops board snapshot was stale and undercounted ready work.
- `RUT` is the cleanest same-day candidate. Its dossier is all-pass, its dashboard status is `promotion_ready`, and Memo 56 reports footnote alignment success.
- `1ES` is functionally close behind `RUT`, but not yet a same-day promotion candidate. Its dossier is all-pass and Memo 54 reports perfect footnote alignment, but the dashboard still shows `editorially_clean` because `staged_matches_dossier` is `false`. That is queue drift, not a new structural defect.
- `JOS` must be treated as a structural hold despite `promotion_ready` status in the dashboard. Memo 56 documents chapter absorption into Chapter 20 and marker/index desync that the current validator surface does not express.
- `1KI` must also stay on structural hold. Memo 54 documents chapter-boundary corruption across Chapters 10-15, and the dashboard only reflects dossier-checksum drift rather than the deeper semantic problem.
- The Minor Prophets now form the largest harvestable promotion pool:
  - `promotion_ready`: `AMO`, `MIC`, `OBA`, `JON`, `NAH`, `ZEP`, `HAG`, `ZEC`, `MAL`
  - `editorially_clean`: `JOL`, `HAB`
  - `extracting`: `HOS`
- Memo 55 remains the default engineering baseline. There is no value in reopening broad refactor work today unless `JOS` or `1KI` structural reset exposes a shared extraction-core defect.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Ark takes `JOS` structural reset first | `JOS` is contaminating the active release train and has explicit chapter/container corruption | `1KI` remains unsolved one more cycle | Switch priority back to `1KI` if Ark proves the shared defect is easier to fix there |
| `1KI` stays queued as the next structural reset | Memo 54 already established semantic unsoundness beyond dashboard status | Queue may stay blocked if `JOS` expands | Repackage `1KI` as the first target if Ark finds clearer repair primitives there |
| Ezra packages `RUT` and `1ES` as the top release candidates | They are the cleanest books surfaced by Photius’s audit work | `1ES` could be mistaken as promotion-ready before dossier refresh | Hold `1ES` until Ark refreshes dossier/validation artifacts |
| Minor Prophets become the main promotion-harvest lane | Nine books are already `promotion_ready` with no residual blockers | Human queue could get flooded | Split into small packets and keep Human asks capped |
| Photius continues only on structurally trustworthy books | Prevents wasted cleanup on semantically broken scripture substrates | Some evidence gathering slows on `JOS` and `1KI` | Allow Photius evidence-only work on structural holds |
| Long-horizon extraction stays visible but deferred | Release-train discipline is higher leverage today | Future extraction context may cool | Reopen Wisdom / Major Prophets / NT planning after one structural reset and one promotion packet land |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Dashboard counts reconciled | `pass` | [reports/book_status_dashboard.json](/home/ark/orthodoxphronema/reports/book_status_dashboard.json) shows `2 / 20 / 12 / 42` |
| `RUT` same-day candidate | `pass` | [reports/RUT_promotion_dossier.json](/home/ark/orthodoxphronema/reports/RUT_promotion_dossier.json) is all-pass; Memo 56 marks `RUT` ready |
| `1ES` requires artifact refresh, not structural rescue | `warn` | [reports/1ES_promotion_dossier.json](/home/ark/orthodoxphronema/reports/1ES_promotion_dossier.json) is all-pass, but [reports/book_status_dashboard.json](/home/ark/orthodoxphronema/reports/book_status_dashboard.json) shows `staged_matches_dossier: false` |
| `JOS` must be held | `warn` | Memo 56 documents chapter-20 absorption and marker/index desync despite [reports/JOS_promotion_dossier.json](/home/ark/orthodoxphronema/reports/JOS_promotion_dossier.json) remaining structurally passable |
| `1KI` must be held | `warn` | Memo 54 documents chapter drift across 10-15 despite [reports/1KI_promotion_dossier.json](/home/ark/orthodoxphronema/reports/1KI_promotion_dossier.json) remaining structurally passable |
| Minor Prophets promotion pool exists now | `pass` | Memo 48 plus [reports/book_status_dashboard.json](/home/ark/orthodoxphronema/reports/book_status_dashboard.json) agree on 9 promotion-ready books and 3 blocked books |

## Open Questions
- Does Ark want `JOS` and `1KI` solved as one generalized historical-book chapter-header repair, or as two book-specific resets first?
- After `1ES` dossier refresh, does it join `RUT` in the same human-facing packet or the next one?

## Requested Next Action
- Ark: take `JOS` structural reset first and queue `1KI` next.
- Photius: continue footnote alignment on structurally sound books and provide evidence-only support for `JOS` and `1KI`.
- Ezra: package `RUT`, `1ES`, and the first Minor Prophets promotion subset into bounded review packets.
- Human: hold until Ezra presents a capped packet; do not spend decision bandwidth on `JOS` or `1KI` yet.

## Handoff
**To:** `ark | photius | human`  
**Ask:** `Use the refreshed ops board as the daily queue; treat JOS and 1KI as structural holds, RUT as the cleanest near-term candidate, and 1ES as a dossier-refresh candidate rather than a structural rescue.`
