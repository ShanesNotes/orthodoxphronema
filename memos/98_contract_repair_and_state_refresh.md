# Contract Repair And State Refresh — 2026-03-12

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `shared pipeline contracts / dashboard truth / memo-governance reconciliation`
**Workstream:** `workflow`  
**Phase:** `2`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- Shared contract drift in `pipeline/promote/`, `pipeline/common/`, and `pipeline/parse/` had turned the test suite red and left the live coordination surfaces behind the actual repo state.
- Photius packaged the repair evidence in Memos `99` and `100`.
- The user authorized Ezra to take the direct engineering lane, then requested a full state refresh once the core repairs were complete.

## Objective
- Close the shared engineering repair lane with durable repo-native evidence.
- Refresh the machine and narrative state surfaces so they reflect current truth.
- Make stale dossier debt and memo-number governance drift explicit instead of leaving both hidden in old counts and duplicate filenames.

## Files / Artifacts
- `pipeline/promote/promote.py`
- `pipeline/common/{frontmatter.py,patterns.py,registry.py,text.py}`
- `pipeline/parse/osb_extract.py`
- `reports/book_status_dashboard.json`
- `memos/ezra_ops_board.md`
- `PROJECT_BOARD.md`
- `memos/INDEX.md`
- `memos/{98_contract_repair_and_state_refresh.md,99_structural_drift_evidence_packet.md,100_dossier_schema_drift_packet.md,101_photius_companion_recovery_evidence.md}`

## Findings Or Changes
- Repaired the shared promotion/common/parser drift that had been driving the failing suite.
  - `promote.py` now honors the composed gate flow and dossier/status expectations covered by the promote-gate tests.
  - common-layer compatibility was restored for registry, frontmatter, text, and pattern helpers.
  - `osb_extract.py` now handles typed records coherently and emits structured marker sidecar data that satisfies the verse-split contract.
- Re-ran the dashboard after the repair lane and surfaced the current state honestly.
  - Dashboard counts are now `49 promoted`, `15 extracting`, `10 editorially_clean`, `2 promotion_ready`.
  - `2JN` and `3JN` are the only fresh `promotion_ready` books.
  - `74` promotion dossiers are stale; this lane intentionally surfaced that debt and did not regenerate dossiers.
- Reconciled live memo-number drift.
  - Photius evidence packets were renumbered to Memos `99`, `100`, and `101`.
  - Placeholder template files were de-numbered out of the memo sequence.
  - Live coordination surfaces now point at canonical memo IDs instead of duplicate `90` / `91` / `94` references.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Refresh the dashboard before boards and memo index | Machine state is the source of truth for live routing | Dashboard can expose uncomfortable freshness debt | Re-run the generator after any later dossier batch |
| Surface stale dossier debt instead of regenerating dossiers immediately | Truth-first refresh is faster and safer than an unbounded dossier batch | Readiness counts drop sharply | Schedule a dedicated freshness sweep as the next Ezra ops lane |
| Renumber duplicate evidence/support memos instead of preserving collisions | Duplicate memo numbers break routing and index integrity | Historical references can become ambiguous during the transition | Keep a reconciliation table in `memos/INDEX.md` |
| De-number placeholder templates | Template files should not occupy governed memo IDs | Older narrative references to the placeholder slot remain awkward | Replace broken references with explicit reconciled wording |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Full test suite | `pass` | `pytest -q` -> `321 passed in 0.83s` |
| Dashboard regeneration | `pass` | `python3 pipeline/tools/generate_book_status_dashboard.py` |
| Dossier freshness census | `warn` | `python3 pipeline/tools/check_stale_dossiers.py` -> `74` stale, `2` fresh |
| Promotion-ready census | `pass` | `reports/book_status_dashboard.json` -> `2JN`, `3JN` only |
| Memo-number reconciliation | `pass` | `memos/INDEX.md` numbering reconciliation table plus canonical filenames |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | shared pipeline files, refreshed dashboard, ops board, project board, memo index, new Memo `98`, reconciled Memo `99` / `100` / `101` |
| `Verification run` | `done` | `pytest -q`; `python3 pipeline/tools/generate_book_status_dashboard.py`; `python3 pipeline/tools/check_stale_dossiers.py` |
| `Artifacts refreshed` | `done` | `reports/book_status_dashboard.json`, `memos/ezra_ops_board.md`, `PROJECT_BOARD.md`, `memos/INDEX.md` |
| `Remaining known drift` | `present` | `74` stale promotion dossiers remain; OT lock still hinges on Memo `91`; `reports/2JN_promotion_dossier.json` was intentionally not rewritten |
| `Next owner` | `ark` | Resume book-level NT stabilization with the shared infra blocker closed |
