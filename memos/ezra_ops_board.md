# Ezra Ops Board

Last updated: `2026-03-13`  
Live state source: `reports/book_status_dashboard.json`  
Drift check: `reports/coordination_state.json`

## Working Agreements
- Dashboard = live book truth.
- Ops board = live queue and next-owner dispatch.
- Project board = strategic gates and open decisions only.
- Memos = rationale, ratification packets, and substantial handoffs.
- Any state-changing Ark or Photius session should leave refreshed generated artifacts or explicit stale-state language.
- Ezra routes first, codes second, and owns the coordination drift alarm.

## Current Snapshot
- Promoted: `76`
- Fresh dossiers: `76/76`
- Stale dossiers: `0`
- Worktree: dirty
- Tests: `341 passed`
- OT canon lock still depends on Memo `91` and the `EST.4:6` disposition.
- Memo `88` is the proposed governing Phase 3 spec awaiting Human ratification.
- Phase 3 execution scaffold now exists in code:
  - `pipeline/graph/build_backlinks.py`
  - `pipeline/graph/regenerate_graph.py`
  - `pipeline/validate/validate_phase3.py`
  - `pipeline/tools/check_coordination_surfaces.py`
- Wikilink rollout seed is now implemented:
  - shared parser + audit/rewrite CLIs landed
  - `REV_articles.md` and `REV_footnotes.md` are normalized to wikilinks
  - Ark verification is requested before batch 2
- Ark has now published Memo `122` for full-corpus wikilink rollout.
- Memo `123` reconciles the handoff boundary:
  - marker files remain companion integrity/audit surfaces
  - R1 JSONL remains the Phase 3 backlink and graph input
- Memo `124` closes the cleanup tail taxonomy:
  - `pipeline/cleanup/` now means active reusable cleanup/audit tools
  - historical one-off repair scripts now live under `pipeline/archive/historical_cleanup/`

## Active Dispatch
| lane | owner | status | blocker | next_action |
|---|---|---|---|---|
| OT canon lock | Human | awaiting ratification | Memo `91` | Ratify or reject |
| Historical residual packet A | Human | awaiting ratification | Memo `51` | Ratify or reject |
| Phase 3 launch | Human -> Ark | ready pending ratification | Memo `88` | Ratify Memo `88`, then Ark runs the PSA backlink/graph pilot |
| Wikilink rollout verification | Ezra | active | Need corpus-level verification of Ark Memo `122` claims | Verify `0` convertible refs remain and Phase 3 graph/report outputs stay coherent |
| Phase 3 contract reconciliation | closed | implemented | none | Memo `121` and Memo `123` now agree on the R1-driven Phase 3 boundary |
| Coordination drift control | Ezra | active | none | Refresh `reports/coordination_state.json` after board/dashboard/memo changes |
| Phase 3 rollout verification | Ezra | active | Need full-corpus confirmation of Ark Memo `122` claims | Re-run audit/validation checks and package findings |

## Recently Completed (2026-03-13)
| lane | summary |
|---|---|
| 76-book canon completion | All 49 OT + 27 NT books promoted to `canon/` |
| Dossier freshness sweep | `76/76` fresh, `0` stale |
| Coordination hardening | Strategic board aligned to dashboard truth; drift checker/report added |
| Phase 3 scaffold | Layer 2 backlink builder, graph schema/regenerator, and Phase 3 validator landed |
| Historical OT cleanup separation | Job/Sirach/Psalms one-off recovery scripts moved out of live cleanup paths |
| Wikilink `REV` seed batch | Shared parser + extractor reuse landed; `425` bare refs rewritten to wikilinks in `REV` companions |
| Full wikilink rollout | Ark reports all staged companions normalized and Phase 3 artifacts regenerated in Memo `122` |
| Cleanup tail taxonomy | Historical one-off cleanup scripts archived; active cleanup namespace reduced to reusable tools |

## Standards Track
- Link syntax frozen: `[[GEN.1:1]]` outside `canon/`
- Backlink filename format frozen: `BOOK.CH-V.json`
- Backlink rollout frozen: pre-sharded from day one (`liturgical/`, `patristic/`, `study/`)
- `canon_uri` format locked: `canon/{OT|NT}/BOOK.md#BOOK.CH:V`
- Memo `88` status language: proposed governing spec until Human ratification
- DuckDB remains the intended Layer 3 store; `duckdb` is now an optional graph dependency

## Watch Items
- `reports/coordination_state.json` should stay green; if not, refresh narrative surfaces before selecting the next engineering lane.
- `reports/companion_file_census.json` is advisory, not a live ops source.
- `reports/phase3_validation_report.json` should be rechecked against Memo `122`; Ark reports full-corpus regeneration and warning-only duplicate inbound links.

## Ezra Loop
1. Read new memos, reports, and dashboard deltas.
2. Run or refresh the coordination check when governance or status surfaces change.
3. Update this ops board.
4. Emit concise next-owner asks for Ark, Human, and Photius.
5. Absorb one engineering lane only if direct action is safer or faster than delegation.
