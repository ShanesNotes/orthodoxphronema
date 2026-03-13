# Memo 49: Major Prophets & Wisdom Books Extraction Status

**Date:** 2026-03-10
**Author:** Ark
**Status:** Informational

## Summary

Extracted 13 books this session: 6 Wisdom books (SNG, ECC, WIS, PRO, JOB, SIR) and 7 Major Prophets / Deuterocanonical (ISA, JER, EZK, DAN, LAM, BAR, LJE). Cleaned and stabilized 6 of them to near-promotion quality.

## Successfully Cleaned Books

| Book | V7 | Status | Key Fixes |
|------|-----|--------|-----------|
| DAN | 100% (530/530) | ALL PASS | CVC corrected for LXX ch3 (97v incl. Prayer of Azariah), 60 fused articles, 25 possessives |
| ISA | 99.8% (1290/1292) | editorially_clean | 27 embedded verses split, 31 fused articles, 50 possessives |
| EZK | 99.6% (1260/1265) | editorially_clean | 44 embedded verses split, 2 false ch-advances (ch25/ch37), 122 fused articles, 37 possessives |
| LJE | 100% (73/73) | editorially_clean | 38 fused articles, nav noise removed |
| BAR | 100.7% (141/140) | editorially_clean | 3 fused verses split, fused articles |
| LAM | 96.1% (148/154) | editorially_clean | Full restructure (5 ch-boundary splits), 101 split words, 26 fused articles, CVC fixed |

## Registry Updates

- **DAN** CVC: ch3 30→97 (LXX includes Prayer of Azariah + Song of Three Youth)
- **LAM** CVC: ch5 26→22 (was incorrect)

## Books Needing Major Restructuring

| Book | V7 | Root Cause |
|------|-----|-----------|
| JER | 46.6% | LXX vs MT chapter reordering — ch25 advance fails, chs 26-52 collapse. CVC needs LXX versification |
| SIR | 3.4% | Catastrophic chapter-0 — all 51 chapters collapsed. 1368 expected verses |
| PRO | 4.7% | Chapter-0 — short chapters (7-35v) fail 80% threshold |
| JOB | 19.9% | Chapter-0 — poetry formatting disrupts chapter detection |
| WIS | 46.1% | Only 10/19 chapters detected |
| ECC | 36.0% | Only 4/12 chapters — short chapters fail threshold |
| SNG | 44.4% | Only 4/8 chapters — speaker labels disrupt chapter advance |

### Common Root Cause

The 80%/60% chapter-advance threshold in `osb_extract.py` fails on books with:
1. Very short chapters (SNG: 8-17v, ECC: 10-29v, PRO: 7-35v)
2. Poetry formatting that hides chapter numbers (JOB, SNG)
3. LXX chapter reordering vs registry CVC (JER)

### Potential Fix Approaches

1. **Per-book CVC-aware extraction** — lower threshold for known-short-chapter books
2. **Post-extraction restructuring** — like HOS, LAM: extract with chapter-0, then Brenton-match to correct chapters
3. **Parser enhancement** — detect "bare chapter number" TextItem elements as chapter signals

Option 2 (post-extraction restructuring) is proven and most reliable.

## Overall Pipeline Status

- **Promoted**: 2 (GEN, LEV)
- **Promotion-ready**: 20
- **Editorially clean**: 18 (previous 12 + ISA, EZK, DAN, LAM, LJE, BAR)
- **Needs restructuring**: 7 (JER, SIR, PRO, JOB, WIS, ECC, SNG)
- **Not yet extracted**: ~29

## Next Steps

1. Begin restructuring wisdom books — start with ECC and SNG (smallest, most tractable)
2. Fix JER CVC for LXX versification, then restructure
3. Generate dossiers for newly cleaned books
4. Continue NT extraction planning
