# Memo 61 — Poetry Extractor Support For Photius

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `poetry / wisdom extraction helper seam`

## Context
- Photius’s [Psalms custom extraction memo](/home/ark/orthodoxphronema/memos/59_psa_custom_extraction.md) introduced a useful `pdftotext`-driven state-machine method for poetry-heavy books.
- That method is directionally right for edge-case poetry extraction, but the initial script was still too Psalm-specific to reuse safely for `JOB`, `PRO`, or `SIR`.
- Human asked that Codex help Photius’s coding ability without blocking the innovation.

## Objective
- Preserve the direct `pdftotext` sequential-extraction method.
- Extract the reusable seams so Photius can apply the approach to other poetry / wisdom books without cloning the whole script.
- Avoid reopening Ark’s larger parser architecture lane.

## Files / Artifacts
- [pipeline/common/poetry.py](/home/ark/orthodoxphronema/pipeline/common/poetry.py)
- [pipeline/parse/psa_extract.py](/home/ark/orthodoxphronema/pipeline/parse/psa_extract.py)
- [tests/test_poetry_extraction.py](/home/ark/orthodoxphronema/tests/test_poetry_extraction.py)

## Findings Or Changes
- Added a shared poetry helper in [pipeline/common/poetry.py](/home/ark/orthodoxphronema/pipeline/common/poetry.py) for:
  - chapter-header detection
  - bootstrap phrase detection
  - verse-number parsing
  - cleaned line normalization for common `pdftotext` kerning artifacts
  - the sequential verse-buffer state machine itself
- Refactored [pipeline/parse/psa_extract.py](/home/ark/orthodoxphronema/pipeline/parse/psa_extract.py) to use that shared helper while preserving the Psalms defaults:
  - `Psalm` header prefix
  - `Blessed is the man` bootstrap phrase
  - same raw-output model
- Removed the last Psalm-only architecture seam from the CLI defaults:
  - `--page-start` and `--page-end` now resolve from `schemas/anchor_registry.json` when omitted
  - explicit page arguments still override the registry
  - this makes the extractor reusable for `JOB`, `PRO`, and `SIR` without hardcoded PDF spans in the script
- Removed another Psalm-only metadata seam from frontmatter emission:
  - `book_name`, `testament`, and `canon_position` now default from registry book metadata
  - explicit `--book-name` still overrides the registry when needed
  - reuse on `JOB` or `PRO` no longer emits `Psalms`-biased frontmatter
- Made the Psalm extractor configurable instead of hardcoded:
  - `--book-code`
  - `--book-name`
  - `--page-start`
  - `--page-end`
  - repeatable `--header-prefix`
  - repeatable `--header-regex`
  - repeatable `--bootstrap-phrase`
  - optional `--layout`
  - optional `--out-path`
- Fixed one real state-machine bug discovered during testing:
  - after a chapter header, a literal `1 ...` line now correctly becomes verse 1 text instead of being appended as raw numbered text
- Tightened the shared poetry normalizer with a few bounded capitalized function-word repairs:
  - `B ut` -> `But`
  - `T he` -> `The`
  - `A nd` -> `And`
  - `F or` -> `For`
  - `N or` -> `Nor`

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Keep the `pdftotext` poetry method | It is the actual innovation that solved Psalms-style chapter collapse | Could tempt overuse where Brenton-restructure still works better | Keep it as a specialized helper lane, not a universal parser replacement |
| Generalize helper seams, not the whole wisdom pipeline | Reuse is real, but a full Poetry Engine rewrite would be premature | Photius may still need book-specific tuning | Allow thin book-specific wrappers over the shared helper |
| Use registry page ranges as the extractor default | Book-level PDF spans already live in repo truth and should not be re-hardcoded per script | A bad registry range would mislead the extractor | Pass explicit `--page-start/--page-end` while debugging and fix the registry if needed |
| Use registry book metadata as frontmatter defaults | Registry already owns canonical book identity metadata | A bad registry row would propagate into raw output | Override via CLI while debugging and correct the registry if needed |
| Do not create another kerning dictionary in a new script | The repo already had too much duplication here | Shared defaults may still be incomplete | Extend the shared helper rather than cloning local lists |
| Leave Brenton-matching restructurers intact | `JOB`, `PRO`, and `SIR` already recovered via a different proven route | Two methods now coexist | Use the right tool per book and compare outcomes empirically |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Shared poetry helper tests | `pass` | `pytest tests/test_poetry_extraction.py -q` |
| Existing focused regression tests still pass | `pass` | `pytest tests/test_verify_footnotes.py tests/test_book_status_dashboard.py -q` |
| New extractor module imports compile | `pass` | `python3 -m py_compile pipeline/common/poetry.py pipeline/parse/psa_extract.py` |
| Configurable CLI is exposed | `pass` | `python3 pipeline/parse/psa_extract.py --help` |
| Registry-backed page-range defaults are covered | `pass` | `pytest tests/test_poetry_extraction.py -q` |
| Registry-backed frontmatter defaults are covered | `pass` | `pytest tests/test_poetry_extraction.py -q` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `pipeline/common/poetry.py`, `pipeline/common/__init__.py`, `pipeline/parse/psa_extract.py`, `tests/test_poetry_extraction.py`, this memo |
| `Verification run` | `done` | `pytest tests/test_poetry_extraction.py tests/test_verify_footnotes.py tests/test_book_status_dashboard.py -q`; `python3 -m py_compile ...` |
| `Artifacts refreshed` | `deferred` | no dossier or dashboard refresh needed; this was code-only support work |
| `Remaining known drift` | `none` | no stale dossier or stale dashboard introduced by this pass |
| `Next owner` | `photius` | try the shared extractor seam on one additional poetry book before growing another specialist script |

## Open Questions
- Whether `JOB` is better served by a thin wrapper over the new shared poetry helper or by keeping Brenton-driven restructuring as the primary path should be judged from one bounded experiment.
- Whether the shared kerning rules should later absorb the larger `restructure_wis.py` list remains open; that is a separate cleanup lane.

## Requested Next Action
- Photius should treat [pipeline/parse/psa_extract.py](/home/ark/orthodoxphronema/pipeline/parse/psa_extract.py) as a configurable poetry extractor with registry-backed defaults, not as a one-book dead end.
- Ark should only escalate this into broader parser architecture if repeated poetry books prove the same `pdftotext` seam belongs in core workflow.

## Handoff
**To:** `photius`  
**Ask:** `Reuse the shared poetry helper and configurable psa_extract CLI for the next poetry experiment instead of cloning another specialist script.`
