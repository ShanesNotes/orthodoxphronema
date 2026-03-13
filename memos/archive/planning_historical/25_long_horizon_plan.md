# Memo 25 — Long-Horizon Plan: Phase 1 Completion + Phase 2 Readiness

**Author:** `ark`
**Type:** `plan`
**Status:** `active`
**Date:** 2026-03-08
**Scope:** Full Phase 1 (76 books) + Phase 2 preparation

---

## Context

Day 11 delivered GEN/EXO/LEV at 99%+ extraction quality, proving the pipeline for Pentateuch-scale books. The critical discovery was CVC corruption (LEV plan data was 17% wrong), which led to a backward-signal chapter advance fallback. With 3/76 books extracted and infrastructure hardened, we need a systematic plan to complete Phase 1 (all 76 books extracted, validated, promoted) and prepare Phase 2 (cross-references, notes, search).

**Current state:** 3 books extracted (GEN 99.8%, EXO 100.4%, LEV 99.0%), 20 tests passing, registry v1.2.0, sidecar auto-generation operational.

---

## I. Pre-Extraction Infrastructure Hardening (Days 12-13)

### 1. Batch CVC Verification — ALL 76 Books
**File:** `pipeline/tools/verify_all_cvc.py`
**Why:** LEV's CVC was garbage. Any book with unverified plan-data CVC will fail extraction.
**How:** For each book with Brenton coverage (46+ OT books), compare registry CVC against Brenton verse counts. Flag mismatches. Add missing aliases (ESG→EST, NAM→NAH) to `index_brenton.py`. For 27 NT books, use plan data initially but verify against first extraction.
**Output:** Updated `anchor_registry.json` with verified CVC for all OT books; status report listing corrections.

### 2. Fused-Article Repair Script
**File:** `pipeline/cleanup/fix_articles.py`
**Why:** ~200-250 fused articles per book ("aburnt", "asoul", "aman"). At 76 books that's ~15,000 manual reviews without automation.
**How:** Regex-based detector for article+word fusions (a/an/the + capitalized or known word). Brenton witness for confirmation. Auto-fix when confidence ≥ 0.90, flag for review otherwise.
**Output:** Script that reduces fused-article residue by 80%+.

### 3. EXO CVC Over-Count Investigation
**Why:** EXO ch32/35/36 have more extracted verses than CVC. Brenton confirms CVC is correct — these are parser over-splits.
**Action:** Document as known V7 warning behavior. No code change needed — `--allow-incomplete` handles this.

---

## II. OT Extraction Sequence (Days 13-28)

### Group 1: Complete Pentateuch (Days 13-15)
| Book | Ch | Est. Verses | Notes |
|------|-----|------------|-------|
| NUM | 36 | 1288 | Census lists = fused risk |
| DEU | 34 | 959 | Legal code, enumeration patterns |

**Milestone:** Pentateuch complete (5/76).

### Group 2: Historical Books A (Days 15-18)
| Book | Ch | Est. Verses | Notes |
|------|-----|------------|-------|
| JOS | 24 | 658 | Territory lists |
| JDG | 21 | 618 | Narrative |
| RUT | 4 | 85 | Short, good validation |
| 1SA | 31 | ? | **Missing CVC** |
| 2SA | 24 | ? | **Missing CVC** |

### Group 3: Historical Books B (Days 18-20)
| Book | Ch | Est. Verses | Notes |
|------|-----|------------|-------|
| 1KI | 22 | 816 | |
| 2KI | 25 | 719 | |
| 1CH | 29 | 942 | Genealogies = high fused risk |
| 2CH | 36 | 822 | |

### Group 4: Post-Exilic + Deuterocanon Historical (Days 20-23)
| Book | Ch | Est. Verses | Notes |
|------|-----|------------|-------|
| 1ES | 9 | 400 | |
| EZR | 10 | 280 | |
| NEH | 13 | 406 | |
| TOB | 14 | ? | **Missing CVC** |
| JDT | 16 | ? | **Missing CVC** |
| EST | 16 | 292 | ESG alias needed |
| 1MA | 16 | ? | **Missing CVC** |
| 2MA | 15 | ? | **Missing CVC** |
| 3MA | 7 | 228 | |

### Group 5: Wisdom Literature (Days 23-25)
| Book | Ch | Est. Verses | Notes |
|------|-----|------------|-------|
| JOB | 42 | ? | **Missing CVC**, poetry-heavy |
| PRO | 31 | 915 | |
| ECC | 12 | 222 | |
| SNG | 8 | 126 | Poetry, dialogue |
| WIS | 19 | 436 | |
| SIR | 51 | ? | **Missing CVC**, longest wisdom book |

### Group 6: Psalms (Days 25-26) — DEDICATED SESSION
| Book | Ch | Est. Verses | Notes |
|------|-----|------------|-------|
| PSA | 151 | ? | **Missing CVC**, LXX numbering, superscriptions, Selah |

**Open decisions needed from Human:**
- LXX Psalm numbering (off by 1 from MT for Psalms 10-146)
- Psalm 151 (absent from Protestant Bibles)
- Superscriptions as verse 0 or verse 1?
- Selah markers: strip or preserve?

### Group 7: Prophets A — Major (Days 26-28)
| Book | Ch | Est. Verses | Notes |
|------|-----|------------|-------|
| ISA | 66 | 1292 | Largest prophet |
| JER | 52 | 1364 | LXX order differs from MT |
| LAM | 5 | 158 | Poetry/acrostic |
| BAR | 6 | 212 | |
| LJE | 1 | 73 | Confirmed separate book |
| EZK | 48 | ? | **Missing CVC** |
| DAN | 14 | 464 | Greek additions (Susanna, Bel) |

