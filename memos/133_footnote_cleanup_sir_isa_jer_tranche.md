# 133 Footnote Cleanup SIR ISA JER Tranche

Date: 2026-03-14
Status: active
Owner: Ezra

## Summary

Continued the long-horizon footnote cleanup lane on the published `study/footnotes` surface and cleared the next three open OT books in canonical order that were materially blocking the prophetic/wisdom tranche:

- `SIR`
- `ISA`
- `JER`

All three now pass:

- `mechanical_clean`
- `structural_clean`
- `wikilinks_verified`
- `patristic_entity_verified`
- `apostolic_entity_verified`
- `liturgical_creedal_verified`

All three still remain `review_required` at book status because marker alignment continues to be checked against the staged marker witness and still fails there.

## Files Changed

- `study/footnotes/OT/SIR_footnotes.md`
- `study/footnotes/OT/ISA_footnotes.md`
- `study/footnotes/OT/JER_footnotes.md`
- `schemas/reference_aliases.yaml`
- `tests/test_reference_aliases.py`

## Key Repairs

### SIR

- Repaired the large early-book spill cluster in chs. 1-10:
  - broken `Rom` / `1Co` splits
  - fused midline section starts
  - dangling range continuation at the top of the file
- Repaired the late `50:1-4` broken reference split.
- Normalized unresolved source tokens:
  - `ClemA` -> `CLEMENT_ALEXANDRIA`
  - `St. Photini` -> `PHOTINI_SAMARITAN`

### ISA

- Repaired the major prophetic spill chain in the early file:
  - broken `Jn 15:1-6` split that had produced a false `### 15:1` heading
  - broken `2Ch 26:18ff` split that had produced a false `### 26:18` heading
  - repeated midline reference spills across `5:26-30` through `36:4-6`
- Converted `OWN` from unresolved token form into explicit prose (`ho on`) rather than adding a bad alias.
- Normalized `GrgNa` by adding it as an alias for `GREGORY_THEOLOGIAN`.

### JER

- Repaired the `Dt 30:15` / `Ezk 26` split that had produced a false `### 30:15` heading.
- Repaired the remaining spill cluster around `22:15` through `27:4-5`.
- Removed the false `### 48:5` split by restoring the merged paragraph into a clean `48:5-8` lead.
- Eliminated residual source drift by:
  - normalizing `GrgNa`
  - promoting `James` / `St. James` into the apostolic tier

## Verification Run

- `pytest -q tests/test_reference_aliases.py tests/test_review_footnotes.py tests/test_verify_footnotes.py`
  - result: `13 passed`
- `python3 pipeline/tools/review_footnotes.py --book SIR --report-dir reports/footnote_review`
  - result: `structural_clean: true`
- `python3 pipeline/tools/review_footnotes.py --book ISA --report-dir reports/footnote_review`
  - result: `structural_clean: true`
- `python3 pipeline/tools/review_footnotes.py --book JER --report-dir reports/footnote_review`
  - result: `structural_clean: true`

## Artifacts Refreshed

- refreshed:
  - `reports/footnote_review/SIR.json`
  - `reports/footnote_review/ISA.json`
  - `reports/footnote_review/JER.json`

## Remaining Known Drift

- `reports/footnote_review/dashboard.json` is currently stale relative to this tranche.
  - Cause: a full 76-book refresh was started but had not completed at memo time.
  - Impact: global counts on the dashboard may still under-report the newly clean state of `SIR`, `ISA`, and `JER`.
- Marker alignment remains the blocking witness on these books, but that is staged-surface verification debt rather than study-surface text debt.

## Next Owner

- Ezra continues the canonical pass at `LAM`.
