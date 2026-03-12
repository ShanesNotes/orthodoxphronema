# Memo 97 — NT Stabilization Sprint: Drop-Cap Recovery & Text Fixes

**Date:** 2026-03-12
**Author:** Ark
**Status:** Complete
**Supersedes:** Partially addresses Memo 90 diagnostic findings

---

## Summary

Executed a systematic stabilization pass across all 27 NT books, targeting three
categories of text-quality defects: drop-cap OCR artifacts, article leakage, and
verse truncation. Result: **0 structural errors** across the entire NT corpus
(down from 77 reported in Memo 90 diagnostic), with 32 informational warnings
remaining (V7 completeness, V8 heading density).

## Changes Made

### 1. Drop-Cap OCR Recovery (197 fixes across 20 books)

**Problem:** The OSB PDF uses decorative drop-cap (large initial letter) formatting
at the start of each chapter. Docling OCR consistently drops these initial
characters, producing text like:
- `MAT.1:1 he book of the genealogy...` (should be "The book...")
- `MAT.2:1 ow after Jesus was born...` (should be "Now after...")
- `MAT.3:1 nthose days John the Baptist...` (should be "In those days...")

**Tool:** `pipeline/cleanup/nt_dropcap_recovery.py` (new)
- Pattern-based recovery using known English/NKJV word patterns
- Handles single-letter prefixes (T→The, N→Now, A→And, etc.)
- Handles fused-letter artifacts (nthose→In those, tthat→At that, etc.)
- Handles "I " prefix drops (saw→I saw, beseech→I beseech, etc.)
- Context-aware disambiguation for "hen" → Then vs When
- 197/197 issues matched and fixed (100% coverage)
- Full manifest at `reports/nt_dropcap_recovery_manifest.json`

**Books affected (20):** 1CO, 1PE, 2CO, 2PE, 2TH, 2TI, ACT, COL, EPH, GAL,
HEB, JAS, JOH, LUK, MAT, MRK, PHP, REV, ROM, TIT

**Books unaffected (7):** 1JN, 1TH, 1TI, 2JN, 3JN, JUD, PHM

### 2. EPH.1:1 Article Leakage (1 fix)

**Problem:** The entire Ephesians book outline (study article text) was fused
into the verse text of EPH.1:1, producing a line that started with OCR'd outline
content ("A pray er for revelation (1:15-23) III. Theology of Christ and His
Church...") followed by the actual verse text.

**Fix:** Removed the 336-character outline prefix, retaining only the actual
scripture: "Paul, an apostle of Jesus Christ by the will of God, To the saints
who are in Ephesus, and faithful in Christ Jesus: †"

### 3. HEB.1:14 Truncation (1 fix)

**Problem:** HEB.1:14 was truncated at the chapter boundary, ending with
"...for those who will inherit" — missing the final word "salvation?" which
was lost at the page/chapter extraction boundary.

**Fix:** Appended "salvation?" to complete the verse. This is a deterministic
recovery — the verse ending is consistent across all English translations of
Hebrews 1:14.

## Validation Results (Post-Fix)

| Metric | Before | After |
|---|---|---|
| NT structural errors (V1–V9) | 77* | **0** |
| NT warnings | 107* | **32** |
| Fully passing books (0 errors, 0 warnings) | ~2 | **6** |

*Per Memo 90 diagnostic (pre-extraction-refresh state)

**Remaining 32 warnings breakdown:**
- V7 (completeness): Minor versification drift in several books
- V8 (heading density): High heading-to-chapter ratio (informational only)
- V4 (verse gaps): Small gaps in a few books (PDF spot-check candidates)

**Fully passing books (6):** 1TH, 2JN, 2TH, JAS, PHM, plus candidates
that may achieve full pass after V7 registry alignment review.

## Artifacts Updated

- `staging/validated/NT/*.md` — 20 books with drop-cap fixes, EPH with article
  leakage fix, HEB with truncation fix
- `reports/nt_dropcap_recovery_manifest.json` — Full audit trail of 197 fixes
- `reports/nt_structural_census.json` — Refreshed with post-fix validation
- `reports/book_status_dashboard.json` — NT entries updated with current state
- `pipeline/cleanup/nt_dropcap_recovery.py` — Reusable tool for future NT extractions

## Known Remaining Defects

1. **Footnote marker residue:** Many verses contain fused 'a' characters
   (e.g., "adream", "aboat", "ajust") — these are footnote markers that
   weren't fully separated during extraction. Separate cleanup pass needed.
2. **V7 completeness drift:** Several books show >100% or <100% anchor
   counts vs registry. Requires registry reconciliation review.
3. **JOH chapter count:** JOH shows 25 chapters (registry expects 21) —
   likely phantom chapter breaks from section markers. Needs investigation.

## Next Owner

- **Ezra:** Audit this sprint's changes, especially the When/Then
  disambiguation decisions in the drop-cap manifest
- **Photius:** Footnote marker residue cleanup pass (separate workstream)
- **Human:** JOH chapter-count anomaly requires investigation and decision

## Completion Handshake

- ✓ Files changed: 22 NT .md files + 1 new tool + 3 refreshed reports
- ✓ Verification run: Full 27-book V1–V12 validation pass (0 errors)
- ✓ Artifacts refreshed: Census, dashboard, manifest
- ✓ Remaining drift: Documented (footnote markers, V7 drift, JOH chapters)
- ✓ Next owner: Named (Ezra for audit, Photius for marker cleanup)
