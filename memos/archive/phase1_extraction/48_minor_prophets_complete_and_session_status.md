# Memo 48: Minor Prophets Complete + Session Status

**Date:** 2026-03-10
**Author:** Ark
**Status:** Informational

## Summary

All 12 Minor Prophets are now extracted, cleaned, and validated. This session also fixed JOL's chapter-0 restructuring, completed MAL extraction, and resolved several cross-book issues.

## Minor Prophets Final Status

| Book | V7 | Status | Key Issues |
|------|-----|--------|------------|
| HOS | 94.9% (187/197) | editorially_clean | 10 missing verses (genuine extraction gaps), V8 heading repetition from OSB source |
| AMO | 100% (145/145) | promotion_ready | CVC corrected (ch1: 14, ch9: 15) |
| MIC | 100% (105/105) | promotion_ready | 6 embedded verses fixed |
| JOL | 98.6% (72/73) | editorially_clean | 1 missing (dropcap 1:1), restructured from ch0 to 3 chapters |
| OBA | 100% (21/21) | promotion_ready | V11 false positive fixed (proper noun exclusion) |
| JON | 100% (48/48) | promotion_ready | Clean |
| NAH | 100% (47/47) | promotion_ready | Clean |
| HAB | 96.4% (54/56) | editorially_clean | 2 dropcap gaps (1:1, 3:1), absorbed 2:1 fixed |
| ZEP | 100% (53/53) | promotion_ready | Clean |
| HAG | 100% (38/38) | promotion_ready | Embedded 1:15 fixed, dropcap 2:1 fixed, spurious 2:24 removed |
| ZEC | 100% (211/211) | promotion_ready | 4 embedded verses fixed |
| MAL | 100% (55/55) | promotion_ready | 17 fused articles fixed, dropcap 1:1 fixed |

**9 of 12 promotion-ready.** HOS, JOL, HAB need residual handling before promotion.

## Fixes Applied This Session

### Registry Updates
- JOL CVC: [20, 27, 21] → [20, 32, 21] (3-chapter English numbering, ch2 includes LXX ch3)
- MAL: 4 chapters → 3 chapters, CVC [14, 17, 18, 6] → [14, 17, 24] (LXX numbering)
- AMO: ch1 CVC 15→14, ch9 CVC 9→15

### Validator Fix
- V11 split-word check: added proper-noun exclusion (skip words starting with uppercase before suffix match). Fixes "Negev shall" false positive.
- All 189 tests still pass.

### Cross-Book Possessive Fixes
- HAB: men'sblood → men's blood
- NAH: lion'scub → lion's cub
- JON: man'slife, day'sjourney → man's life, day's journey
- HAG: Lord'shouse, Lord'smessenger, Lord'stemple → Lord's house, etc.

### HOS Restructuring (Major)
- All 187 verses mapped from ch0 to correct chapters using Brenton content matching
- 3 versification differences between OSB and Brenton encoded (ch1/2, ch11/12, ch13/14 boundary shifts)
- 120+ split-word fixes, 60+ fused article fixes
- Script: pipeline/tools/fix_hos_final.py

## Overall Pipeline Status

- **Promoted**: 2 (GEN, LEV)
- **Promotion-ready**: 20
- **Editorially clean**: 12
- **Extracting/not started**: 42

## Next Steps

1. Continue long-horizon extraction: Wisdom books (JOB, PRO, ECC, SNG, WIS, SIR) or Major Prophets (ISA, JER, BAR, LAM, LJE, EZK, DAN)
2. Generate dossiers for editorially_clean books that are close to promotion
3. Begin NT extraction planning
