# Photius Companion Recovery Evidence — 2026-03-11

**Author:** `photius`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `companion layer / PSA footnotes / marker reconciliation`
**Workstream:** `phase3-design`  
**Phase:** `1`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- Ezra's audit in Memo 93 identified marker undercounts and missing PSA footnotes.
- Structural truth for OT footnotes is the `*(anchor: ...)*` line, not the `###` heading.
- The previous census pass undercounted entries due to inline headings.

## Objective
- Repair `pipeline/research/companion_census.py` to use anchor-line structural keys.
- Create `staging/validated/OT/PSA_footnotes.md` using `pdftotext` extraction.
- Produce reconciliation reports for 7 OT books using anchor-line truth.

## Files / Artifacts
- `pipeline/research/companion_census.py` (Corrected to Anchor-Line truth)
- `pipeline/research/reconcile_ot_markers.py` (Corrected to Anchor-Line truth)
- `reports/companion_file_census.json` (Regenerated)
- `staging/validated/OT/PSA_footnotes.md` (New)
- `reports/ot_marker_reconciliation/{PSA,SIR,1ES,ECC,1SA,DEU,NUM}.json` (New)

## Findings Or Changes

### Census Repair (Anchor-Line Verification)
Total OT footnote entries recovered via anchor-line parsing:
- **OT Total Entries**: 3,381 (from ~3,216 via heading-parsing)
- **PSA**: 47 (Stabilized)
- **1ES**: 27 (from ~0 via heading-parsing)
- **ECC**: 45 (from ~5 via heading-parsing)
- **SIR**: 259 (from ~0 via heading-parsing)

### Reconciliation Audit
| Book | Footnote Entries | Matches | Alignment State |
|---|---|---|---|
| **1ES** | 27 | 27 | **Full Alignment** |
| **ECC** | 45 | 5 | **Partial Alignment** (Linkage gap) |
| **1SA** | 81 | 3 | **Partial Alignment** (Linkage gap) |
| **DEU** | 78 | 3 | **Partial Alignment** (Linkage gap) |
| **NUM** | 71 | 3 | **Partial Alignment** (Linkage gap) |
| **SIR** | 259 | 0 | **Systemic Corruption** (Chapter 0 drift in markers) |
| **PSA** | 47 | 2 | **Systemic Corruption** (Placeholder saturation in markers) |

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Anchor-Line Truth | Heading lines in Markdown are often reflowed or inline; anchor lines are structurally isolated | None; this matches project Markdown standards | N/A |
| PSA status split | Distinguishes between successful file creation and failed marker alignment | None; clarifies the two distinct blockers | N/A |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| OT Footnote Count (1ES) | `27` | `reports/companion_file_census.json` |
| OT Footnote Count (ECC) | `45` | `reports/companion_file_census.json` |
| OT Footnote Count (SIR) | `259` | `reports/companion_file_census.json` |
| PSA Footnote Entry Count | `47` | `grep -c "anchor: PSA" staging/validated/OT/PSA_footnotes.md` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `pipeline/research/companion_census.py`, `pipeline/research/reconcile_ot_markers.py`, `staging/validated/OT/PSA_footnotes.md` |
| `Verification run` | `done` | Census + Reconciliation scripts rerun with anchor-line logic. |
| `Artifacts refreshed` | `done` | `reports/companion_file_census.json`, `reports/ot_marker_reconciliation/*.json` |
| `Remaining known drift` | `present` | Systemic anchor corruption in PSA/SIR marker files. |
| `Next owner` | `ark` | Diagnostic review of marker anchor corruption in PSA and SIR. |

## Handoff
**To:** `ark`  
**Ask:** `The footnote files are structurally sound and have been recovered via anchor-line parsing. Linkage is now blocked exclusively by marker anchor corruption in PSA and SIR, and linkage gaps in ECC/1SA/DEU/NUM.`
