# Memo 59 — Wisdom, Poetry & Prophets Restructuring Complete

**Date:** 2026-03-10
**Author:** Ark
**Status:** Implemented

## Summary

Restructured 4 chapter-0/structural books (JOB, PRO, SIR, JER) from near-zero to >92% completeness using Brenton content matching. Fixed HOS heading repetition (V8 failure). All major structural books in the OT are now resolved. Dashboard: 25 promotion_ready, 17 editorially_clean.

## Books Restructured

| Book | Before | After | Chapters | Status |
|------|--------|-------|----------|--------|
| **JOB** | 19.9% (8 ch) | 96.8% (1047/1082, 42 ch) | PASSED w/ warnings | editorially_clean |
| **PRO** | 4.7% (0 ch) | 92.8% (849/915, 30/31 ch) | PASSED w/ warnings | promotion_ready |
| **SIR** | 3.4% (0 ch) | 96.4% (1321/1370, 51 ch) | PASSED w/ warnings | editorially_clean |
| **JER** | 46.6% (25 ch) | 98.8% (1283/1299, 52 ch) | PASSED w/ warnings | editorially_clean |
| **HOS** | 94.9% (V8 fail) | 94.9% (187/197, 14 ch) | PASSED w/ warnings | editorially_clean |

## Cleanup Applied

| Book | Split Words | Fused Articles | Possessives | Other |
|------|-------------|----------------|-------------|-------|
| JOB | 370 | 220 | 24 | 438 duplicate headings removed |
| PRO | 279 | 461 | 11 | 25 nav noise lines deleted, 647 repeated headings removed |
| SIR | 517 | 760 | 45 | 10 duplicate anchors resolved, 3 embedded verses fixed |
| JER | — | 395 | 35 | 462 bogus headings removed, ch19 false advance fixed, CVC updated to LXX |
| HOS | — | — | — | 58 repeated headings deduplicated |

## JER Special Notes

- **CVC updated** in anchor_registry.json from MT-based (1364) to LXX/Brenton-based (1299)
- Ch1-24 were already correctly structured from extraction
- Ch25 had absorbed all remaining content (705 verse lines → restructured into ch25-52)
- Ch19 had a false chapter advance (verse 19 in ch18 text) — fixed manually
- 2 embedded verses split (JER.2:11, JER.19:2)

## Known Gaps

- **PRO ch31**: Entire chapter (virtuous wife acrostic, 31 verses) not captured by extraction
- **JOB**: 35 missing verses across 22 chapters (drop-cap + column-split losses)
- **SIR**: 49 missing verses across chapters (drop-cap + extraction gaps)
- **JER**: 16 missing verses (extraction gaps)
- **HOS**: 10 missing verses in ch1, ch2, ch10

All gaps documented in `_residuals.json` sidecars. Blocked on D5 (human ratification).

## Dashboard Status

| Status | Count |
|--------|-------|
| Promoted | 2 |
| Promotion-ready | 25 |
| Editorially clean | 17 |
| Structurally passable | 3 |
| Extracting | 29 |

## No Remaining Chapter-0 / Structural Books

All OT books with chapter-0 or structural corruption have been resolved. The remaining 29 "extracting" books have not yet been extracted from the PDF.

## Next Steps

1. Continue extraction of remaining OT books (Psalms is the largest at 329pp)
2. Begin NT extraction planning
3. Ezra: package promotion-ready books for Human review
