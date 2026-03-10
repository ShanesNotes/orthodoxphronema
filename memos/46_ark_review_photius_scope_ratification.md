# Memo 46 — Ark Review: Photius Scope Ratification

**Author:** `ark`
**Type:** `decision`
**Status:** `ratified`
**Scope:** `photius role / AGENTS.md update / workflow integration`

## Context
- Memos 42-45 introduced Photius (Gemini CLI) as a parsing specialist, audited the initial session claims, proposed expanded write scope, and requested Ark's architectural review.
- Human explicitly endorsed Photius's staging-focused work and rejected the read-mostly constraint.
- Human preserved two hard boundaries: canon purity and Ark/Ezra architecture ownership.

## Objective
- Record Ark's review and approval of the bounded Photius scope.
- Document the safeguards applied.
- Confirm the AGENTS.md update.

## Findings Or Changes
- **AGENTS.md updated** — Photius added to team roster with bounded write scope.
- **Approved write paths:** `staging/validated/`, `pipeline/cleanup/`, `memos/`, `reports/`
- **Restricted paths:** `canon/`, `pipeline/parse/`, `pipeline/validate/`, `pipeline/promote/`, `schemas/`, `AGENTS.md`, policy files
- **Evidence-packaged commit requirement** — source page, affected anchors, validator before/after, rationale
- **Cleanup script review gate** — single-book fixes ship immediately; batch tools (5+ books) require Ark review
- **Registry stays proposal-only** — Photius proposes corrections with evidence, Ark applies
- **Ark role refocused** — architecture, core pipeline engineering, schema management, promotion execution

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Approve Memo 45 scope with safeguards | Demonstrated parsing value + Human directive | Scope creep from staging into core pipeline | Narrow GEMINI.md and revert to memo-first |
| Require evidence-packaged commits | Traceability for staged recovery work | Overhead per change | Relax packaging if too heavy |
| Batch cleanup review gate | Prevents regression across corpus from untested heuristics | Slower batch rollout | Remove gate if Photius track record is clean |
| Registry proposal-only | CVC errors cascade into false chapter advances and silent verse loss | Slower registry corrections | Grant bounded write if track record warrants |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Structural recoveries verified | `pass` | 1CH.16:7, 2CH.33:1-2, 2SA.17:29, 1KI.22:1 in staging |
| AGENTS.md updated with Photius section | `pass` | `AGENTS.md` lines 52-82 |
| GEMINI.md write boundaries match AGENTS.md scope | `pass` | `GEMINI.md` lines 43-68 |
| No parser/validator/promotion code changed | `pass` | Governance change only |

## Open Questions
- None. All Memo 45 questions answered in this review.

## Requested Next Action
- Ezra: continue auditing Photius staged work with findings-first review.
- Photius: begin operating under the ratified scope per GEMINI.md and AGENTS.md.
- Human: ratify this memo as the durable record of the Photius scope expansion.

## Handoff
**To:** `human`
**Ask:** `Confirm this memo as the ratified Photius scope. No further action needed from Ark on this topic.`
