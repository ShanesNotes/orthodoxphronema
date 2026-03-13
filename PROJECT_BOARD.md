# Orthodox Phronema Archive — Project Board

> **Last updated:** 2026-03-12
> **Role:** Official PM surface
> **Board owner:** Human (ShanesNotes)
> **Maintained by:** Ark, Ezra, Cowork
> **Live data source:** `reports/book_status_dashboard.json`
> **Daily dispatch:** `memos/ezra_ops_board.md`

---

## Vision

Build a durable, local-first, versioned Orthodox textual archive. Start with a pure OSB scripture substrate across the 76-book Orthodox canon, then expand into a traceable graph of footnotes, patristic sources, liturgical references, and study material without contaminating canon.

**Non-negotiables:** OSB purity · one-verse-per-line canon · commentary/scripture separation · traceable provenance · validation-first workflow

## Phase Map

| Phase | Name | Status | Gate |
|---|---|---|---|
| 1 | OT Closeout | Complete | `49/49` OT books promoted |
| 2 | Canon Hygiene & Freshness | Active | OT canon lock pass is down to `EST` plus a `V7` ratification packet |
| 3 | Hyperlinking & Graph | Planned — **subset unblocked** | Companion readiness now proceeds via source-footnote extraction, starting with `ROM` |
| 4 | NT Bootstrap | Active | NT extraction landed; shared contract drift is repaired; stabilization is now the live Ark lane |

## Kanban

### Backlog

| Item | Owner | Phase | Notes |
|---|---|---|---|
| Helper-script consolidation | Ezra | 2 | Untracked one-off OT/NT recovery scripts need classification into adopt/archive/delete_later |
| Staged variant retirement | Ezra | 2 | `*_photius.md` and flash variants should not remain as steady-state scripture artifacts |
| Phase 3 schema and link ratification | Human | 3 | Resolve file layout, link scope, and enforcement gates before implementation |
| NT page-range probes | Human | 4 | `memos/68_nt_page_range_probe_request.md`; start with the Gospels |
| NT marker-density reconciliation follow-up | Photius | 4 | Companion extraction is complete; next bounded support lane is marker/note mismatch analysis after Ark repairs scripture purity blockers |

### Active

| Item | Owner | Phase | Status | Blocker |
|---|---|---|---|---|
| NT scripture warning reduction | Ark | 4 | Active | `JOH`, `LUK`, and `REV` have been patched; the next warning-heavy priorities are back in `EPH`, `MAT`, and `HEB` |
| Promotion dossier freshness sweep | Ezra | 2 | Active | `74` stale dossiers now suppress truthful `promotion_ready` counts; only `2JN` and `3JN` remain fresh |
| OT canon lock follow-through | Ezra | 2 | Active | `EST.4:6` remains the only non-`V7` OT canon blocker; promoted OT staged files need separate resync planning |
| `WIS` canon hygiene + staged/editorial resync | Ezra | 2 | Queued behind OT lock closeout | Canon is clean, but staged/editorial surfaces still need reconciliation |
| Repo cleanup and artifact triage | Ezra | 2 | Active | OT sprint left a large untracked memo/helper/variant tail |
| PSA marker/index repair | Ark | 2 | Active | `PSA_footnotes.md` is stable, but `PSA_footnote_markers.json` is corrupted (`PSA.0:*`) |

### In Review / Awaiting Decision

| Item | Owner | Decision needed from | Notes |
|---|---|---|---|
| OT lock ratification packet | Ezra | Human | `EST` disposition plus the OT `V7` drift set; see `memos/91_ot_canon_lock_ratification_packet.md` |
| Historical residual packet (`JDG`, `1SA`, `2SA`) | Ezra | Human | `memos/51_historical_residual_ratification_packet_a.md` |
| ~~Phase 3 adjudications~~ | — | — | **All closed 2026-03-10.** ADJ-2: phronema-only. ADJ-3: pre-sharded. ADJ-5: informational. |

### Done (Recent)

