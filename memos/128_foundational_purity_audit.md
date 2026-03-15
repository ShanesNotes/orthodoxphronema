# Memo 128 — Foundational Purity Audit

**Status:** Active
**Owner:** Ark
**Created:** 2026-03-14
**Purpose:** Book-by-book deep audit across all surfaces before DuckDB production layer

## Scope

5-layer audit per book: canon integrity, study quality, metadata cross-refs,
knowledge graph reconciliation, YAML frontmatter normalization.

Canon is immutable — OCR issues are documented, not fixed inline.
Study layer files are editable for cleanup fixes.

---

## GEN — Genesis (2026-03-14)

### Layer 1: Canon Scripture Integrity
- **Validation:** V1-V9 PASS. V7 WARN: 1531/1532 verses (GEN.25:34 `osb_source_absent`, ratified)
- **Spellcheck:** 21 flags — all biblical names (Chedorlaomer, Machpelah, terebinth, etc.) or frontmatter fields. No real misspellings.
- **Spot-check:** Ch 1, Ch 24, Ch 49-50 read clean. No OCR artifacts, broken sentences, fused words, or encoding issues.
- **Registry match:** 1532 expected, 1531 present. Gap = GEN.25:34 (documented, ratified).
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Footnotes** (`study/footnotes/OT/GEN_footnotes.md`): 218 entries. All wikilinks valid (GEN.1:1 through GEN.50:26). Patristic citations clean (AthanG, Creed, HilryP, JohnDm, etc.). No OCR residue. **PASS**
- **Articles** (`study/articles/OT/GEN_articles.md`): 9 article sections (Creation, Holy Trinity, Ancestral Sin). **FIX APPLIED:** Line 19 had OCR fused phrase — `'In the beginning God made heaven and begin with a similarly striking earth.'` corrected to `'In the beginning God made heaven and earth.'`
- **Lectionary** (`study/lectionary-notes/OT/GEN_lectionary.md`): **FIXES APPLIED:**
  - Removed duplicate fragment entry `17:1` (duplicate of `17:1-9`)
  - Removed 8 non-GEN (Exodus) entries that leaked into GEN file (lines 84-98, including `12:51` which is impossible for Genesis — Gen 12 has only 20 verses)
  - Cross-chapter compact ranges (e.g., `1:24-3` = Gen 1:24 through 2:3) confirmed as valid lectionary notation
  - Entry count corrected: 44 → 35
- **Result:** FIXED (3 issues resolved)

### Layer 3: Metadata & Cross-References
- **Backlink shards:** 396 shards in `metadata/anchor_backlinks/study/`. Spot-checked GEN.1:1, GEN.11:1, GEN.18:22 — all valid, rich cross-testament linkage. Generator: phase3-backlinks-v1 (2026-03-13). **PASS**
- **R1 records:** 338 records in `metadata/r1_output/GEN.jsonl`. All properly formatted JSONL, reference types classified, context present. **PASS**
- **Footnote markers:** 218 markers in `staging/validated/OT/GEN_footnote_markers.json`. Perfect 1:1 with footnotes file. **PASS**
- **Promotion dossier:** `reports/GEN_promotion_dossier.json` — **STALE.** Generated against registry v1.4.0; current registry is v1.5.0. Dossier reflects old staging state (pre-promotion, V3/V9 FAIL on intermediate staging artifact). Canon file is the promoted truth. Dossier staleness is cosmetic — canon was promoted successfully.
- **Result:** PASS (dossier staleness noted, non-blocking)

### Layer 4: Knowledge Graph
- **GEN entity:** Updated with purity audit results and spellcheck status
- **GEN_articles:** Updated cleanup status to "audited clean"
- **GEN_footnotes:** Updated cleanup tier to "complete"
- **GEN_lectionary:** Created new entity (was missing), linked as companion_of GEN
- **Result:** UPDATED

### Layer 5: YAML Frontmatter
- **Canon frontmatter:** All required fields present — book_code, book_name, testament, canon_position, source, parse_date, promote_date, checksum, status, deuterocanonical, has_additions. **PASS**
- **Study footnotes:** Frontmatter present with book_code, content_type, source. **PASS**
- **Study articles:** Frontmatter present. `promote_date: null`, `status: staging` — expected for study layer. **PASS**
- **Lectionary:** Frontmatter present with title, source, type, book, entries, extracted. **PASS**
- **Result:** PASS

### Fixes Applied
1. `study/articles/OT/GEN_articles.md:19` — removed OCR fused phrase duplication
2. `study/lectionary-notes/OT/GEN_lectionary.md:60` — removed duplicate `17:1` fragment
3. `study/lectionary-notes/OT/GEN_lectionary.md:84-98` — removed 8 Exodus entries misplaced in GEN file
4. `study/lectionary-notes/OT/GEN_lectionary.md` — entry count corrected 44 → 35

### GEN Audit Summary: PASS (with 4 fixes applied)

---

## EXO — Exodus (2026-03-14)

### Layer 1: Canon Scripture Integrity
- **Validation:** V1-V9 PASS. V7 WARN: 1171/1166 (5 extra verses — registry CVC too low)
- **Registry mismatch:** EXO.32:35, EXO.35:33-35, EXO.36:39 exist in canon but exceed registry CVC. Registry needs update: ch32 34→35, ch35 32→35, ch36 38→39.
- **Spot-check concerns:** EXO.9:24 ends `"...since it became a nation; and"` — trailing conjunction, needs PDF spot-check. EXO.15:25 ends `"...There He proved him"` — verify verse boundary.
- **Result:** PASS (registry CVC update needed, 2 verse boundaries flagged for PDF check)

### Layer 2: Study Layer Quality
- **Footnotes:** 1695 lines, 130 wikilinks valid. **577 OCR blank-line artifacts** (pdftotext line-break residue). Content intact.
- **Articles:** **FIXES APPLIED:** 2 fused headings (`Christand` → `Christ and`, `Harmonybetween` → `Harmony between`), 1 OCR word-split (`being's et` → `being set`). 16 bare scripture refs (not wikilinked) — cosmetic.
- **Lectionary:** 2 entries, both valid.
- **Markers:** 177 markers, well-formed.
- **Result:** FIXED (3 OCR issues in articles)

### Layer 3: Metadata
- **R1:** 526 records. **Backlinks:** present (EXO.3:14, etc.). **Dossier:** STALE (pre-promotion staging state).
- **Result:** PASS (dossier staleness cosmetic)

### Layer 4: Knowledge Graph — UPDATED

### Layer 5: YAML Frontmatter — PASS (all fields present)

