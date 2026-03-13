# Memo 119 — 76-Book Canon Completion

**Date**: 2026-03-13
**Author**: Ark
**Status**: Complete

## Summary

All 76 books of the Orthodox canon are now promoted to `canon/` (49 OT + 27 NT). This memo documents the final review, cleanup, and promotion of the remaining 11 NT books.

## Books Promoted This Session

| Book | Pos | Verses | V7 Status | Notes |
|------|-----|--------|-----------|-------|
| MAT  | 50  | 1071/1071 | PASS | 100 cross-refs stripped, 85 fused markers fixed |
| MRK  | 51  | 679/678   | -1   | V9 embedded MRK.15:41 split; cross-refs stripped |
| LUK  | 52  | 1150/1151 | +1   | V9 embedded LUK.18:30 split; cross-refs stripped |
| JOH  | 53  | 879/879   | PASS | 89 fused markers fixed |
| ACT  | 54  | 1007/1007 | PASS | 85 fused markers fixed |
| ROM  | 55  | 431/433   | +2   | 29 fused markers fixed |
| 1CO  | 56  | 436/446   | +10  | 35 fused markers fixed, 3 L ORD fixes |
| PHP  | 60  | 104/95    | -9   | Registry CVC mismatch (NT versification) |
| COL  | 61  | 95/99     | +4   | 13 fused markers fixed |
| 1PE  | 70  | 106/105   | -1   | 15 fused markers fixed |
| REV  | 76  | 404/404   | PASS | 222+ artifacts fixed (worst OCR quality of all NT) |

## Cleanup Applied Across All NT Files

### F1: Trailing Footnote-Letter Residue
- **Scope**: All 27 NT books (canon + staging)
- **Pattern**: Lines ending with stray ` a` or ` b`
- **Total fixed**: 323+ lines across all NT files (including HEB 30, GAL 8, 2CO 8)

### F2: Fused Footnote-Marker Words
- **Scope**: All 11 staging NT books
- **Pattern**: Footnote reference letter fused to next word (`aof`→`of`, `aand`→`and`, etc.)
- **Total fixed**: 530+ lines (first pass) + 387 article-fused patterns + 267 additional
- **Categories**:
  - Footnote markers fused to function words: `aof`, `athe`, `awho`, `afor`, etc.
  - Article 'a' fused to content words: `aloud`→`a loud`, `athird`→`a third`, etc.
  - Stray standalone markers: ` a ` or ` b ` floating between words (153 removed)
  - Dagger symbols `†` stripped from verse text (42 lines)

### F3: Cross-Reference Leakage
- **Scope**: MAT, MRK, LUK, JOH
- **Pattern**: Inline `(Mt N:N; Lk N:N)` references from OSB
- **Total fixed**: 290 cross-references stripped

### F4: V12 Inline Verse-Number Leakage
- MRK.10:40: Duplicate `40` in verse body
- LUK.24:20: Duplicate `20` in verse body
- REV.1:6: Duplicate `6` + fused markers `aus`, `aand`

### F5: Study Article Leak
- REV.4:6: Full study note about Revelation 1:10 embedded in verse text — removed

### OT Trailing Markers
- NUM: 1 line, 1ES: 2 lines — cleaned

## V9 Embedded Verse Splits
- MRK.15:40/41: Verse 41 content was merged into verse 40 line, empty 41 anchor below
- LUK.18:29/30: Verse 30 content was merged into verse 29 line, empty 30 anchor below
- Both fixed by splitting the text at the verse boundary

## Known Residual Warnings (non-blocking)

### V7 Versification Differences
These are known LXX/MT or NT versification differences, NOT missing text:
- OT: 17 books with V7 warnings (all documented in memo 82)
- NT: MRK(-1), LUK(+1), ROM(+2), 1CO(+10), PHP(-9), COL(+4), 1PE(-1)

### V8 Heading Density
The OSB uses extensive pericope headings, especially in the Gospels. The V8 warning threshold triggers at 3+ headings/chapter. These are genuine OSB narrative headings retained in canon per policy.

### V10 (INFO)
NT books show V10 as `?` because no Brenton cross-reference data exists for NT. This is expected.

## Final State

```
76/76 books promoted
41 CLEAN (all V1-V12 pass)
35 with V7/V8 informational warnings
0  errors
0  missing
```

## Verification

- Batch review: `python3 pipeline/tools/batch_review.py`
- Dashboard: `reports/book_status_dashboard.json` → 76/76 promoted
- Full report: `reports/batch_review_76.json`