| Item | Completed | Memo / Surface |
|---|---|---|
| Workflow consolidation and memo governance reset | 2026-03-10 | `memos/70_workflow_consolidation.md` |
| `PSA` promotion and `JOB` narrowing checkpoint | 2026-03-11 | `memos/83_psa_promotion_and_job_narrowed_residual_checkpoint.md` |
| OT closeout complete | 2026-03-11 | `memos/84_ot_closeout_complete_and_canon_hygiene_handoff.md` |
| Long-horizon repo cleanup program | 2026-03-11 | `memos/85_long_horizon_repo_cleanup_program.md` |
| OT canon lock checkpoint | 2026-03-11 | `memos/89_ot_canon_lock_checkpoint.md` |
| NT footnote extraction reset | 2026-03-11 | `memos/95_nt_footnote_extraction_reset.md` |
| `ROM` NT footnote pilot and rollout plan | 2026-03-11 | `memos/96_rom_nt_footnote_pilot_and_long_horizon_plan.md` |
| V11 / V12 activation and Phase 2→3 bootstrap | 2026-03-10 | `memos/69_v11v12_activation_and_phase2_3_bootstrap.md` |
| Human-review queue reduction batch 2 | 2026-03-10 | `memos/64_second_human_review_queue_reduction_batch.md` |
| OT purity audit tooling | 2026-03-10 | `memos/62_ot_purity_pass_and_editorial_queue_integration.md` |
| Completion handshake protocol | 2026-03-10 | `memos/60_completion_handshake_and_stale_state_clarity.md` |
| Shared contract repair + state refresh | 2026-03-12 | `memos/98_contract_repair_and_state_refresh.md` |
| Genesis future-layer seed | 2026-03-12 | `memos/105_genesis_future_layer_seed.md` |
| Reference alias authority and normalization seed | 2026-03-12 | `memos/106_reference_alias_authority_and_normalization_seed.md` |
| NT companion extraction stabilization audit | 2026-03-12 | `memos/103_nt_footnote_stabilization_and_structural_audit.md` |
| PSA footnote extraction refresh | 2026-03-12 | `memos/104_psa_footnote_extraction_report.md` |
| NT purity patch and PSA marker triage | 2026-03-12 | `memos/108_nt_purity_patch_and_psa_marker_triage.md` |

## Release Train

| Track | Books | Status |
|---|---|---|
| Packet A | `PRO`, `SIR` | Complete |
| Packet B | `PSA` | Complete |
| Packet C | `JOB` | Complete |
| OT lock blocker | `EST` | Resolve or ratify `EST.4:6` before calling OT canon locked |
| OT lock ratification packet | `GEN`, `EXO`, `NUM`, `DEU`, `JDG`, `2KI`, `1CH`, `2CH`, `EZR`, `JOB`, `EZK`, `TOB`, `JDT`, `SIR`, `BAR`, `1MA`, `3MA` | `V7`-only warning set |
| Deep polish target | `WIS` | Canon is structurally clean; staged/editorial surfaces still need reconciliation |
| Repo cleanup tail | helper scripts, staged variants, memo sprawl | Classify before deletion or adoption |

## Open Decisions

| ID | Question | Owner | Status |
|---|---|---|---|
| `OT-LOCK-1` | Ratify the OT `V7` drift set and decide `EST` as repair vs source-absent ratification | Human | Open |
| `RES-2` | Ratify historical packet for `JDG`, `1SA`, `2SA` | Human | Open |
| `NT-COMP-1` | Accept the NT companion reset: legacy `_notes.md` are article sources, and real NT footnotes should be extracted from OSB footnote page ranges with marker linkage deferred | Human | Implemented; formal ratification still open |
| `ADJ-2` | `[[BOOK.CH:V]]` scope | Human | **Closed (revised):** Everywhere outside canon. Phronema, notes, and articles all use `[[BOOK.CH:V]]` — including internal cross-references within footnotes (e.g., a GEN.1:1 footnote citing JON.3:16). Canon files remain untouched. |
| `ADJ-3` | Backlink rollout shape | Human | **Closed:** Pre-sharded from day one (`liturgical/`, `patristic/`, `study/`). |
| `ADJ-5` | `V11` / `V12` enforcement | Human | **Closed:** Informational only — not promotion gates. Phase 3 not blocked by backfill status. |

## Agent Summary

| Agent | Role | Primary surfaces | Authority |
|---|---|---|---|
| Ark | Architecture, core pipeline, promotion | `pipeline/`, `canon/`, numbered memos | Governing implementation owner |
| Ezra | Strategic lead, audit, dispatch, selective engineering | `memos/ezra_ops_board.md`, numbered memos | Governing review/throughput owner |
| Photius | Parsing, staged recovery, cleanup, companion extraction | `staging/validated/`, `pipeline/cleanup/`, companion reports, evidence memos | Governing within bounded staging scope |
| Cowork | PM, workflow optimization, research synthesis | `PROJECT_BOARD.md`, `memos/INDEX.md`, `research/` | Official PM surface owner; non-governing outside ratified surfaces |
| External AI | Research or design input | `research/` | Never governing unless ratified by numbered memo |

