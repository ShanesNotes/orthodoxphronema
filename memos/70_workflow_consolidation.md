# Memo 70 — Workflow Consolidation

**Author:** `ezra`  
**Type:** `workflow`  
**Status:** `implemented`  
**Scope:** `project board / memo governance / research separation / Cowork PM lane`  
**Workstream:** `workflow`  
**Phase:** `2`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- The repo accumulated a dense mixed memo surface: durable numbered memos, same-day planning drafts, PM syntheses, and external/speculative artifacts were all living together.
- Recent team growth made that density worse because multiple agents were now producing memo-like outputs with different authority levels.
- The earlier consolidation direction was correct in spirit, but it still needed revision around live repo truth, board/ops-board separation, and the canonical home for non-governing artifacts.

## Objective
- Make `PROJECT_BOARD.md` the official PM surface.
- Keep `memos/ezra_ops_board.md` as the tactical dispatch surface rather than replacing it.
- Make `memos/INDEX.md` the memo-governance overlay.
- Move non-governing advisory/spec artifacts into `research/`.
- Narrow Cowork into a formal PM/research team lane without turning it into a default protocol owner.

## Files / Artifacts
- [PROJECT_BOARD.md](/home/ark/orthodoxphronema/PROJECT_BOARD.md)
- [memos/INDEX.md](/home/ark/orthodoxphronema/memos/INDEX.md)
- [AGENTS.md](/home/ark/orthodoxphronema/AGENTS.md)
- [memos/_template_work_memo.md](/home/ark/orthodoxphronema/memos/_template_work_memo.md)
- [research/](/home/ark/orthodoxphronema/research)

## Findings Or Changes
- Ratified a three-surface model:
  - `PROJECT_BOARD.md` = management view
  - `memos/ezra_ops_board.md` = tactical dispatch
  - `memos/INDEX.md` = memo-governance overlay
- Revised `PROJECT_BOARD.md` to match live repo truth:
  - OT holdouts are `PRO`, `SIR`, `JOB`, and `PSA`
  - promoted stale-dossier debt is explicit
  - `WIS` is surfaced as the highest-priority promoted cleanup lane
- Rebuilt `memos/INDEX.md` around current categories instead of leaving research/advisory docs mixed into `memos/`.
- Collapsed duplicate advisory docs into a single canonical `research/` home.
  - `memos/` now contains `108` markdown files.
  - `research/` now contains `13` markdown artifacts.
  - repo-root markdown files are reduced to the six intended control/board docs only.
- Tightened `AGENTS.md` so Cowork is a formal team agent for PM/research surfaces, but:
  - board/index maintenance is official
  - other Cowork-authored planning/research outputs remain non-governing unless ratified
  - Cowork does not own protocol authority by default
- Updated the memo template with future-facing metadata:
  - `Workstream`
  - `Phase`
  - `Supersedes`
  - `Superseded by`

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Keep both `PROJECT_BOARD.md` and `memos/ezra_ops_board.md` | They serve different audiences and cadences | Two surfaces can drift if not kept distinct | Collapse back to one board only if the relationship proves unworkable |
| Move non-governing advisory/spec docs into `research/` | Separates durable team memos from design inputs and PM syntheses | Historical links to old `memos/` paths can drift | Restore copies or retarget links if a critical reference path was missed |
| Keep Cowork as a formal team agent | Human explicitly chose a standing PM/research lane | Role creep into protocol ownership | Re-narrow Cowork to advisory-only in a later ratified memo |
| Treat board/index as official surfaces but keep Cowork outputs otherwise non-governing | Preserves useful PM structure without blurring authority | Boundary may be misunderstood | Clarify again in `AGENTS.md` if confusion persists |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `memos/` count | `pass` | `108` markdown files after consolidation |
| `research/` count | `pass` | `13` markdown files after consolidation |
| root markdown cleanup | `pass` | only `AGENTS.md`, `ARK_BRIEFING_PACKET.md`, `CLAUDE.md`, `GEMINI.md`, `PROJECT_BOARD.md`, `README.md` remain at repo root |
| board state sanity | `pass` | `PROJECT_BOARD.md` now matches live OT holdouts and stale-dossier priorities from `reports/book_status_dashboard.json` |
| governance overlay sanity | `pass` | `memos/INDEX.md` classifies current governing, operational, historical, and research artifacts without duplicate root/memo advisory copies |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `PROJECT_BOARD.md`, `memos/INDEX.md`, `AGENTS.md`, `memos/_template_work_memo.md`, this memo, and canonicalized files in `research/` |
| `Verification run` | `done` | non-mutating file counts, root markdown inventory, dashboard truth checks, duplicate-content comparison before consolidation |
| `Artifacts refreshed` | `done` | board, index, protocol docs, and research layout now align |
| `Remaining known drift` | `present` | historical memos may still contain old `memos/` path references inside narrative text; those are advisory drift, not active governance drift |
| `Next owner` | `ark | ezra | cowork | human` | use the three-surface model and the new memo placement rules going forward |

## Open Questions
- Whether older historical memos should ever be backfilled with updated links to `research/` remains optional, not required for current governance.
- Whether `V11` / `V12` become immediate promotion gates is still an open Phase 3 / closeout decision rather than part of this workflow reset.

## Requested Next Action
- Use `PROJECT_BOARD.md` as the management surface for the remaining OT closeout and Phase 3 decision queue.
- Use `memos/ezra_ops_board.md` for all session-level dispatch and handoff work.
- Route new advisory/speculative material into `research/` by default.

## Handoff
**To:** `team`  
**Ask:** `Treat the board/index/research split as live now, and stop creating standalone memos for small status updates or advisory research.`
