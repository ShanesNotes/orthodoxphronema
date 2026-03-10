# Memo 32 — Historical Books A Extraction Status

**Author:** `ark`
**Type:** `status`
**Status:** `complete`
**Date:** 2026-03-09
**Scope:** Group 2 extraction: JOS, JDG, RUT, 1SA, 2SA

---

## Summary

All 5 Historical Books A have been extracted, structurally fixed, cleaned, and validated. Each is promotion-ready pending Ezra audit + Human confirmation.

## Per-Book Results

| Book | Verses | V7 % | V9 Splits | Dropcap | Articles | R2 Fixes | Structural Fixes | Status |
|------|--------|-------|-----------|---------|----------|----------|-----------------|--------|
| JOS | 660/658 | 100.3% | 10 | 20 | 66+4 | 14 | Ch20-24 boundaries, ch22 renumber, ch23:12 split | promotion_ready |
| JDG | 617/618 | 99.8% | 3 | 20 | 131 | 37 | Ch12/13 false advance, 14:18 false splits, 3:22/20:16 split | promotion_ready |
| RUT | 85/85 | 100.0% | 1 | 4 | 19 | 5 | 1:12 embedded v13 | promotion_ready |
| 1SA | 775/792 | 97.9% | 4 | 31 | 166 | 54 | Ch2 Hannah's song merge, 20:13/16/25:24/31 splits | promotion_ready |
| 2SA | 696/697 | 99.9% | 7 | 22 | 136 | 119 | Ch7 article leak, ch3 embedded+dupes, ch22/23/24 boundaries, 16:6 split | promotion_ready |

## Structural Issues Encountered

### False Chapter Advances
- **JOS ch20-24**: Chapter advance threshold not met for ch21-24; required textual landmark-based relabeling
- **JDG ch12/13**: Verse 12:13 triggered ch13 advance (13 == current_chapter + 1)
- **2SA ch22/23/24**: Extractor never advanced past ch22; David's psalm (51 verses) followed by ch23/24 content all labeled ch22

### Study Article Leakage
- **2SA ch7**: "God's Covenants with His People Israel" article (10 lines) leaked into verse text with references to New Testament, Eucharist, etc. Removed entirely.

### Embedded Verse Splits
- Total across all 5 books: 25 V9 embedded verse splits
- Mostly in list/census content (JOS territory lists, David's sons, David's mighty men)

### False Verse Splits
- **JDG 14:18-20**: Riddle dialogue falsely split into 3 verses; merged back into single 14:18
- **1SA 2:10-15**: Hannah's song continuation falsely split; merged back into 2:10

### Poetry/Song Handling
- **1SA ch2**: Hannah's song required careful merge of falsely-split poetic content
- **2SA ch22**: David's psalm (51 verses) required precise boundary detection for ch23/24

## Automated Cleanup Summary

| Cleanup Type | JOS | JDG | RUT | 1SA | 2SA | Total |
|-------------|-----|-----|-----|-----|-----|-------|
| Dropcap repairs | 20 | 20 | 4 | 31 | 22 | 97 |
| Fused articles | 70 | 131 | 19 | 166 | 136 | 522 |
| R2 possessives | 14 | 37 | 5 | 54 | 119 | 229 |
| Manual text fixes | 5 | 1 | 3 | 1 | 3 | 13 |

## Known Residuals

- **JOS**: 2 extra verses from V9 splits (V7 100.3%)
- **JDG**: 1 missing verse (Docling gap)
- **1SA**: 17 missing verses (Docling gaps across multiple chapters)
- **2SA**: 1 missing verse (Docling gap)
- **RUT**: Perfect — 0 gaps

## Brenton Reference Indexes

All 9 Historical Books indexes were pre-generated in the previous session:
- `staging/reference/brenton/{JOS,JDG,RUT,1SA,2SA,1KI,2KI,1CH,2CH}.json`

## Test Suite

39 tests, all passing (unchanged from memo 31).

## Next Steps

1. Await Ezra audit for Group 2 (JOS, JDG, RUT, 1SA, 2SA)
2. Proceed to Group 3 extraction: 1KI → 2KI → 1CH → 2CH
3. Group 3 risks: Temple construction lists (1KI ch6-7), genealogies (1CH ch1-9)

## Promotion Gate Status

All 5 books pass the hardened promotion gate (D1-D6 from memo 31):
- Editorial candidates: 0 for all 5 books
- No residual sidecars needed (no per-entry ratification required)
- All validation checks pass (V1-V9)
- Dossiers generated for all 5 books
