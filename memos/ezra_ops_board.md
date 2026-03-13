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

## Today’s Dispatch
| lane | owner | status | artifact | blocker | next_action | done_when |
|---|---|---|---|---|---|---|
| Shared contract repair + state refresh | Ezra | done | `memos/98_contract_repair_and_state_refresh.md` | none | Route shared infra truth from Memo `98` plus evidence Memos `99` and `100` | Tests, dashboard, ops board, project board, and memo index agree |
| Future-layer seed (Genesis) | Ezra | done | `memos/105_genesis_future_layer_seed.md` | none | Route future-layer substrate work from Memo `105`; keep graph/vector work downstream of it | One live canonical slice proves pericope + R1 + embedding contracts without canon mutation |
| Reference alias authority | Ezra | done | `memos/106_reference_alias_authority_and_normalization_seed.md` | none | Route biblical reference normalization through the schema-backed alias registry; keep patristic passage resolution as a later lane | Biblical aliases are versioned and patristic alias growth no longer requires extractor constant churn |
| NT first canon promotion tranche (`2JN`, `3JN`) | Ezra | done | `memos/110_nt_first_canon_promotion_tranche_2jn_3jn.md` | none | Treat the first NT canon write as complete and re-rank the remaining NT queue from validator truth rather than dossier freshness alone | `2JN` and `3JN` exist in `canon/NT/` and their dossiers/dashboard agree on promoted state |
| NT post-promotion reranking (`1TH`, `2TH`, `2TI`, `1JN`) | Ezra | done | `memos/111_nt_post_promotion_reranking_and_purity_gate.md` | none | Treat the reranking lane as historical context behind the closed second NT tranche | Four NT books were identified as the next safe tranche candidate set |
| NT warning reduction (`EPH`, `MAT`, `HEB`) | Ezra | done | `memos/109_nt_warning_reduction_eph_mat_heb.md` | none | Route the next NT lane away from the closed `EPH` / `HEB` warnings and treat `MAT` as the only residual from this batch | `EPH` and `HEB` validate cleanly and `MAT` is reduced to one `V8` warning |
| NT candidate marker purity pass (`1TH`, `2TH`, `2TI`, `1JN`) | Ezra | done | `memos/112_nt_candidate_marker_purity_pass.md` | none | Treat marker/footnote linkage as closed for the second tranche candidate set | All four books now pass `verify_footnotes.py` cleanly |
| NT second canon promotion tranche (`1TH`, `2TH`, `2TI`, `1JN`) | Ark | done | `memos/113_nt_second_canon_promotion_tranche.md` | none | Treat the fused-word cleanup lane as closed and route the next NT lane from refreshed dashboard truth | `1TH`, `2TH`, `2TI`, and `1JN` exist in `canon/NT/` and their dossiers/dashboard agree on promoted state |
| NT promotion packet (`JUD`, `PHM`) | Ark | done | `memos/114_nt_jud_phm_promotion_packet.md` | none | Treat the small-book promotion packet as complete and route the next NT cleanup lane from the remaining four staged books | `JUD` and `PHM` exist in `canon/NT/` and their dossiers/dashboard agree on promoted state |
| NT Titus cleanup and promotion | Ark | done | `memos/115_nt_titus_cleanup_and_promotion.md` | none | Treat the TIT lane as closed and route the next NT packet from the final three staged books | `TIT` exists in `canon/NT/` and its dossier/dashboard agree on promoted state |
| NT final editorial queue closeout (`2PE`, `1TI`, `JAS`) | Ark | done | `memos/116_nt_final_editorial_queue_closeout.md` | none | Treat the NT editorial queue as closed and reroute NT work away from promotion rescue | `2PE`, `1TI`, and `JAS` exist in `canon/NT/`, their dossiers are fresh, and the dashboard shows no remaining `editorially_clean` books |
| NT extracting tranche A checkpoint (`EPH`, `GAL`, `PHP`) | Ark | active | `memos/117_nt_extracting_tranche_a_eph_promoted_gal_held.md` | `GAL` is blocked only by a detector false positive at `GAL.5:24`, while `PHP` is blocked by registry-versification drift rather than local scripture residue | Keep `EPH` closed, route `GAL` as a small policy/heuristic follow-up, and keep `PHP` out of the local cleanup lane | The tranche-A residuals are either promoted or explicitly reclassified away from scripture surgery |
| NT extracting tranche B promotions and phase C holds (`2CO`, `HEB`) | Ark | done | `memos/118_nt_extracting_tranche_b_promotions_and_phase_c_holds.md` | none | Treat `2CO` and `HEB` as closed promotions and route `ROM`, `1CO`, `ACT`, and `REV` as broader holds rather than quick promote books | `2CO` and `HEB` exist in `canon/NT/`, their dossiers are fresh, and the remaining extracting queue is explicitly reclassified |
| Promotion dossier freshness sweep | Ark | done | `reports/book_status_dashboard.json` | none | Dossier freshness is now `76/76`; legacy sidecar normalization fix landed for ISA/LAM | All `76` dossiers are fresh and dashboard is regenerated |
| OT canon lock follow-through | Ezra -> Human | active | `memos/91_ot_canon_lock_ratification_packet.md` | Human decision required for the `17`-book `V7` packet and `EST` disposition | Review Memo 91 and ratify or reject the packet | OT can be called `locked` or held with one explicit residual blocker |
| Historical residual Packet A | Ezra -> Human | active | `memos/51_historical_residual_ratification_packet_a.md` | Still awaiting human decision | Keep `JDG`, `1SA`, and `2SA` isolated from OT closeout packets | Human sees no more than 3 open ratification asks at once |
| Repo cleanup program | Ark | done | `memos/85_long_horizon_repo_cleanup_program.md` | none | No untracked files remain as of `2026-03-13`; the untracked tail described in Memo 85 has been resolved | `git status -u` shows no untracked files |
| NT companion extraction completion | Photius | done | `memos/103_nt_footnote_stabilization_and_structural_audit.md` | none | Route NT companion truth from the full extraction set and keep marker mismatch as a secondary audit layer | All `27` NT `*_footnotes.md` files are source-derived and legacy NT `_notes.md` files are retired |
| PSA marker repair | Ark | done | `staging/validated/OT/PSA_footnote_markers.json` | none | Rebuilt `131` anchors from `PSA_footnotes.md`; marker types set to `unknown` pending Phase 3 recovery; original raw markers preserved as audit trail | `verify_footnotes.py --book PSA` passes cleanly |

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
- Long-horizon repo cleanup: resolved. No untracked files remain as of `2026-03-13`.
- Memo-governance reconciliation is now explicit:
  - evidence packets were renumbered to Memos `99`, `100`, and `101`
  - active routing should no longer cite duplicate Memo `90`, `91`, or `94` identities
