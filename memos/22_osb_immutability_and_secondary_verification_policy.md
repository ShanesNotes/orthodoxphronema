# OSB Immutability And Secondary Verification Policy — 2026-03-08

**Author:** `ezra`
**Type:** `decision`
**Status:** `in_review`
**Scope:** `GEN / source authority / verification workflow`

## Context
- Memo 21 introduced a Brenton-derived insertion for `GEN.25:34` into the staged Genesis artifact.
- Human added a second OSB source at `src.texts/The-Orthodox-Study-Bible-Verification.pdf` and manually verified that `GEN.25:34` is absent there as well as in `src.texts/the_orthodox_study_bible.pdf`.
- Human explicitly set the project direction: keep the canon artifacts OSB-faithful and immutable.

## Objective
- Remove the non-OSB insertion from `staging/validated/OT/GEN.md`.
- Reclassify `GEN.25:34` as a source-witness omission, not a parser recovery.
- Incorporate the second OSB file in a way that improves verification speed without creating a second parsing pipeline.

## Files / Artifacts
- `staging/validated/OT/GEN.md`
- `staging/validated/OT/GEN_residuals.json`
- `reports/GEN_promotion_dossier.json`
- `memos/19_day10_status_and_todos.md`
- `memos/21_greek_witness_layer_pilot.md`
- `src.texts/the_orthodox_study_bible.pdf`
- `src.texts/The-Orthodox-Study-Bible-Verification.pdf`

## Findings Or Changes
- `GEN.25:34` should not be treated as a `docling_issue` or an OSB-recoverable verse boundary miss.
- The correct interpretation is: the verse is absent in both available OSB witnesses and present only in auxiliary upstream witnesses (Rahlfs LXX / Brenton).
- Therefore the Brenton insertion at `staging/validated/OT/GEN.md` must be removed if the project is to remain OSB-faithful.
- The secondary OSB scan is useful as a manual adjudication source, but not as a direct extraction source.
- `pdftotext` returns effectively blank output from the new verification PDF frontmatter, so the scan does not currently offer a usable text layer for normal automation.
- Because of that, a full-OCR approach is not the right next step. A lightweight navigation aid is the efficient path.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Remove the Brenton insertion for `GEN.25:34` from `staging/validated/OT/GEN.md` | Preserves immutable OSB policy and keeps canon artifacts source-faithful | `GEN` completeness returns to an accepted warning state instead of a patched near-complete state | Restore the line from git if policy changes later |
| Reclassify `GEN.25:34` to `osb_dual_witness_absent` or similar | Distinguishes source omission from parser failure | Requires a small validation/promotion vocabulary update if the class is new | Map back to `osb_pdf_absent` if no new class is added |
| Keep both OSB files above all auxiliary witnesses | Aligns with repo source authority and human directive | Ambiguous omissions remain unresolved in a few cases | Fall back to explicit human exception memos if needed |
| Use Greek/Brenton only as explanatory witnesses after OSB review is exhausted | Keeps upstream witnesses informative but non-authoritative | Slower than auto-filling missing verses | Human can explicitly approve a future exception policy if desired |
| Build a lightweight scan-navigation artifact instead of OCRing the whole scan | Improves LLM/manual verification speed with low implementation cost | Manual index may start coarse | Replace later with bookmark extraction or TOC-only OCR |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Electronic OSB witness omission | confirmed | `src.texts/the_orthodox_study_bible.pdf` prior GEN 25 review |
| Scanned OSB witness omission | confirmed by human manual review | `src.texts/The-Orthodox-Study-Bible-Verification.pdf` |
| New scan has no practical text layer for normal navigation | pass | `pdftotext -f 1 -l 25 src.texts/The-Orthodox-Study-Bible-Verification.pdf -` returned blank pages |
| Current staged artifact contains non-OSB insertion | pass | `staging/validated/OT/GEN.md` currently includes `GEN.25:34` |

## Open Questions
- Should `osb_dual_witness_absent` be a new formal residual classification, or should this remain a documented subtype of `osb_pdf_absent`?
- Should promotion require per-entry ratification for any non-OSB remediation or source-absence exception, even when the sidecar has a top-level `ratified_date`?
- Does Human want the scan-navigation artifact committed as a stable reference file, or generated locally on demand?

## Requested Next Action
- Ark: remove `GEN.25:34` from `staging/validated/OT/GEN.md`.
- Ark: update `staging/validated/OT/GEN_residuals.json` so `GEN.25:34` is classified as a dual-OSB-source absence, with no inserted substitute text in the canon artifact.
- Ark: regenerate `reports/GEN_promotion_dossier.json` after the revert and update memo 19 / memo 21 so they no longer describe the insertion as the preferred state.
- Ark: add a small non-canon navigation artifact for the scanned OSB.
- Preferred paths:
- `metadata/source_navigation/osb_scan_book_pages.json`
- `staging/reference/osb_scan_navigation.json`
- Minimum shape:
- `{ "GEN": { "start_page": <int>, "end_page": <int>, "notes": "manual or TOC-derived" } }`
- Build order:
- `1.` extract PDF bookmarks/outlines if present
- `2.` if no outlines exist, OCR only the table-of-contents pages or hand-seed a compact book/page map
- `3.` do not OCR the whole scanned PDF unless later required

## Handoff
**To:** `ark`
**Ask:** Restore GEN to immutable-OSB state, convert `GEN.25:34` into a source-absence residual instead of a text insertion, and add a lightweight navigation aid for the scanned OSB so future LLM verification is faster.

## Notes
- Source roles moving forward:
- `the_orthodox_study_bible.pdf` = canonical extraction source
- `The-Orthodox-Study-Bible-Verification.pdf` = secondary OSB verification witness
- `Rahlfs / Antoniades / Brenton` = auxiliary upstream witnesses only
- Recommended future verification ladder:
- `1.` validate against primary OSB PDF
- `2.` if disputed, verify against scanned OSB
- `3.` if both OSB witnesses omit the verse, classify it as source-absence
- `4.` only then consult Greek / Brenton to explain the omission, not to rewrite canon
