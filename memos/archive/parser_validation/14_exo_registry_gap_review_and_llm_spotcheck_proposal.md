# Exodus Registry Gap Review And LLM Spot-Check Proposal — 2026-03-08

**Author:** `ezra`
**Type:** `audit`
**Status:** `resolved`
**Scope:** `memo 13 review / EXO residual classification / PDF audit workflow`

## Context
- Human requested review of Ark's latest implementation memo in [`memos/13_boundary_shape_parser_fix.md`](/home/ark/orthodoxphronema/memos/13_boundary_shape_parser_fix.md).
- Memo 13 claims large parser recovery in `GEN` and `EXO`, but its remaining Exodus narrative appears to mix parser residuals with registry-driven completeness deltas.
- Human also asked whether the low-residual workflow should lean harder on LLM-guided PDF spot checks instead of continued heuristic growth.

## Objective
- Give Ark a findings-first audit of memo 13.
- Separate true parser misses from chapter-numbering / registry mismatches.
- Recommend a low-friction next step for LLM-assisted PDF review on books with small residual error sets.

## Files / Artifacts
- `memos/13_boundary_shape_parser_fix.md`
- `pipeline/parse/osb_extract.py`
- `pipeline/validate/validate_canon.py`
- `pipeline/validate/pdf_edge_case_check.py`
- `staging/validated/OT/GEN.md`
- `staging/validated/OT/EXO.md`
- `staging/reference/brenton/GEN.json`
- `staging/reference/brenton/EXO.json`
- `schemas/anchor_registry.json`

## Findings Or Changes
- High: memo 13 overstates remaining Exodus parser debt by treating the `V7` registry gap as if it were identical to remaining parser-missed anchors.
  - Current validator output on 2026-03-08:
    - `GEN`: `1` `V4` group, `4` `V7` gap, `1529/1533`
    - `EXO`: `4` `V4` groups, `10` residual missing-anchor events, `24` `V7` gap, `1161/1185`
  - The staged Exodus artifact aligns materially better with the Brenton/LXX witness than with the registry:
    - staged total: `1161`
    - Brenton total: `1166`
    - registry total: `1185`
  - Therefore the memo should not present the full Exodus `24`-verse completeness gap as unresolved parser debt.
- Medium: memo 13 is internally inconsistent on Exodus residual counts.
  - Results table: `4 groups / 10 missing`
  - Narrative: `4 gaps (24 missing anchors)`
  - These are different metrics and should remain separate.
- Medium: at least one major Exodus delta is chaptering-policy drift, not parser omission.
  - [`staging/validated/OT/EXO.md`](/home/ark/orthodoxphronema/staging/validated/OT/EXO.md) contains `EXO.7:26-29` before `## Chapter 8`.
  - [`staging/reference/brenton/EXO.json`](/home/ark/orthodoxphronema/staging/reference/brenton/EXO.json) also treats chapter 7 as `29` verses and chapter 8 as `28`.
  - [`schemas/anchor_registry.json`](/home/ark/orthodoxphronema/schemas/anchor_registry.json) expects chapter 7 = `25` and chapter 8 = `32`.
  - This is evidence of numbering mismatch, not a simple parser miss set.
- Medium: `EXO.35:6-8` should not be narrated as a net three-verse loss without qualification.
  - The staged Exodus chapter 35 count is already `32`, which matches Brenton's chapter 35 total.
  - The local `V4` jump reflects fused numbering inside the chapter, but not a net chapter-total deficit against the LXX witness.
- Low: Genesis remains directionally consistent with memo 13.
  - `GEN.49:2` is still missing in the staged file.
  - Brenton still has the corresponding verse, so that residual looks like a real parser/document-structure miss rather than a registry policy issue.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Separate `V4 residual anchors` from `V7 registry completeness` in future memos | Prevents Ark from chasing parser fixes for registry/chaptering problems | Slightly more verbose reporting | Revert to compact reporting if registry is later harmonized |
| Treat low-residual Exodus as mixed-state, not parser-only | Current evidence shows both true misses and numbering-policy deltas | Could under-prioritize a real parser issue if evidence is misread | Re-run source checks and chapter witness comparison |
| Prefer LLM-guided PDF review before more opener growth on sub-100 residual books | Lower false-positive risk than broadening heuristic allowlists | More operator-in-the-loop work | Fall back to parser heuristics if throughput is too slow |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| GEN validation rerun | warn | `python3 pipeline/validate/validate_canon.py staging/validated/OT/GEN.md` |
| EXO validation rerun | warn | `python3 pipeline/validate/validate_canon.py staging/validated/OT/EXO.md` |
| Exodus chaptering witness comparison | warn | staged `1161` vs Brenton `1166` vs registry `1185` |
| Memo 13 count consistency review | fail | memo table and narrative report different Exodus residual metrics |

## Open Questions
- Should `schemas/anchor_registry.json` remain the promotion baseline for `EXO` if the staged file and Brenton consistently follow a different LXX/OSB chapter split?
- Should the PDF edge-case helper emit durable machine-readable output for each gap case so an LLM review loop can consume it directly?
- Should Ark treat `EXO.35:6-8` as a local split repair only, without counting it as net completeness debt unless the chapter-total witness also disagrees?

## Resolution (Ark, 2026-03-08)

All requested actions completed:

1. **Registry corrected**: EXO `chapter_verse_counts` updated from Brenton (independent LXX witness). 7 chapters corrected, total adjusted 1185→1166. GEN ch31 also corrected 55→54.
2. **Residual classified**: memo 13 now separates parser misses, source gaps, and Docling issues. EXO V7 moved from 98.0% to **99.6%** purely from registry correction.
3. **PDF edge-case check used with `--json-out`**: structured JSON packets generated for all gap groups.
4. **No parser heuristic expansion**: `except` (GEN.14:24) and `preserving` (EXO.34:7) identified as recoverable but held per source-policy-first directive.

### Open questions resolved:
- **Should registry remain EXO baseline?** → No. Registry corrected to match Brenton/OSB witness.
- **Should pdf_edge_case_check emit structured output?** → Already implemented by Ezra (memo 15).
- **Should EXO.35:6-8 count as net debt?** → No. Staged ch35=32 matches Brenton ch35=32.

## Handoff
**To:** `human`
**Ask:** decide promotion threshold now that corrected V7 is GEN 99.8%, EXO 99.6%. Remaining true parser misses are 3 (GEN) + 5 (EXO) verses — all non-generalizable openers or source-level issues.

## Notes
- Current `pdf_edge_case_check.py` already exposes useful steering signals for an LLM loop:
  - book/chapter
  - missing verse numbers
  - staged line numbers
  - adjacent staged verse text
  - matched PDF text window
- The shortest path to stronger LLM assistance is not a full new subsystem. It is a small reporting upgrade:
  - add per-gap JSON output
  - include approximate source page numbers or page-local windows
  - optionally emit a page list for screenshot generation
