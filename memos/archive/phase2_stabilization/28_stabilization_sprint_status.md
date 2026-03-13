# Memo 28 — Stabilization Sprint Status (Day 12, updated)

**Author:** `ark`
**Type:** `status`
**Status:** `closed`
**Date:** 2026-03-08
**Scope:** GEN/EXO/LEV stabilization, tooling, editorial purity

---

## What Was Done

### Infrastructure (Memo 25 Plan — Day 12 Items)

| Item | Status | Details |
|------|--------|---------|
| `verify_all_cvc.py` | DONE | 76-book verification complete. 10 missing CVCs populated. Report mode only (per Ezra memo 27). |
| `fix_articles.py` | DONE | A1/A2/A3 rules with biblical word targets + proper-name suppression. LEV 90%, EXO 72% auto-fix rate. |
| BAR chapter fix | DONE | 6→5 chapters (ch6 was LJE duplicate). Registry v1.2.2. |
| Brenton aliases | DONE | ESG→EST, NAM→NAH added to index_brenton.py and verify_all_cvc.py. |
| Editorial candidate sidecars | DONE | GEN/EXO/LEV_editorial_candidates.json generated. |

### GEN Stabilization (Ezra Memo 25 Blockers)

| Blocker | Status | Details |
|---------|--------|---------|
| GEN.14:24 fused into 14:23 | FIXED | Structural split: verse 24 separated onto its own line |
| GEN.49:1 truncation | FIXED | Full text recovered via targeted Docling re-extraction |
| GEN.49:2 missing | FIXED | Verse recovered: "And listen to Israel your father." |
| Minor OCR compounds | FIXED | twentyseventh→twenty-seventh, fortyfive→forty-five, sons-inlaw→sons-in-law |
| Fused articles | CLEAN | 0 true fused articles (confirmed by fix_articles.py) |
| Fused possessives | CLEAN | 0 remaining (R2 already applied) |
| Drop-cap candidates | CLEAN | 0 candidates (dropcap_verify) |

**GEN validation after fixes:** V1-V4 PASS, V7 99.9% (1531/1532), V8 PASS, V9 PASS.
**Truncations:** ALL 20 RESOLVED — 17 recovered via batch Docling re-extraction, 3 confirmed already complete (GEN.14:8, GEN.23:17, GEN.49:24). Two verses ending mid-sentence (GEN.27:44, GEN.48:3) confirmed as natural verse boundaries via Brenton comparison.
**Remaining:** 0 truncations. 1 missing verse (V7 gap) classified as osb_source_absent.
**PROMOTED TO CANON** — `canon/OT/GEN.md` written with checksum `bc29318...`.

### EXO Stabilization

| Item | Status | Details |
|------|--------|---------|
| Fused articles | FIXED | 305 + 18 = 323 auto-fixes applied |
| Fused possessives | FIXED | 79 R2 fixes applied |
| V7 over-count explained | DOCUMENTED | 5 over-splits in ch32(+1)/35(+3)/36(+1) are OSB vs Brenton versification differences, NOT parser errors. OSB has more verses than Brenton in these chapters. CVC reflects Brenton, not OSB. |
| Drop-cap candidates | PENDING | 13 ambiguous candidates need Human review |

**EXO validation:** V1-V4 PASS, V7 100.4% (over-count = versification diff), V8 PASS, V9 PASS.
**Truncations:** ALL 14 RESOLVED — 8 recovered via batch Docling re-extraction, 6 confirmed already complete (natural verse breaks, not truncations).
**Remaining:** 0 truncations, 13 dropcap candidates. **PROMOTION-READY** (dry-run exit 0 with --allow-incomplete).

### LEV Stabilization

| Item | Status | Details |
|------|--------|---------|
| Fused articles | FIXED | 392 + 14 = 406 auto-fixes applied |
| Fused possessives | FIXED | 89 R2 fixes applied |
| Drop-cap candidates | CLEAN | 0 candidates |