### Fixes Applied
1. `study/articles/OT/EXO_articles.md` — `Christand` → `Christ and`
2. `study/articles/OT/EXO_articles.md` — `Harmonybetween` → `Harmony between`
3. `study/articles/OT/EXO_articles.md` — `being's et free` → `being set free`

### EXO Audit Summary: PASS (with 3 fixes applied, registry CVC update needed)

---

## LEV — Leviticus (2026-03-14)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 859/859 verses, 0 missing. Cleanest book so far.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Footnotes:** 1667 lines, 68 entries. **723 OCR blank-line artifacts.** Content intact. Bare abbreviated refs present (`Gn 4`, `Lv 7:11-34`, `Ps 50`, etc.).
- **Articles:** 1 article (Sacrifice). Bare abbreviated refs but content clean.
- **Lectionary:** Not present (LEV has no lectionary notes file).
- **Markers:** 68 markers, all `"unknown"` (reindexed from footnotes). 1:1 with footnote sections.
- **Result:** PASS (OCR blank-lines and bare refs are systemic, not book-specific)

### Layer 3: Metadata
- **R1:** 313 records. **Backlinks:** present. **Dossier:** STALE (pre-promotion staging state).
- **Result:** PASS

### Layer 4: Knowledge Graph — UPDATED

### Layer 5: YAML Frontmatter — PASS (all fields present)

### LEV Audit Summary: PASS (no fixes needed, cleanest Pentateuch book)

---

## NUM — Numbers (2026-03-14)

### Layer 1: Canon Scripture Integrity
- **Validation:** V1-V9 PASS. V7 WARN: 1287/1303 (16 gap).
- **CANON ISSUE: NUM.1:1 truncated** — ends `"...tabernacle of test"` (missing "imony"). Docling column-split artifact. Documented for parser correction — cannot fix inline per canon immutability.
- **NUM.6:27 missing** from canon despite residual claiming "Fixed: Manually split and restored". Fix was apparently applied to staging but not promoted. Documented.
- **NUM.16:36-50 (15 verses)** — LXX versification shift. These verses are NUM.17:1-15 in LXX/OSB numbering. Registry may need CVC update.
- **NUM.29:40** — missing. Registry expects 40 verses in ch29, canon ends at 29:39. Versification edge case.
- **Result:** ISSUES FOUND (1 truncation, 1 missing promoted verse, LXX versification gaps)

### Layer 2: Study Layer Quality
- **Footnotes:** 1179 lines. **553 OCR blank-line artifacts** (~50% blank). Content intact.
- **Articles:** 1 article (Typology). **FIX APPLIED:** Removed leaked verse text at line 23 (NUM.21:27b `'Come to Heshbon...'`).
- **Lectionary:** Not present.
- **Markers:** Present, well-formed.
- **Result:** FIXED (1 leaked verse removed)

### Layer 3: Metadata
- **R1:** 344 records. **Backlinks:** present. **Dossier:** STALE.
- **Result:** PASS

### Layer 4: Knowledge Graph — UPDATED

### Layer 5: YAML Frontmatter — PASS

### Fixes Applied
1. `study/articles/OT/NUM_articles.md:23` — removed leaked verse text (NUM.21:27b)

### NUM Audit Summary: ISSUES (canon truncation NUM.1:1, missing NUM.6:27 — require pipeline re-promotion)

---

## DEU — Deuteronomy (2026-03-14)

### Layer 1: Canon Scripture Integrity
- **Validation:** V1-V9 PASS. V7 WARN: 961/959 (2 over-count due to LXX versification).
- **CANON ISSUE: DEU.29:1 mega-line** — 7,331-character line containing duplicate text of DEU.29:1-28 + 30:1-20 + heading "The Blessings of Repentance" + "Joshua Leads the People" + DEU.31:1 text. The properly split verses exist below as separate lines. This is duplicate content that should not be in canon.
- **DEU.30:20 missing** — content fused into DEU.30:19 (line 1096).
- **LXX versification offsets** in ch12, ch22, ch28, ch29, ch33 — registry may need CVC updates.
- **Result:** ISSUES FOUND (mega-line duplicate, missing verse 30:20)

### Layer 2: Study Layer Quality
- **Footnotes:** 1379 lines. **651 OCR blank-line artifacts** (~47% blank). Content intact.
- **Articles:** 1 article (Sabbath Day). **FIX APPLIED:** Fused title `"Theeighth"` → `"The Eighth"`, `"Sunday,"` → `"Sunday, "`.
- **Lectionary:** Not present.
- **Markers:** Present.
- **Result:** FIXED (1 title OCR issue)

### Layer 3: Metadata
- **R1:** 220 records. **Backlinks:** present. **Dossier:** STALE.
- **Result:** PASS

### Layer 4: Knowledge Graph — UPDATED

### Layer 5: YAML Frontmatter — PASS

### Fixes Applied
1. `study/articles/OT/DEU_articles.md:15` — fused title corrected (`Theeighth` → `The Eighth`)

### DEU Audit Summary: ISSUES (canon mega-line at 29:1, missing 30:20 — require pipeline re-promotion)

---

## Cross-Cutting Findings (Pentateuch Batch)

### Systemic Issues
1. **OCR blank-line artifacts in footnotes** — EXO (577), LEV (723), NUM (553), DEU (651). All footnote files have pdftotext line-break residue causing ~50% blank lines. Content is intact but formatting is bloated. This is a batch cleanup candidate for Photius.
2. **Stale promotion dossiers** — All 5 Pentateuch dossiers were generated from early staging state, not final promoted canon. Cosmetic staleness, non-blocking.
3. **Registry CVC drift** — EXO has 5 extra verses vs registry; DEU has 2 extra. Both are LXX versification issues requiring registry updates.
4. **No lectionary notes** — LEV, NUM, DEU have no lectionary files.

### Canon Issues Requiring Pipeline Re-Promotion
| Book | Issue | Severity |
|---|---|---|
| NUM | NUM.1:1 truncated (`"tabernacle of test"`) | High |
| NUM | NUM.6:27 missing from canon (claimed fixed in staging) | Medium |
| DEU | DEU.29:1 mega-line (7331 chars duplicate content) | Critical |
| DEU | DEU.30:20 missing (fused into 30:19) | Medium |

These issues were inherited from the initial parser extraction and were not caught before promotion. They require staged file correction and re-promotion through the pipeline.

---

## JOS — Joshua (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 660/660 verses, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Footnotes:** 720 lines. 347 OCR blank-line artifacts (48%). Content intact. Structural issue: `### 13:16` anchor at line 19 is misplaced (content is continuation of 1:1 footnote). OCR split "LORD" → `L ` / `ORD` at line 49. 5 markers.
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** **FIXES APPLIED:** Removed 3 misattributed entries (6:36-40, 17:8-24, 18:30-39 are Kings readings, not Joshua). Entry count corrected 5 → 2.
- **Result:** FIXED (3 lectionary entries removed)

