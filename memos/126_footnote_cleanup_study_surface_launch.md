---
title: Footnote Cleanup Launch On Study Surface
date: 2026-03-14
status: active
author: Ezra
---

# Summary

Footnote cleanup has started on the published `study/footnotes/` surface rather than only on `staging/validated/`.

This session did three things:
- switched the canonical review driver to prefer `study/footnotes/{OT,NT}/`
- cleaned concrete structural and wikilink defects in `GEN` and `LEV`
- regenerated the full 76-book footnote review dashboard from the published study surface

# Files changed

- `pipeline/tools/review_footnotes.py`
- `skills/text-cleaner/scripts/clean.py`
- `pipeline/cleanup/verify_footnotes.py`
- `schemas/reference_aliases.yaml`
- `tests/test_reference_aliases.py`
- `tests/test_review_footnotes.py`
- `study/footnotes/OT/GEN_footnotes.md`
- `study/footnotes/OT/LEV_footnotes.md`
- `staging/validated/OT/GEN_footnotes.md`
- `staging/validated/OT/LEV_footnotes.md`
- `reports/footnote_review/dashboard.json`
- `reports/footnote_review/GEN.json`
- `reports/footnote_review/LEV.json`
- `reports/footnote_review/*.json` regenerated corpus-wide

# Verification run

- `pytest -q tests/test_reference_aliases.py tests/test_review_footnotes.py tests/test_verify_footnotes.py`
  - `12 passed`
- `python3 pipeline/tools/review_footnotes.py --report-dir reports/footnote_review`
  - completed successfully on all `76` books

# Artifacts refreshed

- `reports/footnote_review/dashboard.json`
- `reports/footnote_review/*.json`

# Results

- `GEN` is now `structural_clean: true`
- `LEV` is now `structural_clean: true`
- corpus dashboard moved from `6` complete books to `9`
- corpus `patristic_entity_verified` moved from `15` to `16`
- review tooling now reads the published study footnote tree by default when it exists

# Remaining known drift

- Footnote marker verification still depends on the staged mirror because `study/` does not yet carry marker sidecars
- `GEN` and `LEV` still show `marker_alignment_pass: false`; this session addressed published text cleanup, not marker-gap reconciliation
- many books remain `review_required`, especially for patristic alias residue and marker alignment
- `staging/validated/*_footnotes.md` still exists in parallel with `study/footnotes/*_footnotes.md`; the published cleanup lane should continue on `study/`

# Next owner

- Ezra: continue canonical cleanup from `EXO` forward on `study/footnotes/`
- Ark/Human: decide whether companion marker sidecars should be duplicated or relocated so published footnote verification no longer depends on the staged mirror
