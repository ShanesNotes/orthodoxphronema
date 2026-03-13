# Ezra Ops Board

Last updated: `2026-03-13`  
Live state source: `reports/book_status_dashboard.json`

## Working Agreements
- Dashboard = live truth.
- Ops board = live queue and next-owner dispatch.
- Memos = rationale, decisions, and substantial handoffs.
- Any Ark or Photius session that changes staged, validation, or promotion-affecting state should leave a memo/report and refresh any affected generated artifacts.
- Human ratification asks stay capped at 3 open items.
- Ezra operates as strategic lead: route first, code second, and absorb at most one high-leverage engineering lane when direct action is safer or faster than delegation.

## Current Snapshot
- Promoted: `76` (all books)
- OT holdouts: `0`
- Editorially clean books: `0`
- Promotion-ready books: `0`
- Extracting books: `12`
- NT extraction has landed: `27` NT books are staged per `memos/77_nt_extraction_results.md`
- Shared `promote.py` / common-layer / `osb_extract.py` contract repair is complete; `pytest -q` is green at `327 passed`.
- Dashboard was refreshed on `2026-03-13`; all `27` NT books and all `49` OT books are now promoted.
- Dossier freshness: `76/76` fresh, `0` stale (sweep completed `2026-03-13`).
- Legacy sidecar normalization fix applied to `promote.py` for ISA/LAM bare-list sidecars.
- OT canon lock audit now has `0` structural errors and `18` warning-bearing books in `reports/canon_ot_structural_audit.json`.
- The only remaining non-`V7` OT canon warning is `EST` (`V4`/`V10` around `EST.4:6`).
- Canon-wide note markers (`†`, `ω`) have been removed from OT canon.
- OT promotion is complete; route OT lock work from `reports/canon_ot_structural_audit.json` plus Memos `84`, `89`, and `91`, not from the older holdout packet chain.
- NT companion extraction is now complete enough to route from Memos `103` and `104`, not from the earlier reset/pilot packet alone.

## Active Dispatch
| lane | owner | status | blocker | next_action |
|---|---|---|---|---|
| OT canon lock | Human | awaiting ratification | Human decision on Memo 91 (17 V7 books + EST) | Ratify or reject, then Ark locks OT canon |
| Historical residual Packet A | Human | awaiting ratification | Human decision on Memo 51 (JDG/1SA/2SA) | Ratify or reject |
| NT extracting holds | — | parked | `GAL` detector false-positive, `PHP` registry drift, `ROM`/`1CO`/`ACT`/`REV` broader holds | Phase 3 or dedicated extraction sprint |
| Phase 3 implementation | Ark | ready | Awaiting human ratification of Memo 88 | Begin Memo 86 tasks → 87 → 88 integration |
| Memo archival | Ark | done | none | 155 memos archived; active set reduced to 32 |

## Recently Completed (2026-03-13)
| lane | summary |
|---|---|
| 76-book canon completion | All 49 OT + 27 NT books promoted to `canon/` |
| Dossier freshness sweep | 76/76 fresh, 0 stale; legacy sidecar fix for ISA/LAM |
| PSA marker repair | 131 anchors rebuilt from `PSA_footnotes.md`; types deferred to Phase 3 |
| Repo cleanup | No untracked files remain |
| NT companion extraction | All 27 `*_footnotes.md` source-derived; legacy `_notes.md` retired |
| Contract repair + state refresh | Shared infra, dashboard, tests all green (Memo 98) |
| Future-layer seed | Genesis pericope + R1 + embedding substrate proven (Memo 105) |
| Reference alias authority | Versioned biblical alias schema live (Memo 106) |

## Standards Track
- Link syntax frozen: `[[GEN.1:1]]` — applies everywhere outside `canon/` (ADJ-2 closed)
- Backlink filename format frozen: hyphen escape `BOOK.CH-V.json` (ADJ-1 closed)
- Backlink rollout: pre-sharded from day one — `liturgical/`, `patristic/`, `study/` (ADJ-3 closed)
- Canon directory: `canon/{OT|NT}/BOOK.md` (ADJ-4 closed)
- V11/V12: informational only, not promotion gates (ADJ-5 closed)
- `canon_uri` format locked: `canon/{OT|NT}/BOOK.md#BOOK.CH:V`
- Extraction policy codified: `pipeline/EXTRACTION_POLICY.md` — Docling primary for scripture, `pdftotext` authorized primary for notes/footnotes page ranges
- Future non-canon frontmatter reuse: continue using plain anchor tokens in machine fields such as `canon_anchors_referenced`
- Generated dashboard remains book-state only; standards visibility lives on this ops board

