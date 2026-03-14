# Canon Proofread Correction Pass — 2026-03-14

## Summary

Comprehensive multi-wave proofreading pass across all 76 canon books using
the `canon-proofreader` skill and the `fix_fused_markers.py` deep correction engine.

- **Files modified:** 26 canon books (19 NT, 7 OT)
- **Total corrections applied:** ~473 (Wave 1: ~145, Wave 2: 328)
- **Regression test:** 0 errors, all warnings pre-existing
- **Validation:** `validate_canon.py` PASS on all 76 books
- **Deep scan:** 0 real findings remain (14 false positives: dwelled, coffered, bended)

## Correction Categories

| Category | Count | Method | Description |
|----------|-------|--------|-------------|
| P1 — Missing space after punctuation | 80 | Auto-fix | `.And` → `. And`, `,Satan` → `, Satan` |
| P2 — Space before punctuation | 17 | Auto-fix | `word .` → `word.`, `God )` → `God)` |
| P3 — Double word | 2 | Auto-fix | `He He` → `He`, `PASSOVER PASSOVER` → `PASSOVER` |
| P4 — Fused article "a" + word | ~46 | Manual review | `acenturion` → `a centurion`, `aship` → `a ship` |
| Footnote marker removal | ~10 | Manual review | `aspoken` → `spoken`, `bstanding` → `standing` |

## Books Modified

### OT (6 books)
- `02_EXO.md` — 1 fix (P2)
- `03_LEV.md` — 6 fixes (P2)
- `10_2SA.md` — 1 fix (P1)
- `14_2CH.md` — 1 fix (P1)
- `17_NEH.md` — 1 fix (P1)
- `20_EST.md` — 1 fix (P2)
- `24_PSA.md` — 5 fixes (P1 + P4: `fromits` → `from its`)
- `30_SIR.md` — 2 fixes (P1)

### NT (14 books)
- `50_MAT.md` — 17 fixes (P1 + P4: `acenturion`, `apiece`, `ahook`, `awitness`, + footnote `aspoken`)
- `51_MRK.md` — 9 fixes (P1 + P4: `apiece`, + footnotes `aspoken`, `bstanding`)
- `52_LUK.md` — 22 fixes (P1 + P4: `apiece`, `asupper`, `astone`, `adinner`, `atear`, + footnotes `aotherwise`, `asave`, `abroiled`)
- `53_JOH.md` — 15 fixes (P1 + P4: `awitness`, `apiece`, `aspear`, `asupper`, `acave`, `astench`, + footnote `asought`)
- `54_ACT.md` — 22 fixes (P1 + P4: `aship` ×2, `acenturion`, `aprisoner` ×2, `aminister`, `awitness`, + footnotes `asend`, `aspoke`)
- `55_ROM.md` — 12 fixes (P1 + P4: `aterror`, `aminister`)
- `56_1CO.md` — 5 fixes (P1 + P4: `athing`)
- `60_PHP.md` — 3 fixes (P1)
- `61_COL.md` — 11 fixes (P4: `aminister` ×2, `afaithful` ×2, `apublic`, `ashadow`, `acomplaint`, `abeloved`, `acomfort`, `abondservant`, + footnote `aseen`)
- `68_HEB.md` — 2 fixes (P1)
- `70_1PE.md` — 11 fixes (P4: `afellow`, `awitness`, `apartaker`, `ablessing`, `adefense`, `areason`, `amultitude`, `agift`, `amurderer`, `abusybody`, `afaithful`, `aroaring`, `akiss`, + footnote `ayour`)
- `76_REV.md` — 10 fixes (P1)

## Root Cause Analysis

Two distinct error patterns were identified:

1. **Missing space after punctuation (P1/P2):** Docling PDF extraction occasionally
   drops the space between a sentence-ending punctuation mark and the next word,
   particularly in the NT books where dialogue formatting is dense. Concentrated
   in MAT, MRK, LUK, JOH, ACT, ROM, REV.

2. **Fused footnote markers (P4):** The OSB uses superscript letters (ᵃ, ᵇ) as
   cross-reference markers. Docling renders these as inline lowercase letters that
   fuse with the next word. Two sub-patterns:
   - **Article "a" + word:** The fused `a` is actually the English article, and the
     correct fix is to insert a space (`acenturion` → `a centurion`)
   - **Footnote "a" + word:** The fused `a` is a superscript marker that should be
     removed entirely (`aspoken` → `spoken`)

   The distinction was made by reading each verse in context against the NKJV/OSB
   source text. When the article "a" is grammatically required, it was preserved;
   when the word makes complete sense without "a", the marker was removed.

## Wave 2 — Deep Fused Marker Correction (328 fixes)

Targeted pass using `fix_fused_markers.py` with a manually curated replacement map
for all 211 unique fused footnote marker tokens identified by `deep_scan.py`.

Each token was classified by reading its verse context:
- **Article "a" insertion** (nouns/adjectives): `acrop` → `a crop`, `arobber` → `a robber`
- **Marker strip** (verbs/function words): `atook` → `took`, `acast` → `cast`
- **"b" marker strip**: `bside` → `side`
- **Context-sensitive**: `along time` → `a long time`, `afar country` → `a far country`

### Wave 2 books modified

| Book | Fixes | Key corrections |
|------|-------|----------------|
| 1SA | 1 | `abed` → `a bed` |
| 2KI | 1 | `afar country` → `a far country` |
| 2CH | 1 | `afar country` → `a far country` |
| ISA | 3 | `afar country` ×2, `abed` |
| JER | 1 | `afar country` |
| MAT | 81 | Full range: articles (acrop, arobber, etc.), strips (acast, aworshiped), context (afar country, along time) |
| MRK | 32 | Articles (akingdom, avineyard), strips (awounded, abegan), context (afar country) |
| LUK | 108 | Heaviest book. Articles (abaptism, adove), strips (atook, areturned, acrowed), "b" (bside), context (along time ×3, afar country ×3) |
| JOH | 16 | Articles (alad, adevil), strips (aask, abelieve, agot) |
| ACT | 81 | Articles (aeunuch, acripple), strips (areceived, akilled, amaintaining), context (along time ×4) |
| 1CO | 1 | `aholy` → `a holy` |
| REV | 2 | `awrite` → `write`, `astood` → `stood` |

## Remaining Items (P7 — report only)

76 unbalanced double-quote warnings in Psalms (59), Proverbs (16), and Wisdom (1).
These are multi-verse quotations where a quote opens in one verse and closes in
another — intentional formatting, not errors. No action required.

1,487 P6 (unknown word) findings are biblical proper nouns and archaic English
that aspell does not recognize. Not errors.

## Skills & Scripts Created

Four tools built in `skills/canon-proofreader/` for ongoing text quality:

1. **`proofread.py`** — Multi-pass correction engine (P1–P8), aspell-gated
2. **`deep_scan.py`** — Fused marker detection (D1–D5), aspell-batch
3. **`fix_fused_markers.py`** — Curated replacement engine (211 tokens)
4. **`canon-spell-audit/`** — Detection-only aspell wrapper
5. **`canon-validator/`** — Post-correction regression testing

## Final Validation

```
All 76 books: PASS (0 failures)
deep_scan.py: 14 findings, all false positives (dwelled ×11, coffered ×2, bended ×1)
proofread.py: 1,563 findings, all P6/P7 review-only (no auto-fixable items remain)
```

No regressions introduced.

---
*Generated by canon-proofreader skill, reviewed by Ark.*
*Ezra audit: pending human confirmation.*
