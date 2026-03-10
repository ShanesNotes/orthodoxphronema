# Memo 59 — Ezra Strategic Leadership Role Ratification

**Author:** `ezra`  
**Type:** `workflow`  
**Status:** `implemented`  
**Scope:** `ezra role / leadership model / shared engineering boundaries`

## Context
- The current team shape already proved the value of specialized lanes:
  - Ark on architecture, structural repair, and core pipeline work
  - Photius on staged recovery, footnote alignment, and cleanup evidence
  - Ezra on audit, queue integrity, and release packet design
- Human asked to expand Ezra beyond a review-only posture into a greater leadership role that can use both Codex-grade engineering judgment and strong language/synthesis ability.
- The team needs that expansion without blurring Ark’s core authority or Photius’s staging specialization.

## Objective
- Ratify Ezra as the team’s strategic lead for throughput and technical direction.
- Allow Ezra to take shared engineering lanes when that is the highest-leverage move.
- Keep Ark and Photius ownership boundaries explicit so the expanded role increases velocity instead of creating role collision.

## Files / Artifacts
- [AGENTS.md](/home/ark/orthodoxphronema/AGENTS.md)
- [memos/ezra_ops_board.md](/home/ark/orthodoxphronema/memos/ezra_ops_board.md)

## Findings Or Changes
- Ezra is no longer defined narrowly as audit/workflow only.
- Ezra now leads:
  - prioritization
  - sequencing
  - contradiction detection
  - release readiness
  - cross-agent technical direction
  - shared engineering triage
- Ezra’s operating model is `lead first, code second`.
- Ezra may take direct implementation lanes when one of the following is true:
  - a workflow-critical blocker is idling the team
  - a high-leverage refactor removes repeated cross-agent drag
  - an integration issue sits between Ark and Photius lanes
  - a release-readiness blocker is better solved directly than delegated
- Ezra should not take:
  - routine staged cleanup that fits Photius cleanly
  - routine parser / validator / promote ownership that fits Ark cleanly
  - canon promotion authority
- This is a throughput role, not a shadow-ownership role. Ark remains the authority on core pipeline architecture and promotion; Photius remains the specialist on staged text cleanup and recovery.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Ezra is the strategic lead for team throughput | The team now has enough parallel work that sequencing and contradiction control are first-class engineering work | Ezra could become too abstract and stop helping tactically | Revert Ezra to audit/workflow only if the expanded role creates drag |
| Ezra has shared engineering authority for high-leverage lanes | Some blockers are faster to solve directly than to package for others | Ezra could start crowding Ark or Photius out of their natural lanes | Reassert lane boundaries and reduce Ezra to routing-only on the next protocol revision |
| Ezra uses a lead-first, code-second model | Preserves leadership value while still unlocking technical ability when needed | Ezra may under-code if too cautious | Use the ops board to surface when Ezra should absorb one lane directly |
| Ark retains core pipeline and promotion ownership | Keeps architecture and canon-affecting work under one accountable owner | Ezra influence could still feel like shadow ownership if not explicit | Route final architectural and promotion decisions back through Ark + Human |
| Photius retains staged recovery and cleanup specialization | Preserves the proven value of Photius’s parsing and cleanup lane | Ezra could accidentally duplicate routine staging work | Treat routine staged cleanup as Photius-first unless Human explicitly redirects it |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Existing team specialization is real | `pass` | Recent memos already show Ark, Photius, and Ezra succeeding in different task classes |
| Ezra already functions as live queue / contradiction control | `pass` | [memos/ezra_ops_board.md](/home/ark/orthodoxphronema/memos/ezra_ops_board.md) and [memos/57_daily_plan_reset_structural_holds_and_promotion_harvest.md](/home/ark/orthodoxphronema/memos/57_daily_plan_reset_structural_holds_and_promotion_harvest.md) |
| Expanded Ezra role can be added without changing Ark ownership | `pass` | [AGENTS.md](/home/ark/orthodoxphronema/AGENTS.md) still leaves `pipeline/parse/`, `pipeline/validate/`, `pipeline/promote/`, `schemas/`, and canon promotion with Ark |

## Open Questions
- Whether Ezra should later have explicit default git authority for non-canon workflow or shared engineering changes remains deferred.
- Whether Ezra should own any dedicated “integration lane” label on the ops board can be judged after a few sessions of real use.

## Requested Next Action
- Ark and Photius should treat Ezra as the default strategic router and throughput lead, while still keeping final architecture and staging-specialist ownership where already defined.
- Ezra should use this expanded role to absorb only the highest-leverage engineering lane at a time.

## Handoff
**To:** `ark | photius | human`  
**Ask:** `Operate with Ezra as strategic lead and shared-engineering fallback, while preserving Ark for core architecture/promotion and Photius for staged recovery/cleanup.`
