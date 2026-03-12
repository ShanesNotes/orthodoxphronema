# Memo 90 — NT Triage Diagnostic (EPH, HEB, MAT)

**Author:** Ark
**Date:** 2026-03-11
**Status:** Executed
**Depends on:** Memo 86 (NT Quality Push), Memo 92 (NT Structural Census)

## Context

Steps 0-3, 5 of the NT Quality Push (memo 86) are complete. 77 errors, 107 warnings remain across 27 NT books. EPH (91%), HEB (95%), and MAT (101%) are the three sharpest stabilization priorities per the Ezra ops board. This diagnostic classifies every failure in these three books and recommends fix strategies before anyone writes fixes.

---

## Per-Book Failure Inventory

### EPH — 6 errors, 8 warnings, 141/155 verses (91.0%)

| Check | Count | Details |
|-------|-------|---------|
| V2 | 1 err | 7 chapters found, 6 expected (phantom Chapter 0 — empty header at line 15) |
| V4 | 14 warn | ch.2:1-7 absent (article leakage survivors — cleanup only deleted 2:1-5); ch.1:20, ch.3:4-7, ch.3:15, ch.4:16 embedded |
| V8 | 2 err | Lines 81, 84 — orphaned heading triplet ("Paul's Revelation" / "The Unity of Jew and Gentile in Christ" / duplicate "Paul's Revelation") |
| V9 | 4 err | EPH.1:19→20, EPH.3:2→3-7, EPH.3:14→15, EPH.4:15→16 (fused: "head-Christ16") |

**Root causes:**
- (a) Article leakage incomplete — EPH.2:6-7 were not in DELETE_ANCHORS
- (b) V9 recovery missed 4 embeds
- (c) EPH.3:3 anchor has wrong verse text (holds v7 content)

### HEB — 9 errors, 13 warnings, 288/303 verses (95.0%)

| Check | Count | Details |
|-------|-------|---------|
| V4 | 15 warn | ch.1:6-8,13; ch.2:13; ch.3:7; ch.4:5; ch.7:16,22; ch.8:9; ch.10:8-10,17; ch.11:19 |
| V8 | 3 err | Lines 18, 21 — orphaned heading pair + duplicate at line 24 |
| V9 | 7 err | HEB.4:4→5, 7:15→16, 7:21→22, 8:8→9 (fused: "Judah9"), 10:7→10 (false positive — absent not embedded), 10:16→17, 11:18→19 |
| Drop-cap | 8 warn | Chapter starts missing first letter: 2:1, 3:1, 4:1, 5:1, 6:1, 7:1, 8:1, 13:1 |

**Root causes:**
- (a) V9 recovery missed 6 true embeds + 1 false positive (10:7-10 absent, not embedded)
- (b) Orphaned headings from study article leakage
- (c) Drop-cap OCR systematic across chapter starts

### MAT — 6 errors, 7 warnings, 1082/1071 verses (101.0%)

| Check | Count | Details |
|-------|-------|---------|
| V2 | 1 err | 29 chapters found, 28 expected (phantom Chapter 0 at line 15 with "The Genealogy of Jesus") |
| V4 | 5 warn | ch.4:15-16 (truly absent), ch.5:2 (truly absent), ch.5:45 (embedded in 5:44), ch.24:49 (embedded in 24:48) |
| V7 | 1 err | 101.0% — overcounting caused by phantom chapter 0 |
| V8 | 4 err | Line 18 (ch0 orphan), lines 1028, 1053, 1350 — duplicate heading pairs |
| V9 | 2 warn | MAT.5:44→45, MAT.24:48→49 |

**Root causes:**
- (a) Phantom ch0 not deleted by article removal (has no anchors, just a heading)
- (b) 3 duplicate heading pairs from column-split extraction
- (c) 2 straightforward V9 embeds
- (d) 3 truly absent verses need PDF verification

---

## Fix Strategy Classification

### Photius-safe batch cleanup (bounded, evidence-packaged)

1. **Delete phantom Chapter 0** — EPH, MAT: remove `## Chapter 0` line + any orphaned heading before `## Chapter 1`. Simple structural fix.

