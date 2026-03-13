# NT First Canon Promotion Tranche (`2JN`, `3JN`) — 2026-03-12

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `2JN / 3JN NT promotion`
**Workstream:** `canon-hygiene`  
**Phase:** `4`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- The repaired promotion gate and refreshed dossier schema made the first NT canon write safe.
- The live dashboard showed only `2JN` and `3JN` as fresh, `promotion_ready` NT books before this tranche.
- The user explicitly authorized NT promotion and push to GitHub.

## Objective
- Promote the bounded ready NT tranche without broadening scope to warning-bearing NT books.
- Refresh the affected generated surfaces so canon, dossiers, and dashboard all agree on the new state.

## Files / Artifacts
- `canon/NT/2JN.md`
- `canon/NT/3JN.md`
- `reports/2JN_promotion_dossier.json`
- `reports/3JN_promotion_dossier.json`
- `reports/book_status_dashboard.json`

## Findings Or Changes
- Promoted `2JN` into `canon/NT/2JN.md` using the live promote pipeline.
- Promoted `3JN` into `canon/NT/3JN.md` using the live promote pipeline.
- Rewrote both promotion dossiers under the repaired schema, preserving promoted decision state and current registry version.
- Regenerated the dashboard so `2JN` and `3JN` moved from `promotion_ready` to `promoted`.
- Post-promotion machine state is now `51` promoted, `15` extracting, `10` editorially clean, `0` promotion-ready.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Promote only `2JN` and `3JN` | They were the only fresh, ready NT books in the dashboard | Leaves the rest of NT staged | Revert the two canon files and regenerate dossiers/dashboard if needed |
| Refresh dashboard immediately after promotion | Prevent stale queue routing | None beyond regenerated truth surfaces | Re-run the dashboard generator |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `python3 pipeline/promote/promote.py --book 2JN --dry-run` | pass | ready for promotion |
| `python3 pipeline/promote/promote.py --book 3JN --dry-run` | pass | ready for promotion |
| `python3 pipeline/promote/promote.py --book 2JN` | pass | `canon/NT/2JN.md` written |
| `python3 pipeline/promote/promote.py --book 3JN` | pass | `canon/NT/3JN.md` written |
| `python3 pipeline/tools/generate_book_status_dashboard.py` | pass | dashboard refreshed |
| `python3 pipeline/tools/check_stale_dossiers.py` | pass | `74` stale, `2` fresh; `2JN` and `3JN` fresh |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `canon/NT/2JN.md`, `canon/NT/3JN.md`, `reports/2JN_promotion_dossier.json`, `reports/3JN_promotion_dossier.json`, `reports/book_status_dashboard.json` |
| `Verification run` | `done` | promote dry-runs, live promote runs, dashboard regeneration, stale-dossier check |
| `Artifacts refreshed` | `done` | both dossiers and `reports/book_status_dashboard.json` |
| `Remaining known drift` | `present` | `74` stale dossiers remain across the wider corpus; NT queue must be re-ranked from validator truth |
| `Next owner` | `ezra` | refresh live dispatch and project surfaces to route the post-promotion NT queue |

## Requested Next Action
- Re-rank the remaining NT staged books from current validator results and pick the next bounded tranche instead of treating dossier freshness as readiness.

## Handoff
**To:** `ezra`  
**Ask:** `Update the ops board, project board, and memo index so the promoted NT tranche becomes the new baseline.`
