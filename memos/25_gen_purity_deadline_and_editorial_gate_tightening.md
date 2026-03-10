# GEN Purity Deadline And Editorial Gate Tightening — 2026-03-08

**Author:** `ezra`
**Type:** `audit`
**Status:** `in_review`
**Scope:** `GEN / editorial quality gate / workflow optimization`

## Context
- Human reviewed `staging/validated/OT/GEN.md` again and explicitly set the expectation that a visibly pure `GEN.md` should exist by end of day.
- Structural validation and promotion dry-runs are passing for GEN under `--allow-incomplete`, but the staged artifact is still not clean enough for that bar.
- The current workflow is strong on structural defects and weaker on final editorial/OCR residue.

## Objective
- Make it unambiguous that `GEN.md` is still blocked on visible text-quality defects.
- Push the workflow toward a first-class editorial gate so "structurally passable" does not get mistaken for "promotion-ready."
- Suggest tooling that improves speed without lowering standards.

## Files / Artifacts
- `staging/validated/OT/GEN.md`
- `pipeline/validate/validate_canon.py`
- `memos/24_day11_status_and_roadmap.md`
- `staging/validated/OT/GEN_residue_audit.json`

## Findings Or Changes
- `GEN` is not pure yet.
- Two concrete blockers remain in the staged artifact:
- `GEN.14:24` is still fused into the previous line at `staging/validated/OT/GEN.md:459`
- `GEN.49:1` is visibly truncated at `staging/validated/OT/GEN.md:1818`
- This means the current readiness language in `memos/24_day11_status_and_roadmap.md` is too optimistic for a purity-standard promotion decision.
- The deeper workflow issue is that structural checks (`V1–V9`) are being interpreted as near-sufficient, while obvious OCR/editorial residue is still slipping through.
- The project now needs an explicit "editorial finish" layer before promotion, at least for books the team wants to call pure.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Treat `GEN` as blocked until visible OCR/editorial residue is resolved | Aligns repo status with Human's stated quality bar | Slower promotion cadence in the short term | Revert to current threshold-only model if Human later lowers the bar |
| Add an explicit editorial pre-promotion review loop | Prevents structural green lights from masking visibly bad text | Requires one more workflow step | Keep it advisory-only if it proves too heavy |
| Prioritize tooling for article/possessive fusion and truncation detection | These are the dominant time sinks now | Heuristic false positives need curation | Scope to advisory reports only |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Structural validator | pass with warnings | `python3 pipeline/validate/validate_canon.py staging/validated/OT/GEN.md` |
| Visible fused verse boundary | fail | `staging/validated/OT/GEN.md:459` |
| Visible truncation | fail | `staging/validated/OT/GEN.md:1818` |
| Existing residue sidecar still insufficient as purity gate | pass | structural status is cleaner than visible text quality |

## Open Questions
- Should editorial purity become a formal validator (`V10`) or remain a required advisory report checked before promotion?
- Does Human want zero high-confidence OCR candidates before promotion, or a small ratified residual list?
- Should the final editorial pass be book-local only, or backed by a repo-wide reusable cleanup tool?

## Requested Next Action
- Ark: do not treat `GEN` as promotion-ready yet.
- Ark: produce a visibly clean `staging/validated/OT/GEN.md` by end of day.
- Ark: fix the known blockers first:
- `GEN.14:24` line-boundary fusion
- `GEN.49:1` truncation
- Ark: after those fixes, run one bounded editorial sweep for common fused-article / fused-possessive residue and refresh the supporting sidecars.

## Handoff
**To:** `ark`
**Ask:** Restore a truly clean `GEN.md` today, then tighten the workflow so editorial purity is measured explicitly rather than inferred from structural success.

## Notes
- Suggested workflow / engineering improvements:
- `1.` Add an editorial candidate report, separate from `V1–V9`, that surfaces:
- fused article patterns like `aman`, `aburnt`, `asacrifice`
- fused possessives like `Aaron'ssons`
- suspicious truncations near chapter/poetic boundaries
- `2.` Emit that report as a durable sidecar, e.g. `BOOK_editorial_candidates.json`, with:
- line number
- anchor
- token
- rule that flagged it
- `3.` Add a pre-promotion checklist that requires:
- no known truncations
- no unresolved high-confidence fused-word defects
- structural validation recorded
- `4.` Build a dedicated cleanup utility for the dominant OCR class instead of solving it ad hoc inside each book:
- candidate idea: `pipeline/cleanup/fix_articles.py`
- keep it bounded and reviewable; do not let it rewrite free text wholesale
- `5.` Add a final "pure-book spot check" command that prints the top 25 high-confidence editorial defects so Human/Ark can confirm cleanliness quickly.
- `6.` Keep structural and editorial status separate in memos and dashboards:
- `structurally passable`
- `editorially clean`
- `promotion-ready`
