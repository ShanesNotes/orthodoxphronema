# Phase 3 Contract Reconciliation — 2026-03-13

**Author:** `ezra`
**Type:** `integration`
**Status:** `implemented`
**Scope:** `companion-layer contract / phase3 handoff`
**Workstream:** `workflow`
**Phase:** `3`
**Supersedes:** `none`
**Superseded by:** `none`

## Context

Memo `121` completed a real companion cleanup pass and Memo `122` completed the full staged wikilink rollout. Both should stand.

The drift was in the forward contract:
- Memo `121` described marker anchors as the Phase 3 backlink/graph edge source.
- The implemented Phase 3 pipeline already uses R1 JSONL citation records as the backlink input.

## Reconciled Contract

- `*_footnotes.md` is authoritative for companion anchor integrity.
- `*_footnote_markers.json` is a normalized companion-side audit/index surface.
- Phase 3 backlinks and graph edges are generated from R1-extracted citation records, not from marker inventories.
- Marker files remain useful for companion verification and later trace/recovery work, but they are not the Layer 2 edge source.

## Code Repair

- `pipeline/cleanup/reindex_markers.py`
  - `--force` now rebuilds even when marker anchors already align.
  - Equal-count anchor mismatches now rebuild by default instead of being skipped.
  - Skip behavior remains conservative only when marker counts exceed footnote anchors and `--force` is not set.

## Test Coverage Added

- `tests/test_companion_cleanup.py`
  - equal-count marker mismatch triggers rebuild
  - `--force` rebuilds aligned marker files
  - `companion_audit.py` reports real marker/footnote set drift and empty-article sentinels

## Memo 121 Interpretation

Accept Memo `121` as the authoritative record of the companion cleanup results:
- 76/76 marker alignment
- frontmatter/header/schema cleanup
- sentinel article completion

Do not use Memo `121` as the forward Phase 3 contract where it implies marker-driven backlink generation. This memo and Memo `122` now define the live handoff boundary.

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `reindex_markers.py`, cleanup tests, this memo, memo/index/ops references |
| `Verification run` | `done` | `pytest -q tests/test_companion_cleanup.py`, `python3 pipeline/cleanup/companion_audit.py`, `pytest -q` |
| `Artifacts refreshed` | `not-needed` | no staged or graph artifacts changed |
| `Remaining known drift` | `none` | forward contract now matches code and memo surfaces |
| `Next owner` | `ark` | verify the contract repair and confirm Memo `121` + Memo `122` now describe one forward path |
