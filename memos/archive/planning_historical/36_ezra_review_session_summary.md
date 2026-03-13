# Memo 36 — Ezra Review: Pipeline Status & Promotion Audit Guide

**Date:** 2026-03-09 (updated)
**Author:** Ark
**For:** Ezra audit + Human review

---

## Overall Progress

| Metric | Count |
|--------|-------|
| Total books in canon | 76 |
| Promoted (in canon/) | 2 (GEN, LEV) |
| Awaiting Ezra audit | 21 |
| Broken (poetry/wisdom) | 2 (SNG, ECC) |
| Not yet extracted | 51 |
| **Total extracted + promoted** | **25 / 76 (33%)** |

---

## Promotion Readiness — Tiered Summary

### Tier 1: Promotion-Ready (V7 ≥ 100%, no unratified residuals)

These books pass all promotion gates. Only the D5 human-ratification gate remains.

| Book | V7% | Verses | Residuals | Decision |
|------|-----|--------|-----------|----------|
| EXO | 100.4% | 1171/1166 | 0 (ratified by human) | dry-run ✓ |
| JOS | 100.3% | 660/658 | none needed | dry-run ✓ |
| RUT | 100.0% | 85/85 | none needed | dry-run ✓ |
| 2KI | 100.6% | 723/719 | none needed | dry-run ✓ |
| 1ES | 100.0% | 434/434 | none needed | dry-run ✓ |
| EZR | 100.4% | 281/280 | none needed | dry-run ✓ |
| JDT | 100.3% | 340/339 | none needed | dry-run ✓ |

**Ezra action:** Spot-check text quality, then ratify for promotion.

### Tier 2: Needs Residuals Ratification (sidecar exists, `ratified_by` = None)

These books have documented gaps with residuals sidecars. Ezra must review each sidecar and set `ratified_by: "human"`.

| Book | V7% | Verses | Gap | Residual Count | Sidecar |
|------|-----|--------|-----|----------------|---------|
| NUM | 99.9% | 1287/1288 | 1 | 1 | `NUM_residuals.json` |
| DEU | 100.1% | 960/959 | -1 | 1 | `DEU_residuals.json` |
| 1CH | 98.4% | 927/942 | 15 | 1 | `1CH_residuals.json` |
| 2CH | 101.2% | 832/822 | -10 | 1 | `2CH_residuals.json` |
| NEH | 96.1% | 390/406 | 16 | 7 | `NEH_residuals.json` |
| TOB | 100.4% | 246/245 | -1 | 2 | `TOB_residuals.json` |
| EST | 99.5% | 194/195 | 1 | 1 | `EST_residuals.json` |
| 1MA | 99.8% | 922/924 | 2 | 2 | `1MA_residuals.json` |
| 2MA | 99.5% | 552/555 | 3 | 3 | `2MA_residuals.json` |
| 3MA | 99.6% | 227/228 | 1 | 1 | `3MA_residuals.json` |

**Ezra action:** Review each `_residuals.json`, confirm gaps are `docling_issue` (not correctable), set `ratified_by: "human"` + `ratified_date`.

**Note:** 1CH (15 gaps, 1 residual) and NEH (16 gaps, 7 residuals) have residuals that don't fully cover their V7 gaps. The uncovered gaps are end-of-chapter shortfalls not detected by V4 (monotonic ordering passes). These books may need additional residuals entries or investigation.

### Tier 3: Needs Residuals Sidecar Created (gaps exist, no sidecar file)

These books have V7 < 100% but no residuals sidecar has been created to document the gaps. Ark needs to create residuals sidecars before Ezra can review.

| Book | V7% | Verses | Gap | Blocker |
|------|-----|--------|-----|---------|
| JDG | 99.8% | 617/618 | 1 | No `_residuals.json` |
| 1SA | 97.9% | 775/792 | 17 | No `_residuals.json` |
| 2SA | 99.9% | 696/697 | 1 | No `_residuals.json` |
| 1KI | 99.4% | 818/823 | 5 | No `_residuals.json` |

**Ark action:** Create residuals sidecars documenting specific missing anchors for each book.
**1SA** is the most concerning — 17 missing verses (97.9%) warrants investigation before residuals creation.

---

## Sidecar Completeness Matrix

All sidecars live in `staging/validated/OT/`.

