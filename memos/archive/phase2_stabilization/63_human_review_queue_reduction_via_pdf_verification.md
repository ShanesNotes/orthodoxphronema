# Memo 63 — Human Review Queue Reduction Via PDF Verification

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `drop-cap review queue / staged scripture / dossier refresh`

## Context
- Human asked Ezra to target issues still requiring human review and collapse them where `pdftotext` or other repo-native evidence could settle them.
- The tractable queue was the live `ambiguous_human` drop-cap sidecars, not the entire editorial backlog.
- `EXO`, `AMO`, and `DAN` were high-leverage because they had either stale human-review debt or clearly source-verifiable chapter-opening losses.

## Objective
- Reduce the live human-review queue by resolving chapter-opening drop-cap cases with direct OSB PDF evidence.
- Refresh sidecars and dossiers so the reduced queue is visible in repo state.
- Leave only genuinely ambiguous items for Human.

## Files / Artifacts
- [staging/validated/OT/AMO.md](/home/ark/orthodoxphronema/staging/validated/OT/AMO.md)
- [staging/validated/OT/DAN.md](/home/ark/orthodoxphronema/staging/validated/OT/DAN.md)
- [staging/validated/OT/EXO_dropcap_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/EXO_dropcap_candidates.json)
- [staging/validated/OT/AMO_dropcap_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/AMO_dropcap_candidates.json)
- [staging/validated/OT/DAN_dropcap_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/DAN_dropcap_candidates.json)
- [staging/validated/OT/AMO_editorial_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/AMO_editorial_candidates.json)
- [staging/validated/OT/DAN_editorial_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/DAN_editorial_candidates.json)
- [reports/AMO_promotion_dossier.json](/home/ark/orthodoxphronema/reports/AMO_promotion_dossier.json)
- [reports/DAN_promotion_dossier.json](/home/ark/orthodoxphronema/reports/DAN_promotion_dossier.json)
- [reports/EXO_promotion_dossier.json](/home/ark/orthodoxphronema/reports/EXO_promotion_dossier.json)
- [reports/book_status_dashboard.json](/home/ark/orthodoxphronema/reports/book_status_dashboard.json)

## Findings Or Changes
- Resolved stale Exodus human-review debt.
  - [EXO_dropcap_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/EXO_dropcap_candidates.json) is now `0` candidates.
  - The staged file was already repaired; the sidecar was simply stale.
- Resolved all live Daniel drop-cap review items.
  - Repaired the chapter-open losses in [DAN.md](/home/ark/orthodoxphronema/staging/validated/OT/DAN.md) for `DAN.2:1`, `DAN.3:1`, `DAN.4:1`, `DAN.5:1`, `DAN.6:1`, `DAN.7:1`, `DAN.8:1`, `DAN.9:1`, `DAN.10:1`, and `DAN.13:1`.
  - Refreshed [DAN_dropcap_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/DAN_dropcap_candidates.json) to `0`.
  - Refreshed [DAN_editorial_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/DAN_editorial_candidates.json) to `0`.
  - Refreshed the dossier and dashboard state; `DAN` now shows `promotion_ready`.
- Reduced Amos from nine chapter-open drop-cap suspects to two true unresolved cases.
  - Repaired [AMO.md](/home/ark/orthodoxphronema/staging/validated/OT/AMO.md) at `AMO.1:1`, `AMO.2:1`, `AMO.4:1`, `AMO.6:1`, `AMO.7:1`, `AMO.8:1`, and `AMO.9:1`.
  - Refreshed [AMO_dropcap_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/AMO_dropcap_candidates.json) from `9` candidates (`7 ambiguous`) down to `2` ambiguous.
  - Refreshed [AMO_editorial_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/AMO_editorial_candidates.json) down to `2` `chapter_open_dropcap` items.
  - Refreshed the dossier and dashboard state; `AMO` remains `structurally_passable` with exactly two editorial blockers.
