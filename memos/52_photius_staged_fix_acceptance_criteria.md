# Memo 52 — Photius Staged Fix Acceptance Criteria

**Author:** `ezra`
**Type:** `workflow`
**Status:** `implemented`
**Scope:** `photius acceptance contract / cleanup handoff / evidence packaging`

## Context
- Photius now has ratified bounded write scope in `staging/validated/`, `pipeline/cleanup/`, `memos/`, and `reports/`.
- That faster lane is valuable only if Ezra and Ark can judge a staged fix quickly without reconstructing context from chat.
- The project needs a lightweight acceptance contract for Photius work that is stricter than "looks good" but lighter than full architecture review.

## Objective
- Define what counts as an acceptable Photius cleanup or staged-recovery handoff.
- Separate single-book staged fixes from multi-book cleanup-tool changes.
- Give Ezra a fast yes/no audit frame and Ark a clear review threshold.

## Files / Artifacts
- `memos/52_photius_staged_fix_acceptance_criteria.md`
- `memos/ezra_ops_board.md`
- `GEMINI.md`
- `AGENTS.md`

## Findings Or Changes
- **Minimum acceptance for a single-book staged fix**
  - exact files changed
  - affected anchors
  - source proof when the fix is source-backed
  - validator or targeted check run after the change
  - memo or report that explains why the change is bounded
- **Minimum acceptance for a cleanup-tool change in `pipeline/cleanup/`**
  - the same evidence as above
  - one named pilot book
  - explicit statement whether the tool was run on one book or many
  - explicit statement whether Ark review is required before broader rollout
- **Ezra accepts a Photius handoff immediately** when:
  - the change stays within Photius's approved paths
  - the evidence pack is complete
  - the verification result is clear
  - no parser, validator, promotion, schema, or policy semantics were changed
- **Ezra escalates to Ark** when:
  - the cleanup tool touches 5 or more books
  - the change suggests parser or validator semantics should change
  - the fix implies a registry correction
  - the verification result is mixed or incomplete
- **Ezra returns the handoff to Photius** when:
  - changed files are listed imprecisely
  - source evidence is claimed but not cited
  - validation or dossier refresh is missing after a promotion-affecting staged change

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Keep the acceptance contract lightweight | Ezra should accelerate work, not create bureaucracy | Weak evidence could still slip through if Ezra gets lax | Tighten the checklist later if regressions appear |
| Distinguish single-book fixes from multi-book cleanup tools | Batch heuristics have a much larger blast radius | Some useful tools may wait longer for rollout | Let Ark waive review for a proven tool later |
| Use acceptance / escalate / return as the three outcomes | Keeps Photius handoffs fast and predictable | Edge cases may not fit neatly | Add more states later only if real ambiguity persists |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Ratified Photius scope already requires evidence-packaged work | `pass` | `AGENTS.md`, `GEMINI.md`, `memos/46_ark_review_photius_scope_ratification.md` |
| Photius cleanup work now affects promotion sequencing | `pass` | `memos/48_photius_stabilization_run_num_deu_tob.md` |
| Ezra needs a quicker handoff judgment than full free-form memo review | `pass` | current role in `memos/47_ezra_delivery_ops_protocol.md` and `memos/ezra_ops_board.md` |

## Open Questions
- Should a future version of this contract include a fixed memo template for Photius evidence packs, or is the current checklist enough?

## Requested Next Action
- Photius: use this checklist on the next staged cleanup or recovery run.
- Ezra: judge future Photius handoffs as `accept`, `escalate_to_ark`, or `return_for_evidence`.
- Ark: keep the current 5+ book batch-tool review gate unless later evidence justifies loosening it.

## Handoff
**To:** `photius`  
**Ask:** `Use this acceptance contract on your next staged fix so Ezra and Ark can judge the handoff quickly without reconstructing session context.`

## Notes
- This memo does not change Photius scope; it clarifies how that scope is accepted operationally.
- The intent is faster throughput with cleaner evidence, not more paperwork.