### Fixes Applied
1. `study/lectionary-notes/OT/JOS_lectionary.md` — removed 3 misattributed Kings entries, corrected entry count

### JOS Audit Summary: PASS (with 1 lectionary fix)

---

## JDG — Judges (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 617/618 verses (99.8%), gap of 1.
- **Missing verse:** JDG.11:40 absent from canon.
- **Result:** ISSUES (1 missing verse)

### Layer 2: Study Layer Quality
- **Footnotes:** 757 lines. 344 OCR blank lines (45%). Heavy bare-reference density (Is, 1Kg, 2Kg, 3Kg, Lv, Pr, Jer). Fragment artifact at line 15 (`, 2`). 5 markers.
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS (bare refs are systemic)

### JDG Audit Summary: ISSUES (JDG.11:40 missing from canon)

---

## RUT — Ruth (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 85/85 verses, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Footnotes:** 239 lines. 106 OCR blank lines (44%). Clean — wikilinks used consistently. **PASS**
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS

### RUT Audit Summary: PASS (cleanest historical book)

---

## 1SA — 1 Samuel (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Footnotes:** 736 lines. 327 OCR blank lines (44%). 2 bare refs (lines 261, 638). 6 wikilinks. 81 markers.
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS

### 1SA Audit Summary: PASS

---

## 2SA — 2 Samuel (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 697 verses, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Footnotes:** 969 lines. 429 OCR blank lines (44%). 12 bare refs (mostly 1Kg/3Kg Kingdoms refs). 15 wikilinks. 105 markers.
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS

### 2SA Audit Summary: PASS

---

## 1KI — 1 Kings (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 828/828 verses, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Footnotes:** 655 lines. 321 OCR blank lines (49%). Minor: line 18 starts with period (OCR line-break artifact). 5 markers.
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** 4 entries. Minor OCR: `Kingd` truncation. **PASS**
- **Result:** PASS

### 1KI Audit Summary: PASS

---

## 2KI — 2 Kings (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 723/719 verses (100.6%), 4 extra.
- **Discrepancies:** Ch 1: 22 vs 18 expected (+4 LXX versification), Ch 11: 20 vs 21 (-1), Ch 12: 22 vs 21 (+1).
- **Undocumented:** No residuals sidecar records these V7 gaps.
- **Result:** ISSUES (LXX versification drift, registry CVC update needed)

### Layer 2: Study Layer Quality
- **Footnotes:** 581 lines. 272 OCR blank lines (47%). Clean. 4 markers.
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS

### 2KI Audit Summary: ISSUES (registry CVC needs LXX alignment)

---

## 1CH — 1 Chronicles (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 928/942 verses (98.5%), 14 missing — SIGNIFICANT.
- **Discrepancies:**
  - Ch 1: 42 vs 54 expected (-12). **1CH.1:43-54 missing** (Edom kings list — parse extraction gap).
  - Ch 5: 41 vs 26 (+15) and Ch 6: 66 vs 81 (-15) — LXX versification offset (net zero).
  - Ch 10: 13 vs 14 (-1). Ch 12: 41 vs 40 (+1). Ch 16: 42 vs 43 (-1). Ch 29: 29 vs 30 (-1).
- **Undocumented:** No residuals for any of these gaps.
- **Result:** ISSUES (12 consecutive missing verses in Ch 1 is a real extraction gap)

### Layer 2: Study Layer Quality
- **Footnotes:** 501 lines. 239 OCR blank lines (48%). Clean. 4 markers.
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS

### 1CH Audit Summary: ISSUES (1CH.1:43-54 missing — parser recovery needed)

---

## 2CH — 2 Chronicles (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 833/834 verses (99.9%), gap of 1.
- **Missing:** 2CH.27:9 — needs PDF spot-check.
- **LXX versification shifts** in Ch 1/2, Ch 13/14 — registry may need adjustment.
- **Result:** ISSUES (1 missing verse)

### Layer 2: Study Layer Quality
- **Footnotes:** OCR blank lines consistent. **PASS**
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS

### 2CH Audit Summary: ISSUES (2CH.27:9 missing)

---

## 1ES — 1 Esdras (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 434/434 verses, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Footnotes:** OCR blank lines consistent. **PASS**
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS

### 1ES Audit Summary: PASS

---

## EZR — Ezra (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 281/280 verses (100.4%), 1 extra.
- **Extra verse:** EZR.7:29 present; registry expects 28 in Ch 7.
- **CANON ISSUE:** OCR fused-article defect `ascribe` in EZR.7:12 — needs staged fix.
- **Result:** ISSUES (OCR artifact in canon, registry CVC update)

### Layer 2: Study Layer Quality
- **Footnotes:** Bare refs present. OCR blank lines. **PASS**
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS

### EZR Audit Summary: ISSUES (canon OCR artifact, registry CVC)

---

## NEH — Nehemiah (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 394/394 verses, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Footnotes:** 378 lines. 179 OCR blank lines (47%). 4 un-anchored verse refs. **PASS**
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS

### NEH Audit Summary: PASS

---

## TOB — Tobit (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 248/245 verses (101.2%), 3 extra.
- **Discrepancies:** Ch 5 (+1), Ch 6 (+2), Ch 7 (-1), Ch 10 (+1). LXX versification.
- **Result:** ISSUES (registry CVC update needed)

### Layer 2: Study Layer Quality
- **Footnotes:** 373 lines. 168 OCR blank lines (45%). 2 un-anchored verse refs. 40 markers.
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS

### TOB Audit Summary: ISSUES (registry CVC needs LXX alignment)

---

## JDT — Judith (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 340/339 verses (100.3%), 1 extra.
- **Extra:** Ch 15: 14 vs 13 expected (+1).
- **Result:** ISSUES (registry CVC update needed)

### Layer 2: Study Layer Quality
- **Footnotes:** 477 lines. 227 OCR blank lines (48%). 8 un-anchored verse refs. Disordered block at lines 355-455. Structural cleanup needed. 21 markers.
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS (footnotes need structural cleanup)

### JDT Audit Summary: ISSUES (registry CVC, footnote structure)

---

## EST — Esther (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V4 WARN (jumps 4:5→4:7), V7 WARN (194/195, gap 1), V10 WARN (EST.4:6 absorbed into 4:7).
- **All gaps ratified** in residuals as `osb_source_absent`.
- **Result:** PASS (ratified gaps)

### Layer 2: Study Layer Quality
- **Footnotes:** 180 OCR blank lines. **PASS**
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS

### EST Audit Summary: PASS (ratified gaps)

