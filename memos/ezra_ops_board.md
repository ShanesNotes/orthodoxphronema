# Ezra Ops Board

Last updated: `2026-03-11`  
Live state source: `reports/book_status_dashboard.json`

## Working Agreements
- Dashboard = live truth.
- Ops board = live queue and next-owner dispatch.
- Memos = rationale, decisions, and substantial handoffs.
- Any Ark or Photius session that changes staged, validation, or promotion-affecting state should leave a memo/report and refresh any affected generated artifacts.
- Human ratification asks stay capped at 3 open items.
- Ezra operates as strategic lead: route first, code second, and absorb at most one high-leverage engineering lane when direct action is safer or faster than delegation.

## Current Snapshot
- Promoted: `49`
- OT holdouts: `0`
- Editorially clean OT holdouts: `0`
- Promotion-ready books: `6`
- Extracting books: `15`
- NT extraction has landed: `27` NT books are staged per `memos/77_nt_extraction_results.md`
- Promoted dossiers are now fresh again after the canon verification pass.
- OT canon lock audit now has `0` structural errors and `18` warning-bearing books in `reports/canon_ot_structural_audit.json`.
- The only remaining non-`V7` OT canon warning is `EST` (`V4`/`V10` around `EST.4:6`).
- Canon-wide note markers (`†`, `ω`) have been removed from OT canon.
- OT promotion is complete; route OT lock work from `reports/canon_ot_structural_audit.json` plus Memos `84`, `89`, and `91`, not from the older holdout packet chain.
- Companion-layer census and Wave 1 NT transition are now complete enough to route from Memo `95`, not from the earlier provisional companion text.

## Today’s Dispatch
| lane | owner | status | artifact | blocker | next_action | done_when |
|---|---|---|---|---|---|---|
| OT Packet A checkpoint | Ezra | done | `memos/81_ot_packet_a_promotion_and_ezk_cleanup_checkpoint.md` | none | Keep `PRO` and `SIR` out of the active holdout lane; they are promoted now | Packet A is reflected in canon, dossiers, dashboard, and memo surfaces |
| `JOB` final residual lane | Ezra | done | `memos/84_ot_closeout_complete_and_canon_hygiene_handoff.md` | none | Keep `JOB` out of the active holdout lane; it is promoted now | `JOB` is reflected in canon, dossier, dashboard, and memo surfaces |
| `PSA` normalization and promotion | Ezra | done | `memos/83_psa_promotion_and_job_narrowed_residual_checkpoint.md` | none | Keep `PSA` out of the active holdout lane; it is promoted now | `PSA` is reflected in canon, dossier, dashboard, and memo surfaces |
| NT stabilization | Ark | active | `memos/77_nt_extraction_results.md` | Raw NT extraction landed with severe instability in books like `MAT`, `HEB`, and `EPH` | Prioritize `V1` dedup, `EPH` recovery, and chapter-count / chapter-zero fixes | NT extraction output is structurally trustworthy enough for cleanup lanes |
| OT canon lock follow-through | Ezra -> Human | active | `memos/91_ot_canon_lock_ratification_packet.md` | Human decision required for the `17`-book `V7` packet and `EST` disposition | Review Memo 91 and ratify or reject the packet | OT can be called `locked` or held with one explicit residual blocker |
| Historical residual Packet A | Ezra -> Human | active | `memos/51_historical_residual_ratification_packet_a.md` | Still awaiting human decision | Keep `JDG`, `1SA`, and `2SA` isolated from OT closeout packets | Human sees no more than 3 open ratification asks at once |
| Promoted OT staged/canon resync | Ezra | queued | `memos/89_ot_canon_lock_checkpoint.md` | The canon-first lock pass proved several promoted OT staged files are not safe as a bulk re-promotion base | Defer until Memo 91 is decided, then triage which promoted OT books can be safely resynced to canon | Canon lock status and staged-source-of-truth status are no longer conflated |
| Repo cleanup program | Ezra | active | `memos/85_long_horizon_repo_cleanup_program.md` | OT sprint left a large untracked helper/memo/variant tail | Triage the tail into `adopt`, `archive`, `consolidate`, and `delete_later` classes without destructive cleanup on the live branch | Long-horizon repo debt is explicit and no longer hidden in `git status` |
| NT companion extraction reset | Ezra | active | `memos/96_rom_nt_footnote_pilot_and_long_horizon_plan.md` | `ROM` pilot is complete, but Wave 1 replacement extraction has not started yet | Use `ROM` as the acceptance baseline and dispatch source-footnote replacement for `LUK`, `MAT`, `JOH`, `ACT`, and `REV` | Wave 1 placeholder footnote files are replaced by source-derived footnote files and the next NT wave is clearly ranked |

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
  - `48` untracked memo files are currently outside the indexed historical/governing set
  - `17` untracked cleanup scripts exist, many of them one-book or one-lane specialists
  - `5` staged variant scripture files (`*_photius.md`, `SIR_flash.md`) remain in the OT tree and should not survive as steady-state artifacts
  - cleanup now needs explicit triage, not blind deletion
