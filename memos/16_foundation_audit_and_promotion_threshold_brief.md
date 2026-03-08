# Foundation Audit And Promotion Threshold Brief — 2026-03-08

**Author:** `ezra`
**Type:** `audit`
**Status:** `in_review`
**Scope:** `project foundation / promotion gate / workflow consolidation`

## Context
- Ark has finished the current GEN/EXO loop for now.
- `schemas/anchor_registry.json`, memo 11, memo 13, and memo 14 were updated.
- Human indicated the next decision should be the first-promotion threshold.
- The project now has enough history to step back and separate durable foundation work from local GEN/EXO repair work.

## Objective
- Audit the current project foundation, not just the latest parser pass.
- Identify blockers to a clean first promotion.
- Recommend organizational and workflow consolidations for Ark to handle in plan mode.

## Files / Artifacts
- `schemas/anchor_registry.json`
- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `reports/`
- `pipeline/validate/validate_canon.py`
- `pipeline/validate/pdf_edge_case_check.py`
- `staging/validated/OT/GEN.md`
- `staging/validated/OT/EXO.md`
- `memos/11_project_audit_todos.md`
- `memos/13_boundary_shape_parser_fix.md`
- `memos/14_exo_registry_gap_review_and_llm_spotcheck_proposal.md`
- `memos/15_page_targeted_pdf_edge_case_packets.md`

## Findings Or Changes
- High: the promotion-threshold decision is currently misframed if treated as a percentage question.
  - Project policy says one-verse-per-line is mandatory.
  - Current Exodus staging still embeds later verse numbers inside earlier verse lines:
    - `EXO.21:23` contains `24` and `25`
    - `EXO.25:3` contains `4-7`
    - `EXO.34:6` contains `7`
    - `EXO.35:5` contains `6-8`
  - These are structural failures, not merely acceptable residual completeness deltas.
  - Therefore the first-promotion threshold should be class-based, not count-based.
- High: the registry governance contract was broken during valid corrective work.
  - `schemas/anchor_registry.json` says the registry is ratified and locked, and that changes require a version bump and migration plan.
  - The GEN/EXO count corrections were applied, but the registry version and ratification metadata were not advanced.
  - This is a foundation problem because promotion decisions and validator outputs now depend on a silent policy change.
- Medium: durable validation evidence is still under-institutionalized.
  - `reports/` exists as the stated audit trail, but it is empty.
  - Current evidence lives in memos and ad hoc command reruns rather than a standardized promotion dossier.
- Medium: stable workflow knowledge is still fragmented across too many memos.
  - Core durable rules now span `AGENTS.md`, `CLAUDE.md`, memo 11, memo 12, memo 13, memo 14, and memo 15.
  - This is workable during GEN/EXO, but it is not yet a clean operating surface for scale.
- Medium: parser and registry changes are moving faster than the regression discipline.
  - There is still no automated edge-case test harness around the known GEN/EXO boundary shapes.
  - This increases the cost of every future parser or validator adjustment.
- Low: repo hygiene still reflects an active lab rather than a stabilized foundation.
  - The worktree contains many modified and untracked foundational artifacts.
  - `.claude/` local state is present but not explicitly governed by `.gitignore` or repo policy.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Promotion threshold should be class-based | Structural integrity matters more than headline percentages | Harder decision surface than a single numeric threshold | Collapse back to a numeric threshold later if invariants stabilize |
| Registry changes need explicit provenance and versioning | Prevents silent policy drift in the source of truth | Slightly more process overhead | Keep a minimal migration note if full versioning is too heavy |
| Low-residual books should use PDF/LLM packet review before heuristic growth | Reduces unnecessary parser broadening | Some cases will still require manual judgment | Resume parser heuristics only for source-confirmed misses |
| Reports should become first-class promotion evidence | Reduces dependence on terminal state and memo archaeology | Extra implementation work | Start with a small generated report, not a full dashboard |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| GEN validation | warn | `1529/1532`, `1` `V4` group, `3` `V7` gap |
| EXO validation | warn | `1161/1166`, `4` `V4` groups, `5` `V7` gap |
| GEN PDF packet | pass | `GEN.49:2` source text present in page-targeted packet |
| EXO PDF packet | mixed | `EXO.34:7` and `EXO.35:6-8` matched; `EXO.21:24-25` and `EXO.25:4-7` unresolved in text layer |
| Reports audit trail | fail | `reports/` currently empty |
| Registry governance | fail | registry text says changes require version bump / migration plan, but metadata remains unchanged |

## Recommended Promotion Threshold Frame
- Do not decide first promotion by `% complete` alone.
- Use this gate shape instead:
  - `V1/V2/V3/V5/V6/V8` must pass.
  - No unresolved confirmed source-present verse may remain embedded inside another verse line.
  - `V4` may be non-zero only for explicitly ratified numbering-policy differences or source ambiguities documented in memo/sidecar form.
  - `V7` may be non-zero only if the baseline registry/witness policy for that book is itself under explicit human ratification.
- Applying that frame today:
  - `GEN` is not promotion-ready because `GEN.49:2` is source-confirmed and still absent as a verse line.
  - `EXO` is not promotion-ready because the staged file still contains inline fused verse-number groups.

## Organizational / Workflow Improvements
- Consolidate the stable operating surface:
  - `AGENTS.md` for durable policy
  - one live project-state memo for current gates
  - immutable evidence memos for parser/audit episodes
- Add a promotion dossier pattern under `reports/`:
  - validator output
  - PDF edge-case JSON packet
  - human ratification note
  - promotion command/result
- Add a small regression harness for known edge cases:
  - parser fixtures for confirmed shapes such as `14(`, `2that`, `7preserving`, poetic-block carryover
  - validator fixtures for `V4/V7` boundary interpretation
- Add registry provenance discipline:
  - version bump or explicit provisional status on change
  - short memo or ledger entry for each count correction set
- Normalize repo hygiene:
  - decide whether `.claude/` is local-only and ignore it, or formalize it as tracked tooling config
  - reduce long-lived dirty state before first promotion

## Open Questions
- Does Human want registry corrections to remain provisional until a formal version bump and ratification note are added?
- Does Human want the first promotion threshold to forbid any residual source-confirmed `V4` issue, even if the total gap count is low?
- Should Ark build the regression harness before the first promotion, or immediately after the first clean promotion-ready book?

## Requested Next Action
- Ark: enter plan mode for a foundation-consolidation pass before setting the first promotion threshold.
- Human: decide whether the registry corrections should be formally ratified as version `1.0.1` or treated as provisional pending a migration note.
- Ark: return with a short plan covering
  - promotion-threshold policy
  - registry provenance fix
  - reports/dossier generation
  - edge-case regression harness

## Handoff
**To:** `ark`
**Ask:** enter plan mode and treat the next step as foundation consolidation plus promotion-gate design, not another local parser tweak.
