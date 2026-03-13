# Memo 31 — Pentateuch Audit Blockers And Dashboard Corrections

**Author:** `ezra`
**Type:** `audit`
**Status:** `active`
**Date:** `2026-03-09`
**Scope:** `GEN / EXO / LEV / NUM / DEU audit review`

## Summary
- Human asked Ezra to verify Ark's claim that the entire Pentateuch is extracted and promotion-ready.
- The extraction claim is true.
- The promotion-ready claim is not yet true for the whole Pentateuch.
- `GEN` remains promoted and intact.
- `LEV` currently looks clean and promotion-ready from repo evidence.
- `EXO` is close, but its staged artifact no longer matches its recorded dry-run dossier checksum.
- `NUM` and `DEU` are blocked by live one-verse-per-line violations and residual/governance issues.

## Key Findings

### 1. `NUM` is not promotion-ready
- [`NUM.6:27`](/home/ark/orthodoxphronema/staging/validated/OT/NUM_residuals.json#L8) is documented as absorbed into [`NUM.6:23`](/home/ark/orthodoxphronema/staging/validated/OT/NUM.md#L310) instead of being emitted as its own verse line.
- That violates the repo invariant at [`AGENTS.md:178`](/home/ark/orthodoxphronema/AGENTS.md#L178): one verse per line is mandatory.
- The book also still shows visible OCR residue, e.g. [`NUM.md:189`](/home/ark/orthodoxphronema/staging/validated/OT/NUM.md#L189) and [`NUM.md:244`](/home/ark/orthodoxphronema/staging/validated/OT/NUM.md#L244).

### 2. `DEU` is not promotion-ready
- The staged file still jumps from [`DEU.33:7`](/home/ark/orthodoxphronema/staging/validated/OT/DEU.md#L1206) to [`DEU.33:9`](/home/ark/orthodoxphronema/staging/validated/OT/DEU.md#L1207).
- The content for `DEU.33:8` is visibly fused into the `33:7` line, so this is still a structural one-verse-per-line failure even though `V9` does not catch it.
- The file is also not editorally pure yet, with visible OCR residue at [`DEU.md:1200`](/home/ark/orthodoxphronema/staging/validated/OT/DEU.md#L1200), [`DEU.md:1206`](/home/ark/orthodoxphronema/staging/validated/OT/DEU.md#L1206), [`DEU.md:1207`](/home/ark/orthodoxphronema/staging/validated/OT/DEU.md#L1207), [`DEU.md:1211`](/home/ark/orthodoxphronema/staging/validated/OT/DEU.md#L1211), [`DEU.md:1222`](/home/ark/orthodoxphronema/staging/validated/OT/DEU.md#L1222), and [`DEU.md:1228`](/home/ark/orthodoxphronema/staging/validated/OT/DEU.md#L1228).

### 3. Residual governance is inconsistent for `NUM` and `DEU`
- Both sidecars say `ratified_by: "ark"` at [`NUM_residuals.json:4`](/home/ark/orthodoxphronema/staging/validated/OT/NUM_residuals.json#L4) and [`DEU_residuals.json:4`](/home/ark/orthodoxphronema/staging/validated/OT/DEU_residuals.json#L4).
- The workflow requires human ratification for ambiguous cases at [`AGENTS.md:18`](/home/ark/orthodoxphronema/AGENTS.md#L18), [`AGENTS.md:57`](/home/ark/orthodoxphronema/AGENTS.md#L57), and [`AGENTS.md:173`](/home/ark/orthodoxphronema/AGENTS.md#L173).

### 4. Residual schema drift exists
- `NUM` and `DEU` sidecars use `class` instead of `classification` at [`NUM_residuals.json:9`](/home/ark/orthodoxphronema/staging/validated/OT/NUM_residuals.json#L9) and [`DEU_residuals.json:9`](/home/ark/orthodoxphronema/staging/validated/OT/DEU_residuals.json#L9).
- The rest of the repo uses `classification`, so this weakens taxonomy-driven workflow logic.

### 5. `EXO` evidence is stale
- The current staged `EXO.md` body no longer matches the dry-run checksum recorded in [`EXO_promotion_dossier.json:6`](/home/ark/orthodoxphronema/reports/EXO_promotion_dossier.json#L6).
- That conflicts with the workflow rule that promotion must use the same staged artifact that was validated and audited, at [`AGENTS.md:95`](/home/ark/orthodoxphronema/AGENTS.md#L95) and [`AGENTS.md:174`](/home/ark/orthodoxphronema/AGENTS.md#L174).

## Dashboard Correction
- The previous dashboard logic was too optimistic.
- It treated `promotion_ready` mostly as:
  - pass/warn validation
  - zero editorial candidates
  - residual count not obviously blocking
- That missed four real blockers:
  - stale dossier checksum vs current staged text
  - residual exceptions ratified by Ark instead of Human
  - sidecar schema drift (`class` vs `classification`)
  - residual descriptions that explicitly admit embedded/absorbed verse content

## Ezra Changes Requested Of Ark
1. `NUM`
- emit `NUM.6:27` as its own verse line or mark the book blocked and stop calling it promotion-ready
- clean remaining visible OCR residue
- normalize the sidecar to `classification`
- get human ratification if a residual exception remains

2. `DEU`
- separate `DEU.33:8` into its own verse line
- clean the visible OCR residue in chapter 33 before resubmitting for promotion
- normalize the sidecar to `classification`
- get human ratification if a residual exception remains

3. `EXO`
- rerun the dry-run promotion so the dossier checksum matches the current staged artifact
- then return for a narrow final audit, not a broad re-litigation

4. `LEV`
- no blocker found in this audit pass
- still acceptable to do one last human skim, but repo evidence currently supports promotion-readiness

## Dashboard Operating Rule
- Regenerate [`reports/book_status_dashboard.json`](/home/ark/orthodoxphronema/reports/book_status_dashboard.json) after any change that affects:
  - staged scripture body text
  - editorial candidate sidecars
  - residual sidecars
  - promotion dossiers
- Do not treat old dashboard state as authoritative after staged text changes.

## Handoff
**To:** `ark`
**Ask:** Treat the Pentateuch as partially ready, not fully ready. `LEV` is the clean success case. `EXO` needs dossier refresh. `NUM` and `DEU` need structural cleanup plus sidecar/governance normalization before they can re-enter promotion discussion.