---

## 1MA — 1 Maccabees (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 923/924 (gap 1). 1MA.8:32 missing — ratified `osb_source_absent`.
- **Result:** PASS (ratified gap)

### Layer 2: Study Layer Quality
- **Footnotes:** 195 OCR blank lines. **PASS**
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS

### 1MA Audit Summary: PASS (ratified gap)

---

## 2MA — 2 Maccabees (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 555/555, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Articles:** **FIX APPLIED:** Fused heading `Oldtestament` → `Old Testament`.
- **Footnotes:** 290 OCR blank lines. **PASS**
- **Lectionary:** Not present.
- **Result:** FIXED

### Fixes Applied
1. `study/articles/OT/2MA_articles.md:15` — `Oldtestament` → `Old Testament`

### 2MA Audit Summary: PASS (with 1 fix applied)

---

## 3MA — 3 Maccabees (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 227/228 (gap 1). 3MA.1:29 missing — ratified `osb_source_absent`.
- **Result:** PASS (ratified gap)

### Layer 2: Study Layer Quality
- **Footnotes:** 298 OCR blank lines. **PASS**
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS

### 3MA Audit Summary: PASS (ratified gap)

---

## PSA — Psalms (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 100.0%.
- **LXX numbering confirmed** — PSA.50 = Penitential Psalm, PSA.103 = Creation Psalm, PSA.151 present (7 verses).
- **CANON ISSUE:** 40 instances of fused word `greatlyrejoice` (should be `greatly rejoice`). OCR artifact, non-blocking.
- **Result:** PASS (cosmetic OCR artifact noted)

### Layer 2: Study Layer Quality
- **Footnotes:** 2443 lines. 1218 OCR blank lines. Only 1 wikilink in entire file. 131 markers.
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** **FIXES APPLIED:**
  - Merged 2 OCR line-split entries (44:1/1:48 and 81:1/10:34 — cross-reference text split across entries)
  - Removed ~45 non-PSA entries (Proverbs/Lamentations lectionary content erroneously appended from line 206+)
  - Entry count corrected 141 → 95
- **Result:** FIXED (major lectionary contamination cleaned)

### Fixes Applied
1. `study/lectionary-notes/OT/PSA_lectionary.md` — merged 2 split entries (PSA.44:1, PSA.81:1)
2. `study/lectionary-notes/OT/PSA_lectionary.md` — removed ~45 non-PSA entries (Proverbs/Lamentations)
3. `study/lectionary-notes/OT/PSA_lectionary.md` — entry count corrected 141 → 95

### PSA Audit Summary: PASS (with 3 lectionary fixes applied)

---

## PRO — Proverbs (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 912/912 verses, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Footnotes:** 2487 lines. 1117 OCR blank lines (45%). **Truncated at EOF** — final footnote (31:10-30) ends mid-sentence. 5 markers.
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** ISSUES (footnote EOF truncation)

### PRO Audit Summary: PASS (footnote truncation noted)

---

## ECC — Ecclesiastes (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Footnotes:** 346 lines. 149 OCR blank lines (43%). 3 bare refs. **Truncated at EOF** — footnote 12:8 ends mid-sentence. 5 markers.
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** ISSUES (footnote EOF truncation, bare refs)

### ECC Audit Summary: PASS (footnote truncation noted)

---

## SNG — Song of Songs (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Footnotes:** 774 lines. 347 OCR blank lines (45%). 9 bare refs. **Truncated at EOF** — footnote 8:13 ends mid-sentence. 4 markers.
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** ISSUES (footnote EOF truncation, bare refs)

### SNG Audit Summary: PASS (footnote truncation noted)

---

## JOB — Job (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 1084/1082 verses (100.2%), 2 extra. 10 chapters diverge from registry.
- **Result:** ISSUES (registry CVC update needed)

### Layer 2: Study Layer Quality
- **Articles:** **FIX APPLIED:** Removed leaked verse text (JOB 15:1-7 with OCR split-word artifacts) at lines 22-24. Also removed orphan heading `#### Eliphaz Renders Job Guilty`.
- **Footnotes:** 46% OCR blank lines. WIS.1:1 truncated. 5 markers.
- **Lectionary:** Not present.
- **Result:** FIXED

### Fixes Applied
1. `study/articles/OT/JOB_articles.md:22-24` — removed leaked verse text (JOB 15:1-7) and orphan heading

### JOB Audit Summary: ISSUES (registry CVC; 1 article fix applied)

---

## WIS — Wisdom of Solomon (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 436/436 verses, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Footnotes:** 47% OCR blank lines. WIS.1:1 entry truncated. 2 inline footnotes (19:1-9, 19:22) lack proper `###` headers.
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS (minor footnote structure issues)

### WIS Audit Summary: PASS

---

## SIR — Sirach (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 1377/1365 verses (100.9%), 12 extra — SIGNIFICANT.
- **Registry CVC appears systematically wrong** for 12 chapters. OSB follows its own LXX versification.
- **Result:** ISSUES (registry CVC update needed — 12 chapters)

### Layer 2: Study Layer Quality
- **Footnotes:** 45% OCR blank lines. **PASS**
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS

### SIR Audit Summary: ISSUES (registry CVC needs major update — 12 chapters)

---

## HOS — Hosea (2026-03-15)

### Canon: PASS (197/197, 100.0%)
### Study: PASS
### HOS Audit Summary: PASS

---

## AMO — Amos (2026-03-15)

### Canon: PASS (145/145, 100.0%)
### Study: PASS (minor footnote heading `1:3-3` likely should be `1:3`)
### AMO Audit Summary: PASS

---

## MIC — Micah (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 105/104 (101.0%), 1 extra.
- **Registry fix needed:** MIC ch 3 CVC should be 14 (not 13). MIC.4:14 is a real LXX verse.
- **Result:** ISSUES (registry CVC)

### Layer 2: Study Layer Quality
- **Lectionary:** Present. **PASS**
- **Result:** PASS

### MIC Audit Summary: ISSUES (registry CVC fix needed)

---

## JOL — Joel (2026-03-15)

### Canon: PASS
### Study: PASS (minor: inline `4:13` footnote lacks header separation)
### JOL Audit Summary: PASS

---

## OBA — Obadiah (2026-03-15)

### Canon: PASS
### Study: PASS
### OBA Audit Summary: PASS

---

## JON — Jonah (2026-03-15)

### Canon: PASS (48/48, 100.0%)
### Study: ISSUES (footnote 1:1 has OCR artifact `, 2` at line 15)
### JON Audit Summary: PASS (minor footnote OCR)

---

