# Memo 47 — Ezra Delivery Ops Protocol

**Author:** `ezra`
**Type:** `workflow`
**Status:** `implemented`
**Scope:** `coordination cadence / ops board / agile repo-native workflow`

## Context
- The team now has a clearer role split:
  - Ark owns architecture, core engineering, and promotion execution.
  - Photius owns staged recovery, cleanup tooling, and evidence-packaged cleanup work.
  - Ezra already owns audit and workflow review.
- The repo already has strong raw coordination artifacts:
  - `reports/book_status_dashboard.json`
  - per-book promotion dossiers
  - durable memos in `memos/`
- What is still missing is a lightweight live operating layer that keeps the team aligned without adding a second management system.

## Objective
- Formalize Ezra as the repo-native delivery ops lead.
- Keep coordination lean, per-session, and grounded in generated repo artifacts.
- Reduce memo drift, duplicate retellings, and unclear next-owner handoffs.

## Files / Artifacts
- `AGENTS.md`
- `memos/47_ezra_delivery_ops_protocol.md`
- `memos/ezra_ops_board.md`
- `reports/book_status_dashboard.json`

## Findings Or Changes
- Ezra is now formalized as the delivery ops / prioritization owner in addition to audit.
- The live operating model is:
  - dashboard = machine-readable truth
  - ops board = human-readable queue
  - memos = rationale, decisions, and substantial handoffs
- Ezra cadence is `per_session_ops_loop`, not a heavyweight daily standup model.
- Ezra's core responsibilities in this lane are:
  - normalize current state from dashboard, dossiers, and new memos
  - route the next concrete action to the correct owner
  - cap Human asks to the top 3 live decisions or ratifications
  - keep blockers visible until resolved or explicitly deferred
- Default WIP limits are now explicit:
  - Ark: 1 core engineering lane
  - Photius: 2 cleanup/recovery lanes max, or 1 batch-tool lane plus 1 book lane
  - Ezra: 1 active audit queue + 1 active ops board

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Use a lean repo-native ops layer | The repo already has good generated state; adding a second PM system would create drift | Some coordination may still live in chat unless rigor is maintained | Fall back to memos + dashboard only |
| Make `reports/book_status_dashboard.json` the live truth surface | Generated status is less error-prone than narrative recounting | Dashboard can still go stale if not refreshed | Revert to manual status review until refresh discipline is fixed |
| Add `memos/ezra_ops_board.md` as the live queue | Gives Human, Ark, and Photius one readable current queue without replacing memos | Another doc can itself drift if not maintained | Retire it if it fails to stay current |
| Run Ezra on a per-session ops loop | Matches bursty agent work better than a rigid daily ritual | Sessions may become too reactive without periodic reset | Add a weekly review later if needed |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Team contract already recognizes separate Ark / Photius / Ezra lanes | `pass` | `AGENTS.md` |
| Dashboard exists and exposes current book state for coordination | `pass` | `reports/book_status_dashboard.json` |
| Dashboard was previously identified as the best live planning surface | `pass` | `memos/29_workflow_dashboard_and_promotion_gate_followup.md` |
| Current dashboard state is rich enough to seed an ops board | `pass` | `promotion_ready: 10`, `structurally_passable: 1`, `editorially_clean: 6` in `reports/book_status_dashboard.json` |

## Open Questions
- Should Ezra add a lightweight weekly review memo later, or keep the cadence purely per-session until the team feels pain?
- Should the ops board eventually reflect NT / Phase 2 workstreams separately from OT substrate work?

## Requested Next Action
- Ark: consult `memos/ezra_ops_board.md` before selecting the next core engineering lane.
- Photius: use the ops board to pick the highest-leverage cleanup/recovery target that fits current scope.
- Human: use the ops board as the first coordination surface and memos as supporting rationale.

## Handoff
**To:** `human`  
**Ask:** `Use Memo 47 and ezra_ops_board.md as the new Ezra operating layer, and judge it by whether next-owner handoffs stay clear without adding process drag.`

## Notes
- This change is coordination-only; it does not alter canon or core pipeline semantics.
- The goal is not bureaucracy. The goal is fewer lost decisions and faster, cleaner handoffs.
