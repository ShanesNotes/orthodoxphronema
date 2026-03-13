# Memo 38 — Stabilization Sprint Completion Report

**Date:** 2026-03-09
**From:** Ark
**Status:** Phases 1-3 COMPLETE, Phase 4 BLOCKED (Human), Phase 5 partially verified

---

## What Was Done

### Phase 1 — Dossier Schema Hardening
- Extended `generate_dossier()` with `allow_incomplete`, `staged_path`, `editorial_candidates_path`, `residuals_path` fields
- Added `V11`, `V12` to promotion gate check names
- 4 new dossier schema tests in `tests/test_promote_gate.py`

### Phase 2 — Validator Hardening
- **V8 heading repetition/density**: Counter-based; >3 repeats of same heading = error; >3× chapters = density warning
- **V11 split-word detection**: Regex for Docling column-split artifacts (ov|ev|iv|erv|alv|elv|olv patterns)
- **V12 inline verse-number leakage**: Detects verse's own number after punctuation in text body
- Expanded `_KNOWN_BIBLICAL_TARGETS` in `fix_articles.py` with 11 new words
- 7 new validator tests in `tests/test_validate.py`

### Phase 3 — Book Recovery

| Book | Fixes Applied | V7 | V8 | V11 | V12 |
|------|--------------|-----|-----|------|------|
| **1KI** | 478→51 headings (cycling bug), 1 V12 fix (7:31) | 99.4% | PASS | PASS | PASS |
| **JOS** | Registry CVC updated 33→36 (LXX appendix) | 99.8% | PASS | PASS | PASS |
| **2CH** | 2 V12 fixes (2:4, 5:14), "ahandbreadth", 3× "forev er", split words | 101.2% | PASS | PASS | PASS |
| **2SA** | ~30+ split words in ch1, 22-23 (David's psalm) | 99.9% | PASS | PASS | PASS |
| **1CH** | 18+ split words in ch16 (David's psalm) | 98.4% | PASS | PASS | PASS |
| **RUT** | 6 fused articles ("ahusband", "arelative" ×2, "apile", "arelation", "aclose") | 100% | PASS | PASS | PASS |
| **JDG** | ~17 split words in ch5 (Song of Deborah) | 99.8% | PASS | PASS | PASS |
| **1SA** | ~7 split words in ch2 (Hannah's prayer) | 97.9% | PASS | PASS | PASS |
| **2KI** | 1 V12 fix (4:19) | 100% | PASS | PASS | PASS |

All 9 dossiers regenerated with new schema. 0 editorial candidates blocking any book.

### Phase 4 — Residual Governance
- Created residuals sidecars for 4 books: JDG (1 gap), 1SA (19 gaps), 2SA (2 gaps), 1KI (5 gaps)
- Normalized 1CH/2CH residuals to standard schema format
- **All 6 books BLOCKED on `ratified_by: null`** — see memo `38_residual_ratification_request.md`

### Phase 5 — Exit Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | 1KI no spurious headings | PASS |
| 2 | JOS CVC matches actual count (36) | PASS |
| 3 | V11 clean on all Group 2/3 books | PASS (9/9) |
| 4 | Dossiers have `allow_incomplete` field | PASS (9/9) |
| 5 | Residuals human-ratified | BLOCKED (0/6) |

---

## Test Suite
- **58 tests passing** (up from 32 at sprint start)
- Registry version: 1.2.3

## Remaining Blocker
Human must ratify 6 residuals sidecars (see `memos/38_residual_ratification_request.md`). Once done, all Group 2-3 books clear D5 and can proceed to Ezra audit → promotion.

## Dashboard
Regenerated: `reports/book_status_dashboard.json`