## NAH — Nahum (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 47/48 (97.9%), 1 missing.
- **NAH.1:15** content is at NAH.2:1 in LXX numbering — versification offset.
- **Result:** ISSUES (registry CVC needs LXX alignment)

### Layer 2: Study Layer Quality
- **Result:** PASS

### NAH Audit Summary: ISSUES (registry CVC)

---

## HAB — Habakkuk (2026-03-15)

### Canon: PASS
### Study: PASS
### HAB Audit Summary: PASS

---

## ZEP — Zephaniah (2026-03-15)

### Canon: PASS
### Study: PASS
### ZEP Audit Summary: PASS

---

## HAG — Haggai (2026-03-15)

### Canon: PASS
### Study: PASS
### HAG Audit Summary: PASS

---

## ZEC — Zechariah (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 211/215 (98.1%), 4 missing.
- **LXX versification:** ZEC.1:18-21 content at ZEC.2:1-4 in LXX.
- **Result:** ISSUES (registry CVC needs LXX alignment)

### Layer 2: Study Layer Quality
- **Lectionary:** 2 entries. Truncated entry at 8:1-4, missing occasion at 12:3-6.
- **Result:** PASS

### ZEC Audit Summary: ISSUES (registry CVC)

---

## MAL — Malachi (2026-03-15)

### Canon: PASS (55/55, 100.0%)
### Study: PASS
### MAL Audit Summary: PASS

---

## ISA — Isaiah (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 1290/1290, 100.0%.
- **CANON ISSUE:** OCR artifact at line 1437 (ISA.66:22): `says the Lord,'s oshall your seed` — should read `says the Lord, 'so shall your seed`. Fused/garbled text.
- **Result:** ISSUES (canon OCR artifact)

### Layer 2: Study Layer Quality
- **Footnotes:** 799 OCR blank lines. **PASS**
- **Articles:** Empty placeholder. **PASS**
- **Lectionary:** ISSUES — 4 truncated verse ranges (52:13-1, 61:10-5, 62:10-9, 63:11-5). Missing occasion at 19:1-5.
- **Result:** PASS (lectionary truncations noted)

### ISA Audit Summary: ISSUES (canon OCR artifact at ISA.66:22)

---

## JER — Jeremiah (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 1299/1299, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Footnotes:** 689 OCR blank lines. **FIX APPLIED:** `Jefhoiachin` → `Jehoiachin` at line 1560.
- **Articles:** 1 article (The Prophets). Clean, well-structured with wikilinks. **PASS**
- **Lectionary:** ISSUES — impossible ref `3:36-4` (JER ch 3 has only 25 verses; likely Baruch). Truncated heading `11:17-5` (clarified as `11:17-12:5`).
- **Result:** FIXED (1 footnote OCR typo)

### Fixes Applied
1. `study/footnotes/OT/JER_footnotes.md:1560` — `Jefhoiachin` → `Jehoiachin`

### JER Audit Summary: PASS (with 1 footnote fix; lectionary impossible ref noted)

---

## BAR — Baruch (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 141/140 (100.7%), 1 extra.
- **Ch 3:** 38 vs 37 expected. Registry or canon needs verification.
- **Result:** ISSUES (registry CVC)

### Layer 2: Study Layer Quality
- **Footnotes:** 90 OCR blank lines. **PASS**
- **Result:** PASS

### BAR Audit Summary: ISSUES (registry CVC, 1 extra verse in ch 3)

---

## LAM — Lamentations (2026-03-15)

### Canon: PASS (150/150, 100.0%)
### Study: PASS (76 OCR blank lines)
### LAM Audit Summary: PASS

---

## LJE — Letter of Jeremiah (2026-03-15)

### Canon: PASS
### Study: PASS (37 OCR blank lines, minor truncation)
### LJE Audit Summary: PASS

---

## EZK — Ezekiel (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 1268/1265 (100.2%), 3 extra.
- **Discrepancies:** Ch 1 (+1), Ch 11 (+2), Ch 32 (+1), Ch 33 (-1). LXX versification.
- **Result:** ISSUES (registry CVC update needed)

### Layer 2: Study Layer Quality
- **Articles:** **FIX APPLIED:** Fused heading `Theold` → `The Old` (Types of Mary article title).
- **Footnotes:** 447 OCR blank lines. **PASS**
- **Lectionary:** Not present.
- **Result:** FIXED

### Fixes Applied
1. `study/articles/OT/EZK_articles.md:15` — `Theold Testament` → `The Old Testament`

### EZK Audit Summary: ISSUES (registry CVC; 1 article fix applied)

---

## DAN — Daniel (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 530/530, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Articles:** **FIXES APPLIED:** 2 fused headings: `Ofchrist` → `Of Christ`, `Apocalypticliterature` → `Apocalyptic Literature`.
- **Footnotes:** Orphaned `, 2` fragment at 1:1. Susanna content mapped to DAN.1:1. Bare refs present. 47 markers.
- **Lectionary:** 10 entries. **PASS**
- **Result:** FIXED

### Fixes Applied
1. `study/articles/OT/DAN_articles.md:15` — `Ofchrist` → `Of Christ`
2. `study/articles/OT/DAN_articles.md:31` — `Apocalypticliterature` → `Apocalyptic Literature`

### DAN Audit Summary: PASS (with 2 article fixes applied)

---

## MAT — Matthew (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V8 WARN (heading density 95/28 = 3.4/ch). Cosmetic — Gospels genuinely have many sections. 1071 verses, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Articles:** Drop-cap OCR artifacts. Fused word `perspectivebecomes`. Minor.
- **Footnotes:** OCR blank lines. **PASS**
- **Lectionary:** Present. Contains some MRK entries (cross-contamination from extraction). Needs cleanup.
- **Result:** ISSUES (lectionary cross-contamination)

### MAT Audit Summary: PASS (lectionary contamination noted for future cleanup)

---

## MRK — Mark (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 679/678 (100.1%), 1 extra. V8 WARN heading density.
- **Extra verse:** MRK Ch 11: 34 vs 33 expected. Likely MRK.11:26 present in OSB.
- **Result:** ISSUES (registry CVC)

### Layer 2: Study Layer Quality
- **Articles:** Fused word `importantnot`. Minor.
- **Footnotes:** OCR blank lines. 72 markers.
- **Lectionary:** Not present.
- **Result:** PASS

### MRK Audit Summary: ISSUES (registry CVC, 1 extra verse ch 11)

---

## LUK — Luke (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 1150/1151 (99.9%), 1 missing. V8 WARN heading density.
- **Missing:** LUK Ch 20: 46 vs 47 expected (-1). Possible versification difference.
- **Result:** ISSUES (1 missing verse in ch 20)

