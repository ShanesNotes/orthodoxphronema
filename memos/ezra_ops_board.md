# Ezra Ops Board

Last updated: `2026-03-10`  
Live state source: `reports/book_status_dashboard.json`

## Working Agreements
- Dashboard = live truth.
- Ops board = live queue and next-owner dispatch.
- Memos = rationale, decisions, and substantial handoffs.
- Any Ark or Photius session that changes staged, validation, or promotion-affecting state should leave a memo/report and refresh any affected generated artifacts.
- Human ratification asks stay capped at 3 open items.
- Ezra operates as strategic lead: route first, code second, and absorb at most one high-leverage engineering lane when direct action is safer or faster than delegation.

## Current Snapshot
- Promoted: `2`
- Promotion ready: `16`
- Structurally passable: `12`
- Editorially clean but still blocked: `17`
- Extracting / not ready: `29`
- Dashboard remains the machine-readable book-state surface; long-horizon standards and cross-agent awareness live here.
- Queue drift is currently visible for `1ES`, `1KI`, and `JOS`; daily routing must read memos and dossiers, not dashboard status alone.

## Today’s Dispatch
| lane | owner | status | artifact | blocker | next_action | done_when |
|---|---|---|---|---|---|---|
| Strategic routing / throughput lead | Ezra | active | `memos/59_ezra_strategic_leadership_role_ratification.md` | leadership value disappears if Ezra gets buried in too many direct edits | Keep queue control, contradiction detection, release routing, and one-lane engineering triage explicit in every session | The team has one clear strategic router without role confusion or management overhead |
| JOS structural reset | Ark | active | `memos/56_batch_a_footnote_audit_and_jos_structural_warning.md` | dashboard and dossier are structurally passable, but Memo 56 documents chapter-20 absorption and marker/index desync | Re-partition `JOS` against OSB chapter truth, then refresh affected marker and dossier artifacts | `JOS` no longer depends on a semantically broken Chapter 20 container |
| 1KI structural reset | Ark | queued | `memos/54_footnote_alignment_report_1es_1ki.md` | Memo 54 documents chapter drift across 10-15 and stale marker state | Queue behind `JOS`, unless Ark finds the shared defect is easier to repair first in `1KI` | `1KI` chapter boundaries and marker artifacts align to OSB structure |
| RUT + 1ES release packet | Ezra | active | `memos/57_daily_plan_reset_structural_holds_and_promotion_harvest.md` | `1ES` has checksum drift between staged text and dossier; `RUT` is clean but not yet packaged | Mark `RUT` as same-day promote candidate; mark `1ES` as dossier-refresh candidate and package them together once aligned | One bounded packet lands with exact `promote` or `refresh_then_promote` asks |
| Minor Prophets promotion harvest | Ezra | active | `memos/48_minor_prophets_complete_and_session_status.md` | the ready pool is large enough to sprawl unless packetized | Split `AMO`, `MIC`, `OBA`, `JON`, `NAH`, `ZEP`, `HAG`, `ZEC`, and `MAL` into small promotion packets; route `JOL`, `HAB`, and `HOS` separately | Minor Prophets have explicit packet owners instead of one undifferentiated ready pile |
| OT purity pass tooling | Ark + Ezra | implemented | `memos/62_ot_purity_pass_and_editorial_queue_integration.md` | chapter-opening truncation and split-word residue were systemic but under-surfaced | Keep `purity_audit.py` as the non-mutating sweep entrypoint and the editorial sidecar as the single queue | The team has one purity audit surface instead of ad hoc notes and one-off scripts |
| OT purity sweep on structurally sound books | Photius | active | `memos/62_ot_purity_pass_and_editorial_queue_integration.md` | major/prophetic chapter-open losses and conjoined words remain live in staged text | Run `purity_audit.py`, merge findings into `BOOK_editorial_candidates.json`, verify against OSB PDF where needed, and leave completion-handshake memos | Promotion-ready and editorially clean books have refreshed purity queues instead of hidden chapter-open defects |
| Human-review queue reduction | Ezra | implemented | `memos/63_human_review_queue_reduction_via_pdf_verification.md` | stale or over-broad drop-cap review debt was obscuring the true manual queue | Keep targeting the books with the largest remaining `ambiguous_human` drop-cap counts; do not spend Human time on `EXO` or `DAN` chapter-open review anymore | Human review is reserved for truly unresolved PDF ambiguities |
| Human-review queue reduction batch 2 | Ezra | implemented | `memos/64_second_human_review_queue_reduction_batch.md` | several historical books still looked blocked on chapter-open review even though staged text was already clean | Treat `2CH`, `1SA`, `1CH`, `2KI`, `JDG`, `2SA`, and `JOS` as cleared for chapter-open review; keep only `AMO` in the active ambiguity lane | The manual queue is small, explicit, and no longer dominated by stale sidecars |
| Footnote alignment on structurally sound books | Photius | active | `memos/50_photius_nonscripture_extraction_audit.md` | structural holds can waste cleanup effort if treated as normal alignment work | Continue on sound books such as `EXO` and ready historical books; switch `JOS` and `1KI` to evidence-only support until Ark resets structure | Footnote work keeps improving promotion candidates instead of accumulating on broken substrates |
| Memo 54 refactor baseline | Ark + Ezra | implemented | `memos/55_memo54_audit_and_structured_validation_followthrough.md` | none | Keep `ValidationResult` and `pipeline/common/pdf_source.py` as the shared baseline; do not reopen broad refactor work unless a structural reset exposes a real core defect | Source-proof and typed validation stay the default path |
| Human ratification Packet A | Ezra -> Human | active | `memos/51_historical_residual_ratification_packet_a.md` | awaiting human decision | Keep `JDG`, `1SA`, and `2SA` isolated from today’s release packet so Human is not overloaded | Human sees no more than 3 open ratification asks at once |
| Non-scripture contract review | Ark | queued | `memos/53_footnote_workflow_and_link_standards_ratification.md` | legacy `_notes.md` assumptions still exist in parser and discovery paths | Clear or phase legacy `_notes.md` assumptions after the structural reset lane is stable | Naming no longer carries hidden parser/discovery risk |

