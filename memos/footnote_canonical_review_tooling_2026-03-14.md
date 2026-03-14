# Footnote Canonical Review Tooling Seed — 2026-03-14

## Summary

Implemented the first tooling pass for a full canonical footnote review lane.

This work does not attempt the entire human correction pass in one session. Instead it
creates the review infrastructure needed to execute that pass safely in canonical order:

- canonical footnote review driver
- per-book review reports and dashboard
- patristic entity-first audit
- reusable machine-readable footnote verification output
- text-cleaner JSON-mode fix discovered while probing `LEV_footnotes.md`

## What Changed

- Added `pipeline/tools/review_footnotes.py`
  - walks books in registry order
  - audits `*_footnotes.md` one book at a time
  - records mechanical, structural, marker, wikilink, and patristic findings
  - writes per-book JSON reports plus `reports/footnote_review/dashboard.json`
- Extended `pipeline/cleanup/verify_footnotes.py`
  - added `build_verification_result(book_code)` for machine-readable reuse
  - preserved the existing CLI output path
- Fixed `skills/text-cleaner/scripts/clean.py`
  - JSON mode no longer crashes when writing the report file
- Added tests for:
  - canonical book ordering
  - structural spill detection
  - patristic entity/unresolved token detection
  - text-cleaner JSON-mode stability

## Verification Run

- `pytest -q tests/test_review_footnotes.py tests/test_verify_footnotes.py`
- `python3 pipeline/tools/review_footnotes.py --report-dir reports/footnote_review`

## Artifacts Refreshed

- `reports/footnote_review/dashboard.json`
- `reports/footnote_review/{BOOK}.json` for all reviewed books

## Remaining Known Drift

- The driver is an audit/report scaffold, not the full human correction pass.
- Patristic handling is intentionally entity-first only; it does not resolve work/passage
  references or generate patristic backlinks.
- Structural findings are heuristic and intended to prioritize human review, not replace
  it.

## Next Owner

- Human / Ark / Ezra to use the new dashboard and start the canonical correction pass,
  beginning with `LEV` recalibration and then continuing from `GEN` forward.
