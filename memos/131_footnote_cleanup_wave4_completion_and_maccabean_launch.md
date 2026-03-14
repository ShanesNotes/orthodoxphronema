## Summary

Continued the canonical footnote cleanup lane on the published `study/footnotes` surface without widening scope to articles.

This tranche completed the remainder of Wave 4 and advanced the next canonical block through the Maccabean books.

Books materially advanced:
- `1ES`
- `EZR`
- `NEH`
- `TOB`
- `JDT`
- `EST`
- `1MA`
- `2MA`
- `3MA`

Key outcomes:
- `EZR`, `NEH`, `TOB`, `JDT`, and `EST` are now structurally clean on `study/footnotes`.
- `1ES` and `1MA` required no text edits under the current rubric.
- `2MA` and `3MA` were already structurally clean; this tranche resolved remaining source-normalization drift around `St. John`.
- Wave 4 (`EZR`-`EST`) is now `5/5` structurally clean and `5/5` patristic verified.
- Corpus dashboard now reflects `60` structurally clean books and `50` patristic-verified books.

## Files changed

Content:
- `study/footnotes/OT/EZR_footnotes.md`
- `study/footnotes/OT/NEH_footnotes.md`
- `study/footnotes/OT/TOB_footnotes.md`
- `study/footnotes/OT/JDT_footnotes.md`
- `study/footnotes/OT/EST_footnotes.md`

Alias / tooling support:
- `schemas/reference_aliases.yaml`
- `tests/test_reference_aliases.py`

Generated artifacts:
- `reports/footnote_review/EZR.json`
- `reports/footnote_review/NEH.json`
- `reports/footnote_review/TOB.json`
- `reports/footnote_review/JDT.json`
- `reports/footnote_review/EST.json`
- `reports/footnote_review/1MA.json`
- `reports/footnote_review/2MA.json`
- `reports/footnote_review/3MA.json`
- `reports/footnote_review/dashboard.json`

## What changed

`EZR`
- Cleared three fused subsection transitions.
- Left the staged-witness invalid anchor `EZR.7:52` untouched in published text because the current evidence was sufficient only for structural cleanup, not safe anchor renumbering.

`NEH`
- Cleared the dominant fused subsection pattern across chapters `2`, `4`, `5`, `6`, `7`, and `8`.
- Repaired the broken `Mt 10:16` citation to archive-native form: `[[MAT.10:16]]`.
- Left the unsupported chapter-range citation `Ex 22-25` as-is and explicitly reviewable rather than forcing a bad rewrite.

`TOB`
- Cleared five fused subsection boundaries in the Tobias/Sarah travel and marriage block.

`JDT`
- Cleared seven structural subsection spills and normalized `St. Clement`.

`EST`
- Cleared five structural defects, including the dangling range continuation around `3:13a-13g`.
- Repaired the broken Acts reference to `[[ACT.6:11]]-14`.
- Normalized `St. Jerome`.

`2MA` / `3MA`
- No content edits required.
- Added `JOHN_THEOLOGIAN` so the generic authorial reference `St. John` no longer blocks patristic verification.

Additional alias additions:
- `CLEMENT_ROME`
- `JEROME`
- `JOHN_THEOLOGIAN`

## Verification run

- `pytest -q tests/test_reference_aliases.py tests/test_review_footnotes.py tests/test_verify_footnotes.py`
  - `13 passed`
- Per-book review refreshes:
  - `1ES`
  - `EZR`
  - `NEH`
  - `TOB`
  - `JDT`
  - `EST`
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
- `structural_clean: 60`
- `patristic_entity_verified: 50`
- `wikilinks_verified: 76`

Wave highlights:
- Wave 4 (`EZR`-`EST`) is `5/5` structurally clean and `5/5` patristic verified.
- Wave 5 (`1MA`-`PRO`) is currently `4/5` structurally clean and `3/5` patristic verified.

## Remaining known drift

- `marker_alignment_pass` remains the main blocker to `complete` status for most OT books because verification still depends on staged witness files under `staging/validated`.
- `3MA` still carries one unsupported chapter-range citation (`Ex 5-12`), but this does not represent a malformed or auto-convertible biblical reference.
- Full repo `pytest -q` was not run in this tranche.

## Next owner

Ezra continues the canonical footnote cleanup lane at `JOB`, then `PSA`, then `PRO`, preserving `study/footnotes` as authoritative and treating staged marker sidecars as witness-only verification.