## Standards Track
- Link syntax frozen: `[[GEN.1:1]]`
- Backlink artifact contract reserved: `metadata/anchor_backlinks/GEN.1.1.json`
- Future non-canon frontmatter reuse: continue using plain anchor tokens in machine fields such as `canon_anchors_referenced`
- First linked-text prototype deferred until first-promotion discipline remains stable
- Generated dashboard remains book-state only; standards visibility lives on this ops board

## Cross-Agent Awareness
- The historical non-scripture substrate split is real: `*_articles.md` and `*_footnotes.md` now exist, but anchor linkage is still hot.
- Footnote mismatch work is adjacent to the release train, not a replacement for it.
- `pdftotext` is now the preferred tool for notes / footnotes extraction and a sanctioned verifier for scripture edge cases.
- `purity_audit.py` is now the default non-mutating entrypoint for chapter-open drop-cap and split-word sweeps; editorial findings still converge into `BOOK_editorial_candidates.json`.
- Memo 55 finished the Memo 54 refactor at the two weakest seams: duplicate PDF verifier logic and string-parsed validation truth.
- Ezra is now the strategic lead and may take one shared engineering lane when that is the highest-leverage unblocker.
- `RUT` is the cleanest same-day promote candidate.
- `DAN`, `EXO`, `1CH`, `2CH`, `2KI`, and `JOS` are now `promotion_ready` after queue reduction and dossier refresh.
- `1SA`, `JDG`, and `2SA` are editorially clear; they remain held only by governance / residual policy.
- `AMO` is now the only active chapter-open ambiguity lane from Ezra's review-reduction work, with `2` unresolved items remaining.
- `1ES` is not blocked on content quality; it is blocked on stale dossier alignment after Photius’s marker recovery.
- `JOS` and `1KI` are semantic structural holds even where the dashboard still reports structurally passable or editorially clean states.
- Minor Prophets promotion-ready pool: `AMO`, `MIC`, `OBA`, `JON`, `NAH`, `ZEP`, `HAG`, `ZEC`, `MAL`.
- Minor Prophets blocked pool: `JOL` and `HAB` remain `editorially_clean`; `HOS` remains `extracting` on `V8`.
- Any cleanup tool affecting 5+ books still requires Ark review before corpus-wide use.
- `_articles.md` / `_footnotes.md` naming is the working standard, but legacy `_notes.md` assumptions still exist in `pipeline/parse/osb_extract.py`, `pipeline/common/text.py`, `pipeline/tools/batch_validate.py`, and `pipeline/cleanup/refine_notes.py`.

## Blockers To Watch
- `JOS` and `1KI` are not safe to treat as normal promotion-ready or editorially clean books until structural reset work lands.
- `1ES` needs refreshed dossier state before it should be placed in a human-facing promotion packet.
- `JDG`, `1SA`, and `2SA` are governance-blocked on residual ratification, not on staged text quality alone.
- Ezra should not become a second default owner for routine staged cleanup or routine parser ownership.
- Footnote mismatch counts are not self-interpreting; they must be routed by root cause before they influence priorities.
- If footnote verification exposes scripture marker misses or verse-boundary defects, that routes to Ark parser work rather than silent cleanup expansion.
- Do not grow a third PDF verification path; future source-proof work must route through `pipeline/common/pdf_source.py`.
- Batch cleanup heuristics should not jump to corpus-wide use without Ark review.
- `***` markers are human reference only; they are ignored by machine detection and should not become workflow syntax.
- The ops board must be reconciled whenever a new memo changes dashboard truth; stale queue state is itself an operational bug.

## Release Train
- Same-day candidates: `RUT`
- Refresh-then-promote candidates: `1ES`
- Structural holds: `JOS`, `1KI`
- Historical ready queue behind today’s packet: `EXO`, `NUM`, `DEU`, `TOB`, `EZR`, `JDT`, `1CH`, `2CH`, `2KI`, `DAN`
- Corpus purity sweep priority set: `ZEC`, `DAN`, `AMO`, `MIC`, `JON` first; then `ISA`, `EZK`, `JER`, `JOB`, `ECC`; keep `JOS` evidence-only until structural reset lands
- Minor Prophets Packet A: `MIC`, `OBA`
- Minor Prophets near-ready with explicit blocker: `AMO` (`2` chapter-open ambiguities remaining)
- Minor Prophets Packet B: `JON`, `NAH`, `ZEP`
- Minor Prophets Packet C: `HAG`, `ZEC`, `MAL`
- Minor Prophets blocked queue: `JOL`, `HAB`, `HOS`

## Long-Horizon Queue
- Wisdom extraction lane: deferred until one structural reset and one promotion packet land
- Major Prophets extraction lane: deferred until the current release train is normalized
- NT planning lane: visible but deferred behind OT release-train stabilization
- Shared historical structural-reset utility: watch item only; promote to active work only if `JOS` and `1KI` prove the same reusable defect

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
