# PDF Edge-Case Spot-Check Gate — 2026-03-07

**Author:** `ark`
**Type:** `workflow`
**Status:** `implemented`
**Scope:** `validation / audit workflow`

## Context
- Residual `V4` gaps in `GEN` and `EXO` are no longer all simple lowercase-opener misses.
- Source verification against the OSB PDF showed a smaller but important class of edge cases:
  - fused digit-to-opener boundaries such as `2that`
  - parenthetical or quoted openers such as `18(` or `5"`
  - separate poetic-block carryover such as `GEN.49:2`
- For small remaining gap sets, broad allowlist expansion is a blunt tool.

## Objective
- Add a low-friction PDF text-layer check for residual `V4` gaps.
- Prefer source-backed spot-checking before widening parser heuristics when the remaining gap count is small.

## Files / Artifacts
- `pipeline/validate/pdf_edge_case_check.py`
- `pipeline/validate/validate_canon.py`
- `AGENTS.md`
- `CLAUDE.md`

## Findings Or Changes
- Added a validator-side helper that:
  - reads a staged `BOOK.md`
  - computes remaining missing anchors from `V4` gaps
  - extracts the OSB PDF text layer for that book via `pdftotext -layout`
  - prints candidate source windows for each gap so an LLM or human can classify them quickly
- Added a workflow threshold:
  - when residual missing-anchor count is `<= 100`, prefer PDF spot-check review before broadening parser allowlists
- Added a validator hint so the PDF check is surfaced at the moment the staged file is evaluated.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Default PDF spot-check threshold = `100` missing anchors | Small enough for manual / LLM review, large enough to cover late-stage cleanup books | Threshold may be too high or too low for some books | Tune CLI flag and docs later |
| Keep PDF check as a separate tool, not a promotion blocker | This is an audit aid, not a deterministic truth engine | Users may skip it | Validator hint + protocol docs |
| Use OSB PDF text layer, not Brenton, for edge-case confirmation | Keeps source authority aligned with canon policy | PDF text layer still has OCR / layout artifacts | Treat output as source-backed evidence, not final rewrite logic |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Script syntax | pass | `python3 -m py_compile pipeline/validate/pdf_edge_case_check.py` |
| GEN spot-check run | pass | `python3 pipeline/validate/pdf_edge_case_check.py staging/validated/OT/GEN.md --limit 2` |
| EXO spot-check run | pass | `python3 pipeline/validate/pdf_edge_case_check.py staging/validated/OT/EXO.md --limit 2` |

## Open Questions
- Should the PDF spot-check report eventually write durable output into `reports/` by default?
- Should promotion require explicit acknowledgment when `V4` is non-zero but PDF spot-check evidence exists?

## Requested Next Action
- Ark: use the PDF edge-case checker before expanding `_LC_OPENERS` or similar heuristics on low-residual books.
- Ezra: continue using source-backed spot checks to separate true parser misses from boundary-shape failures.

## Handoff
**To:** `ark`
**Ask:** run the new PDF edge-case checker on low-residual `V4` books before widening parser heuristics.

## Notes
- This does not replace parser fixes.
- It reduces unnecessary heuristic growth when the remaining issue set is already small enough to inspect directly.
