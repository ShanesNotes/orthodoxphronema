# Orthodox Phronema Archive — Project Board

> **Last updated:** 2026-03-13
> **Role:** Official PM surface
> **Board owner:** Human (ShanesNotes)
> **Maintained by:** Ark, Ezra, Cowork
> **Live data source:** `reports/book_status_dashboard.json`
> **Coordination check:** `reports/coordination_state.json`
> **Daily dispatch:** `memos/ezra_ops_board.md`

---

## Vision

Build a durable, local-first, versioned Orthodox textual archive. The canon substrate is now complete across all 76 books. The next value layer is not more scripture extraction; it is reliable hyperlinking, derived graph structure, and future retrieval interfaces built without contaminating canon.

**Non-negotiables:** OSB purity · one-verse-per-line canon · commentary/scripture separation · traceable provenance · validation-first workflow

## Phase Map

| Phase | Name | Status | Gate |
|---|---|---|---|
| 1 | Canon Substrate | Complete | `76/76` books promoted |
| 2 | Canon Lock & Governance | Active | Human ratification of Memo `91` and Memo `51`; OT lock remains pending `EST` disposition |
| 3 | Hyperlinking & Graph | Ready to launch | Human ratification of Memo `88`, then Ark runs the first PSA pilot through Layer 2 + Layer 3 |
| 4 | Archive Interfaces | Planned | Wait for stable backlink shards and derived graph before MCP / retrieval exposure |

## Current Priorities

| Priority | Owner | Why now | Next action |
|---|---|---|---|
| OT canon lock packet | Human | Closes the last canon-governance ambiguity | Ratify or reject Memo `91` |
| Historical residual packet A | Human | Clears long-standing residual drift from active routing | Ratify or reject Memo `51` |
| Phase 3 ratification | Human | Unlocks the next engineering phase without reopening architecture | Ratify or reject Memo `88` |
| Phase 3 PSA pilot | Ark | The architecture is decided; the missing step is a real end-to-end pilot | Use the new backlink + graph scaffold on `PSA` after Memo `88` is ratified |
| Coordination drift control | Ezra | The repo is cleaner than the PM board unless checked explicitly | Refresh `reports/coordination_state.json` whenever dashboard or governance state changes |

## Open Decisions

| ID | Question | Owner | Status |
|---|---|---|---|
| `OT-LOCK-1` | Ratify the OT `V7` drift set and decide `EST` as repair vs source-absent ratification | Human | Open |
| `RES-2` | Ratify historical packet for `JDG`, `1SA`, `2SA` | Human | Open |
| `PHASE3-1` | Ratify Memo `88` as the governing Phase 3 document | Human | Open |

## Metrics

| Metric | Current |
|---|---|
| Total promoted books | `76` |
| Fresh promotion dossiers | `76/76` |
| Promoted books with stale dossiers | `0` |
| Open human ratification packets | `3` |
| OT non-`V7` warning books | `1` (`EST`) |
| Phase 3 execution scaffold | `R1 seed + backlink builder + graph schema + Phase 3 validator` |

## Coordination Contract

- `reports/book_status_dashboard.json` is the machine-readable source of live book truth.
- `memos/ezra_ops_board.md` is the tactical queue and next-owner dispatch surface.
- This board is strategic only: phase gates, open decisions, and stable metrics.
- `reports/coordination_state.json` is the drift alarm. If it fails, refresh the narrative surfaces before selecting the next lane.

## Notes

- The old repo-cleanup tail is now bounded: historical Phase 2 one-off repair scripts have been archived out of live cleanup paths, while `pipeline/cleanup/` is reserved for active reusable cleanup and audit tools.
- Memo `88` remains the proposed governing Phase 3 document until Human ratifies it. The repo should not describe it as already ratified.
- Auxiliary reports that are not named above are advisory, not live coordination truth, unless a memo or board line explicitly adopts them.