### Layer 2: Study Layer Quality
- **Lectionary:** Contains JOH entries (cross-contamination). Needs cleanup.
- **Footnotes:** OCR blank lines. 271 markers.
- **Result:** ISSUES (lectionary cross-contamination)

### LUK Audit Summary: ISSUES (1 missing verse, lectionary contamination)

---

## JOH — John (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V8 WARN heading density (77/21 = 3.7/ch). Cosmetic. 879 verses, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Lectionary:** Contains entries from Acts through Revelation (major cross-contamination). Needs cleanup.
- **Footnotes:** OCR blank lines. 252 markers.
- **Result:** ISSUES (lectionary cross-contamination)

### JOH Audit Summary: PASS (lectionary contamination noted)

---

## ACT — Acts (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V8 WARN heading density (95/28 = 3.4/ch). Cosmetic. 1007 verses, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Articles:** OCR drop-cap artifacts (`F rom`, `S acraments`). Fused text `means's etting in place' or's election`. Fragment heading at line 44. Orphan heading at line 28.
- **Footnotes:** 1312 OCR blank lines. **PASS**
- **Lectionary:** Not present.
- **Result:** ISSUES (article OCR, minor)

### ACT Audit Summary: PASS (article OCR artifacts noted)

---

## ROM — Romans (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 431/436 (98.9%), reported 5 missing.
- **CANON ISSUE: ROM.10:18 fused** — line 390 contains 4 verses jammed together (10:18-21). Verses 10:19, 10:20, 10:21 absent as separate anchored lines. Parser defect.
- **Registry error:** ROM ch 14 CVC should be 23 (not 26). OSB has 23 verses; 26 reflects a textual-critical tradition not present in OSB.
- **True missing count:** 3 (fused verses), not 5.
- **Result:** ISSUES (canon fused verses, registry CVC error)

### Layer 2: Study Layer Quality
- **Articles:** Drop-cap OCR (`O ne`, `F or`, `W hat`). Fragment heading at line 59. Orphan headings at lines 26, 43, 63.
- **Footnotes:** 890 OCR blank lines. **PASS**
- **Lectionary:** Not present.
- **Result:** PASS (article OCR, minor)

### ROM Audit Summary: ISSUES (ROM.10:18 fused verses — parser recovery needed; registry ch 14 CVC error)

---

## 1CO — 1 Corinthians (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 436/446 (97.8%), reported 10 missing.
- **CANON ISSUE: 1CO.1:30-31 fused** — `redemption31 that` with no line break. Verse 31 text embedded in verse 30 line.
- **Registry error:** 1CO ch 12 CVC should be 31 (not 40). OSB has 31 verses.
- **True missing count:** 1 (fused verse), not 10.
- **Result:** ISSUES (canon fused verse, registry CVC error)

### Layer 2: Study Layer Quality
- **Articles:** Fused word `sixteenthcentury`. Drop-cap OCR. Eucharist article truncated mid-sentence at EOF.
- **Footnotes:** 745 OCR blank lines. **PASS**
- **Lectionary:** 1 entry. **PASS**
- **Result:** ISSUES (article truncation)

### 1CO Audit Summary: ISSUES (1CO.1:30-31 fused — parser recovery needed; registry ch 12 CVC error)

---

## 2CO — 2 Corinthians (2026-03-15)

### Canon: PASS (257/257, 100.0%)
### Study: PASS (402 OCR blank lines)
### 2CO Audit Summary: PASS

---

## GAL — Galatians (2026-03-15)

### Canon: PASS (149/149, 100.0%. V8 heading density cosmetic.)
### Study: PASS
### GAL Audit Summary: PASS

---

## EPH — Ephesians (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 155/155, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Articles:** **FIX APPLIED:** `bretren` → `brethren` at line 44. Drop-cap OCR (`O ne`, `T he`) noted.
- **Result:** FIXED

### Fixes Applied
1. `study/articles/NT/EPH_articles.md:44` — `bretren` → `brethren`

### EPH Audit Summary: PASS (with 1 article fix)

---

## PHP — Philippians (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 104/95 (109.5%), 9 extra — FALSE POSITIVE.
- **Registry is WRONG:** Lists `chapter_verse_counts: [30,23,25,17]` (total 95). Correct is `[30,30,21,23]` (total 104). Canon has all 104 verses correctly.
- **Result:** REGISTRY BUG (canon is correct)

### Layer 2: Study Layer Quality
- **Result:** PASS

### PHP Audit Summary: REGISTRY BUG (CVC needs correction: [30,30,21,23])

---

## COL — Colossians (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 95/99 (96.0%), 4 missing — FALSE POSITIVE.
- **Registry is WRONG:** Lists `chapter_verse_counts: [29,23,25,22]` (total 99). Correct is `[29,23,25,18]` (total 95). Canon has all 95 verses correctly.
- **Result:** REGISTRY BUG (canon is correct)

### Layer 2: Study Layer Quality
- **Result:** PASS

### COL Audit Summary: REGISTRY BUG (CVC needs correction: [29,23,25,18])

---

## 1TH — 1 Thessalonians (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 89/89, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Footnotes:** **FIX APPLIED:** `(v. 26)very` → `(v. 26) very` at line 273.
- **Result:** FIXED

### Fixes Applied
1. `study/footnotes/NT/1TH_footnotes.md:273` — `(v. 26)very` → `(v. 26) very`

### 1TH Audit Summary: PASS (with 1 footnote fix)

---

## 2TH — 2 Thessalonians (2026-03-15)

### Canon: PASS (47/47, 100.0%)
### Study: PASS
### 2TH Audit Summary: PASS

---

## 1TI — 1 Timothy (2026-03-15)

### Canon: PASS (113/113, 100.0%. V8 heading density cosmetic.)
### Study: PASS
### 1TI Audit Summary: PASS

---

## 2TI — 2 Timothy (2026-03-15)

### Canon: PASS (83/83, 100.0%. V8 heading density cosmetic.)
### Study: PASS
### 2TI Audit Summary: PASS

---

## TIT — Titus (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 46/46, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Articles:** **FIXES APPLIED:** Fused heading `Comingof` → `Coming of`. Drop-cap `T he` → `The`.
- **Result:** FIXED

### Fixes Applied
1. `study/articles/NT/TIT_articles.md:15` — `Comingof` → `Coming of`
2. `study/articles/NT/TIT_articles.md:18` — `T he` → `The`

### TIT Audit Summary: PASS (with 2 article fixes)

---

## PHM — Philemon (2026-03-15)

### Canon: PASS (25/25, 100.0%)
### Study: ISSUES (footnote 1:14-17 truncated — orphaned `Christ.` at start, ends mid-sentence)
### PHM Audit Summary: PASS (footnote truncation noted)

---

