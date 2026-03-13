# Cleanup Tail Taxonomy And Archive — 2026-03-13

**Author:** `ezra`
**Type:** `implementation`
**Status:** `implemented`
**Scope:** `cleanup namespace taxonomy / historical tool archive`
**Workstream:** `workflow`
**Phase:** `3`
**Supersedes:** `none`
**Superseded by:** `none`

## Context

The remaining repo cleanup tail was no longer corpus quality work. It was namespace ambiguity inside `pipeline/cleanup/`: active reusable tools were mixed with closed one-off repair scripts from earlier Phase 2 campaigns.

That ambiguity was the real operational risk:
- it made the live cleanup surface look larger than it actually is
- it invited accidental reuse of historical one-off mutators
- it kept the boards describing deferred cleanup work that was already ready to classify

## Taxonomy

### Active reusable cleanup tools remain in `pipeline/cleanup/`

- companion integrity and inventory:
  - `companion_audit.py`
  - `normalize_companion_frontmatter.py`
  - `split_fused_footnote_headers.py`
  - `unify_marker_schema.py`
  - `reindex_markers.py`
  - `verify_footnotes.py`
  - `extract_footnotes.py`
- generic scripture recovery/audit helpers:
  - `dropcap_verify.py`
  - `nt_dropcap_recovery.py`
  - `nt_dedup_merge.py`
  - `nt_verse_recovery.py`
  - `fix_articles.py`
  - `fix_split_words.py`
  - `audit_cleanup_residue.py`

### Historical one-off tools moved to `pipeline/archive/historical_cleanup/`

- `book_specific/`
  - `fix_3ma_structure.py`
  - `fix_dan_structure.py`
  - `fix_est_structure.py`
  - `restructure_psa.py`
  - `restructure_wis.py`
- `nt_oneoffs/`
  - `nt_article_removal.py`
  - `nt_safe_purity.py`
  - `nt_structural_reorder.py`
  - `nt_surgical_fix.py`
- `legacy_companion/`
  - `refine_notes.py`
  - `recover_markers.py`
- `pdf_repairs/`
  - `repair_truncations.py`
  - `repair_verse_1.py`

## Decision

- Archived tools are preserved for auditability and historical replay, not deleted.
- `pipeline/cleanup/` now means active reusable cleanup/audit tooling only.
- This change does not reopen canon or companion decisions and does not add new mutation behavior.

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | archive moves, this memo, refreshed board/index/ops text |
| `Verification run` | `done` | coordination check `PASS`, full wikilink audit `0` convertible / `32` unresolved, companion audit `76/76`, Phase 3 validation `WARN` with duplicate inbound links only, `pytest -q` |
| `Artifacts refreshed` | `done` | `reports/coordination_state.json`, `reports/wikilink_audit.json`, `reports/phase3_validation_report.json`, `reports/companion_audit.json` |
| `Remaining known drift` | `none` | cleanup namespace and coordination surfaces agree on the active tail |
| `Next owner` | `ezra` | finish verification and route back to Phase 3 verification / PSA readiness |
