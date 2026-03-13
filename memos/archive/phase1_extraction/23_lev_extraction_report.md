# Memo 23 — LEV Extraction Report (Day 11)

**Date:** 2026-03-08
**Book:** Leviticus (LEV), canon position 3
**Pages:** 305–385 (OSB PDF)

## CVC Correction (Critical)

The registry CVC for LEV was unverified plan data (total 713). Brenton LXX witness shows
27 chapters totaling **859 verses**. The old CVC caused the chapter advance guard to fail
at ch6→ch7 (only 23/30 = 76.7% extracted, below 80% threshold), cascading all subsequent
chapters into ch6.

**Fix:** Updated `anchor_registry.json` CVC to Brenton counts, bumped registry to v1.2.0.

Key differences: ch5 (19→26), ch6 (30→23), ch11 (44→47), ch12 (29→8), ch13 (36→59),
ch14 (9→57), ch15 (47→33), ch16 (55→34), ch18 (40→30), ch19 (9→37), ch20 (28→27),
ch21 (27→24), ch22 (17→33), ch23 (17→44), ch24 (18→23), ch25 (20→55), ch26 (19→46),
ch27 (16→34). OSB follows LXX numbering (confirmed from ch5 extraction reaching v26).

## Chapter Advance Guard Enhancement

Added backward-signal fallback to `osb_extract.py`:
- Primary: 80% threshold (unchanged)
- Fallback: if `chapter_num < current_verse AND current_verse >= 60% of max_v`, advance
- This catches missed advances where the parser couldn't extract enough verses to reach 80%
- Safe because false advances always have `chapter_num ≥ current_verse`

## Extraction Quality

| Metric | Value |
|--------|-------|
| V1 (duplicates) | PASS — 850 unique anchors |
| V2 (chapters) | PASS — 27 chapters |
| V3 (sequence) | PASS |
| V4 (gaps) | INFO — 6 residual missing anchors |
| V7 (completeness) | 850/859 (99.0%) |
| V8 (fragments) | PASS |
| V9 (embedded) | PASS (after manual separation) |

## Cleanup Stats

- **R2 (apostrophe spacing):** 93 fixes
- **R7 (Brenton auto-split):** 17 fixes
- **Dropcap repairs:** 22 (15 auto-confirmed + 7 upgraded from ambiguous)
- **Manual verse separation:** 13 lines → 36 lines (23 embedded verses resolved)
- **Study article leakage:** 1 block removed (Pentecost study article, ch23 — 7 numbered points misidentified as verses)
- **Cleanup residue:** 249 findings (218 fused_article, 31 fused_compound)

## Residuals (6 total — all docling_issue)

- LEV.8:18–21 (4 verses): gap in ordination chapter, likely Docling page/column boundary
- LEV.21:2–3 (2 verses): gap in priestly conduct chapter

All non-blocking. Ratification pending Ezra review.

## Open Questions

1. **Remaining 12 books with unverified CVC** — LEV's CVC was completely wrong.
   Should we proactively verify all CVC against Brenton before extracting more books?
2. **Fused articles (218 in LEV)** — "aburnt", "asoul" etc. are systematic OCR artifacts.
   A global fix_articles.py script would save significant manual cleanup time.