| Book | `.md` | `_residuals.json` | `_editorial_candidates.json` | `_dropcap_candidates.json` | Dossier |
|------|-------|--------------------|-------------------------------|---------------------------|---------|
| EXO | ✓ | ✓ (ratified) | ✓ | ✓ | ✓ |
| NUM | ✓ | ✓ (unratified) | ✓ | ✓ | ✓ |
| DEU | ✓ | ✓ (unratified) | ✓ | ✓ | ✓ |
| JOS | ✓ | — | ✓ | ✓ | ✓ |
| JDG | ✓ | **MISSING** | ✓ | ✓ | ✓ |
| RUT | ✓ | — | ✓ | ✓ | ✓ |
| 1SA | ✓ | **MISSING** | ✓ | ✓ | ✓ |
| 2SA | ✓ | **MISSING** | ✓ | ✓ | ✓ |
| 1KI | ✓ | **MISSING** | ✓ | ✓ | ✓ |
| 2KI | ✓ | — | ✓ | ✓ | ✓ |
| 1CH | ✓ | ✓ (unratified) | ✓ | ✓ | ✓ |
| 2CH | ✓ | ✓ (unratified) | ✓ | ✓ | ✓ |
| 1ES | ✓ | — | ✓ | ✓ | ✓ |
| EZR | ✓ | — | ✓ | ✓ | ✓ |
| NEH | ✓ | ✓ (unratified) | ✓ | ✓ | ✓ |
| TOB | ✓ | ✓ (unratified) | ✓ | ✓ | ✓ |
| JDT | ✓ | — | ✓ | ✓ | ✓ |
| EST | ✓ | ✓ (unratified) | ✓ | ✓ | ✓ |
| 1MA | ✓ | ✓ (unratified) | ✓ | ✓ | ✓ |
| 2MA | ✓ | ✓ (unratified) | ✓ | ✓ | ✓ |
| 3MA | ✓ | ✓ (unratified) | ✓ | ✓ | ✓ |

Legend: ✓ = present, — = not needed (V7 ≥ 100%), **MISSING** = needs creation

---

## Groups by Extraction Status

### Group 1: Pentateuch (5 books — complete)
GEN and LEV promoted. EXO, NUM, DEU awaiting Ezra.

### Group 2: Historical Books A (5 books — complete)
JOS, JDG, RUT, 1SA, 2SA all extracted and cleaned. JDG, 1SA, 2SA, 1KI need residuals sidecars.

### Group 3: Historical Books B (4 books — complete)
1KI, 2KI, 1CH, 2CH all extracted and cleaned.

### Group 4: Post-Exilic + Deuterocanon (9 books — complete)
1ES, EZR, NEH, TOB, JDT, EST, 1MA, 2MA, 3MA. Includes catastrophic reconstructions for EST, 3MA.

### Group 5: Wisdom/Poetry (attempted, blocked)
- **SNG** — catastrophically broken (poetry word-splits, chapter collapse)
- **ECC** — catastrophically broken (all 12 chapters collapsed into ch0)
- **WIS, PRO, JOB, SIR, PSA** — not yet attempted
- Brenton indexes generated for all 7 books
- Blocked: needs specialized poetry-mode extraction approach

### Group 6: Minor Prophets (starting)
- Brenton indexes generated for all 12 books (HOS, JOL, AMO, OBA, JON, MIC, NAH, HAB, ZEP, HAG, ZEC, MAL)
- OBA extraction attempted — 0 verses extracted (page range issue, needs investigation)
- Mostly prose — expected to extract cleanly with existing pipeline

### Groups 7+: Major Prophets, NT (not started)
53 books remaining.

---

## This Session's Work

### Completed
1. **EST reconstruction** — Catastrophic structure (ch0-7 → ch1-10). OSB integrates Greek additions A-F inline. Registry CVC corrected from 16ch to 10ch.
2. **1MA extraction + cleanup** — 16 chapters, 922/924 verses. 5 V9 splits, ch3 duplicate resolution, 16 dropcap + 200 article + 52 possessive fixes.
3. **2MA extraction + cleanup** — 15 chapters, 552/555 verses. 4 V9 splits, 13 dropcap + 196 article + 49 possessive fixes.
4. **3MA extraction + reconstruction** — Chapters 3-7 collapsed into ch2 (same pattern as EST). Reconstructed using Brenton content matching. 2 V9 splits, 2 dropcap + 68 article + 15 possessive fixes. 9 recurring page-layout section headers removed.
5. **All 9 Group 4 sidecars** — residuals, editorial candidates, dropcap candidates, promotion dossiers.
6. **Dashboard regenerated** — 23+ books tracked.
7. **Minor Prophets prep** — Brenton indexes for all 12 books.

### Bug Fixes
- **dropcap_verify.py** — `missing_prefix` field was storing full repair prefix ("Then ") instead of just the missing character ("T"). `apply_repairs()` prepends this to existing text, so the old value caused double text ("Then hen Philopator..."). Fixed: `matched_prefix = repair_prefix[:missing_count]`.

---

## Ark's TODO Before Next Ezra Review

1. Create residuals sidecars for JDG, 1SA, 2SA, 1KI (Tier 3 books)
2. Investigate 1SA's 17 missing verses — determine if docling extraction issue or structural problem
3. Verify 1CH and NEH residuals cover all V7 gaps (currently incomplete coverage)
4. Continue Minor Prophets extraction (Group 6)
5. Regenerate dashboard with corrected statuses

---

## Open Questions for Human

1. **Poetry book strategy** — SNG and ECC extractions are catastrophically broken. Should we:
   - (a) Invest time in a specialized poetry-mode extractor/reconstructor?
   - (b) Skip wisdom/poetry and move to Minor Prophets (mostly prose)?
   - (c) Attempt manual reconstruction per-book?

2. **Batch Ezra audit** — 21 books are waiting. Can Tier 1 (7 books at V7 ≥ 100%) be batch-promoted without per-book review?

3. **1SA quality** — 97.9% V7 is the lowest of all extracted books. Should this be re-extracted before audit, or accepted with residuals?
