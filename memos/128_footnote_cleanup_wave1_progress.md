---
title: Footnote Cleanup Wave 1 Progress
date: 2026-03-14
status: active
author: Ezra
---

# Summary

Continued the canonical footnote cleanup lane on `study/footnotes/` and completed the remaining structural cleanup work for Wave 1 books `NUM` and `DEU`.

# Files changed

- `study/footnotes/OT/NUM_footnotes.md`
- `study/footnotes/OT/DEU_footnotes.md`
- `schemas/reference_aliases.yaml`
- `tests/test_reference_aliases.py`
- `reports/footnote_review/dashboard.json`
- `reports/footnote_review/NUM.json`
- `reports/footnote_review/DEU.json`
- `reports/footnote_review/*.json`

# Verification run

- `pytest -q tests/test_reference_aliases.py tests/test_review_footnotes.py tests/test_verify_footnotes.py`
  - `13 passed`
- `python3 pipeline/tools/review_footnotes.py --book NUM --report-dir reports/footnote_review`
  - completed successfully
- `python3 pipeline/tools/review_footnotes.py --book DEU --report-dir reports/footnote_review`
  - completed successfully
- `python3 pipeline/tools/review_footnotes.py --report-dir reports/footnote_review`
  - completed successfully on all `76` books

# Artifacts refreshed

- `reports/footnote_review/dashboard.json`
- `reports/footnote_review/*.json`

# Results

- `NUM` is now:
  - `structural_clean: true`
  - `patristic_entity_verified: true`
  - still `marker_alignment_pass: false`
- `DEU` is now:
  - `structural_clean: true`
  - `patristic_entity_verified: true`
  - still `marker_alignment_pass: false`
- Wave 1 (`GEN`–`DEU`) now reports:
  - `structural_clean_books: 5/5`
  - `patristic_verified_books: 3/5`
  - `marker_alignment_books: 0/5`
- Corpus totals now report:
  - `structural_clean: 46`
  - `patristic_entity_verified: 37`
  - `complete: 12`

# Remaining known drift

- `GEN` and `LEV` still have patristic alias residue even though they are structurally clean
- all five Wave 1 books still depend on staged marker witnesses and remain `marker_alignment_pass: false`
- unresolved chapter-only range citations remain intentionally untouched in some books, including `NUM`
- full repo `pytest -q` was not run in this session

# Next owner

- Ezra: continue canonical cleanup at `JOS`, then `JDG`, `RUT`, `1SA`, and `2SA`
- Ark/Human: decide when published study marker sidecars will move out of staged witness mode
