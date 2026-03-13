# Ezra Ops Board

Last updated: `2026-03-12`  
Live state source: `reports/book_status_dashboard.json`

## Working Agreements
- Dashboard = live truth.
- Ops board = live queue and next-owner dispatch.
- Memos = rationale, decisions, and substantial handoffs.
- Any Ark or Photius session that changes staged, validation, or promotion-affecting state should leave a memo/report and refresh any affected generated artifacts.
- Human ratification asks stay capped at 3 open items.
- Ezra operates as strategic lead: route first, code second, and absorb at most one high-leverage engineering lane when direct action is safer or faster than delegation.

## Current Snapshot
- Promoted: `51`
- OT holdouts: `0`
- Editorially clean books: `6`
- Promotion-ready books: `4`
- Extracting books: `15`
- NT extraction has landed: `27` NT books are staged per `memos/77_nt_extraction_results.md`
- Shared `promote.py` / common-layer / `osb_extract.py` contract repair is complete; `pytest -q` is green at `327 passed`.
- Dashboard was refreshed on `2026-03-12`; `2JN` and `3JN` are now promoted into `canon/NT/`, and `1TH`, `2TH`, `2TI`, and `1JN` are now `promotion_ready` by current gate logic.
- Dossier freshness truth is now explicit: `70` dossiers are stale and `6` are fresh.
- OT canon lock audit now has `0` structural errors and `18` warning-bearing books in `reports/canon_ot_structural_audit.json`.
- The only remaining non-`V7` OT canon warning is `EST` (`V4`/`V10` around `EST.4:6`).
- Canon-wide note markers (`†`, `ω`) have been removed from OT canon.
- OT promotion is complete; route OT lock work from `reports/canon_ot_structural_audit.json` plus Memos `84`, `89`, and `91`, not from the older holdout packet chain.
- NT companion extraction is now complete enough to route from Memos `103` and `104`, not from the earlier reset/pilot packet alone.

