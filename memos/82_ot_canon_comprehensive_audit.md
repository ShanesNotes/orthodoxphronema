# Memo 82 — OT Canon Comprehensive Audit

**Date:** 2026-03-11
**Author:** Ark
**Scope:** All 49 promoted OT books in `canon/OT/`
**Status:** Audit complete, fixes applied
**Tools:** `batch_validate.py --dir canon/OT`, `spell_audit.py` (new)

---

## Executive Summary

| Metric | Result |
|--------|--------|
| Books audited | 49 / 49 promoted OT |
| V1-V6 errors | **0** (all PASS) |
| V4 missing verse gaps | **1** (EST.4:6 — versification difference, not true gap) |
| V7 completeness warnings | 15 books (mostly ±1-3 verses from LXX/MT versification differences) |
| V10 absorbed content | **1** (EST.4:6 absorbed into EST.4:7) |
| V11 split-word warnings | **0** (all cleared) |
| Article leakage | **0** (3 found and fixed: EXO.20:1, 2SA.7:1, NUM.18:1) |
| Fused verse blobs | **0** (8 found and fixed + WIS.9:1 user-identified) |
| Split-word fixes applied | **~3,000+** across 49 books |
| Note markers remaining | **0** (confirmed via grep) |

---

## Part 1: Structural Validation (V1-V12)

**All 47 books pass all error-level checks (V1-V6).** No duplicate anchors, no chapter sequence gaps, no article bleed, no frontmatter issues.

### V4 Missing Verses (1 book)
- **EST.4:6** — jumps from verse 5 to verse 7. V10 confirms EST.4:6 is absorbed into EST.4:7 (56% Brenton word match).

### V7 Completeness Gaps
Most V7 warnings are versification differences (LXX vs MT) not actual missing text:

| Book | Actual | Expected | Gap | Notes |
|------|--------|----------|-----|-------|
| GEN | 1531 | 1532 | -1 | |
| EXO | 1171 | 1166 | +5 | |
| NUM | 1287 | 1288 | -1 | |
| DEU | 961 | 959 | +2 | |
| JDG | 617 | 618 | -1 | |
| 2KI | 723 | 719 | +4 | |
| 1CH | 928 | 942 | **-14** | Investigate |
| 2CH | 833 | 822 | +11 | |
| EZR | 281 | 280 | +1 | |
| EST | 194 | 195 | -1 | EST.4:6 missing |
| EZK | 1268 | 1265 | +3 | |
| TOB | 248 | 245 | +3 | |
| JDT | 340 | 339 | +1 | |
| SIR | 1377 | 1371 | +6 | |
| BAR | 141 | 140 | +1 | |
| 1MA | 923 | 924 | -1 | |
| 3MA | 227 | 228 | -1 | |

**1CH at 98.5% (14 verses short)** warrants investigation — may be a CVC registry issue or genuine gaps.

### V11 Split-Word Detections
- JOS line 287: "v alley"
- JDG lines 181, 217: "v alley"

### V8 Heading Density
- HAB: 10 headings / 3 chapters (3.3/ch) — acceptable for poetic book
- LJE: 6 headings / 1 chapter (6.0/ch) — single chapter, acceptable
- 1MA: 60 headings / 16 chapters (3.8/ch) — narrative book, acceptable
- 2MA: 48 headings / 15 chapters (3.2/ch) — acceptable

---

## Part 2: Article Leakage (2 instances)

Both in **EXO.20:1**:
1. `HARMONYBETWEEN LAW AND GRACE Christ is...` — study article text fused into verse
2. `The pre-incarnate Christ gave Mo...` — study article text fused into verse

**Action required:** Clean EXO.20:1 to remove leaked article text.

---

## Part 3: Spelling / OCR Artifact Audit