- Fixed the purity sidecar write-path so resolved categories can actually clear.
  - [purity_audit.py](/home/ark/orthodoxphronema/pipeline/cleanup/purity_audit.py) now replaces its owned categories (`chapter_open_dropcap`, `split_word_residue`, `fused_article_explicit`) before merging refreshed output.
  - Without this, editorial sidecars only grew and could not shrink when staged text improved.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Fix staged scripture where OSB `pdftotext` evidence was direct | Removes real Human review debt instead of only reclassifying it | Incorrect inference would contaminate staged text | Re-run PDF probe and revert only the affected verse lines |
| Leave `AMO.3:1` and `AMO.5:1` unresolved | The PDF snippets remain formatting-ambiguous at the exact opening token | Human queue is not fully eliminated for Amos | Keep them in `chapter_open_dropcap` until image/PDF review settles them |
| Refresh dossiers after staged repairs | Prevent stale-checksum drift from hiding the actual status change | Dry-run dossier generation can still leave non-editorial blockers visible | Re-run `promote.py --dry-run --allow-incomplete` after any further edits |
| Fix purity sidecar merge semantics now | A queue that cannot shrink is operationally broken | Could drop categories if replacement ownership is wrong | Limit replacement to purity-audit-owned categories only |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Amos validation | `pass` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/AMO.md` |
| Daniel validation | `pass` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/DAN.md` |
| Amos dossier refresh | `pass` | `python3 pipeline/promote/promote.py --book AMO --dry-run --allow-incomplete` |
| Daniel dossier refresh | `pass` | `python3 pipeline/promote/promote.py --book DAN --dry-run --allow-incomplete` |
| Exodus dossier refresh | `pass` | `python3 pipeline/promote/promote.py --book EXO --dry-run --allow-incomplete` |
| Dashboard refresh | `pass` | `python3 pipeline/tools/generate_book_status_dashboard.py` |
| Purity-audit regression tests | `pass` | `pytest tests/test_purity_audit.py tests/test_fix_articles.py -q` |
| Purity-audit compile | `pass` | `python3 -m py_compile pipeline/cleanup/purity_audit.py` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | staged `AMO.md` / `DAN.md`, refreshed `EXO` / `AMO` / `DAN` sidecars, refreshed dossiers, refreshed dashboard, `purity_audit.py`, tests, this memo |
| `Verification run` | `done` | `validate_canon.py` on `AMO` and `DAN`; `promote.py --dry-run --allow-incomplete` on `AMO`, `DAN`, `EXO`; `generate_book_status_dashboard.py`; `pytest tests/test_purity_audit.py tests/test_fix_articles.py -q` |
| `Artifacts refreshed` | `done` | `EXO_dropcap_candidates.json`, `AMO_dropcap_candidates.json`, `DAN_dropcap_candidates.json`, `AMO_editorial_candidates.json`, `DAN_editorial_candidates.json`, `AMO_promotion_dossier.json`, `DAN_promotion_dossier.json`, `EXO_promotion_dossier.json`, `book_status_dashboard.json` |
| `Remaining known drift` | `present` | `AMO.3:1` and `AMO.5:1` remain ambiguous; broader historical drop-cap queues still exist in `2CH`, `1SA`, `1CH`, `2KI`, `JOS`, `2SA`, `1MA`, `TOB`, `2MA`, `JDG`, `EZR`, `1ES`, `RUT`, `1KI` |
| `Next owner` | `human` | review the two remaining Amos openings if you want to keep collapsing the ambiguous queue manually; otherwise route the next batch to Ark/Photius using the refreshed counts |

## Open Questions
- `AMO.3:1` and `AMO.5:1` both present as `house of Israel...` after the chapter heading, but the exact missing opening token remains formatting-ambiguous in the current `pdftotext` extraction.
- If we want the next queue-reduction batch automated, the best next targets are the books with the largest remaining `ambiguous_human` drop-cap counts: `2CH`, `1SA`, `1CH`, and `2KI`.

## Requested Next Action
- Human can now ignore `EXO` and `DAN` for chapter-open drop-cap review.
- If you want another Ezra pass, the next best lane is a `2CH` / `1SA` targeted PDF-review batch rather than a broad corpus sweep.

## Handoff
**To:** `ark`  
**Ask:** `Treat the remaining Amos ambiguity and the next highest-count drop-cap books as the true human-review queue; the stale Exodus and Daniel review debt is already cleared.`