### Group 8: Prophets B — Minor (Days 28-29)
| Book | Ch | Est. Verses | Notes |
|------|-----|------------|-------|
| HOS–MAL (12 books) | 67 total | ~1050 | Short books, fast extraction |

**OT Milestone (Day 29):** All 49 OT books extracted and validated.

---

## III. NT Extraction (Days 29-35)

### NT Probe Session (Day 29)
Probe 3 diverse NT books before bulk extraction: MAT, ROM, REV.

**Expected issues:**
- Footnote marker ordering (known non-monotonic)
- Red-letter text (words of Christ)
- Epistle greetings/closings
- Study article density differences

### NT Extraction Groups (Days 30-35)
- **Group 9:** Gospels — MAT, MRK, LUK, JHN (Days 30-31)
- **Group 10:** Acts + Pauline — ACT, ROM, 1CO, 2CO, GAL, EPH, PHP, COL, 1TH, 2TH (Days 31-33)
- **Group 11:** Pastoral + General — 1TI–JUD (Days 33-34)
- **Group 12:** Revelation — REV (Day 35)

---

## IV. Promotion Pipeline (Days 35-40)

### Ezra Audit Protocol
Each book requires Ezra audit before promotion, batched:
- **Batch 1 (Day 35):** GEN, EXO, LEV (already validated)
- **Batch 2 (Day 36):** NUM, DEU
- **Batch 3-8 (Days 36-39):** 10-12 books per batch
- **Batch 9 (Day 40):** Final sweep

**Phase 1 Complete (Day 40):** All 76 books in `canon/` with checksums.

---

## V. Automation Improvements (Parallel Track)

### 5A. Batch Extraction Runner (`pipeline/tools/batch_extract.py`)
Runs extract → index_brenton → validate → cleanup → sidecar for a list of books.

### 5B. V5 Article Bleed Detector
Enhance `validate_canon.py` — flag verses with >3 consecutive numbered sub-points that reset the verse counter.

### 5C. CVC Auto-Correction from Extraction
After successful extraction with >95% V7, auto-update registry CVC. Safety: only if V1 PASS AND V3 PASS.

### 5D. Parallel Extraction
Test 2-way concurrent Docling extraction (GPU memory: RTX 4060 Ti 8GB).

---

## VI. Quality Gates

### Per-Book Gate (before promotion)
- [ ] V1 PASS (no duplicate anchors)
- [ ] V2 PASS (correct chapter count)
- [ ] V3 PASS (sequential chapters)
- [ ] V4 INFO or better (gaps documented in sidecar)
- [ ] V7 ≥ 98% (or residuals explain the gap)
- [ ] V8 PASS (no heading fragments)
- [ ] V9 PASS (no embedded verses)
- [ ] Residuals classified and ratified (osb_* entries need per-entry ratification)
- [ ] Study article leakage check passed
- [ ] Ezra audit recorded

### Phase 1 Completion Gate
- [ ] All 76 books in `canon/` with checksums
- [ ] All residual sidecars ratified
- [ ] Registry CVC verified for all books
- [ ] Test suite ≥ 40 tests (currently 20)
- [ ] All memos indexed and current

---

## VII. Phase 2 Readiness (Post Day 40)

- **2A.** Cross-Reference System — anchor-link syntax, build from OSB study notes
- **2B.** Study Notes Extraction — structured schema, anchor attribution, search indexing
- **2C.** Footnote Layer — link markers to footnote content from OSB PDF footnote pages
- **2D.** Search and Navigation — full-text search, anchor-based navigation
- **2E.** Obsidian Integration — Eve vault as human review layer

---

## VIII. Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| CVC wrong for more books | HIGH | HIGH | Batch verify all CVC before extraction |
| Docling drops pages/columns | HIGH | MEDIUM | V7 threshold + manual recovery |
| Study article leakage at scale | MEDIUM | HIGH | V5 detector automation |
| PSA LXX numbering complexity | HIGH | CERTAIN | Dedicated session with Brenton cross-ref |
| NT footnote non-monotonicity | MEDIUM | HIGH | Probe session before bulk NT |
| Fused articles overwhelm manual review | LOW | CERTAIN | fix_articles.py automation |
| GPU memory limits parallel extraction | LOW | MEDIUM | Test 2-way before 3-way |
| Brenton missing for 3 OT + all NT | MEDIUM | CERTAIN | Add aliases; NT post-extraction verify |

---

## IX. Timeline Summary

| Days | Milestone | Books |
|------|-----------|-------|
| 12-13 | Infrastructure hardening | 0 (CVC verification, fix_articles.py) |
| 13-15 | Pentateuch complete | NUM, DEU (5 total) |
| 15-20 | Historical books | JOS–2CH, 1ES–3MA (18 total = 23) |
| 20-26 | Wisdom + Psalms | JOB–SIR, PSA (7 total = 30) |
| 26-29 | Prophets | ISA–MAL (19 total = 49 OT) |
| 29-35 | NT extraction | MAT–REV (27 total = 76) |
| 35-40 | Promotion pipeline | All 76 promoted to canon/ |

**Total: ~28 working days (Day 12 to Day 40).**

---

## X. Immediate Next Actions (Day 12)

| Priority | Task | Blocked by |
|----------|------|-----------|
| 1 | GEN promotion | Human confirmation |
| 2 | Batch CVC verification (all 76 books) | Nothing |
| 3 | `fix_articles.py` — fused article repair | Nothing |
| 4 | NUM extraction + cleanup | CVC verification |
| 5 | EXO CVC over-count documentation | Nothing |