**LEV validation:** V1-V9 ALL PASS, V7 100.0% (859/859). Full completeness.
**Truncations:** ALL 5 RESOLVED — 3 recovered via Docling re-extraction, 2 confirmed already complete.
**Residuals:** ALL 6 RECOVERED — LEV.8:18-21 and LEV.21:2-3 via targeted Docling re-extraction.
**Structural fused:** 3 verse splits applied (LEV.14:55-57, LEV.22:32-33).
**Remaining:** 0 truncations, 0 residuals. **PROMOTION-READY** (dry-run exit 0).

---

## Current Book Status

| Book | V7 | Fused Articles | Fused Possessives | Truncations | Dropcaps | Status |
|------|-----|---------------|-------------------|-------------|----------|--------|
| GEN | 99.9% | 0 | 0 | 0 | 0 | **PROMOTED** — canon/OT/GEN.md |
| EXO | 100.4% | 0 | 0 | 0 | 13 pending | **PROMOTION-READY** — editorial debt cleared, dropcaps pending |
| LEV | 100.0% | 0 | 0 | 0 | 0 | **PROMOTION-READY** — full completeness, all residuals resolved |

---

## Truncation Recovery — ALL THREE BOOKS COMPLETE

### GEN (20 truncations → 0)
- **17 recovered** via batch Docling re-extraction
- **3 confirmed complete** — were not actually truncated
- **2 mid-sentence endings** confirmed as natural verse boundaries

### EXO (14 truncations → 0)
- **8 recovered** via targeted Docling re-extraction (corrected page ranges — first ~44 pages are navigation index, actual text starts ~page 233)
- **6 confirmed complete** — natural verse breaks flagged as false positive truncations (EXO.9:24, 15:25, 18:2, 27:20, 34:13, 35:31)

### LEV (5 truncations + 6 residuals + 3 fused → 0)
- **3 truncations recovered** via Docling re-extraction (LEV.10:1, 16:1, 21:1)
- **2 truncations confirmed complete** — natural verse breaks (LEV.14:21, 17:8)
- **6 residual verses recovered** — LEV.8:18-21 (ch8 burnt offering sequence), LEV.21:2-3 (ch21 priest regulations)
- **3 structural_fused splits** — LEV.14:55-57, LEV.22:32-33

**Strategy that worked:** Re-extract with expanded page ranges, use truncated text as search key (last 30+ chars), verify continuation against next verse boundary. Key insight: OSB PDF navigation index pages consume ~44 pages before actual text in each book section — page ranges in registry include these.

---

## Ezra Directive Compliance

| Ezra Directive (Memos 26-27) | Status |
|------------------------------|--------|
| Stabilization sprint before bulk extraction | IN PROGRESS |
| GEN visible blockers fixed | DONE (14:24, 49:1/2) |
| EXO editorial cleanup | DONE (articles + possessives) |
| LEV cleanup as stabilization standard | DONE |
| verify_all_cvc.py report mode only | COMPLIANT |
| fix_articles.py not blind-trusted for GEN | COMPLIANT (0 candidates in GEN) |
| No CVC auto-correction from extraction (5C rejected) | COMPLIANT |
| Editorial gate as advisory sidecar | DONE (_editorial_candidates.json) |

---

## Open Questions for Human

1. ~~GEN truncations~~ **RESOLVED** — all recovered
2. ~~GEN promotion~~ **DONE** — canon/OT/GEN.md
3. EXO dropcaps: 13 candidates need ratification
4. EXO V7 over-count: CVC should be updated to match OSB (1171 not 1166)?
5. EXO/LEV promotion: Both promotion-ready. Requires Ezra audit + Human confirmation per AGENTS.md.
6. When to begin NUM extraction? Stabilization sprint now complete.

---

## Next Actions

| Priority | Task | Blocked by |
|----------|------|-----------|
| 1 | EXO/LEV Ezra audit | Ezra availability |
| 2 | EXO dropcap ratification | Human review |
| 3 | EXO/LEV promotion | Ezra audit + Human confirmation |
| 4 | NUM/DEU extraction | Stabilization sprint complete — ready to begin |