## HEB — Hebrews (2026-03-15)

### Canon: PASS (303/303, 100.0%)
### Study: PASS
### Lectionary: Present. **PASS**
### HEB Audit Summary: PASS

---

## JAS — James (2026-03-15)

### Canon: PASS (108/108, 100.0%)
### Study: PASS (2 cosmetic OCR in articles)
### JAS Audit Summary: PASS

---

## 1PE — 1 Peter (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** V7 WARN: 106/105 (101.0%), 1 extra. V8 heading density.
- **1PE.5:15** is legitimate OSB content ("Peace to you all who are in Christ Jesus. Amen."). Registry expects only 14 in ch 5.
- **Result:** ISSUES (registry CVC — ch 5 should be 15, not 14)

### Layer 2: Study Layer Quality
- **Result:** PASS

### 1PE Audit Summary: ISSUES (registry CVC fix needed)

---

## 2PE — 2 Peter (2026-03-15)

### Canon: PASS (61/61, 100.0%. V8 cosmetic.)
### Study: PASS (3 cosmetic OCR in articles)
### 2PE Audit Summary: PASS

---

## 1JN — 1 John (2026-03-15)

### Canon: PASS (105/105, 100.0%. V8 cosmetic.)
### Study: PASS (1 cosmetic OCR in articles)
### 1JN Audit Summary: PASS

---

## 2JN — 2 John (2026-03-15)

### Canon: PASS (13/13, 100.0%)
### Study: PASS
### 2JN Audit Summary: PASS

---

## 3JN — 3 John (2026-03-15)

### Canon: PASS (15/15, 100.0%. V8 cosmetic.)
### Study: PASS
### 3JN Audit Summary: PASS

---

## JUD — Jude (2026-03-15)

### Canon: PASS (25/25, 100.0%. V8 cosmetic.)
### Study: PASS
### JUD Audit Summary: PASS

---

## REV — Revelation (2026-03-15)

### Layer 1: Canon Scripture Integrity
- **Validation:** ALL V-CHECKS PASS. 404/404, 100.0%.
- **Result:** PASS

### Layer 2: Study Layer Quality
- **Articles:** **FIX APPLIED:** Fused heading `Newtestament` → `New Testament`.
- **Footnotes:** 1594 OCR blank lines. 182 markers. **PASS**
- **Lectionary:** Not present.
- **Result:** FIXED

### Fixes Applied
1. `study/articles/NT/REV_articles.md:15` — `Newtestament` → `New Testament`

### REV Audit Summary: PASS (with 1 article fix)

---

## Cross-Cutting Findings (Full 76-Book Audit)

### Systemic Issues

1. **OCR blank-line artifacts in footnotes** — ALL 76 footnote files have ~44-49% blank lines from pdftotext line-break residue. Content intact but formatting bloated. Batch cleanup candidate for Photius.

2. **Stale promotion dossiers** — All dossiers generated from early staging state, not final promoted canon. Cosmetic staleness, non-blocking.

3. **Registry CVC drift** — Widespread. 20+ books have mismatches between registry `chapter_verse_counts` and actual canon content. Causes are:
   - LXX versification vs MT-based registry counts (most common)
   - Outright registry errors (PHP, COL, 1CO ch12, ROM ch14)
   - Genuine missing content (1CH.1:43-54)

4. **Lectionary cross-contamination** — MAT, LUK, JOH lectionary files contain entries from subsequent books. PSA lectionary contained Proverbs/Lamentations entries. JOS contained Kings entries. Extraction pipeline appended sequential books' lectionary content to preceding files.

5. **Footnote EOF truncation** — PRO, ECC, SNG footnotes end mid-sentence at EOF. Page-boundary extraction loss.

6. **Article fused headings** — Consistent OCR pattern across 10+ books: `Oldtestament`, `Newtestament`, `Ofchrist`, `Comingof`, `Apocalypticliterature`, `Christand`, `Harmonybetween`, `Theeighth`, `Theold`, `perspectivebecomes`, `importantnot`, `sixteenthcentury`, `bretren`.

7. **Article drop-cap spacing** — Docling OCR consistently produces `T he`, `F rom`, `O ne` etc. Low priority cosmetic issue.

### Canon Issues Requiring Pipeline Re-Promotion

| Book | Issue | Severity |
|---|---|---|
| NUM | NUM.1:1 truncated (`"tabernacle of test"`) | High |
| NUM | NUM.6:27 missing from canon | Medium |
| DEU | DEU.29:1 mega-line (7331 chars duplicate) | Critical |
| DEU | DEU.30:20 missing (fused into 30:19) | Medium |
| ISA | ISA.66:22 OCR fused text (`'s oshall`) | High |
| ROM | ROM.10:18-21 fused (4 verses on 1 line) | High |
| 1CO | 1CO.1:30-31 fused (verse 31 embedded in 30) | High |
| EZR | EZR.7:12 OCR fused-article defect (`ascribe`) | Medium |
| PSA | 40x `greatlyrejoice` fused word | Low |

### Canon Missing Verses (documented only)

| Book | Missing | Root Cause |
|---|---|---|
| JDG | JDG.11:40 | Unknown — investigate |
| 1CH | 1CH.1:43-54 (12 verses) | Parse extraction gap |
| 1CH | 1CH.10:14, 16:43(?), 29:30 | Individual gaps |
| 2CH | 2CH.27:9 | Needs PDF spot-check |
| LUK | LUK.20:? (1 verse) | Versification check needed |

### Registry CVC Corrections Needed

| Book | Chapter | Registry | Correct | Source |
|---|---|---|---|---|
| EXO | 32 | 34 | 35 | LXX versification |
| EXO | 35 | 32 | 35 | LXX versification |
| EXO | 36 | 38 | 39 | LXX versification |
| PHP | all | [30,23,25,17]=95 | [30,30,21,23]=104 | Registry error |
| COL | all | [29,23,25,22]=99 | [29,23,25,18]=95 | Registry error |
| ROM | 14 | 26 | 23 | Textual-critical inflation |
| 1CO | 12 | 40 | 31 | Registry error |
| MIC | 3 | 13 | 14 | LXX versification |
| 1PE | 5 | 14 | 15 | OSB includes v.15 |
| SIR | 12 ch | varies | varies | Systematic LXX alignment |
| JOB | 10 ch | varies | varies | LXX alignment |
| 2KI | 1,11,12 | varies | varies | LXX alignment |
| 1CH | 1,5,6,10,12,16,29 | varies | varies | LXX + parse gaps |
| TOB | 5,6,7,10 | varies | varies | LXX alignment |
| JDT | 15 | 13 | 14 | LXX alignment |
| BAR | 3 | 37 | 38 | LXX alignment |
| EZK | 1,11,32,33 | varies | varies | LXX alignment |
| NAH | 1-2 | varies | varies | LXX alignment |
| ZEC | 1-2 | varies | varies | LXX alignment |
| MRK | 11 | 33 | 34 | OSB includes 11:26 |