- NT spot-audit findings:
  - `2JN` and `3JN` are now promoted into `canon/NT/`.
  - `1TH`, `2TH`, `2TI`, and `1JN` are now promoted into `canon/NT/`.
  - `JUD` and `PHM` are now promoted into `canon/NT/`.
  - `TIT` is now promoted into `canon/NT/`.
  - `2PE`, `1TI`, and `JAS` are now promoted into `canon/NT/`.
  - `EPH` is now promoted into `canon/NT/`.
  - `2CO` and `HEB` are now promoted into `canon/NT/`.
  - `1TH`, `2TH`, `2TI`, and `1JN` pass `verify_footnotes.py` cleanly and now show `0` purity-audit candidates.
  - `JUD` and `PHM` pass `verify_footnotes.py` cleanly and now show `0` purity-audit candidates.
  - `TIT` now passes validation cleanly, passes `verify_footnotes.py`, and shows `0` purity-audit candidates after its local `3:15` closeout.
  - `2PE`, `1TI`, and `JAS` now pass `verify_footnotes.py` cleanly and show `0` purity-audit candidates.
  - `EPH` now passes validation cleanly, passes `verify_footnotes.py`, and shows `0` purity-audit candidates.
  - `2CO` now passes validation cleanly, passes `verify_footnotes.py`, and shows `0` purity-audit candidates after the source-confirmed `2CO.13:14` closeout.
  - `HEB` now passes validation cleanly, passes `verify_footnotes.py`, and shows `0` purity-audit candidates after the sidecar rebuild and residue sweep.
  - `GAL` is locally cleaned and its footnotes align, but the current purity/V11 detectors still false-positive on `GAL.5:24` (`Christ’s have`).
  - `PHP` is not a local text-repair book right now; its active `V7` warning is registry drift (`30/30/21/23` staged vs `30/23/25/17` in registry).
  - `ROM` remains an extracting hold with a `V7` gap and invalid `ROM.16:25` footnote/marker anchor.
  - `1CO` remains an extracting hold with a `V7` gap plus heavy purity and marker drift.
  - `ACT` remains an extracting hold with accepted `V8` only structurally, but heavy purity and footnote-sidecar drift.
  - `REV` remains an extracting hold with live `V12` inline verse-number leakage plus heavy purity and marker drift.
  - The NT editorial queue is closed; remaining NT work should route to extraction or broader structural lanes, not more promotion rescue.
  - The second NT tranche blocker chain is closed; the next NT lane should be reranked from current dashboard truth instead of the former fused-word packet.
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
- Dossier freshness is resolved (`76/76` fresh); readiness can now be routed from dossiers directly.
- The current NT promote gate remains broader than purity readiness in general, but the former second-tranche fused-word blocker has been cleared and promoted.
- `PSA` footnotes and markers are now reconciled (`131` anchors); marker type recovery deferred to Phase 3.
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