### Worst-affected books (by true error count)
| Book | Errors | Primary issue |
|------|--------|---------------|
| SIR | 279 | Fused words, split fragments, OCR artifacts |
| PRO | 88 | Split-word fragments |
| JDG | 65 | Split-word fragments |
| WIS | 61 | Split-word fragments |
| SNG | 39 | Split-word fragments |
| 1SA | 36 | Split-word fragments |
| EST | 31 | Mixed |
| TOB | 28 | Split-word fragments |
| DEU | 27 | Split-word fragments, fused words |
| NUM | 26 | Fused words, truncations |
| ISA | 23 | Mixed |

### Fused words (missing spaces) — highest priority
These are words where a space was lost between two words:

| Anchor | Fused text | Should be |
|--------|-----------|-----------|
| EXO.20:1 | HARMONYBETWEEN | (article leak — remove) |
| 2KI.20:1 | InAmoz | In Amoz |
| 2KI.13:1 | InJehuthebecame | In Jehu...the...became |
| 2KI.14:1 | InJoash | In Joash |
| 2CH.23:1 | InAzariah | In Azariah |
| ISA.41:20 | Lord'S | Lord's |
| ISA.9:8 | knowEphraim | know Ephraim |
| JER.30:32 | BenHadad | Ben-Hadad |
| SIR.24:23 | GodThe | God. The |
| SIR.36:11 | LordUpon | Lord. Upon |
| SIR.10:22 | alikeTheir | alike. Their |
| SIR.41:24 | maidservantAnd | maidservant. And |
| SIR.25:19 | manSuch | man. Such |
| SIR.12:2 | repaidIf | repaid. If |
| SIR.38:27 | sealsHe | seals. He |
| SIR.41:14 | treasureWhat | treasure. What |
| SIR.11:14 | wealthThese | wealth. These |
| EZR.8:4 | PahathMoab | Pahath-Moab |
| EZR.5:3 | ShetharBoznai | Shethar-Boznai |
| NEH.10:14 | PahathMoab | Pahath-Moab |

### Split-word OCR fragments (sample from worst books)
These are word fragments from Docling column-split artifacts where a word was split mid-word with a space:

**SIR examples:**
- "hum ble", "ey es", "hy pocrite", "anv il", "phy sician", "ty pes", "alm sgiving"
- "inv olv ed", "av oid", "am ong"

**PRO examples:**
- "ey es", "ev il", "inv ite", "env ious", "ov erthrows", "aly ing"

**WIS examples:**
- "im m ortality", "m uch m ore", "m elting", "tim e", "rhy thm", "roy al"

**NUM examples:**
- "m ay", "m ade", "flam e", "Chem osh", "Assy rians", "secon" (truncated)

**1SA examples:**
- "sm ile", "enem ies", "em pty"

---

## Part 4: Action Items

### Critical (fix immediately)
1. **EXO.20:1** — Remove study article leakage (HARMONYBETWEEN, pre-incarnate Christ)
2. **EST.4:6** — Recover missing verse (absorbed into 4:7)

### High Priority (split-word cleanup)
3. **SIR** — 279 OCR artifacts, worst book by far; needs systematic cleanup pass
4. **PRO** — 88 artifacts; second worst
5. **JDG** — 65 artifacts
6. **WIS** — 61 artifacts

### Medium Priority
7. **SNG, 1SA, EST, TOB, DEU, NUM, ISA** — 20-40 artifacts each
8. **Fused word fixes** across 2KI, 2CH, EZR, NEH, ISA, JER, SIR

### Investigation
9. **1CH** — 14 verses short of CVC expectation (98.5%). May be registry CVC error or genuine gaps.

---

## Part 5: Fixes Applied (2026-03-11)

### Fused Verse Blobs (8 fixed)
Verses where extractor fused entire chapters into a single :1 line (same class as WIS.9:1):

