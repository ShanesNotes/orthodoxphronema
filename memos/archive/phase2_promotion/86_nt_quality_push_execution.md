# Memo 86 — NT Quality Push Execution Report

**Date**: 2026-03-11
**Author**: Ark
**Status**: Steps 0-3, 5 complete; Steps 4, 6, 7 deferred

## Summary

Executed NT quality push plan. Starting from raw extraction (695 errors, 353 warnings), achieved **77 errors, 107 warnings** across all 27 NT books. 10 books at >=100% V7, all 27 V1-clean (no duplicates).

## Step 0: CVC Registry Fixes (DONE)

Registry v1.4.0:
- **1TH**: `[10,19,18,21,18]` → `[10,20,13,18,28]` (sum 86→89)
- **3JN**: `[14]` → `[15]`

Impact: 1TH 92.1%→98.9%, 3JN 86.7%→100.0%

## Step 1: Article Leakage Removal (DONE)

Created `pipeline/cleanup/nt_article_removal.py` (v2, generic patterns).
- **136 article lines deleted** across 16 books
- **5 mixed lines cleaned** (EPH.2:19, 1CO.1:3, PHP.1:1, 1TH.1:5, HEB.1:9)
- **42 leaked headings removed** (spaced-caps, outline, book-title repeats)
- Generic detectors: nav junk ("Back to TOC"), article intros ("Author -"), ch0 content
- Per-book targets: EPH.2:1-5, HEB.1:2-8, 1TI.2:1-4+16-22, ROM.2:1-7, ch0 content in all books

## Step 2: REV/1CO Structural Reorder (DONE)

Created `pipeline/cleanup/nt_structural_reorder.py`.
- **REV ch16/17 boundary**: 4 verses relabeled (17:1→16:17, 17:19-21→16:19-21), ch17 sorted
- **REV ch21/22 boundary**: 6 verses relabeled (22:1→21:22, 22:23-27→21:23-27), 22:22→22:1
- **1CO ch1**: Verses reordered from 1,5,2,3,4,6,7... to correct 1,2,3,4,5,6,7...

## Step 3: V9 Recovery (DONE)

Ran `nt_verse_recovery.py` on all 27 books. **369 embedded verses split**.
Also ran `nt_dedup_merge.py` (new script): **74 duplicate anchors merged** pre-recovery.

## Step 5: Purity Cleanup (DONE — safe tools only)

Ran `fix_split_words.py` on all NT books. Did NOT run `nt_surgical_fix.py` (has catastrophic regex bug that splits multi-digit verse numbers: `MAT.1:12` → `MAT.1:1` + `MAT.1:2`). Did NOT run V12 leakage fix (too aggressive, strips legitimate numbers from text).

## Bug Found: nt_surgical_fix.py

The second regex pattern `re.match(rf'^({book_code}\.(\d+):(\d+))(\d+)\s+([A-Z...])...')` is missing `\s+` between the anchor verse number and the next-verse digit. This causes `MAT.1:12` to be parsed as anchor verse `1` + embedded verse `2`, destroying all multi-digit verse anchors ending in digit pairs that differ by 1 (e.g., 12→1+2, 23→2+3, 34→3+4). **Do not use this script.**

## Results Summary

| Metric | Raw Extraction | After Cleanup | Target |
|--------|---------------|---------------|--------|
| Errors | 695 | **77** | ~5 |
| Warnings | 353 | **107** | - |
| Books >=100% V7 | 2 | **10** | 8+ |
| Books >=95% V7 | 6 | **19** | 21 |
| V1 clean | 12 | **27** | 27 |

### Per-Book V7 After Cleanup

| V7% Range | Books |
|-----------|-------|
| 100%+ | GAL, 2TH, PHM, 2JN, 3JN, 1JN, 2TI, TIT, LUK, JOH, MAT, MRK |
| 95-99% | 1CO(97.1%), ACT(99.1%), 1TH(98.9%), REV(98.8%), 2PE(98.4%), PHP(109.5%), JAS(99.1%), HEB(95.0%), 1TI(96.5%), 2CO(99.2%) |
| 90-94% | EPH(91.0%), COL(94.9%), 1PE(94.3%), ROM(95.6%) |
| <90% | JUD(96.0%) |

### Remaining Errors (77 total)

- **V8** (heading integrity): ~30 errors — narrative headings in wrong positions
- **V9** (embedded verses): ~40 errors — remaining embeds the recovery couldn't split
- **V4** (verse ordering): ~7 errors — small gaps remaining

## Deferred Steps

- **Step 4** (Re-extraction of EPH, TIT, COL, PHM, JUD, HEB): Not needed for books already at 100%. EPH(91%) and COL(94.9%) would benefit most.
- **Step 6** (Drop-cap recovery): ~50+ lowercase-start verses across NT. Needs targeted script.
- **Step 7** (Residual classification): Generate sidecars for remaining V4 gaps.

## New Scripts Created

1. `pipeline/cleanup/nt_article_removal.py` — Generic NT article/nav junk removal
2. `pipeline/cleanup/nt_structural_reorder.py` — REV/1CO structural fixes
3. `pipeline/cleanup/nt_dedup_merge.py` — Duplicate anchor merger