## Today’s Dispatch
| lane | owner | status | artifact | blocker | next_action | done_when |
|---|---|---|---|---|---|---|
| Shared contract repair + state refresh | Ezra | done | `memos/98_contract_repair_and_state_refresh.md` | none | Route shared infra truth from Memo `98` plus evidence Memos `99` and `100` | Tests, dashboard, ops board, project board, and memo index agree |
| Future-layer seed (Genesis) | Ezra | done | `memos/105_genesis_future_layer_seed.md` | none | Route future-layer substrate work from Memo `105`; keep graph/vector work downstream of it | One live canonical slice proves pericope + R1 + embedding contracts without canon mutation |
| Reference alias authority | Ezra | done | `memos/106_reference_alias_authority_and_normalization_seed.md` | none | Route biblical reference normalization through the schema-backed alias registry; keep patristic passage resolution as a later lane | Biblical aliases are versioned and patristic alias growth no longer requires extractor constant churn |
| NT first canon promotion tranche (`2JN`, `3JN`) | Ezra | done | `memos/110_nt_first_canon_promotion_tranche_2jn_3jn.md` | none | Treat the first NT canon write as complete and re-rank the remaining NT queue from validator truth rather than dossier freshness alone | `2JN` and `3JN` exist in `canon/NT/` and their dossiers/dashboard agree on promoted state |
| NT post-promotion reranking (`1TH`, `2TH`, `2TI`, `1JN`) | Ezra | done | `memos/111_nt_post_promotion_reranking_and_purity_gate.md` | none | Treat the second NT tranche as queued-but-not-yet-clean; route the next lane as purity rather than auto-promotion | Four NT books are now gate-ready by current promote logic |
| NT warning reduction (`EPH`, `MAT`, `HEB`) | Ezra | done | `memos/109_nt_warning_reduction_eph_mat_heb.md` | none | Route the next NT lane away from the closed `EPH` / `HEB` warnings and treat `MAT` as the only residual from this batch | `EPH` and `HEB` validate cleanly and `MAT` is reduced to one `V8` warning |
| NT candidate marker purity pass (`1TH`, `2TH`, `2TI`, `1JN`) | Ezra | done | `memos/112_nt_candidate_marker_purity_pass.md` | none | Treat marker/footnote linkage as closed for the second tranche candidate set | All four books now pass `verify_footnotes.py` cleanly |
| NT candidate fused-word cleanup (`1TH`, `2TH`, `2TI`, `1JN`) | Ezra | active | `memos/112_nt_candidate_marker_purity_pass.md` | dry-run previews still show fused scripture residue such as `aafter`, `aliar`, and `apreacher` | Use the old per-book cleanup reports plus current dry-run previews to clear the next bounded purity blocker | The four fresh NT candidates are clean enough to promote, not just structurally valid and marker-clean |
| Promotion dossier freshness sweep | Ezra | active | `reports/book_status_dashboard.json` | `70` stale dossiers still distort most of the corpus if read as fresh readiness evidence | Keep the dashboard authoritative and package a bounded regeneration plan separately | Dossier freshness debt is explicit and no board surface overstates readiness |
| OT canon lock follow-through | Ezra -> Human | active | `memos/91_ot_canon_lock_ratification_packet.md` | Human decision required for the `17`-book `V7` packet and `EST` disposition | Review Memo 91 and ratify or reject the packet | OT can be called `locked` or held with one explicit residual blocker |
| Historical residual Packet A | Ezra -> Human | active | `memos/51_historical_residual_ratification_packet_a.md` | Still awaiting human decision | Keep `JDG`, `1SA`, and `2SA` isolated from OT closeout packets | Human sees no more than 3 open ratification asks at once |
| Repo cleanup program | Ezra | active | `memos/85_long_horizon_repo_cleanup_program.md` | OT sprint left a large untracked helper/memo/variant tail | Triage the tail into `adopt`, `archive`, `consolidate`, and `delete_later` classes without destructive cleanup on the live branch | Long-horizon repo debt is explicit and no longer hidden in `git status` |
| NT companion extraction completion | Photius | done | `memos/103_nt_footnote_stabilization_and_structural_audit.md` | none | Route NT companion truth from the full extraction set and keep marker mismatch as a secondary audit layer | All `27` NT `*_footnotes.md` files are source-derived and legacy NT `_notes.md` files are retired |
| PSA marker repair | Ark | active | `memos/108_nt_purity_patch_and_psa_marker_triage.md` | Psalm markers are not a local typo set; `73` raw markers currently collapse to `3` effective anchors with one invalid `PSA.0:7` | Open a dedicated marker-index repair lane instead of hand-editing the Psalm sidecar blindly | Psalm marker anchors reconcile against the stabilized 131-entry footnote file |

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
- Memo 72 supersedes Memo 71 for OT closeout routing.
- `PRO` is no longer a text-recovery problem; it is a governance-closeout problem. The last easy formatting residue has been removed.
- `SIR` was misclassified as light polish only. Chapter 1 had a leaked heading stream, and leaked Sirach headings also sat in chapters `4` and `6`.
- `SIR` has now been repaired to source-backed heading placement using the full Sirach `pdftotext` span. Chapter 1 now carries only `### Wisdom Is from the Lord`, and relocated headings now sit at chapters `7`, `8`, `19`, `38`, `39`, `40`, and `44`.
- `PRO` and `SIR` are now promoted.
- `JOB` is promoted. The final live warning is `V7` overcount against the current registry, not a remaining verse-sequence failure.
- `PSA` has been normalized, validated, and promoted by Ezra.
- Dashboard + dossiers are authoritative for OT closeout; older packet memos are historical unless ratified into newer dispatch.
- `pdftotext` remains the sanctioned scripture edge-case verifier; it closed the remaining `JOB` chapter-open gaps in this pass.
- Canon lock pass results are now explicit:
  - OT canon has `0` structural errors and `18` warning-bearing books
  - `17` of those warning books are `V7`-only versification drift cases
  - `EST` is the only remaining non-`V7` OT canon warning book
  - Memo 91 now packages the full Human decision packet for both the `V7` drift set and the `EST` disposition
  - canon-wide note markers have been removed from OT canon
  - `1MA`, `2MA`, `HAB`, and `LJE` no longer carry `V8` heading-density warnings
  - `JOB` no longer carries `V8` fragment-heading errors
  - the spell audit remains advisory (`905` suspects) and is not yet a lock blocker without curated confirmation