2. **Delete duplicate headings** — MAT lines 1028/1031, 1053/1056, 1350/1353; HEB lines 18/21 (keep line 24 which precedes first verse). Pattern: when two identical `###` headings appear with only blank lines between, keep the second.

3. **Delete orphaned heading pairs** — EPH lines 81/84 (keep line 87 which precedes EPH.2:19).

4. **V9 embed splitting** — All 13 embeds across 3 books. Standard `nt_verse_recovery.py` pattern: split at inline digit boundary.
   - Simple splits (10 cases): digit + space + uppercase or lowercase continuation
   - Fused splits (2 cases): EPH "head-Christ16", HEB "Judah9" — need space insertion before digit
   - Complex split (1 case): EPH.3:2 contains verses 3-6 inline, and EPH.3:3 anchor has verse 7 text — requires anchor renumbering

5. **Drop-cap restoration** — HEB 8 chapter starts. Known first letters from context.

### Ark-only structural repair

1. **EPH.2:6-7 recovery** — Missed by `nt_article_removal.py` DELETE_ANCHORS (only had 2:1-5). Either deleted as article leakage and need re-extraction, or never extracted. Needs PDF verification.

2. **EPH.3:3 anchor renumbering** — EPH.3:3 holds verse 7 text. Requires understanding the full 3:2→3:8 sequence and renumbering.

3. **MAT.4:15-16, MAT.5:2 absence** — Need PDF verification. If present in source, need targeted re-extraction.

4. **HEB truly absent verses** (ch.1:6-8,13; ch.2:13; ch.3:7; etc.) — Need PDF verification to classify as extraction failure vs source-absent.

---

## Recommended Stabilization Order

1. **MAT first** (lowest effort, highest impact): Only 6 errors. Delete ch0 + 3 duplicate headings + 2 V9 splits. Expected outcome: ~0 errors, ~2 warnings (V4 for 3 truly absent verses needing PDF check).

2. **EPH second** (medium effort, high impact): Delete ch0 + orphaned headings + 4 V9 splits + EPH.3 renumbering. Then PDF-verify EPH.2:6-7 to determine recovery path. Expected outcome: 91% → ~96%+ V7.

3. **HEB third** (highest effort): 7 V9 splits + orphaned headings + 8 drop-caps + PDF verification of 15 absent verses. Expected outcome: 95% → ~97%+ depending on PDF results.

---

## Execution Results (2026-03-11)

All fixes executed. PDF verification used for every absent-verse decision.

| Book | Before (err/warn/V7%) | After (err/warn/V7%) | Key fixes |
|------|-----------------------|----------------------|-----------|
| **MAT** | 6/7/101.0% | **0/4/101.2%** | Ch0 deleted, 3 dup headings removed, 2 V9 splits. 3 verses (4:15-16, 5:2) confirmed source-absent by PDF. |
| **EPH** | 6/8/91.0% | **0/1/100.0%** | Ch0 deleted, orphaned headings removed, 4 V9 splits, EPH.3:2-7 renumbered, **EPH.2:1-7 recovered from PDF**, study article leak in 2:22 cleaned, 3:1 drop-cap fixed. |
| **HEB** | 9/13/95.0% | **0/1/100.0%** | Orphaned headings removed, HEB.1:5 split into 1:5-8 (study article contamination removed), 1:12→13, 2:12→13, 3:6→7 splits, **10:8-10 recovered from PDF**, 8 drop-caps fixed, 1:4 article leak cleaned, 5:7 duplicate number fixed. |

### Extended sweep (all 27 NT books)

After the initial 3-book fix, a full-NT sweep was executed covering all remaining error books.