| Verse | Absorbed Content | Chars | Fix |
|-------|-----------------|-------|-----|
| ECC.3:1 | ECC.1:3-1:18 duplicate | 1924 | Replaced with "To everything there is a season..." |
| ECC.6:1 | ECC.4:6-5:2 duplicate | 1740 | Replaced with "There is an evil I have seen..." |
| JDG.5:1 | JDG.5:2-7:1 (Song of Deborah + Gideon) | 10908 | Replaced with "Then Deborah and Barak...sang..." |
| JDG.6:1 | JDG.5:6-7:1 duplicate | 10443 | Replaced with "Then the sons of Israel did evil..." |
| NUM.18:1 | NUM.21:18-22:1 (wrong chapter) | 2657 | Replaced with "Now the Lord spoke to Aaron..." |
| SNG.2:1 | SNG.1:2-1:17 duplicate | 1825 | Replaced with "I am a flower of the plain..." |
| TOB.13:1 | TOB.13:2-13:18 duplicate | 2734 | Replaced with "Then Tobit with exceeding joy..." |
| WIS.17:1 | WIS.16:17-16:29 duplicate | 2036 | Replaced with "Great are Your judgments..." |

All individual verses already existed as separate anchored lines — only the :1 blob was incorrect.

### Study Article Leaks (3 fixed)
- **EXO.20:1** — Removed HARMONYBETWEEN LAW AND GRACE study article
- **2SA.7:1** — Removed GOD'S COVENANTS study article
- **NUM.18:1** — Removed TYPOLOGY study article (in earlier session)

### WIS.9:1 Fusion (user-identified)
- WIS.9:1 had absorbed WIS.8:9-8:21 + chapter heading + actual 9:1 text (all on one line)
- Replaced with correct "O God of our fathers and the Lord of mercy..."
- Cleaned WIS.8:21 trailing contamination

### Split-Word / Spelling Fixes (~3,000+ across 49 books)
Dispatched parallel agents for all affected books. Major operations:

| Book | Fixes | Primary patterns |
|------|-------|-----------------|
| PSA | ~1300 | m-space splits (commandments, mountains, mighty, Egypt, David, etc.) |
| JOB | ~170+ | m-space splits, fused words (in progress at time of audit) |
| SIR | ~230 | Split words, fused words, space-before-punctuation |
| PRO | ~88 | Split words (receiveth, lovecovers, destroysher) |
| ECC | garbled blobs | Lines 84 and 178 had massive garbled content (now replaced) |
| JDG | split words | m ade, m ountains, v alley, dy ed, garm ents |
| WIS | split words | im mortality, m ultitudes, rhy thm, roy al |
| EST | ~34 | Possessive fusions (king'stwo, women'squarters) |
| TOB | ~28 | conv erted, bery l, ony x |
| LAM | ~6 | Stutter artifacts (You ou, Our ur, Because ecause) |

Additional fixes across GEN, LEV, NUM, DEU, JOS, 1SA, 2SA, 1KI, 2KI, 1CH, 2CH, EZR, NEH, ISA, JER, EZK, DAN, HOS, AMO, MIC, HAB, HAG, ZEC, JDT, 1ES, 1MA, 2MA, 3MA, RUT, SNG, BAR.

### Truncation/Corruption Fixes
- 2SA.1:1 — "slaugh" restored to full text
- 1KI.3:1 — was just "." — restored
- 1KI.3:2 — "becau" restored
- NUM.9:21 — "wou.ld" → "would"
- 1SA.3:1 — massive duplicate text block removed
- RUT.1:1 — garbled opening restored

### Photius Census Cross-Reference
Photius (OT Census, memo 93) reported 35/49 clean, 8 minor, 6 unstable (note markers).
Post-audit verification: **0 note markers († or ω) remain in any canon file.** All 49 files pass structural checks.

---

## Methodology
- Structural: `python3 pipeline/tools/batch_validate.py --dir canon/OT --output-json reports/canon_ot_structural_audit.json`
- Spelling: `python3 pipeline/tools/spell_audit.py --dir canon/OT --allowlist schemas/biblical_names.txt --output-json reports/canon_ot_spell_audit.json`
- Allowlist: 3,160 biblical proper nouns auto-extracted from canon files
- Full JSON results preserved in `reports/` for drill-down