- NT spot-audit findings:
  - `2JN` validates cleanly and remains the current NT `promotion_ready` exemplar.
  - `MAT` still has chapter-zero drift, chapter-count mismatch (`28` expected / `29` found), heavy `V3`, and embedded-verse failures.
  - `HEB` still has duplicate anchors, embedded verses, and `44` missing verses.
  - `EPH` remains the sharpest stabilization priority with chapter-zero drift, duplicate anchors, and a `50`-verse completeness gap.
- Ark stays on NT stabilization by default; OT should only interrupt for parser/schema escalations or a ready promotion checkpoint.
- Companion-layer dispatch has shifted from triage to extraction reset:
  - Wave 1 (`LUK`, `MAT`, `JOH`, `ACT`, `REV`) is accepted as `article_only`
  - legacy NT `_notes.md` files are now treated as article sources, not the primary source of NT footnotes
  - NT real footnotes should come from the OSB footnote page ranges and the verse labels printed there
  - marker files remain secondary linkage metadata for later structured wikilink work
  - `ROM` pilot now proves the extraction path is viable: `137` extracted entries, `112 / 130` marker-anchor overlap, one invalid shared anchor (`ROM.16:25`)
  - next extraction step is Wave 1 replacement (`LUK`, `MAT`, `JOH`, `ACT`, `REV`), not a broader marker-repair pass

## Blockers To Watch
- OT promotion is complete, but OT canon is not yet formally locked; use Memo 91 as the active decision packet and Memo 89 as the checkpoint behind it.
- `EST.4:6` is the only live non-`V7` OT canon blocker.
- Human has one bounded OT lock decision packet open in Memo 91.
- Fresh promoted dossiers can hide real canon debt if they are read as “fully clean”; use Memo 80 plus Memo 89 for that distinction.
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
- **Execution sequence:** Memo 86 tasks → Memo 87 tasks → Integration validation (memo 88 step 3).
- **Research folder** fully cleaned and naming-convention-compliant as of 2026-03-11. Convention codified in `research/README.md`.

## Long-Horizon Queue
- Promoted-canon freshness sweep after OT closeout, starting with `WIS`
- Promoted-canon cleanup packet after OT closeout, starting with `JOS` and `JDG`
- Helper-script consolidation and staged-variant retirement after current canon-hygiene packet
- Historical residual packet (`JDG`, `1SA`, `2SA`) remains open but separate from the OT holdout lane
- Phase 3 implementation: memo 86 → 87 → 88 integration (blocked on human ratification)
- NT extraction is active under Ark
- NT companion source-footnote replacement wave (`LUK`, `MAT`, `JOH`, `ACT`, `REV`) should follow the completed `ROM` pilot in Memo `96`

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
