# Memo 60 — Completion Handshake And Stale-State Clarity

**Author:** `ezra`  
**Type:** `workflow`  
**Status:** `implemented`  
**Scope:** `agent completion protocol / stale-state vocabulary / memo contract`

## Context
- Recent Ezra audits repeatedly had to use the word `stale` because repo state often changed without the corresponding memo, dossier, or dashboard refresh landing in the same completion loop.
- The problem is not just technical drift; it is completion ambiguity. A run can look finished in chat while the repo still contains old generated state.
- Human requested a tighter task-completion and agentic-communication contract for Ark and Photius.

## Objective
- Define what `done` means for substantial Ark and Photius sessions.
- Require explicit declaration of whether memo, verification, dossier, and dashboard surfaces were refreshed.
- Replace vague `stale` language with named stale surfaces and impact.

## Files / Artifacts
- [AGENTS.md](/home/ark/orthodoxphronema/AGENTS.md)
- [GEMINI.md](/home/ark/orthodoxphronema/GEMINI.md)
- [memos/_template_work_memo.md](/home/ark/orthodoxphronema/memos/_template_work_memo.md)

## Findings Or Changes
- Added a repo-level `Completion Handshake` section to [AGENTS.md](/home/ark/orthodoxphronema/AGENTS.md).
- Substantial sessions now require three surfaces to be resolved before they are truly done:
  - durable memo/report
  - verification run
  - affected generated artifacts refreshed or explicitly deferred
- Added named stale-state vocabulary:
  - `stale dossier`
  - `stale dashboard`
  - `stale memo`
- Tightened Photius’s runtime contract in [GEMINI.md](/home/ark/orthodoxphronema/GEMINI.md) so end-of-run debriefs must say whether the completion handshake was actually closed.
- Extended the memo template with a required `Completion Handshake` block so Ark, Photius, and Ezra can report the same completion surfaces in the same format.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Define `done` as state + evidence + handoff agreement | Prevents chat-level completion from outrunning repo truth | Slightly more memo discipline required | Revert to lighter memo expectations if it creates drag |
| Name stale surfaces explicitly | `stale` alone is too vague to route work correctly | More precise language may feel stricter at first | Collapse back to generic wording if the team stops finding value in the distinction |
| Require refresh or explicit defer for dossiers and dashboard | Ezra should not have to infer whether generated state was intentionally left behind | Some runs will end with declared drift instead of silent drift | Relax this only if generated-state churn becomes excessive |
| Add a standard completion block to the memo template | Keeps Ark, Photius, and Ezra reporting the same closing facts | Authors may leave low-signal placeholders at first | Trim fields later if one proves unused |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Repo contract updated | `pass` | [AGENTS.md](/home/ark/orthodoxphronema/AGENTS.md) |
| Photius runtime contract updated | `pass` | [GEMINI.md](/home/ark/orthodoxphronema/GEMINI.md) |
| Memo template updated | `pass` | [memos/_template_work_memo.md](/home/ark/orthodoxphronema/memos/_template_work_memo.md) |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `AGENTS.md`, `GEMINI.md`, `memos/_template_work_memo.md`, this memo |
| `Verification run` | `done` | manual consistency read across updated protocol docs |
| `Artifacts refreshed` | `done` | protocol docs only; no generated dossier/dashboard artifact required for this pass |
| `Remaining known drift` | `none` | no protocol-level stale surface introduced by this change |
| `Next owner` | `ark | photius | ezra` | use the new completion block and stale-state vocabulary on the next substantial run |

## Open Questions
- Whether Ark should also receive a dedicated runtime checklist like `GEMINI.md` remains open.

## Requested Next Action
- Ark and Photius should use the new completion block on their next substantial memo.
- Ezra should start classifying stale surfaces as `stale dossier`, `stale dashboard`, or `stale memo` in future audits.

## Handoff
**To:** `ark | photius | ezra`  
**Ask:** `Treat the completion handshake as part of the work itself, not as optional cleanup after the fact.`
