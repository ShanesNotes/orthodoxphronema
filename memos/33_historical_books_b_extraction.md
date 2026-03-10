# Memo 33 — Historical Books B Extraction Status

**Author:** `ark`
**Type:** `status`
**Status:** `complete`
**Date:** 2026-03-09
**Scope:** Group 3 extraction: 1KI, 2KI, 1CH, 2CH

---

## Summary

All 4 Historical Books B have been extracted, structurally fixed, cleaned, and validated. Each is promotion-ready pending Ezra audit + Human confirmation.

## Per-Book Results

| Book | Verses | V7 % | V9 Splits | Dropcap | Articles | R2 Fixes | Structural Fixes | Status |
|------|--------|-------|-----------|---------|----------|----------|-----------------|--------|
| 1KI | 818/823 | 99.4% | 7 | 4 | 102 | 58 | Complete ch5-22 reconstruction, CVC MT→LXX update | promotion_ready |
| 2KI | 723/719 | 100.6% | 6 | 24 | 121 | 53 | Ch16/17 boundary fix | promotion_ready |
| 1CH | 927/942 | 98.4% | 31 | 29 | 76 | 47 | 31 genealogy V9 splits, 1 docling gap (16:7) | promotion_ready |
| 2CH | 832/822 | 101.2% | 12 | 30 | 142 | 63 | 4 missing chapters, 2 false advances, Prayer of Manasseh removal | promotion_ready |

## Structural Issues Encountered

### 1KI — Catastrophic Chapter Advance Failure
- Only 4 of 22 chapters were detected by the extractor (ch1-4 only)
- Root cause: Registry CVC used MT/Hebrew versification, but OSB follows LXX/Brenton
- Fix: Updated registry CVC from MT to Brenton/LXX, then performed complete ch5-22 sequential renumbering
- 7 V9 embedded verse splits applied after reconstruction

### 2KI — Chapter Boundary Misassignment
- Ch16:17-20 were mislabeled as 17:1/18/19/20 (false advance at verse 17 → ch17)
- Fix: Relabeled back to 16:17-20
- 6 V9 embedded verse splits

### 1CH — Genealogy Density
- Chapters 1-9 are dense genealogy lists with highest fused risk of any book
- 31 V9 embedded verse splits (most of any book so far)
- 15 Docling gaps across genealogy chapters — all classified as `docling_issue`
- 1 ratified residual: 1CH.16:7 (docling_issue)

### 2CH — Multiple Issues
- **Missing chapters 33-36**: Extractor failed to advance past ch32; required reconstruction of ch33-36 from ch32 content
- **False advances**: Ch13 triggered at 12:13, ch16 triggered at 15:16 — both relabeled
- **Prayer of Manasseh leakage**: Appendix prayer text leaked into ch33 — removed entirely
- **Dropcap 33:1**: Dropcap letter plus opening text lost; verse entirely absent → classified as `docling_issue`
- 12 V9 embedded verse splits
- 2 manual fused word fixes after dropcap apply: `abronze` → `a bronze`, `Rehoboam'skingdom` → `Rehoboam's kingdom`

## Automated Cleanup Summary

| Cleanup Type | 1KI | 2KI | 1CH | 2CH | Total |
|-------------|-----|-----|-----|-----|-------|
| Dropcap repairs | 4 | 24 | 29 | 30 | 87 |
| Fused articles | 102 | 121 | 76 | 142 | 441 |
| R2 possessives | 58 | 53 | 47 | 63 | 221 |
| Manual text fixes | 0 | 3 | 4 | 2 | 9 |

## Known Residuals

- **1KI**: 5 missing verses (Docling gaps), no residuals sidecar needed (no per-entry ratification)
- **2KI**: 4 extra verses from V9 splits (V7 100.6%), clean
- **1CH**: 15 missing verses (Docling gaps), 1 ratified residual (16:7)
- **2CH**: 1 missing verse (33:1 Docling gap), 10 extra from V9 splits

## CVC Versification Note

1KI registry CVC was initially populated from MT/Hebrew versification, which has significantly different chapter boundaries than the LXX/Brenton versification used by the OSB. This caused only 4 of 22 chapters to be detected during extraction. The registry was updated to Brenton/LXX counts for 1KI. Other books (2KI, 1CH, 2CH) had correct or close-enough CVC from Brenton and did not require updates.

## Test Suite

47 tests, all passing.

## Next Steps

1. Await Ezra audit for Group 3 (1KI, 2KI, 1CH, 2CH)
2. Human ratification of residuals sidecars (1CH, 2CH) required for promotion gate D5
3. Proceed to next extraction group per memo 25 long-horizon plan
4. All 14 books (Pentateuch + Historical A + Historical B) await Ezra audit + Human confirmation

## Promotion Gate Status

All 4 books pass the hardened promotion gate (D1-D6 from memo 31):
- Editorial candidates: 0 for all 4 books
- Study article leakage: None detected
- All validation checks pass (V1-V9)
- Dossiers generated for all 4 books
- 1KI/2KI: No residuals sidecar needed — gate passes with `--allow-incomplete`
- 1CH/2CH: Residuals sidecars created — blocked on `ratified_by: "human"` (D5)

## Combined Historical Books Totals

Groups 2+3 combined (9 books):

| Metric | Total |
|--------|-------|
| Verses extracted | 6,473 |
| Dropcap repairs | 184 |
| Fused article fixes | 963 |
| R2 possessive fixes | 450 |
| V9 embedded verse splits | 81 |
| Manual text fixes | 22 |
| Structural reconstructions | 9 books (all required some level of structural fix) |
