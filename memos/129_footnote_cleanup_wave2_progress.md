---
title: Footnote Cleanup Wave 2 Progress
date: 2026-03-14
status: active
author: Ezra
---

# Summary

Continued the canonical footnote cleanup lane on `study/footnotes/` and completed structural cleanup for `JOS` and `JDG`.

# Files changed

- `study/footnotes/OT/JOS_footnotes.md`
- `study/footnotes/OT/JDG_footnotes.md`
- `schemas/reference_aliases.yaml`
- `tests/test_reference_aliases.py`
- `reports/footnote_review/dashboard.json`
- `reports/footnote_review/JOS.json`
- `reports/footnote_review/JDG.json`
- `reports/footnote_review/*.json`

# Verification run

- `pytest -q tests/test_reference_aliases.py tests/test_review_footnotes.py tests/test_verify_footnotes.py`
  - `13 passed`
- `python3 pipeline/tools/review_footnotes.py --book JOS --report-dir reports/footnote_review`
  - completed successfully
- `python3 pipeline/tools/review_footnotes.py --book JDG --report-dir reports/footnote_review`
  - completed successfully
- `python3 pipeline/tools/review_footnotes.py --report-dir reports/footnote_review`
  - completed successfully on all `76` books

# Artifacts refreshed

- `reports/footnote_review/dashboard.json`
- `reports/footnote_review/*.json`

# Results

- `JOS` is now:
  - `structural_clean: true`
  - still `patristic_entity_verified: false` because `ElPres` remains unresolved
  - still `marker_alignment_pass: false`
- `JDG` is now:
  - `structural_clean: true`
  - `patristic_entity_verified: true`
  - still `marker_alignment_pass: false`
- corpus totals now report:
  - `structural_clean: 48`
  - `patristic_entity_verified: 37`
  - `complete: 12`
- Wave 2 (`JOS`–`2SA`) now reports:
  - `structural_clean_books: 2/5`
  - `patristic_verified_books: 3/5`
  - `marker_alignment_books: 0/5`

# Remaining known drift

- `JOS` still carries one unresolved source token: `ElPres`
- marker verification still depends on staged witness sidecars, so all cleaned Wave 2 books remain non-complete
- `RUT`, `1SA`, and `2SA` still need full structural cleanup in Wave 2
- full repo `pytest -q` was not run in this session

# Next owner

- Ezra: continue canonical cleanup at `RUT`, then `1SA`, then `2SA`
- Ark/Human: decide whether the unresolved `ElPres` abbreviation has an authoritative expansion in the source-abbreviation material
