---
title: Footnote Cleanup Three-Tier Study Lane
date: 2026-03-14
status: active
author: Ezra
---

# Summary

Implemented the long-horizon footnote cleanup lane on the published `study/footnotes/` surface.

This session:
- kept `study/footnotes/` as the authoritative content surface
- upgraded source normalization from one patristic bucket to three tiers
- refreshed the 76-book dashboard with wave summaries
- cleaned `EXO` as the first post-calibration book after `GEN` and `LEV`

# Files changed

- `pipeline/tools/review_footnotes.py`
- `pipeline/reference/reference_aliases.py`
- `schemas/reference_aliases.yaml`
- `tests/test_reference_aliases.py`
- `tests/test_review_footnotes.py`
- `study/footnotes/OT/EXO_footnotes.md`
- `reports/footnote_review/dashboard.json`
- `reports/footnote_review/*.json`

# Verification run

- `pytest -q tests/test_reference_aliases.py tests/test_review_footnotes.py tests/test_verify_footnotes.py`
  - `13 passed`
- `python3 pipeline/tools/review_footnotes.py --book EXO --report-dir reports/footnote_review`
  - completed successfully
- `python3 pipeline/tools/review_footnotes.py --report-dir reports/footnote_review`
  - completed successfully on all `76` books

# Artifacts refreshed

- `reports/footnote_review/dashboard.json`
- `reports/footnote_review/*.json`

# Results

- dashboard now reports:
  - `complete: 12`
  - `review_required: 64`
  - `structural_clean: 44`
  - `patristic_entity_verified: 36`
  - `apostolic_entity_verified: 76`
  - `liturgical_creedal_verified: 76`
- `EXO` is now:
  - `structural_clean: true`
  - `patristic_entity_verified: true`
  - still `marker_alignment_pass: false`
- `GEN` and `LEV` remain structurally clean on the study surface
- dashboard now includes 5-book wave summaries to support canonical checkpointing

# Remaining known drift

- marker verification still depends on the staged mirror because marker sidecars do not yet live under `study/`
- `EXO`, `GEN`, and `LEV` still carry staged marker-gap debt even though the published text is improved
- the new source-tier model reduced unresolved noise sharply, but patristic alias coverage is still incomplete in several OT and NT books
- full repo `pytest -q` was not run in this session

# Next owner

- Ezra: continue canonical cleanup at `NUM`, then `DEU`, `JOS`, and `JDG`
- Ark/Human: decide whether marker sidecars should be relocated or duplicated into `study/` so published footnote verification no longer depends on `staging/validated/`
