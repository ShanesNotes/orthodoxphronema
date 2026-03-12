# Memo 67 — Catastrophic Structural Failure in NT Extraction

**Date:** 2026-03-10
**From:** Photius
**To:** Ark, Human (Shane)
**Status:** NT Staging Blocked by Systemic Failure
**Scope:** `new_testament_audit / structural_integrity`

## 1. Executive Summary
The New Testament extraction recently staged in `staging/validated/NT/` has failed every project invariant for structural and canonical integrity. These files are not "raw artifacts" suitable for normalization; they are **structurally corrupt**. Every one of the 27 books has failed validation with high-severity errors.

## 2. Primary Failure Classes

### Class A: Pervasive V9 (Embedded Verses)
The extractor failed to anchor thousands of verses that appear in the middle of a line. 
- **Symptom:** Verse text for N+1 is buried inside the buffer for Verse N.
- **Example:** `ACT.1:3` is inside `ACT.1:2`. `COL.1:8` is inside `COL.1:7`.
- **Scale:** Affects almost every chapter in all 27 books.

### Class B: V3 & V1 Tracking Collapse
The state machine lost context for chapter and verse numbering, leading to "Chapter 0" artifacts and backward jumps.
- **Symptom:** Chapters start at 0 instead of 1, or repeat previously extracted verses.
- **Affected:** Most prominent in the Gospels (MAT, MRK, LUK, JOH) and ROM, PHP, REV.

### Class C: Completeness & Truncation (V7)
Large blocks of text are missing or cut off.
- **Symptom:** Completeness percentages range from 75% to 95%.
- **Example:** TIT (78.3%), HEB (85.5%), ACT (95.3%).

### Class D: OCR Purity (V11/V12)
Heavy kerning residue and digit leakage.
- **Symptom:** `sev en`, `aliv e`, `pray er`, and verse digits like `20` leaked into the sentence body.

## 3. Recommendation for Ark
**Immediate Halt:** These files should not be promoted. The current extraction strategy (likely standard Docling without coordinate-aware pinning) is unsuitable for the OSB New Testament layout.

**Next Steps:**
1. **Re-extraction required:** The sequential `psa_extract.py` or a layout-aware pericope-driven parser must be used.
2. **Coordinate Pinning:** The parser must be configured to prioritize "Centered Digits" for chapters and "Leading/Inline Digits" for verses.
3. **Purity Dictionary:** The V11 cleanup pass I established for Wisdom must be integrated into the base extraction pipeline.

## 4. Completion Handshake
- **Files checked:** `staging/validated/NT/*.md` (27 books)
- **Verification run:** `FAIL` across all 27 books.
- **Artifacts:** This memo.
- **Remaining known drift:** Total (100% of NT requires re-work).
- **Next owner:** Ark (Architecture/Re-extraction).
