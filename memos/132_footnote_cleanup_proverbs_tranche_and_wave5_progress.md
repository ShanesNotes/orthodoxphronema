## Summary

Continued the canonical footnote cleanup lane on the published `study/footnotes` surface from `JOB` through the end of the current wave front.

This tranche did not open `JOB` itself yet; instead it cleared the canonical books before it:
- `PSA`
- `PRO`

It also completed the surrounding canonical block already started in the unattended run:
- `1MA`
- `2MA`
- `3MA`

Key outcomes:
- `PRO` is now structurally clean and patristic-verified.
- `2MA` and `3MA` no longer fail source normalization over generic `St. John` author references.
- `PSA` remains structurally clean and marker-aligned; its remaining drift is source-classification (`LXX`) plus explicit unsupported chapter-range references, not formatting corruption.
- Wave 5 (`1MA`-`PRO`) is now `5/5` structurally clean and `4/5` patristic verified.

## Files changed

Content:
- `study/footnotes/OT/PRO_footnotes.md`

Alias / tooling support:
- `schemas/reference_aliases.yaml`
- `tests/test_reference_aliases.py`

Generated artifacts:
- `reports/footnote_review/PSA.json`
- `reports/footnote_review/PRO.json`
- `reports/footnote_review/1MA.json`
- `reports/footnote_review/2MA.json`
- `reports/footnote_review/3MA.json`
- `reports/footnote_review/dashboard.json`

## What changed

`PRO`
- Cleared the remaining structural residue:
  - dangling continuation around `[[1CO.6:15]]-20`
  - fused subsection headings in chapters `5`, `6`, `9`, and `16`
- Added missing source aliases:
  - `HIPPOLYTUS_ROME`
  - `VINCENT_LERINS`

`2MA` / `3MA`
- No content edits required.
- Added `JOHN_THEOLOGIAN` so generic `St. John` references no longer block source normalization.

`PSA`
- No content edits required in this tranche.
- Remaining non-complete state is due to:
  - `LXX` being treated as unresolved source taxonomy
  - three unsupported chapter-range references (`Ps 55-59`, `Ps 119-133`, `Ps 148-150`)
- These are classification/contract issues, not study-text corruption.

## Verification run

- `pytest -q tests/test_reference_aliases.py tests/test_review_footnotes.py tests/test_verify_footnotes.py`
  - `13 passed`
- Per-book review refreshes:
  - `JOB`
  - `PSA`
  - `PRO`
  - `1MA`
  - `2MA`
  - `3MA`
- Full corpus refresh:
  - `python3 pipeline/tools/review_footnotes.py --report-dir reports/footnote_review`

## Artifacts refreshed

- `reports/footnote_review/dashboard.json`
- Per-book review reports for the books listed above

Current dashboard highlights after refresh:
- `complete: 14`
- `review_required: 62`
- `structural_clean: 61`
- `patristic_entity_verified: 51`
- `wikilinks_verified: 76`

Wave highlights:
- Wave 5 (`1MA`-`PRO`) is `5/5` structurally clean and `4/5` patristic verified.
- Wave 6 (`ECC`-`SIR`) remains the next active canonical block.

## Remaining known drift

- `PSA` still needs source-classification handling for `LXX`; it is not a structural cleanup book.
- `marker_alignment_pass` remains the main blocker to `complete` status for most OT books because verification still depends on staged witness files under `staging/validated`.
- Full repo `pytest -q` was not run in this tranche.

## Next owner

Ezra continues the canonical footnote cleanup lane at `ECC`, then `SNG`, then `JOB`, preserving `study/footnotes` as authoritative and treating staged marker sidecars as witness-only verification.
