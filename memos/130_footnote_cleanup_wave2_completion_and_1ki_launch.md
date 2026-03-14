## Summary

Continued the long-horizon canonical footnote cleanup lane on the published `study/footnotes` surface.

This tranche completed the remaining Wave 2 book work that had been opened in prior passes and advanced the next wave by cleaning `1KI`.

Books materially advanced:
- `RUT`
- `1SA`
- `2SA`
- `1KI`

Key outcomes:
- `RUT`, `1SA`, and `2SA` are now structurally clean on `study/footnotes`.
- `1KI` moved from a high-noise structural state (`20` structure findings) to structurally clean.
- Patristic alias coverage was extended to remove recurring unresolved source tokens found in this tranche.
- Corpus dashboard now reflects `52` structurally clean books and `39` patristic-verified books.

## Files changed

Content:
- `study/footnotes/OT/RUT_footnotes.md`
- `study/footnotes/OT/1SA_footnotes.md`
- `study/footnotes/OT/2SA_footnotes.md`
- `study/footnotes/OT/1KI_footnotes.md`

Alias / tooling support:
- `schemas/reference_aliases.yaml`
- `tests/test_reference_aliases.py`

Generated artifacts:
- `reports/footnote_review/RUT.json`
- `reports/footnote_review/1SA.json`
- `reports/footnote_review/2SA.json`
- `reports/footnote_review/1KI.json`
- `reports/footnote_review/dashboard.json`

## What changed

`RUT`
- Split the fused `4:7-8` continuation from the preceding sentence so the book now passes structural review.

`1SA`
- Split the fused `17:4-33` subsection from the preceding prose.
- Added `AUGUSTINE_HIPPO` alias coverage for `St. Augustine`.

`2SA`
- Repaired three fused subsection transitions in chapters `14`, `15`, and `21`.
- Normalized the split `Nm 35:19-21` citation into archive-native wikilink form: `[[NUM.35:19]]-21`.
- Corrected malformed heading text `15:19-14` to `15:19-23`.

`1KI`
- Repaired the dominant repeated defect class: doctrinal paragraphs with the next subsection fused onto the same line.
- Cleared `20` structural findings down to `0`.
- Added safe patristic/source aliases for:
  - `ELIJAH_PROPHET`
  - `GREGORY_SINAI`

## Verification run

- `pytest -q tests/test_reference_aliases.py tests/test_review_footnotes.py tests/test_verify_footnotes.py`
  - `13 passed`
- `python3 pipeline/tools/review_footnotes.py --book RUT --report-dir reports/footnote_review`
- `python3 pipeline/tools/review_footnotes.py --book 1SA --report-dir reports/footnote_review`
- `python3 pipeline/tools/review_footnotes.py --book 2SA --report-dir reports/footnote_review`
- `python3 pipeline/tools/review_footnotes.py --book 1KI --report-dir reports/footnote_review`
- `python3 pipeline/tools/review_footnotes.py --report-dir reports/footnote_review`

## Artifacts refreshed

- `reports/footnote_review/dashboard.json`
- Per-book footnote review reports for `RUT`, `1SA`, `2SA`, and `1KI`

Current dashboard highlights after refresh:
- `complete: 12`
- `review_required: 64`
- `structural_clean: 52`
- `patristic_entity_verified: 39`
- `wikilinks_verified: 76`

Wave highlights:
- Wave 2 (`JOS`-`2SA`) is now `5/5` structurally clean and `4/5` patristic verified.
- Wave 3 (`1KI`-`1ES`) is now `2/5` structurally clean and `3/5` patristic verified.

## Remaining known drift

- `marker_alignment_pass` remains the main blocker to `complete` status for most cleaned OT books because marker verification still reads the staged witness under `staging/validated`.
- Full repo `pytest -q` was not run in this tranche.
- `JOS` still carries unresolved patristic/source token `ElPres`.

## Next owner

Ezra continues the canonical footnote cleanup lane at `2KI`, then `1CH`, then `2CH`, preserving the published `study/footnotes` surface as authoritative and treating staged marker sidecars as witness-only verification.
