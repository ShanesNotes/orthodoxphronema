# Memo 45 — Photius Scope Expansion And Ark Review Request

**Author:** `ezra`
**Type:** `decision`
**Status:** `in_review`
**Scope:** `photius role / staging authority / ark handoff`

## Context
- Memo 44 argues that keeping Photius in a read-mostly lane creates coordination tax in staged recovery work.
- Human has now explicitly stated that Photius should not remain bound to a read-mostly role and that Photius's staging points are correct.
- Human also explicitly preserved two boundaries:
  - purity remains mandatory for pushed `canon/`
  - architecture and codebase ownership remain with Ezra and Ark

## Objective
- Record the human-directed expansion of Photius's role.
- Keep canon purity and core ownership boundaries intact.
- Ask Ark for implementation and workflow feedback on the revised handoff model.

## Files / Artifacts
- `GEMINI.md`
- `memos/42_photius_introduction_and_parsing_findings.md`
- `memos/43_photius_debrief_audit_and_normalization.md`
- `memos/44_photius_role_counter_proposal.md`
- `memos/45_photius_scope_expansion_and_ark_review_request.md`

## Findings Or Changes
- Photius is expanded beyond a read-mostly role.
- Photius now has bounded default write scope for evidence-backed staged recovery work in:
  - `staging/validated/`
  - `pipeline/cleanup/`
  - `memos/`
  - `reports/`
- Photius remains restricted from:
  - `canon/`
  - `pipeline/parse/`
  - `pipeline/validate/`
  - `pipeline/promote/`
  - `schemas/`
  - workflow policy files and git authority
- This means Photius may implement staged structural/editorial recovery and cleanup tooling, but may only propose architecture, parser, validator, registry, and promotion changes.
- The intended operating model is an evidence-packaged staged fix:
  - Photius makes the bounded staged or cleanup change
  - Photius records source evidence and verification
  - Ezra audits the result
  - Ark retains ownership of core pipeline and architecture follow-through

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Expand Photius into staged recovery and cleanup execution | Matches demonstrated value and reduces coordination tax on verified staged fixes | Scope may creep from staging into core pipeline ownership | Narrow `GEMINI.md` again and revert to memo-first operation |
| Keep canon, parser, validator, promotion, and schema ownership outside Photius | Preserves purity and single-owner control over core workflow | Some fixes will still require Ark involvement | Human can later widen scope further if needed |
| Require evidence-packaged writes for Photius changes | Keeps the faster write lane auditable | More memo/report overhead per change | Relax packaging if it becomes too heavy |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Human explicitly rejects a read-mostly Photius role | `pass` | Human instruction following Memo 44 review |
| Human preserves canon purity and Ark/Ezra ownership of architecture/codebase | `pass` | Human instruction following Memo 44 review |
| Memo 44 proposed broader staging-centered authority | `pass` | `memos/44_photius_role_counter_proposal.md` |
| Prior audit still stands on governance overclaims and residual distinctions | `pass` | `memos/43_photius_debrief_audit_and_normalization.md` |

## Open Questions
- Ark: does this bounded Photius write scope fit the current workflow without creating merge or ownership ambiguity?
- Ark: should `pipeline/cleanup/` changes from Photius require a standing review pattern before reuse on additional books?
- Ark: do you want a standard evidence packet format for staged fixes, such as source page, affected anchors, validator result, and dossier delta?
- Ark: should any part of registry correction stay proposal-only permanently, or is there a future bounded path for that too?

## Requested Next Action
- Ark: review the revised Photius scope and respond with any workflow constraints or required safeguards.
- Ezra: keep auditing Photius's staged work with findings-first promotion-oriented review.
- Human: ratify any further expansion only after Ark responds on merge, rollback, and tool-maintenance implications.

## Handoff
**To:** `ark`  
**Ask:** `Review memos 42-45 and respond with your opinion on bounded Photius write scope, evidence-packaged staged fixes, and any safeguards you want before this becomes steady-state workflow.`

## Notes
- This memo does not modify `AGENTS.md`.
- Memo 44's request for `schemas/anchor_registry.json` ownership is not adopted here.
- The expansion implemented here follows the human's staging-focused endorsement, not the full maximal scope proposed in Memo 44.
