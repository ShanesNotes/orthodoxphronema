# Memo 76 — NT Extraction Sprint (All 27 Books)

**Author:** Ark
**Date:** 2026-03-11
**Status:** IN PROGRESS

## Scope

Extract all 27 NT books from OSB PDF to `staging/validated/NT/`.
No promotions — staging only, per AGENTS.md.

## Pre-Conditions

- 45/49 OT books promoted; NT staging empty
- All 27 NT books have page ranges in registry
- CVC populated for 25/27; **1CO and EPH fixed in this session** (Step 0)
- V11/V12 activated in validator

## Strategy

1. **Pilot MAT** — largest Gospel (28 ch, 1071 v), validates NT extraction works
2. **Batch Gospels** — MRK, LUK, JOH
3. **Acts** — ACT (28 ch, 1007 v)
4. **Pauline Epistles** — ROM, 1CO, 2CO, GAL, EPH, PHP, COL, 1TH, 2TH, 1TI, 2TI, TIT, PHM
5. **Catholic Epistles** — HEB, JAS, 1PE, 2PE, 1JN, 2JN, 3JN, JUD
6. **Revelation** — REV (highest structural risk, last)

## Known Risks

- **Footnote non-monotonic ordering** — documented Codex finding, NT expected
- **No Brenton for V10** — V10 will SKIP for all NT books
- **REV structural risk** — ordinal numbers (seven seals/trumpets) may cause false verse splits
- **Single-chapter books** (PHM, 2JN, 3JN, JUD) — false chapter-2 risk
- **Docling OOM** — large page ranges may exhaust 8GB VRAM; extract in chunks if needed

## Decision Rules

- V7 >= 85% → proceed
- V7 80-85% → proceed with caution, note gaps
- V7 < 80% → STOP, diagnose

## Pipeline

```
osb_extract.py → fix_split_words.py → fix_omissions.py → validate → dossier
```

## Results

_To be filled as extraction progresses._

## Files Changed

- `schemas/anchor_registry.json` — 1CO/EPH CVC fix
- `staging/validated/NT/*.md` — all 27 books
- `reports/` — dossiers and dashboard

## Next Owner

Human — promotion approval after Ezra audit