## Cross-Agent Awareness
- Dashboard + dossiers are authoritative; older packet memos are archived historical record.
- `pdftotext` remains the sanctioned scripture edge-case verifier.
- OT canon: `0` structural errors, `18` warning-bearing books (`17` V7-only + `EST`). Memo 91 packages the Human decision.
- Spell audit remains advisory (`905` suspects) — not yet a lock blocker.
- NT extracting holds: `GAL` (detector false-positive), `PHP` (registry drift), `ROM`/`1CO`/`ACT`/`REV` (broader structural debt).
- All `27` NT `*_footnotes.md` are source-derived; legacy `_notes.md` retired. Marker files are secondary linkage for Phase 3.
- PSA markers rebuilt (`131` anchors); type recovery (†/ω) deferred to Phase 3.
- `155` memos archived to `memos/archive/` on 2026-03-13. See `memos/INDEX.md` for the full map.

## Blockers To Watch
- OT canon lock awaits Human ratification of Memo 91 (17 V7 books + EST.4:6 disposition).
- Phase 3 implementation awaits Human ratification of Memo 88.
- Historical residual Packet A (Memo 51: JDG/1SA/2SA) still awaiting Human decision.
- Promoted OT staged files are not safe as a wholesale re-promotion base; canon lock and staged resync tracked separately.

## Release Train
- Packet A: `PRO` + `SIR` complete
- Packet B: `PSA` complete
- Packet C: `JOB` complete
- OT canon lock decision packet: Memo 91
- OT canon lock blocker: `EST` pending disposition
- OT canon ratification packet: `GEN`, `EXO`, `NUM`, `DEU`, `JDG`, `2KI`, `1CH`, `2CH`, `EZR`, `JOB`, `EZK`, `TOB`, `JDT`, `SIR`, `BAR`, `1MA`, `3MA`
- First post-lock deep polish target: `WIS`

## Phase 3 Design Status
- **Memo 88** — Ratified Phase 3 spec (supersedes both skeleton drafts). All five adjudications closed. Awaiting human ratification.
- **Memo 86** — R1 anchor extraction pipeline. Seven Cowork tasks defined. Awaiting ratification of memo 88.
- **Memo 87** — DuckDB citation graph + duckpgq risk register. Eight Cowork tasks defined. Depends on memo 86 output.
- **Memo 105** — Genesis future-layer seed implemented. One real slice now proves the metadata substrate (`pericope_index` + narrow R1 + derived embedding document) without graph/vector work.
- **Memo 106** — Reference alias authority implemented. Biblical reference normalization now routes through a versioned schema with a reserved patristic entity layer.
- **Execution sequence:** Memo 86 tasks → Memo 87 tasks → Integration validation (memo 88 step 3).
- **Research folder** fully cleaned and naming-convention-compliant as of 2026-03-11. Convention codified in `research/README.md`.

## Long-Horizon Queue
- Promoted-canon freshness sweep after OT closeout, starting with `WIS`
- Promoted-canon cleanup packet after OT closeout, starting with `JOS` and `JDG`
- Historical residual packet (`JDG`, `1SA`, `2SA`) remains open but separate from the OT holdout lane
- Phase 3 implementation: memo 86 → 87 → 88 integration (blocked on human ratification)
- NT extraction is complete; the next NT lane should route from the remaining extracting set and broader structural debt, not the former editorial queue
- NT companion extraction is complete; the promotion-rescue queue is now closed
- PSA marker type recovery (†/ω) deferred to Phase 3

## Photius Handoff Outcomes
- `accept` — evidence complete, scope allowed, verification clear
- `escalate_to_ark` — batch tool, registry implication, parser/validator implication, or mixed verification
- `return_for_evidence` — unclear changed files, missing source proof, or missing post-change verification

## Ezra Loop
1. Read newly landed memos, reports, and dashboard deltas.
2. Update this ops board.
3. Emit concise next-owner asks for Ark, Photius, and Human.
4. Decide whether Ezra should route, package, or directly absorb one high-leverage lane.
5. Keep only the top live blockers and active lanes visible.
