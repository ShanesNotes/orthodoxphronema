# OT Canon Lock Ratification Packet — 2026-03-11

**Author:** `ezra`  
**Type:** `decision`  
**Status:** `ratified`  
**Scope:** `ot canon lock`
**Workstream:** `canon-hygiene`  
**Phase:** `2`  
**Supersedes:** `89`  
**Superseded by:** `none`

## Context
- OT canon now validates with `0` structural errors in `reports/canon_ot_structural_audit.json`.
- `18` OT canon books still carry warnings.
- `17` of those books are `V7`-only versification drift cases.
- `EST` is the only remaining non-`V7` OT canon blocker.

## Objective
- Present one bounded Human ratification packet for the `17` `V7`-only OT canon books.
- Present one bounded disposition recommendation for `EST.4:6`.
- Reduce OT canon lock to a short decision surface instead of an open investigation.

## Files / Artifacts
- `reports/canon_ot_structural_audit.json`
- `reports/EST_promotion_dossier.json`
- `staging/validated/OT/*_residuals.json`
- `schemas/anchor_registry.json`
- `memos/82_job_retriage_recovery_pass_and_est_disposition.md`
- `memos/89_ot_canon_lock_checkpoint.md`

## Human Decision Packet

### Ask 1
Ratify these `17` books as `V7`-acceptable, meaning the versification difference is a known property of the OSB text tradition and not a pipeline defect.

| Book | Issue | Recommendation | Evidence |
|---|---|---|---|
| `GEN` | `GEN.25:34` absent; ch.25 has `33/34` verses | Ratify as genuine versification difference | Residual sidecar already classifies `GEN.25:34` as `osb_source_absent`; canon audit is `V7`-only |
| `EXO` | chapter-end redistribution: ch.32 carries extra `35`, ch.35 carries extra `33-35`, ch.36 carries extra `39` | Ratify as genuine versification difference | Clean chapter-boundary redistribution with `V1/V2/V3/V4/V8/V9` all passing; no live structural defect remains |
| `NUM` | chapter-boundary redistribution: ch.16 missing `36-50`, ch.17 carries extra `14-28`; also `NUM.6:27` and `NUM.29:40` absent with matching next-chapter extras | Ratify as genuine versification difference | Clean renumbering pattern across adjacent chapters, not random extraction loss; canon audit is `V7`-only |
| `DEU` | chapter-end redistribution across ch.12/13, 22/23, 28/29, 29/30, 33; missing final verses appear as next-chapter extras | Ratify as genuine versification difference | Repeated chapter-boundary renumbering pattern with all structural checks passing |
| `JDG` | `JDG.11:40` absent; ch.11 has `39/40` verses | Ratify as genuine versification difference | Residual sidecar already says `osb_source_absent`; note says OSB/LXX ends at `39` and content is covered in v39 |
| `2KI` | chapter-boundary redistribution: ch.1 carries extra `19-22`, ch.11 missing `21`, ch.12 carries extra `22` | Ratify as genuine versification difference | Clean adjacent-chapter renumbering pattern, no `V4`/`V9` defect |
| `1CH` | redistributed counts in ch.1/5/6 plus single end-verse shifts in ch.10, ch.12, ch.16, ch.29 | Ratify as genuine versification difference | All chapter counts and verse order pass; mismatch is concentrated in chapter-boundary/end-verse numbering |
| `2CH` | redistributed counts in ch.1/2, ch.13/14, ch.27, and large chapter-boundary carry in ch.35/36 | Ratify as genuine versification difference | Clean numbering drift with `V1/V2/V3/V4/V8/V9` all passing |
| `EZR` | `EZR.7:29` present beyond registry count | Ratify as genuine versification difference | Registry already carries EZR-specific `cvc_overrides`; canon audit is `V7`-only |
| `JOB` | end-verse redistribution across ch.5, 12, 13, 16, 21, 30, 33, 34, 35, 36 | Ratify as genuine versification difference | Canon is structurally clean and `V7`-only; direct `pdftotext` probe for `JOB.36:33` confirms the source numbering in the OSB text layer, so the tail reads as registry mismatch rather than live extraction loss |
| `EZK` | ch.1 has extra `28`; ch.11 extra `24-25`; ch.32 extra `32`; ch.33 missing `32` | Ratify as genuine versification difference | Residual sidecar already records multiple `osb_source_absent` verse decisions; current canon warning is now `V7`-only |
| `TOB` | chapter-end redistribution across ch.5/6/7/10 | Ratify as genuine versification difference | Clean adjacent-chapter numbering drift with all structural checks passing |
| `JDT` | `JDT.15:14` present beyond registry count | Ratify as genuine versification difference | Single end-verse overrun with no other structural failures |
| `SIR` | multiple chapter-end extras and one shortfall at `SIR.48:20-25`; current overage is `+6` verses | Ratify as genuine versification difference | Canon is structurally clean and `V7`-only; direct `pdftotext` on the Sirach source span shows `SIR.48:23-25` flowing into chapter `49` in the OSB text layer, supporting source versification drift rather than a live parser defect |
| `BAR` | `BAR.3:38` present beyond registry count | Ratify as genuine versification difference | Single end-verse overrun with all structural checks passing |
| `1MA` | `1MA.8:32` absent; ch.8 has `31/32` verses | Ratify as genuine versification difference | Residual sidecar already classifies `1MA.8:32` as `osb_source_absent`; canon audit is `V7`-only |
| `3MA` | `3MA.1:29` absent; ch.1 has `28/29` verses | Ratify as genuine versification difference | Residual sidecar already classifies `3MA.1:29` as `osb_source_absent`; canon audit is `V7`-only |