- Long-horizon repo cleanup truth:
  - `11` untracked memo files are currently outside the indexed historical/governing set
  - `6` untracked cleanup scripts remain outside the governed tool tree
  - untracked staged variant scripture files are now at `0`; the next cleanup target is loose root/helper drift, not parallel scripture artifacts
  - cleanup now needs explicit triage, not blind deletion
- Memo-governance reconciliation is now explicit:
  - evidence packets were renumbered to Memos `99`, `100`, and `101`
  - active routing should no longer cite duplicate Memo `90`, `91`, or `94` identities
- NT spot-audit findings:
  - `2JN` and `3JN` are now promoted into `canon/NT/`.
  - `1TH`, `2TH`, `2TI`, and `1JN` are now `promotion_ready` by current gate logic after fresh dry-runs.
  - `1TH`, `2TH`, `2TI`, and `1JN` now pass `verify_footnotes.py` cleanly after sidecar realignment.
  - The remaining blocker on the second NT tranche is fused-word scripture residue, not marker linkage.
  - `MAT` now passes structural validation and is down to one broad `V8` heading-density warning.
  - `HEB` now validates cleanly after heading consolidation.
  - `EPH` now validates cleanly after heading consolidation.
- Ark stays on NT stabilization by default; OT should only interrupt for parser/schema escalations or a ready promotion checkpoint.
- Companion-layer dispatch has shifted from reset to post-extraction purity:
  - all `27` NT `*_footnotes.md` files are now source-derived from OSB footnote page ranges
  - legacy NT `_notes.md` files are retired; surviving NT companion layers are `*_articles.md` plus `*_footnotes.md`
  - marker files remain secondary linkage metadata for later structured wikilink work
  - `JOH`, `LUK`, and `REV` were repaired in Memo `108`; the next NT purity pass should return to the wider warning set
  - `PSA_footnotes.md` is complete at `131` entries; the remaining Psalm blocker is marker-index corruption, not missing notes

## Blockers To Watch
- OT promotion is complete, but OT canon is not yet formally locked; use Memo 91 as the active decision packet and Memo 89 as the checkpoint behind it.
- `EST.4:6` is the only live non-`V7` OT canon blocker.
- Human has one bounded OT lock decision packet open in Memo 91.
- `70` stale dossiers mean readiness must be routed from the refreshed dashboard, not from older dossier assumptions.
- The current NT promote gate is broader than purity readiness; the second NT tranche is now held by fused-word scripture residue even though the books are structurally valid and marker-clean.
- `PSA` footnotes are stable, but Psalm marker linkage remains broken until `PSA_footnote_markers.json` is repaired.
- Promoted OT staged files are not currently safe as a wholesale re-promotion base; canon lock and staged resync must be tracked separately.
- The ops board must be reconciled whenever OT state changes; stale dispatch is itself an operational bug.

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
- Promotion dossier freshness sweep for `70` stale books; `2JN` / `3JN` are already fresh and promoted, and the next four NT candidates are now fresh dry-run surfaces
- Promoted-canon freshness sweep after OT closeout, starting with `WIS`
- Promoted-canon cleanup packet after OT closeout, starting with `JOS` and `JDG`
- Helper-script consolidation and staged-variant retirement after current canon-hygiene packet
- Historical residual packet (`JDG`, `1SA`, `2SA`) remains open but separate from the OT holdout lane
- Phase 3 implementation: memo 86 → 87 → 88 integration (blocked on human ratification)
- NT extraction is complete; the next NT lane should be re-ranked from fresh validator truth rather than stale readiness assumptions
- NT companion extraction is complete; the immediate next NT lane is the fused-word cleanup pass on `1TH`, `2TH`, `2TI`, and `1JN`

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
