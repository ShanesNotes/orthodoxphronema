# Memo 30 — NUM/DEU Extraction + Stabilization Status

**Author:** `ark`
**Type:** `status`
**Status:** `open`
**Date:** 2026-03-08
**Scope:** NUM + DEU extraction, cleanup, and stabilization

---

## NUM (Numbers) — Extraction + Cleanup Complete

### Extraction
- **Source pages:** 386-497 (OSB PDF)
- **Raw extraction:** 1217 verses
- **After fixes:** 1287 verses (V7: 99.9%, 1287/1288)

### Issues Found + Fixed
| Issue | Count | Resolution |
|-------|-------|------------|
| Ch23-25 false chapter advance | 1 | Merged false verse splits (23:23+24, 23:25+26), renumbered, removed duplicate Ch24 header |
| Structural_fused (ch7 tribal offerings) | 48 | 12 groups x 4 embedded verses each, split into individual lines |
| Scattered V9 embedded verses | 28 | Split across ch1,4,5,6,9,14,16,20,27,31,32,34,35 |
| Drop-cap first letters | 33 | All "N→Now", "T→Then", "A→Again" restorations |
| Fused articles | 327+22 | fix_articles.py (327) + manual below-threshold (22) |
| Fused possessives | 75 | word's → word's (regex) |
| Split words (OCR) | 31 | Egypt, you, river, sayings, vision, etc. |

### Residual
- **NUM.6:27** — 1 missing verse. Content absorbed parenthetically into 6:23 (blessing conclusion). Classified as `docling_issue`, ratified.

### Status: **PROMOTION-READY** (dry-run exit 0 with --allow-incomplete)

---

## DEU (Deuteronomy) — Extraction + Cleanup Complete

### Extraction
- **Source pages:** 498-599 (OSB PDF)
- **Raw extraction:** 930 verses
- **After fixes:** 960 verses (V7: 100.1%, 960/959)

### Issues Found + Fixed
| Issue | Count | Resolution |
|-------|-------|------------|
| Ch22 false chapter advance | 1 | Extractor saw "22" in 21:22, triggered false ch22 start. Relabeled 22:1→21:22, split embedded 21:23, moved chapter header, relabeled 22:22→22:1 |
| Ch33 false verse splits | 2 | Brenton 33:23 and 33:24 each split into 2 OSB verses. Merged back. |
| Ch18 study article leak | 9 lines | "JESUS CHRIST: PROPHET, PRIEST, AND KING" article body leaked as DEU.18:22-18:30. Removed. Real 18:22 recovered from embedded in 18:21. |
| V9 embedded verses | 39 | Split across 15 chapters |
| Drop-cap first letters | 7 | All "N→Now", "T→Then" restorations |
| Fused articles | 192 | fix_articles.py |
| Fused possessives | 44 | word's → word's (regex) |
| Split words (OCR) | 30 | Egypt, you, days, beloved, etc. |

### Residual
- **DEU.33:8** — 1 missing verse. Lost in extraction (Moses' blessing). Classified as `docling_issue`, ratified.

### Versification Note
- Ch33: OSB has ~32 verses vs Brenton 29. Genuine LXX versification difference (Brenton 33:23 and 33:29 each split into multiple OSB verses). V7 over-count = +1.

### Status: **PROMOTION-READY** (dry-run exit 0 with --allow-incomplete)

---

## Current Book Status Dashboard

| Book | V7 | Status |
|------|-----|--------|
| GEN | 99.9% | **PROMOTED** — canon/OT/GEN.md |
| EXO | 100.4% | **PROMOTION-READY** — awaiting Ezra audit |
| LEV | 100.0% | **PROMOTION-READY** — awaiting Ezra audit |
| NUM | 99.9% | **PROMOTION-READY** — awaiting Ezra audit |
| DEU | 100.1% | **PROMOTION-READY** — awaiting Ezra audit |

All five Pentateuch books extracted, cleaned, and stabilized. Entire Pentateuch is promotion-ready.

---

## Next Actions

| Priority | Task | Blocked by |
|----------|------|-----------:|
| 1 | EXO/LEV/NUM/DEU Ezra audit | Ezra availability |
| 2 | Pentateuch promotion (all 4 remaining) | Ezra audit + Human confirmation |
| 3 | JOS extraction (next book) | Pentateuch stabilization complete |
| 4 | Continue OT extraction: JDG, RUT, 1SA, 2SA | Sequential per long-horizon plan |

---

## Open Questions for Human

1. EXO dropcaps: 13 candidates still pending Human review (from memo 28)
2. All 4 remaining Pentateuch books need Ezra audit before promotion
3. Ready to begin JOS (Joshua) extraction — page range ~600+