| Book | Before | After | Key fixes |
|------|--------|-------|-----------|
| **ROM** | 4 err / — | **0/1/99.5%** | Ch9:1-7 reordered + article cleanup, ch9:23-29 V9 splits (6 verses recovered), ch2:1-10 inserted from PDF, ch11:8→9 split, ch11:34→35 re-anchored + v34 inserted, ch3:1/10:1/11:1 drop-caps |
| **1TH** | 2 err / — | **0/0/100%** | Ch1:1+1:5 split from fused anchor, reordered, dup heading deleted, 4 drop-caps |
| **1TI** | 4 err / — | **0/1/100%** | Ch1:1-7 fully restructured (article cleanup + reorder), ch2:1-4 inserted from PDF, ch3 heading repositioned, 6:20→21 V9 split, 4 drop-caps |
| **1JN** | 3 err / — | **0/1/100%** | Ch1:7-8 cleaned of article text + reordered, 4 drop-caps |
| **ACT** | — | **0/1/100%** | 1:19→20 split, 2:16 inserted from PDF, 13:34→35 split, 2:1 drop-cap |
| **1CO** | — | **0/1/97.8%** | 1:4-8 cleaned of article text + split into 5 clean verses |
| **MAT** | — | **0/2** | 4:14→15+16 inserted from PDF, 5:1+5:2 inserted from PDF, 5:1 drop-cap |
| **LUK** | — | **0/3** | 4:10→11 split |
| **REV** | — | **0/2/99.8%** | 16:17 drop-cap, 16:18 recovered, 17:1-2 recovered + 17:17-18 corrected (were cross-contaminated) |
| **PHP** | — | **0/1** | Ch0 deleted |
| **COL** | — | **0/2/96.0%** | 1:1 inserted from PDF |
| **JAS** | — | **0/0/100%** | 1:1 inserted from PDF |
| **2PE** | — | **0/1/100%** | 1:1 inserted from PDF |
| **1PE** | — | **0/2** | 2:7→8 V9 split |

**Final NT totals**: 77 err / 107 warn → **0 err / 32 warn**

19/27 books at 100% verse completeness. 0 errors across all 27 books.

### PDF verification summary (complete)
- MAT.4:15-16, MAT.5:2: **ALL in PDF** — recovered (poetry block + truncation)
- EPH.2:1-7: **ALL in PDF** — recovered (were article-cleanup casualties)
- HEB.1:6-8, 1:13: **ALL in PDF** — embedded in 1:5 and 1:12, split out
- HEB.2:13: **In PDF** — embedded in 2:12, split out
- HEB.3:7: **In PDF** — embedded in 3:6, split out
- HEB.10:8-10: **ALL in PDF** — were simply missing from extraction, inserted
- ROM.2:1-10: **ALL in PDF** — were simply missing from extraction, inserted
- ROM.11:9: **In PDF** — embedded in 11:8, split out
- ROM.11:34-35: **In PDF** — v34 was missing, v35 was mis-anchored as v34
- 1CO.1:7-8: **In PDF** — embedded in article-contaminated 1:5 line, split out
- ACT.1:20: **In PDF** — embedded in 1:19, split out
- ACT.2:16: **In PDF** — was simply missing from extraction, inserted
- ACT.13:35: **In PDF** — embedded in 13:34, split out
- REV.16:18: **In PDF** — was mis-anchored as 17:18 (cross-contaminated with actual 17:18)
- REV.17:1-2: **In PDF** — were mis-anchored inside 17:17
- LUK.4:11: **In PDF** — embedded in 4:10, split out
- COL.1:1: **In PDF** — was simply missing from extraction, inserted
- JAS.1:1: **In PDF** — was simply missing from extraction, inserted
- 2PE.1:1: **In PDF** — was simply missing from extraction, inserted
- 1TI.2:1-4: **ALL in PDF** — were simply missing from extraction, inserted

## Verification

After fixes, run:
```bash
python3 pipeline/validate/validate_canon.py staging/validated/NT/{EPH,HEB,MAT}.md
python3 pipeline/tools/batch_validate.py --dir staging/validated/NT  # full NT regression
```

## Critical Files

- `staging/validated/NT/EPH.md` (141 verses, 6 errors)
- `staging/validated/NT/HEB.md` (288 verses, 9 errors)
- `staging/validated/NT/MAT.md` (1082 verses, 6 errors)
- `pipeline/cleanup/nt_article_removal.py` (EPH.2:6-7 gap in DELETE_ANCHORS)
- `pipeline/cleanup/nt_verse_recovery.py` (V9 splitting tool)
- `pipeline/validate/validate_canon.py` (validation)
- `pipeline/tools/pdf_verify.py` (PDF source verification for absent verses)
