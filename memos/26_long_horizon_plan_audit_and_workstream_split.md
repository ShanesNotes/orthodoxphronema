# Long-Horizon Plan Audit And Workstream Split — 2026-03-08

**Author:** `ezra`
**Type:** `audit`
**Status:** `in_review`
**Scope:** `Phase 1 sequencing / workflow optimization / Ark-Ezra split`

## Context
- Human asked for review and optimization of `memos/25_long_horizon_plan.md` before assigning both agents to long-horizon work.
- Ark's plan is directionally strong, especially on CVC verification and systematic cleanup tooling.
- Current repo reality still shows a mismatch between structural progress and editorial purity in the active books (`GEN`, `EXO`, `LEV`).

## Objective
- Preserve the strength of Ark's long-horizon plan while tightening sequencing.
- Prevent the project from scaling extraction throughput before the quality workflow is mature enough to keep output clean.
- Define a clean split between Ark-owned implementation work and Ezra-owned audit/workflow work.

## Files / Artifacts
- `memos/25_long_horizon_plan.md`
- `memos/24_day11_status_and_roadmap.md`
- `memos/25_gen_purity_deadline_and_editorial_gate_tightening.md`
- `staging/validated/OT/GEN.md`
- `staging/validated/OT/EXO.md`
- `staging/validated/OT/LEV.md`

## Findings Or Changes
- The plan's big picture is good: batch CVC verification, article-fusion tooling, NT probe session, and Psalms as a dedicated complexity block are all strong calls.
- The sequence needs tightening. The current active books are not clean enough to justify moving immediately into high-throughput extraction or promotion.
- `GEN` still has visible quality blockers.
- `EXO` is structurally much healthier but not yet editorally pure.
- `LEV` is still a first-pass extraction with unreviewed residuals and heavy fused-article residue.
- Because of that, the correct order is:
- `1.` finish current-book purity and residual policy
- `2.` harden batch CVC + editorial tooling
- `3.` only then scale extraction cadence
- The single riskiest proposal in Ark's memo is **V5C: CVC auto-correction from extraction**. The registry should not self-mutate from extracted output, even above 95% completeness, without an external witness check. LEV and EXO already showed why.
- Parallel extraction is a later optimization, not a current bottleneck. The bottleneck right now is quality cleanup and reference correctness.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Insert a current-books stabilization phase before bulk extraction | Keeps quality debt from compounding across dozens of books | Slightly slower near-term throughput | Resume Ark's original timeline once GEN/EXO/LEV are clean |
| Keep batch CVC verification as top priority | Highest leverage prevention step after LEV discovery | Requires up-front time | Revert to per-book verification if batch tooling proves noisy |
| Prioritize `fix_articles.py` over parallel extraction | Editorial residue is the dominant visible defect class | Heuristics need review | Keep it advisory-only if auto-fix confidence is weak |
| Reject automatic registry CVC mutation from extracted output alone | Registry must remain witness-backed, not extraction-backed | More manual verification work | Revisit later if a separate witness-verification layer is added |
| Add an explicit editorial gate before promotion | Aligns workflow with Human's quality bar | Another gate to maintain | Keep it memo/checklist-only if not formalized in code |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Long-horizon priorities mostly sound | pass | `memos/25_long_horizon_plan.md` |
| Current active books still have editorial blockers | fail for promotion | `staging/validated/OT/GEN.md`, `staging/validated/OT/EXO.md`, `staging/validated/OT/LEV.md` |
| Current bottleneck is not extraction concurrency | pass | visible cleanup debt still dominates |
| CVC can be wrong enough to break extraction | pass | LEV correction history in `memos/23_lev_extraction_report.md` |

## Open Questions
- Should the editorial gate be implemented as a formal validator now, or remain a required audit sidecar for the next 5-10 books?
- Does Human want Pentateuch completion prioritized over proving the NT path with one short NT book after cleanup tooling lands?
- Should batch CVC verification write changes directly to the registry, or produce a report for ratified application?

## Requested Next Action
- Ark: revise the long-horizon sequence to start with a **Stabilization Sprint**:
- `A.` make `GEN` visibly pure
- `B.` make `EXO` editorally clean and resolve the V7/CVC mismatch question
- `C.` classify and clean `LEV` enough to establish a reliable first-pass standard
- `D.` finish `verify_all_cvc.py`
- `E.` finish `fix_articles.py`
- Ark: defer parallel extraction and any registry auto-correction logic until after the stabilization sprint proves the new workflow.

## Handoff
**To:** `ark`
**Ask:** Keep the long-horizon plan, but gate it with a stabilization phase and remove the risky assumption that extracted output can auto-correct registry truth.

## Notes
- Suggested Ark-owned implementation workstream:
- `1.` current-book cleanup and promotion readiness
- `2.` `verify_all_cvc.py`
- `3.` `fix_articles.py`
- `4.` safe extraction sequencing for NUM/DEU after the stabilization sprint
- Suggested Ezra-owned audit/workflow workstream:
- `1.` define the editorial-gate criteria and sidecar/report shape
- `2.` spot-check the output of `verify_all_cvc.py` against witness sources
- `3.` review residual taxonomy usage as more `osb_*` and `docling_issue` cases appear
- `4.` audit current-book readiness in order: GEN, EXO, LEV
- Recommended near-term status vocabulary:
- `structurally passable`
- `editorially clean`
- `promotion-ready`
- `long-horizon ready`
