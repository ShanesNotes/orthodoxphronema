# NT Footnote Extraction Reset — 2026-03-11

**Author:** `ezra`  
**Type:** `workflow`  
**Status:** `implemented`  
**Scope:** `nt companion extraction / phase3 companion model`
**Workstream:** `phase3-design`  
**Phase:** `1`  
**Supersedes:** `94, 101` in part  
**Superseded by:** `none`

## Context
- Earlier companion triage established the normalization lane and confirmed that NT still sat on legacy `_notes.md`; the placeholder draft that held that slot has since been de-numbered during memo-governance reconciliation.
- Photius repaired the companion census and recovered the OT baseline companion truth in Memo 101.
- Photius then completed NT Wave 1 companion splitting for `LUK`, `MAT`, `JOH`, `ACT`, and `REV`; all five proved to be `article_only`.
- Human clarified the intended data model: the OSB footnote page ranges should be the primary source for NT footnote content, and marker hyperlinks can be reconciled later through the structured wikilink layer.

## Objective
- Reset the NT companion lane around the correct primary source of truth for footnotes.
- Accept Wave 1 article separation as valid transition work.
- Separate article splitting from real footnote extraction so marker mismatch no longer blocks the next step.

## Files / Artifacts
- `memos/_draft_companion_file_triage.md`
- `memos/94_nt_wave1_companion_split.md`
- `pipeline/EXTRACTION_POLICY.md`
- `schemas/anchor_registry.json`

## Findings Or Changes
- Wave 1 is accepted as a successful transition pass, not a failed extraction run.
  - `LUK`, `MAT`, `JOH`, `ACT`, and `REV` all produced valid `*_articles.md`.
  - Their zero-entry `*_footnotes.md` files are legitimate placeholders, because the legacy `_notes.md` content was article-only.
- The NT companion model is now split into two lanes:
  - `article separation` from legacy `_notes.md`
  - `real footnote extraction` from the OSB footnote page ranges
- Marker files remain useful, but their role changes:
  - primary use: later linkage/audit metadata
  - not primary anchor truth for NT footnote extraction
- The next real NT footnote milestone should be a source-footnote pilot on `ROM`.
  - `ROM` has page ranges in `anchor_registry.json`
  - `ROM` has enough marker density to make the pilot meaningful
  - `ROM` is a better extraction pilot than `EPH`, which is already an NT stabilization hotspot

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Treat footnote page-range verse labels as the primary NT footnote anchor source | Human clarified that the notes pages themselves carry the verse attachment labels | Some books may still have ambiguous page text and need manual verification | Fall back to book-by-book extraction memos if a pilot disproves the assumption |
| Keep `*_footnote_markers.json` as secondary linkage metadata | Marker files remain valuable for later scripture-to-footnote hyperlinking and coverage audits | Marker reconciliation may still expose corruption or drift later | Continue reporting marker mismatches without blocking extraction |
| Accept Wave 1 `article_only` outputs and do not reopen them | The legacy `_notes.md` files were proven to be article-only for those books | Placeholder `*_footnotes.md` files could be mistaken for final artifacts | Replace placeholders only when real source-derived footnotes are extracted |
| Authorize `pdftotext` for notes/footnotes page-range extraction | Existing tooling and Memo 53 already assume `pdftotext` is primary for notes/footnotes | Broadening `pdftotext` use carelessly would blur scripture vs notes policy | Restrict the authorization to notes/footnotes page ranges only |
| Use `ROM` as the first NT source-footnote extraction pilot | Manageable size, real marker density, and cleaner than current NT stabilization hotspots | Pilot may expose extraction issues that do not generalize | Re-rank pilot order after the `ROM` report if needed |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Wave 1 split created valid article artifacts | `pass` | `staging/validated/NT/{LUK,MAT,JOH,ACT,REV}_articles.md` |
| Wave 1 split created valid placeholder footnote artifacts | `pass` | `staging/validated/NT/{LUK,MAT,JOH,ACT,REV}_footnotes.md` |
| Wave 1 books remained article-only | `pass` | `reports/nt_wave1_split/{LUK,MAT,JOH,ACT,REV}.json` |
| NT pilot books have footnote page ranges in the registry | `pass` | `schemas/anchor_registry.json` |
| Existing extraction policy contradicted notes/footnotes practice | `warn` | `pipeline/EXTRACTION_POLICY.md` previously forbade `pdftotext` for footnotes/commentary |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `memos/95_nt_footnote_extraction_reset.md`, `pipeline/EXTRACTION_POLICY.md`, `memos/ezra_ops_board.md`, `PROJECT_BOARD.md`, `memos/INDEX.md` |
| `Verification run` | `done` | Read Wave 1 memo/reports, extraction policy, and registry page ranges |
| `Artifacts refreshed` | `done` | Ops board, project board, memo index, extraction policy memo chain |
| `Remaining known drift` | `present` | NT real footnote extraction has not started yet; Wave 2 article-bearing notes still remain unsplit |
| `Next owner` | `photius` | Run `ROM` source-footnote extraction pilot from the OSB footnote page range |

## Open Questions
- Whether the `ROM` pilot should emit marker-linkage metadata immediately or defer all hyperlinking to the later structured wikilink pass.
- Whether the `14` zero-content legacy NT `_notes.md` files should be normalized proactively or simply left untouched until full source extraction reaches them.

## Requested Next Action
- Photius: run a `ROM` source-footnote extraction pilot from the OSB footnote page range, using verse labels in the notes pages as the primary anchors.
- Ezra: review the `ROM` pilot and then route either a `LUK/MAT/JOH/ACT/REV` replacement wave or a tooling escalation.
- Ark: stay on NT scripture stabilization unless the `ROM` pilot exposes a real parser/schema issue.

## Handoff
**To:** `photius`  
**Ask:** `Extract real NT footnotes for ROM from the OSB footnote page range, anchor them from the printed verse labels in that section, and report marker coverage separately as secondary metadata.`

## Notes
- This memo changes workflow and source interpretation for NT companion extraction only; it does not reopen canon extraction policy broadly.
- Marker corruption in OT books like `PSA` and `SIR` remains a separate linkage problem and should not block NT source-footnote extraction.
