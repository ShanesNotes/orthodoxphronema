# Stabilization Sprint Execution And Tooling Audit — 2026-03-08

**Author:** `ezra`
**Type:** `audit`
**Status:** `in_review`
**Scope:** `memo 26 execution / current-book stabilization / tooling precision`

## Context
- Human asked Ezra to execute memo 26 with precision.
- Memo 26 assigned Ezra the audit/workflow side of the stabilization sprint:
- define editorial-gate direction
- spot-check `verify_all_cvc.py`
- inspect `fix_articles.py`
- reassess current-book readiness for `GEN`, `EXO`, and `LEV`

## Objective
- Turn the stabilization sprint from a planning concept into concrete implementation guidance.
- Identify which new tools are ready, which are promising but unsafe, and which books should get attention first.

## Files / Artifacts
- `pipeline/tools/verify_all_cvc.py`
- `pipeline/cleanup/fix_articles.py`
- `staging/validated/OT/GEN.md`
- `staging/validated/OT/EXO.md`
- `staging/validated/OT/LEV.md`
- `memos/25_long_horizon_plan.md`

## Findings Or Changes
- None of the active books are promotion-clean yet under the current Human quality bar.
- `GEN` still passes structural validation with warnings, but remains blocked on visible defects.
- `EXO` is structurally much stronger than before, but visible OCR/editorial residue remains and the V7 over-count still needs explanation.
- `LEV` is a successful first extraction, but not yet close to promotion quality.
- `verify_all_cvc.py` is already useful in read-only mode.
- `fix_articles.py` is promising, but current precision is uneven by book and not yet good enough for blind trust.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Use `verify_all_cvc.py` immediately in report mode | High leverage and already informative | May tempt unsafe auto-fixes | Keep `--fix` disabled in practice until spot-checked |
| Do not trust `fix_articles.py` for GEN yet | Too many false positives on names and ordinary words | Slower GEN cleanup | Re-enable later after suppression improvements |
| Use `fix_articles.py` as a high-value helper for LEV and likely EXO after refinement | It already identifies many real fused article artifacts there | False positives still require filtering | Run in report mode until confidence rises |
| Keep editorial gate advisory first, not formal `V10` yet | Faster to deploy without destabilizing validator semantics | May remain too soft if not enforced socially | Promote to formal validator later if needed |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| GEN structural validation | pass with warnings | `python3 pipeline/validate/validate_canon.py staging/validated/OT/GEN.md` |
| EXO structural validation | pass with warning | `python3 pipeline/validate/validate_canon.py staging/validated/OT/EXO.md` |
| LEV structural validation | pass with warnings | `python3 pipeline/validate/validate_canon.py staging/validated/OT/LEV.md` |
| CVC batch spot-check | useful | `python3 pipeline/tools/verify_all_cvc.py --book GEN EXO LEV NUM DEU 1SA 2SA TOB JDT 1MA 2MA JOB SIR PSA EZK 1CO EPH` |
| Article-fix audit on GEN | low precision | `python3 pipeline/cleanup/fix_articles.py staging/validated/OT/GEN.md --report` |
| Article-fix audit on EXO | medium precision | `python3 pipeline/cleanup/fix_articles.py staging/validated/OT/EXO.md --report` |
| Article-fix audit on LEV | high potential | `python3 pipeline/cleanup/fix_articles.py staging/validated/OT/LEV.md --report` |

## Open Questions
- Should `fix_articles.py` load a proper-name suppressor from the registry / book metadata / reference witness layer before wider use?
- Should the editorial gate write a dedicated sidecar, or should `fix_articles.py --report` become one section inside a broader `BOOK_editorial_candidates.json`?
- Does Human want `EXO` and `LEV` cleaned to the same visual standard as `GEN` before any further extraction begins?

## Requested Next Action
- Ark: prioritize books in this order:
- `1.` `GEN` — fix the known visible blockers and re-run a bounded editorial sweep
- `2.` `EXO` — clean visible fused-article/editorial residue and explain or correct the V7 over-count
- `3.` `LEV` — use `fix_articles.py` as a guided cleanup accelerator, then re-audit residuals
- Ark: use `verify_all_cvc.py` now in report mode only. The first useful findings are:
- `GEN` mismatch with same total but chapter redistribution (`ch32`, `ch35`)
- `NUM` mismatch with same total but chapter redistribution (`ch16`, `ch17`, `ch29`, `ch30`)
- `DEU` mismatch with total shift (`959→958`)
- Ark: do not use any auto-registry correction path until these mismatches are spot-checked against witnesses.

## Handoff
**To:** `ark`
**Ask:** Treat the new tools as asymmetric: `verify_all_cvc.py` is ready for immediate reporting use; `fix_articles.py` needs refinement but is already high-leverage for LEV and probably EXO. Use that asymmetry to drive the stabilization sprint.

## Notes
- Editorial gate recommendation:
- keep it as a durable advisory artifact first, e.g. `BOOK_editorial_candidates.json`
- minimum fields:
- `line`
- `anchor`
- `category`
- `token`
- `confidence`
- `source_hint`
- `manual_status`
- Suggested categories:
- `fused_article`
- `fused_possessive`
- `truncation`
- `boundary_fusion`
- `source_absence`
- Tool-specific observations:
- `verify_all_cvc.py`
- good: fast, readable, immediately useful
- caution: `--fix` is too broad for same-total chapter redistributions without spot-checks
- `fix_articles.py`
- good: strong hit rate on repetitive sacrificial vocabulary in LEV
- weak: too many proper-name and ordinary-word false positives in GEN
- likely next engineering improvement:
- add a reference-backed suppression layer before trusting auto-fix output broadly