## Research Synthesis (2026-03-10)

8 research artifacts reviewed. Key findings consolidated here for decision-making.

**Architecture validated:** All external inputs (Gemini, Grok, Otzaria study, DraCor, SanghaGPT, SpiritRAG) independently confirm flat-file MD + domain-sharded JSON + regeneratable DuckDB as the correct architecture. No native graph DB warranted. CTS/TEI rejected. Custom anchor format confirmed.

**Phase 4 trajectory confirmed:** The Otzaria MCP study validates embedded DuckDB + Python MCP SDK + docstring engineering as the optimal pattern for exposing this archive to LLM agents. Phronema would be the first Orthodox corpus exposed via MCP. Existing anchor format and directory structure are already MCP-resource-compatible.

**Three workflow optimizations identified:**
1. **Docstring engineering (applies now):** Agent protocol files (CLAUDE.md, GEMINI.md, AGENTS.md) function as tool docstrings. Precision in these files directly reduces pipeline errors. Tighten anchor format rules and validation expectations in all agent-facing docs.
2. **Planner-executor contracts (applies to Phase 3):** SpiritRAG pattern — formalize inter-agent handoffs as typed schemas rather than prose. The completion handshake is a start; Phase 3 backlink extraction needs explicit contracts between Photius (scan), Ark (generate L2), and the regenerator (build L3).
3. **Context decoupling (applies now):** Otzaria pattern — agents should reference anchors and dossier findings, not paste full book contents. Tighten agent protocol to prefer anchor-based references over full-text inclusion.

**ADJ-3 recommendation strengthened:** Every research artifact that addresses rollout strategy recommends pre-sharded from day one. The DuckDB regeneration script already assumes it. Monolithic start would require migration. Strong consensus for closing ADJ-3 as "pre-sharded."

**Research artifacts:** `research/` (15 files). See `memos/INDEX.md` for full listing.

## Metrics

| Metric | Current |
|---|---|
| OT books promoted | `49/49` |
| OT canon structural errors | `0` |
| OT canon warning books | `18` |
| OT non-`V7` warning books | `1` (`EST`) |
| OT holdouts | `0` |
| Promotion-ready books | `2` (`2JN`, `3JN`) |
| Editorially clean books | `10` |
| Extracting books | `15` |
| Promoted books with stale dossiers | `74` |
| High-priority post-lock reconciliation books | `WIS` |
| Active memo files in `memos/` | `177` |
| Research artifacts in `research/` | `27` |
| Untracked memo files | `11` |
| Untracked cleanup scripts | `6` |
| Untracked staged variants | `0` |
| Open Phase 3 adjudications | `0` (all closed 2026-03-10) |
| NT Wave 1 companion books accepted as `article_only` | `5` |
| NT books with real source-derived footnotes | `27` |
| NT legacy `_notes.md` companions remaining | `0` |

## File Map

| Surface | Path | Purpose | Cadence |
|---|---|---|---|
| Project board | `PROJECT_BOARD.md` | Vision, phases, priorities, decisions, metrics | Update when priorities or gates change |
| Ops board | `memos/ezra_ops_board.md` | Daily dispatch, next owner, blockers | Update per agent session |
| Memo index | `memos/INDEX.md` | Memo governance and classification | Update when memos move or change status |
| Machine state | `reports/book_status_dashboard.json` | Book-level validation and dossier truth | Regenerate after state-changing work |
| Agent protocol | `AGENTS.md` | Role boundaries and workflow rules | Update only for protocol changes |
| Research lane | `research/` | Non-governing design, synthesis, and external inputs | Add as advisory artifacts arrive |

## Board ↔ Ops Board Relationship

These two surfaces are complementary:

- `PROJECT_BOARD.md` answers: what matters, why it matters, what phase it belongs to, and which decisions remain open.
- `memos/ezra_ops_board.md` answers: who should pick up what next, what just finished, and what is immediately blocked.

Flow:
- priorities and phase gates are set here
- Ezra translates them into tactical dispatch on the ops board
- completed work or closed decisions then roll back up here

Neither surface should try to replace the other.
