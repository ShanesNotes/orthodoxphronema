# V11/V12 Activation + Phase 2-4 Bootstrap — 2026-03-10

**Author:** `ark`
**Type:** `implementation`
**Status:** `implemented`
**Scope:** validation pipeline, holdout cleanup, schema design, NT probe

## Context
- Phase 2→3 transition plan from cowork session.
- V11/V12 checks existed in `checks.py` but were never callable — `batch_validate.py` imported `run_validation` which didn't exist.
- 4 OT holdouts (JOB, PRO, SIR, PSA) needed cleanup assessment.

## Changes

### Phase 1: V11/V12 Activation
- Added `run_validation(path, strict) -> ValidationResult` to `validate_canon.py`
  - Orchestrates all 12 checks (V1-V12) from `checks.py` in one pass
  - Shared data preparation: frontmatter, anchors, chapters, verse_line_map, gaps
  - Returns structured `ValidationResult` with per-check `CheckResult` objects
- Refactored `validate_file()` to delegate to `run_validation()` internally
  - Preserves CLI output format (backward compatible)
  - Now runs V8 repetition/density, V11, V12 checks (previously missing)
- Fixed `batch_validate.py` `discover_staged_books()` — was passing `book_filter` (list) as `staging_root` (Path)
- Made `generate_sidecar()` accept `ValidationResult` or `list[str]`
- Added `valley` to `KNOWN_SPLIT_JOIN_WORDS` (live PSA split-word artifact)
- Test results: 12 pre-existing failures fixed (40→28), 0 regressions

### Phase 2: Holdout Cleanup
- Split-word fixes applied:
  - SIR: 5 fixes → V11 now PASS
  - JOB: 3 fixes → V11 now PASS
  - PSA: 685 fixes → V11 down from 847 to 3 warnings
- Holdout status (revised from plan):
  - **PRO**: All 12 checks PASS. Promotion-ready.
  - **SIR**: V7 100.4% (6 overcounts). Promotion-ready with `--allow-incomplete`.
  - **JOB**: 12 missing verses, 3 absorbed (V10). Promotion-ready with `--allow-incomplete`.
  - **PSA**: 62 missing verses (verse-2 absorption), 3 V11. Blocked (no residuals sidecar).

### Phase 3: Schema Foundation
- Created 3 new schemas: `schemas/anchor_backlinks.json`, `schemas/patristic_source_metadata.json`, `schemas/liturgical_reference.json`
- Created directory structure: `metadata/anchor_backlinks/{liturgical,patristic,study}/`
- Design memo: `memos/67_phase3_schema_design.md` (awaiting Human ratification)

### Phase 4: NT Bootstrap
- Probe request memo: `memos/68_nt_page_range_probe_request.md` (27 NT books, awaiting Human probes)

## Files / Artifacts
- `pipeline/validate/validate_canon.py` — `run_validation()` added, `validate_file()` refactored
- `pipeline/tools/batch_validate.py` — `discover_staged_books()` filter fix
- `pipeline/common/patterns.py` — `valley` added to `KNOWN_SPLIT_JOIN_WORDS`
- `schemas/anchor_backlinks.json` — NEW
- `schemas/patristic_source_metadata.json` — NEW
- `schemas/liturgical_reference.json` — NEW
- `metadata/anchor_backlinks/{liturgical,patristic,study}/` — NEW (empty)
- `staging/validated/OT/{SIR,JOB,PSA}.md` — split-word fixes applied
- `reports/{PRO,SIR,JOB,PSA}_promotion_dossier.json` — regenerated
- `reports/book_status_dashboard.json` — regenerated
- `memos/67_phase3_schema_design.md` — NEW
- `memos/68_nt_page_range_probe_request.md` — NEW

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `run_validation import` | PASS | `python3 -c "from pipeline.validate.validate_canon import run_validation"` |
| `batch_validate all 49 books` | PASS | V11/V12 columns populated for all books |
| `pytest tests/test_validate.py` | 20/20 PASS | All validation tests green |
| `pytest tests/` | 291 pass, 28 fail | 12 pre-existing failures fixed, 28 remain (test_verse_split, test_promote_gate — pre-existing) |
| `PRO dry-run` | PASS | All 12 checks pass |
| `SIR dry-run` | PASS | V7 WARN only (100.4%) |
| `JOB dry-run` | PASS | V4/V7/V10 WARN only |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| Files changed | done | See list above |
| Verification run | done | batch_validate + pytest |
| Artifacts refreshed | done | dossiers + dashboard regenerated |
| Remaining known drift | present | PSA needs residuals sidecar + verse-2 recovery; 28 pre-existing test failures |
| Next owner | human | Ratify promotions (PRO/SIR/JOB), schema design, NT probes |

## Requested Next Action
1. **Human:** Ratify PRO/SIR/JOB promotion (Ezra audit waiver or explicit approval)
2. **Human:** Ratify Phase 3 schema design (memo 67)
3. **Human:** Begin NT page range probes (memo 68, start with Gospels)
4. **Photius:** PSA verse-2 recovery (systematic absorption pattern needs targeted pdftotext extraction)

## Handoff
**To:** `human`
**Ask:** Approve PRO/SIR/JOB promotion. Review schema design. Begin NT probes when ready.