### Ask 2
Decide `EST` as `ratify-as-is with explicit gap documentation`, not `repair`.

| Book | Issue | Recommendation | Evidence |
|---|---|---|---|
| `EST` | `EST.4:6` missing between `EST.4:5` and `EST.4:7`; canon audit shows `V4`, `V7`, and weak `V10` absorption hint | Ratify as source-absent and keep the documented gap | `EST_promotion_dossier.json` shows only the `4:6` gap; direct `pdftotext` on pages `1419-1427` shows the OSB source flowing from `EST.4:5` directly to `EST.4:7`; `pdf_edge_case_check.py` also does not find `EST.4:6`; `EST_residuals.json` already classifies it as `osb_source_absent`; the current `pdf_verify.py` “match” is a false positive from an unrelated Esther 6 snippet, not a real recovery of `EST.4:6` |

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Package the `17` `V7` books together | Human should be able to ratify the OT drift set in under 5 minutes | Some books have stronger evidence than others | Split into smaller packets later if Human rejects the bundle |
| Recommend `EST` ratify-as-is | Current repo evidence supports source-absence more strongly than recovery | A later image-backed review could still surface a missing verse marker | Re-open `EST` if stronger source evidence appears |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| OT canon warning set | `pass` | `reports/canon_ot_structural_audit.json` |
| `EST` live warning state | `pass` | `reports/EST_promotion_dossier.json` |
| `EST` edge-case probe | `warn` | `python3 pipeline/validate/pdf_edge_case_check.py canon/OT/EST.md` |
| `EST` residual classification | `pass` | `staging/validated/OT/EST_residuals.json` |
| V7 drift details | `pass` | `schemas/anchor_registry.json` vs `canon/OT/*.md` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `memos/91_ot_canon_lock_ratification_packet.md`, `memos/ezra_ops_board.md` |
| `Verification run` | `done` | Canon structural audit, EST dossier review, EST edge-case check, direct `pdftotext` probes for `EST`, `JOB`, and `SIR`, registry/canon drift comparison |
| `Artifacts refreshed` | `partial` | Ops board refreshed; no dossier/dashboard regeneration needed for a decision packet |
| `Remaining known drift` | `present` | Human decision still required for the `V7` packet and `EST` disposition |
| `Next owner` | `human` | Ratify or reject the packet |

## Requested Next Action
- Human decides:
  1. ratify the `17` `V7`-only books as OT-lock acceptable
  2. ratify `EST.4:6` as source-absent, or reject that recommendation and require one more bounded source review

## Handoff
**To:** `human`  
**Ask:** `Approve or reject the V7 ratification bundle and the EST ratify-as-is recommendation so OT canon can be formally locked.`
