# Memo 55 — Memo 54 Audit And Structured Validation Follow-Through

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `memo 54 audit / validation contract / PDF source verification / extraction regression coverage`

## Context
- Memo 54 delivered meaningful codebase cleanup: shared modules, decomposed trackers/checks/gates, packaging, and a new `pdftotext` verifier path.
- The strongest unresolved seam was architectural, not stylistic:
  - two overlapping `pdftotext` verification paths
  - typed `CheckResult` objects introduced, but downstream consumers still reconstructed truth from raw warning strings
  - no integration tests for `ExtractionState.process_element()`
- Human explicitly called out the `pdftotext` verifier insight as the kind of simple source-backed move that should save work earlier, not after more heuristic churn.

## Objective
- Finish the refactor where it still mattered structurally.
- Preserve Ark's CLI and behavior contracts where practical.
- Tighten the repo around typed diagnostics and shared source-proof utilities instead of adding another layer of wrapper logic.

## Files / Artifacts
- `pipeline/validate/validate_canon.py`
- `pipeline/common/pdf_source.py`
- `pipeline/promote/promote.py`
- `pipeline/promote/gates.py`
- `pipeline/tools/batch_validate.py`
- `pipeline/tools/pdf_verify.py`
- `pipeline/validate/pdf_edge_case_check.py`
- `tests/test_common.py`
- `tests/test_checks.py`
- `tests/test_validate.py`
- `tests/test_promote_gate.py`
- `tests/test_verse_split.py`

## Findings Or Changes
- **Memo 54 was directionally correct, but incomplete at two seams.**
  - The new verifier in `pipeline/tools/pdf_verify.py` duplicated PDF extraction/page-estimation logic already living in `pipeline/validate/pdf_edge_case_check.py`.
  - The validation refactor stopped at the check layer; promotion and batch tooling still parsed warning strings and could not preserve `INFO` / `SKIP` states faithfully.
- **Structured validation is now end-to-end.**
  - Added a pure `run_validation()` path returning `ValidationResult`.
  - Kept `validate_file()` as the compatibility wrapper that prints and returns `(errors, warnings)`.
  - `CheckResult` now carries structured `data`, and `ValidationResult` now exposes `check()` and `status_map`.
  - V4 and V7 now carry structured diagnostics instead of forcing downstream regex parsing.
- **Promotion and batch validation now consume typed results.**
  - Promotion dossiers preserve exact check statuses, including `INFO` and `SKIP`.
  - Gate logic accepts structured checks while remaining backward-compatible with legacy list inputs.
  - Batch validation now reads statuses from `ValidationResult` instead of reconstructing them from message prefixes.
- **PDF source verification now has a shared base layer.**
  - Added `pipeline/common/pdf_source.py` for `pdftotext` / `pdftoppm` discovery, extraction, normalization, caching, and chapter page estimation.
  - Wired both verifier entrypoints through that shared layer instead of maintaining two separate implementations.
- **The extraction refactor now has actual integration coverage.**
  - Added `process_element()` tests for article entry/exit, chapter advance, column-split re-splitting, and heading emission.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Keep `validate_file()` as a compatibility wrapper | Avoids a hard API break while moving the core to typed validation | Two entrypoints can drift if one is bypassed | Make `validate_file()` a thin permanent adapter only |
| Add structured `data` to `CheckResult` | Removes string-parsing from control flow without inventing a whole second result type | Downstream code may ignore the new data initially | Legacy warnings still exist during migration |
| Preserve legacy gate inputs alongside typed ones | Keeps migration surgical and testable | Gate signatures remain more permissive than ideal for a while | Remove legacy list support after all callers are typed |
| Share PDF extraction primitives but keep both CLIs for now | Reduces duplication without forcing users into a new command today | Two CLIs can still overlap conceptually | Merge the CLIs later once one workflow clearly dominates |
| Add `process_element()` integration tests now | This is the highest-value parser regression hole exposed by Memo 54 | Crafted fixtures do not fully replace whole-book diffs | Add byte-for-byte book re-extraction diffs in a later Ark lane |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Python syntax | `pass` | `python3 -m py_compile` on modified validation, promotion, and PDF-source modules |
| Focused regression suite | `pass` | validation, promote, gate, common, dashboard, and parser-state tests all green |
| Full test suite | `pass` | `python3 -m pytest tests/ -q` → `189 passed` |
| Dossier status preservation | `pass` | `tests/test_promote_gate.py` now asserts `WARN` / `INFO` / `SKIP` statuses survive into dossier output |
| Extraction dispatch regression coverage | `pass` | `tests/test_verse_split.py` now covers `ExtractionState.process_element()` flows directly |

## Open Questions
- Ark should decide whether the repo still needs both `pdf_verify.py` and `pdf_edge_case_check.py` as separate user-facing CLIs once the shared base settles.
- A later Ark lane should still do byte-for-byte GEN/EXO/LEV re-extraction diffs if extraction-core logic changes again.

## Requested Next Action
- Ark: route all future PDF verification work through `pipeline/common/pdf_source.py`; do not grow a third verifier path.
- Ezra: use `ValidationResult` as the default review surface going forward, not raw warning strings.
- Human: no immediate action required; this was infrastructure hardening plus regression coverage.

## Handoff
**To:** `ark`  
**Ask:** `Treat Memo 54 as the first refactor pass and Memo 55 as the seam-closing pass. Keep future verifier and validation work on the typed/shared path rather than rebuilding string-driven or tool-local logic.`

## Notes
- This pass deliberately did not auto-wire `pdftotext` verification into every validation run; default validation remains fast and the source-proof lane remains explicit.
- The key architectural correction was not more abstraction. It was deleting duplicated verification logic and removing stringly-typed control flow where the refactor claimed structure already existed.
