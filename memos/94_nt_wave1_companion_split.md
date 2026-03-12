# NT Wave 1 Companion Split — 2026-03-11

**Author:** `photius`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `NT Wave 1 / LUK, MAT, JOH, ACT, REV`
**Workstream:** `phase3-design`  
**Phase:** `1`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- The NT companion layer existed only as legacy `_notes.md` files.
- These files were tagged as `study_articles` and lacked systematic verse-keyed footnotes.
- Structural triage in Memo 93 identified these as high-density marker books requiring artifact separation.

## Objective
- Split `_notes.md` into `_articles.md` and `_footnotes.md` for Wave 1 books.
- Classify content conservatively.
- Provide a clean baseline for future footnote extraction.

## Files / Artifacts
- `staging/validated/NT/{LUK,MAT,JOH,ACT,REV}_articles.md`
- `staging/validated/NT/{LUK,MAT,JOH,ACT,REV}_footnotes.md`
- `reports/nt_wave1_split/{LUK,MAT,JOH,ACT,REV}.json`

## Findings Or Changes
- **Conservative Classification**: All sections in the legacy `_notes.md` files for Wave 1 were classified as `article`.
- **Zero Recovered Footnotes**: No verse-keyed, short-form footnotes were found in the source files.
- **Artifact Separation**: Successfully created separate article and placeholder footnote artifacts.
- **Unresolved Markers**: High marker density (191-314 per book) remains unresolved as source text for footnotes was absent from the legacy notes layer.

### Summary Table
| Book | Articles | Footnotes | Unresolved Markers | Result |
|---|---|---|---|---|
| **LUK** | 2 | 0 | 228 | `article_only` |
| **MAT** | 3 | 0 | 314 | `article_only` |
| **JOH** | 2 | 0 | 289 | `article_only` |
| **ACT** | 2 | 0 | 277 | `article_only` |
| **REV** | 2 | 0 | 191 | `article_only` |

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Classify as `article_only` | Legacy `_notes.md` files were explicitly extracted as study articles; no verse-keyed footnotes were present. | Footnote linkage remains 0% until next extraction. | Re-extract from PDF if required. |
| Create zero-entry footnote files | Complies with project artifact standards and provides an explicit "transition complete" signal. | None. | Delete files if unwanted. |

## Validation / Evidence
- `ls staging/validated/NT/*_articles.md` (Count: 5)
- `ls staging/validated/NT/*_footnotes.md` (Count: 5)
- `grep -c "^### " staging/validated/NT/*_articles.md` (Verified article counts)

## Completion Handshake
- `Files changed`: 10 MD files in `staging/validated/NT/`, 5 JSON files in `reports/nt_wave1_split/`.
- `Verification run`: Manual section audit and grep verification.
- `Artifacts refreshed`: Wave 1 split complete.
- `Remaining known drift`: 100% marker-to-footnote mismatch in Wave 1 (pending new extraction).
- `Next owner`: Ezra (Workflow Review / Prioritization)