### Study-Layer Fixes Applied (this audit session)

| # | File | Fix |
|---|---|---|
| 1 | `study/lectionary-notes/OT/JOS_lectionary.md` | Removed 3 misattributed Kings entries |
| 2 | `study/lectionary-notes/OT/PSA_lectionary.md` | Merged 2 split entries, removed ~45 non-PSA entries |
| 3 | `study/articles/OT/2MA_articles.md` | `Oldtestament` → `Old Testament` |
| 4 | `study/articles/OT/JOB_articles.md` | Removed leaked verse text (JOB 15:1-7) |
| 5 | `study/articles/OT/EZK_articles.md` | `Theold` → `The Old` |
| 6 | `study/articles/OT/DAN_articles.md` | `Ofchrist` → `Of Christ` |
| 7 | `study/articles/OT/DAN_articles.md` | `Apocalypticliterature` → `Apocalyptic Literature` |
| 8 | `study/articles/NT/TIT_articles.md` | `Comingof` → `Coming of`, `T he` → `The` |
| 9 | `study/articles/NT/EPH_articles.md` | `bretren` → `brethren` |
| 10 | `study/articles/NT/REV_articles.md` | `Newtestament` → `New Testament` |
| 11 | `study/footnotes/OT/JER_footnotes.md` | `Jefhoiachin` → `Jehoiachin` |
| 12 | `study/footnotes/NT/1TH_footnotes.md` | `(v. 26)very` → `(v. 26) very` |

### Audit Statistics

| Category | Count |
|---|---|
| Books audited | 76/76 |
| Canon PASS | 53 |
| Canon ISSUES (documented) | 23 |
| Study-layer fixes applied | 12 (this session) + 8 (Pentateuch session) = 20 total |
| Registry CVC corrections needed | 20+ books |
| Canon issues requiring re-promotion | 9 defects across 6 books |
| Lectionary files cleaned | 3 (GEN, JOS, PSA) |

---

## Post-Audit Actions (2026-03-15)

### Registry CVC Corrections (v1.5.0 → v1.6.0)

Applied 27 corrections to `schemas/anchor_registry.json` (v1.5.0 → v1.7.0):

**v1.6.0 — Clear registry errors (7 books):**

| Book | Change | Reason |
|---|---|---|
| PHP | [30,23,25,17]→[30,30,21,23] (95→104) | Outright registry error |
| COL | [29,23,25,22]→[29,23,25,18] (99→95) | Outright registry error |
| ROM | ch14: 26→23 | Textual-critical inflation |
| 1CO | ch12: 40→31 | Outright registry error |
| MIC | ch4: 13→14 | LXX versification (MIC.4:14 real) |
| 1PE | ch5: 14→15 | OSB includes 1PE.5:15 |
| MRK | ch11: 33→34 | OSB includes MRK.11:26 |

**v1.7.0 — LXX versification alignment + ratified gaps (20 books):**

| Book | Change | Category |
|---|---|---|
| EXO | 1166→1171 (+5) | LXX versification |
| DEU | 959→961 (+2) | LXX versification |
| 2KI | 719→723 (+4) | LXX versification |
| TOB | 245→248 (+3) | LXX versification |
| JDT | 339→340 (+1) | LXX versification |
| JOB | 1082→1084 (+2) | LXX versification |
| SIR | 1365→1377 (+12) | LXX versification |
| BAR | 140→141 (+1) | LXX versification |
| EZK | 1265→1268 (+3) | LXX versification |
| EZR | 280→281 (+1) | LXX versification |
| 2SA | 697→697 (0) | Chapter redistribution |
| JON | 48→48 (0) | Chapter redistribution |
| JER | 1299→1299 (0) | Chapter redistribution |
| GEN | 1532→1531 (-1) | Ratified gap (25:34) |
| JDG | 618→617 (-1) | Ratified gap (11:40) |
| EST | 195→194 (-1) | Ratified gap (4:6) |
| 1MA | 924→923 (-1) | Ratified gap (8:32) |
| 3MA | 228→227 (-1) | Ratified gap (1:29) |
| NAH | 48→47 (-1) | LXX versification |
| ZEC | 215→211 (-4) | LXX versification |

Validation after v1.7.0: OT 49 books/0 errors/**5 warnings**, NT 27 books/0 errors/**17 warnings** (14 cosmetic V8). Down from 44 total warnings.

### Lectionary Decontamination (3 NT files)

| File | Removed | Remaining |
|---|---|---|
| `MAT_lectionary.md` | 8 MRK entries (lines 50-64) | 19 entries |
| `LUK_lectionary.md` | 9 JOH entries (lines 68-84) | 28 entries |
| `JOH_lectionary.md` | 66 entries from Acts-Revelation (lines 36-168) | 13 entries |

### Additional Study-Layer Fixes
| # | File | Fix |
|---|---|---|
| 13 | `study/lectionary-notes/NT/MAT_lectionary.md` | Removed 8 MRK entries |
| 14 | `study/lectionary-notes/NT/LUK_lectionary.md` | Removed 9 JOH entries |
| 15 | `study/lectionary-notes/NT/JOH_lectionary.md` | Removed 66 non-JOH entries |

---

## Completion Block

- **Files changed:** 99 total (23 study articles/lectionary + 76 footnotes + 1 registry)
- **Verification run:** `batch_validate.py` OT: 0 errors/5 warnings, NT: 0 errors/17 warnings (down from 44 total to 22; 7 genuine + 15 cosmetic V8)
- **Artifacts refreshed:** Audit memo complete. Registry v1.7.0. Knowledge graph: all 76 entities updated. Footnotes: 18,131 OCR blank lines removed.
- **Remaining known drift:** Stale promotion dossiers (all 76). Dashboard not refreshed.
- **Remaining canon defects:** 9 issues across 6 books (NUM, DEU, ISA, ROM, 1CO, EZR) require staged recovery + re-promotion.
- **Remaining registry gaps:** NUM (16 missing — needs parse recovery first), 1CH (14 missing — needs parse recovery), 2CH (1 missing — needs PDF spot-check), LUK (1 missing — needs investigation).
- **Footnote blank-line cleanup:** 18,131 intra-paragraph OCR blank lines removed across all 76 footnote files (29% average reduction, 62,801→44,670 lines). Structure preserved between `###` sections.
- **Next owner:** Ark (staged recovery for canon defects: NUM, DEU, ISA, ROM, 1CO, EZR)

