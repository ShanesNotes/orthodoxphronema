# Memo 62 — OT Purity Pass And Editorial Queue Integration

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `editorial queue / purity audit / dashboard reasoning`

## Context
- Manual review surfaced repeated truncated first sentences after `## Chapter` headings plus ongoing conjoined-word residue.
- A targeted OT scan confirmed the chapter-opening issue is systemic rather than anecdotal.
- The repo already had a durable editorial queue surface in `BOOK_editorial_candidates.json`; the missing piece was a non-mutating auditor that could feed that queue without creating a parallel system.

## Objective
- Add a safe purity auditor for chapter-opening drop-cap loss and split-word residue.
- Keep one editorial queue per book.
- Make dashboard reasoning name the purity categories instead of reporting only generic editorial blockage.

## Files / Artifacts
- [pipeline/cleanup/purity_audit.py](/home/ark/orthodoxphronema/pipeline/cleanup/purity_audit.py)
- [pipeline/tools/generate_book_status_dashboard.py](/home/ark/orthodoxphronema/pipeline/tools/generate_book_status_dashboard.py)
- [tests/test_purity_audit.py](/home/ark/orthodoxphronema/tests/test_purity_audit.py)
- [tests/test_book_status_dashboard.py](/home/ark/orthodoxphronema/tests/test_book_status_dashboard.py)

## Findings Or Changes
- Added [pipeline/cleanup/purity_audit.py](/home/ark/orthodoxphronema/pipeline/cleanup/purity_audit.py) as a non-mutating editorial scanner that can:
  - detect lowercase chapter-opening `:1` lines after `## Chapter`
  - classify them through the existing drop-cap residual model
  - detect live split-word residue using the same core patterns as `V11`
  - optionally merge existing fused-article candidates into the same report
- Kept `BOOK_editorial_candidates.json` as the single purity queue.
  - The new auditor emits or merges the same sidecar shape already used by dashboard and promotion tooling.
  - No parallel purity-tracker artifact was introduced.
- Explicitly ignored inline `***` markers during detection.
  - Human review graffiti does not become machine syntax.
  - The text around the marker is still scanned, so real defects remain visible.
- Tightened [generate_book_status_dashboard.py](/home/ark/orthodoxphronema/pipeline/tools/generate_book_status_dashboard.py) so status reasons now include top editorial categories such as `chapter_open_dropcap` and `split_word_residue`.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Add a dedicated purity auditor instead of overloading `fix_articles.py` | Chapter-open loss and split-word residue are broader than fused-article cleanup | Another tool increases surface area | Keep it report-only and reuse the same editorial sidecar/output contract |
| Reuse `BOOK_editorial_candidates.json` | Dashboard and promotion logic already understand this queue | Sidecar may accumulate mixed categories | Continue using explicit `category` fields and notes |
| Ignore `***` during machine detection | Human review marks are reference-only, not durable syntax | Inline markers can still linger in staged files | Keep them visible in human review and clear them before promotion |
| Surface editorial categories in dashboard reasons | Queue triage needs root-cause visibility, not just counts | Longer status messages | Limit to top categories only |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Purity audit tests | `pass` | `pytest tests/test_purity_audit.py -q` |
| Dashboard regression tests | `pass` | `pytest tests/test_book_status_dashboard.py -q` |
| Existing article-audit coverage still passes | `pass` | `pytest tests/test_fix_articles.py -q` |
| Modules compile | `pass` | `python3 -m py_compile pipeline/cleanup/purity_audit.py pipeline/tools/generate_book_status_dashboard.py` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `pipeline/cleanup/purity_audit.py`, `pipeline/tools/generate_book_status_dashboard.py`, `tests/test_purity_audit.py`, `tests/test_book_status_dashboard.py`, this memo |
| `Verification run` | `done` | `pytest tests/test_purity_audit.py tests/test_book_status_dashboard.py tests/test_fix_articles.py -q`; `python3 -m py_compile ...` |
| `Artifacts refreshed` | `deferred` | no per-book editorial sidecars or dashboard JSON were regenerated in this implementation pass |
| `Remaining known drift` | `present` | live books still need actual purity sweeps; dashboard code is updated but `reports/book_status_dashboard.json` has not been regenerated in this pass |
| `Next owner` | `photius` | run corpus sweep on structurally sound OT books with `purity_audit.py`, refresh editorial sidecars, and leave evidence-backed memos |

## Open Questions
- Whether `chapter_open_dropcap` should eventually become a dedicated validation key instead of only an editorial sidecar category should be judged after one full OT sweep.
- Whether `split_word_residue` should absorb additional conjoined-word families beyond current `V11` patterns remains a separate Ark-reviewed heuristic lane.

## Requested Next Action
- Photius should run [pipeline/cleanup/purity_audit.py](/home/ark/orthodoxphronema/pipeline/cleanup/purity_audit.py) across structurally sound OT books and merge findings into `BOOK_editorial_candidates.json`.
- Ezra should batch the resulting queue into:
  - promotion-ready purity packets
  - blocked but structurally sound packets
  - structural-hold evidence-only packets

## Handoff
**To:** `photius`  
**Ask:** `Use purity_audit.py as the default chapter-open and split-word sweep entrypoint, then refresh editorial sidecars and verification per book.`
