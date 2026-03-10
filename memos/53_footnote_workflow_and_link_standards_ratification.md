# Memo 53 — Footnote Workflow And Link Standards Ratification

**Author:** `ezra`  
**Type:** `workflow`  
**Status:** `implemented`  
**Scope:** `footnote workflow / non-scripture companions / link standards`

## Context
- Memo 49 proposed separating study articles from verse-linked footnotes and using `pdftotext` for the OSB notes section.
- Memo 50 reports that Photius completed that substrate split across the historical books and surfaced new mismatch classes that affect staged recovery and parser triage.
- Memo 17 previously recommended freezing anchor-link and backlink standards before Phase 2 work expands.
- Human requested that Photius's lessons learned become durable workflow improvements and that long-horizon visibility move onto the live board.

## Objective
- Ratify the working footnote and non-scripture conventions already emerging in staging.
- Freeze the minimal cross-text link standard now without pulling Phase 2 backlink implementation forward.
- Keep the generated dashboard focused on book-state while surfacing standards work and footnote risk on the Ezra ops board.

## Files / Artifacts
- `AGENTS.md`
- `memos/49_footnote_extraction_and_notes_restructuring.md`
- `memos/50_photius_nonscripture_extraction_audit.md`
- `memos/ezra_ops_board.md`

## Findings Or Changes
- The staged non-scripture contract is now explicit:
  - `BOOK_articles.md` for study articles / commentary blocks
  - `BOOK_footnotes.md` for verse-linked OSB notes
  - `BOOK_footnote_markers.json` for scripture-side marker trace
- `BOOK_notes.md` is now treated as a legacy / transitional name, not the preferred steady-state artifact.
- Extractor selection is now fixed by content type:
  - scripture pages: `Docling` primary
  - scripture edge cases: `pdftotext` targeted verifier / fallback
  - notes and footnotes pages: `pdftotext` primary
- Footnote mismatch reports are now recognized as first-class triage signals rather than “nice to have” cleanup:
  - parser false positives
  - missing inline markers
  - versification drift
- Cross-text link syntax is frozen for authored Markdown as `[[GEN.1:1]]`.
- Future backlink artifact naming is reserved as `metadata/anchor_backlinks/GEN.1.1.json`, but generator/schema work remains deferred until the first linked-text phase is intentionally opened.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Ratify `_articles.md` and `_footnotes.md` as the standard non-scripture companions | Matches the schema, the current staged artifacts, and downstream separation-of-concerns needs | Legacy references to `_notes.md` may linger in docs or tools | Keep aliases temporarily while Ark reviews pipeline implications |
| Use `pdftotext` as the primary extractor for notes / footnotes | Photius's run demonstrated cleaner, more deterministic note extraction than Docling for the OSB notes section | Overconfidence if applied blindly to scripture pages | Restrict `pdftotext` to notes/footnotes primary use and scripture edge-case verification |
| Treat footnote mismatch reports as routing signals, not just cleanup noise | They expose parser false positives, missed markers, and versification drift early | The team could overfocus on linkage and neglect release-train priorities | Keep mismatch triage on the ops board adjacent to, not replacing, promotion work |
| Freeze authored link syntax now as `[[GEN.1:1]]` | Avoids later retrofit across notes, articles, patristics, and exports | A future tool may prefer a different display syntax | Keep machine fields on plain anchor tokens and transform at export if needed |
| Reserve backlink artifact naming but defer implementation | Preserves Phase 2 options without starting product work too early | Deferred work may look incomplete | Keep the contract visible on the ops board until Phase 2 opens |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Notes frontmatter already supports separated article / footnote content types | `pass` | `schemas/notes_frontmatter.json` enum includes `article` and `footnotes` |
| Historical staging already contains the split non-scripture artifacts | `pass` | `staging/validated/OT/GEN_articles.md`, `staging/validated/OT/GEN_footnotes.md`, parallel files across historical books |
| Footnote extraction and verification tools already exist | `pass` | `pipeline/cleanup/extract_footnotes.py`, `pipeline/cleanup/refine_notes.py`, `pipeline/cleanup/verify_footnotes.py` |
| Long-horizon standards work was previously identified as safe to pull forward | `pass` | `memos/17_repo_maximization_triage.md` |
| Legacy `_notes.md` assumptions still exist and need Ark review | `warn` | `pipeline/parse/osb_extract.py`, `pipeline/common/text.py`, `pipeline/tools/batch_validate.py`, `pipeline/cleanup/refine_notes.py` |

## Open Questions
- Ark should decide whether to update the remaining `_notes.md` assumptions in one bounded contract pass or support a temporary alias period.
- Ezra should decide whether the first mismatch-audit packet should prioritize the highest-volume books (`1KI`, `3MA`) or release-train-adjacent books first.

## Requested Next Action
- Ark: review and clear the remaining `_notes.md` assumptions in parser, common text discovery, and batch validation paths before promotion logic relies on the new names.
- Photius: continue footnote alignment, marker recovery, and evidence-packaged staged fixes within the ratified workflow.
- Ezra: triage mismatch reports into staged cleanup, parser follow-up, or known-source drift and keep the live queue current.
- Human: reserve product and backlink build-out until the first linked-text prototype is intentionally scheduled.

## Handoff
**To:** `ark`  
**Ask:** `Review the remaining _notes.md assumptions in pipeline/parse/osb_extract.py, pipeline/common/text.py, pipeline/tools/batch_validate.py, and pipeline/cleanup/refine_notes.py, then decide whether to clear them in one bounded contract pass or keep a temporary alias period.`

## Notes
- This memo changes workflow and standards only; it does not expand backlink implementation, schema surfaces, or generated dashboard semantics.
- The live coordination surface for the new long-horizon and footnote lanes remains `memos/ezra_ops_board.md`.
