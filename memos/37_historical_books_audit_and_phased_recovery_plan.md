# Memo 37 — Historical Books Audit And Phased Recovery Plan

**Author:** `ezra`  
**Type:** `audit / planning`  
**Status:** `active`  
**Date:** `2026-03-09`  
**Scope:** `Group 2 + Group 3 audit reset / recovery sequencing / evidence hardening`

## Summary
- Group 2 and Group 3 are **not** broadly promotion-ready.
- `1KI` is the main structural blocker.
- `JOS` has an unresolved versification / source-policy issue.
- `RUT`, `2SA`, `1CH`, and `2CH` still show visible editorial residue despite zero-candidate sidecars.
- Current dossiers prove validation snapshots, but they do **not** fully prove promotion-gate satisfaction for incomplete books because dossier evidence does not record whether `--allow-incomplete` was used.

This memo supersedes the readiness framing in memos 32 and 33 for planning purposes.

## Findings

### 1. `1KI` has structural heading contamination
- The live staged file contains clearly wrong narrative headings interleaved into chapter 20-22 verse flow:
  - [`staging/validated/OT/1KI.md:2000`](/home/ark/orthodoxphronema/staging/validated/OT/1KI.md#L2000)
  - [`staging/validated/OT/1KI.md:2030`](/home/ark/orthodoxphronema/staging/validated/OT/1KI.md#L2030)
  - [`staging/validated/OT/1KI.md:2056`](/home/ark/orthodoxphronema/staging/validated/OT/1KI.md#L2056)
  - [`staging/validated/OT/1KI.md:2236`](/home/ark/orthodoxphronema/staging/validated/OT/1KI.md#L2236)
  - [`staging/validated/OT/1KI.md:2266`](/home/ark/orthodoxphronema/staging/validated/OT/1KI.md#L2266)
- These headings are semantically unrelated to the surrounding verses and should not pass as canonical heading content.
- This directly contradicts the broad readiness claim in [`memos/33_historical_books_b_extraction.md:13`](/home/ark/orthodoxphronema/memos/33_historical_books_b_extraction.md#L13) and [`memos/33_historical_books_b_extraction.md:84`](/home/ark/orthodoxphronema/memos/33_historical_books_b_extraction.md#L84).

### 2. Editorial candidate sidecars are under-detecting visible residue
- Zero-candidate sidecars do not currently imply visually clean staged text.
- Representative live defects:
  - [`staging/validated/OT/RUT.md:31`](/home/ark/orthodoxphronema/staging/validated/OT/RUT.md#L31)
  - [`staging/validated/OT/RUT.md:47`](/home/ark/orthodoxphronema/staging/validated/OT/RUT.md#L47)
  - [`staging/validated/OT/RUT.md:60`](/home/ark/orthodoxphronema/staging/validated/OT/RUT.md#L60)
  - [`staging/validated/OT/RUT.md:66`](/home/ark/orthodoxphronema/staging/validated/OT/RUT.md#L66)
  - [`staging/validated/OT/2SA.md:41`](/home/ark/orthodoxphronema/staging/validated/OT/2SA.md#L41)
  - [`staging/validated/OT/2SA.md:43`](/home/ark/orthodoxphronema/staging/validated/OT/2SA.md#L43)
  - [`staging/validated/OT/2SA.md:45`](/home/ark/orthodoxphronema/staging/validated/OT/2SA.md#L45)
  - [`staging/validated/OT/2SA.md:48`](/home/ark/orthodoxphronema/staging/validated/OT/2SA.md#L48)
  - [`staging/validated/OT/1CH.md:747`](/home/ark/orthodoxphronema/staging/validated/OT/1CH.md#L747)
  - [`staging/validated/OT/1CH.md:772`](/home/ark/orthodoxphronema/staging/validated/OT/1CH.md#L772)
  - [`staging/validated/OT/2CH.md:89`](/home/ark/orthodoxphronema/staging/validated/OT/2CH.md#L89)
  - [`staging/validated/OT/2CH.md:126`](/home/ark/orthodoxphronema/staging/validated/OT/2CH.md#L126)
  - [`staging/validated/OT/2CH.md:129`](/home/ark/orthodoxphronema/staging/validated/OT/2CH.md#L129)
  - [`staging/validated/OT/2CH.md:134`](/home/ark/orthodoxphronema/staging/validated/OT/2CH.md#L134)
  - [`staging/validated/OT/1KI.md:2024`](/home/ark/orthodoxphronema/staging/validated/OT/1KI.md#L2024)
  - [`staging/validated/OT/1KI.md:2058`](/home/ark/orthodoxphronema/staging/validated/OT/1KI.md#L2058)
  - [`staging/validated/OT/1KI.md:2062`](/home/ark/orthodoxphronema/staging/validated/OT/1KI.md#L2062)
  - [`staging/validated/OT/1KI.md:2144`](/home/ark/orthodoxphronema/staging/validated/OT/1KI.md#L2144)
  - [`staging/validated/OT/1KI.md:2246`](/home/ark/orthodoxphronema/staging/validated/OT/1KI.md#L2246)
- Relevant sidecars still report zero candidates:
  - [`staging/validated/OT/RUT_editorial_candidates.json:5`](/home/ark/orthodoxphronema/staging/validated/OT/RUT_editorial_candidates.json#L5)
  - [`staging/validated/OT/2SA_editorial_candidates.json:5`](/home/ark/orthodoxphronema/staging/validated/OT/2SA_editorial_candidates.json#L5)
  - [`staging/validated/OT/1CH_editorial_candidates.json:5`](/home/ark/orthodoxphronema/staging/validated/OT/1CH_editorial_candidates.json#L5)
  - [`staging/validated/OT/2CH_editorial_candidates.json:5`](/home/ark/orthodoxphronema/staging/validated/OT/2CH_editorial_candidates.json#L5)
  - [`staging/validated/OT/1KI_editorial_candidates.json:5`](/home/ark/orthodoxphronema/staging/validated/OT/1KI_editorial_candidates.json#L5)

### 3. `JOS` needs source-policy classification, not just a generic `V7` shrug
- [`memos/32_historical_books_a_extraction.md:69`](/home/ark/orthodoxphronema/memos/32_historical_books_a_extraction.md#L69) reduces `JOS` to “2 extra verses from V9 splits.”
- The live file still contains extra anchored verses at:
  - [`staging/validated/OT/JOS.md:885`](/home/ark/orthodoxphronema/staging/validated/OT/JOS.md#L885)
  - [`staging/validated/OT/JOS.md:886`](/home/ark/orthodoxphronema/staging/validated/OT/JOS.md#L886)
- The registry still expects chapter 24 to end at 33 verses, so this is not yet a clean “promotion-ready” state.

### 4. Dossier evidence is incomplete for incomplete-book decisions
- `promote.py` blocks on `V7` unless `--allow-incomplete` is passed:
  - [`pipeline/promote/promote.py:381`](/home/ark/orthodoxphronema/pipeline/promote/promote.py#L381)
- The dossier schema created at:
  - [`pipeline/promote/promote.py:168`](/home/ark/orthodoxphronema/pipeline/promote/promote.py#L168)
- does **not** record whether `allow_incomplete` was used.
- Current historical dossiers therefore prove only `dry-run` or `blocked`, not the full promotion-gate semantics implied by memos 32-33:
  - [`reports/JOS_promotion_dossier.json:52`](/home/ark/orthodoxphronema/reports/JOS_promotion_dossier.json#L52)
  - [`reports/1SA_promotion_dossier.json:52`](/home/ark/orthodoxphronema/reports/1SA_promotion_dossier.json#L52)
  - [`reports/2SA_promotion_dossier.json:52`](/home/ark/orthodoxphronema/reports/2SA_promotion_dossier.json#L52)
  - [`reports/1KI_promotion_dossier.json:52`](/home/ark/orthodoxphronema/reports/1KI_promotion_dossier.json#L52)
  - [`reports/2KI_promotion_dossier.json:52`](/home/ark/orthodoxphronema/reports/2KI_promotion_dossier.json#L52)

### 5. Residual ratification was overstated
- [`memos/33_historical_books_b_extraction.md:41`](/home/ark/orthodoxphronema/memos/33_historical_books_b_extraction.md#L41) says `1CH.16:7` is a ratified residual.
- The actual sidecars still have no human ratification metadata:
  - [`staging/validated/OT/1CH_residuals.json:5`](/home/ark/orthodoxphronema/staging/validated/OT/1CH_residuals.json#L5)
  - [`staging/validated/OT/1CH_residuals.json:6`](/home/ark/orthodoxphronema/staging/validated/OT/1CH_residuals.json#L6)
  - [`staging/validated/OT/2CH_residuals.json:5`](/home/ark/orthodoxphronema/staging/validated/OT/2CH_residuals.json#L5)
  - [`staging/validated/OT/2CH_residuals.json:6`](/home/ark/orthodoxphronema/staging/validated/OT/2CH_residuals.json#L6)
- `1CH` and `2CH` remain blocked under the active gate for that reason.

## Interpretation Reset
- Memo 32 should now be read as: `Group 2 extracted, not yet audit-cleared`.
- Memo 33 should now be read as: `Group 3 extracted, not yet audit-cleared`.
- Keep both as progress records, not as the active readiness brief.

## Phased Recovery Plan

### Phase 0 — Truth Reset
- Treat this memo as the active planning brief for historical books.
- Do not use memos 32-33 as the current readiness source.
- Treat the dashboard as operational truth only after the dossier/evidence hardening below.

### Phase 1 — Evidence Hardening
- Extend promotion dossier output to record:
  - `staged_path`
  - `staged_body_checksum`
  - `allow_incomplete`
  - `editorial_candidates_path`
  - `residuals_path`
  - `current_staged_body_checksum` or equivalent staged-parity field
- Regenerate dossiers for Group 2 and Group 3 after no-text-change validation runs.
- Update dashboard interpretation only after the richer dossier exists.

### Phase 2 — Validator / Gate Hardening
- Add a heading-quality check for repeated or semantically implausible headings in canon text.
- Add editorial detection for split-word residue like:
  - `Giv epraise`
  - `forev er`
  - `oliv eoil`
  - `lov eof`
- Add a detector or audit rule for inline verse-number leakage such as:
  - `cloud of the Lord's glory, 14 so`
- Keep these as advisory/editorial blockers first unless confidence is already high enough for a hard fail.

### Phase 3 — Book Recovery Order
Use this order:
1. `1KI`
2. `JOS`
3. `2CH`
4. `1CH`
5. `2SA`
6. `RUT`
7. `1SA`
8. `JDG`
9. `2KI`

Reasoning:
- `1KI` first because it has both structural heading contamination and visible editorial residue.
- `JOS` second because extra anchored verses need source-policy classification.
- `2CH` and `1CH` next because they combine residual governance with live text residue.
- `2SA` and `RUT` are bounded editorial cleanup tasks.

### Phase 4 — Residual Governance
- Re-check `1CH.16:7` and `2CH.33:1` with the strongest available OSB witness path.
- Do not describe a residual as “ratified” unless sidecar-level human ratification is actually present.
- Keep item-level and sidecar-level semantics separate:
  - item-level `ratified: true`
  - sidecar-level `ratified_by: "human"` plus `ratified_date`

### Phase 5 — Resume Scale Only After Exit Criteria
Do not continue to the next extraction group until all are true:
- `1KI` has no spurious headings in canon text.
- `JOS` extra verses are classified and resolved.
- Group 2 and 3 books have no obvious split-word / fused-word residue on spot check.
- Dossiers are regenerated with complete evidence fields.
- Residual sidecars with content are human-ratified.

## Ark Planning Prompt
Enter planning mode from this memo, not memos 32-33. Treat the next step as a stabilization-and-evidence sprint, not new extraction. Return a short implementation plan covering:
1. dossier schema hardening
2. heading-quality / editorial detector additions
3. `1KI` structural cleanup
4. `JOS` versification/source-policy classification
5. residual ratification cleanup for `1CH` and `2CH`

Use the phased recovery order in this memo and do not schedule Group 4 extraction until the exit criteria are met.

## Required Test Coverage
- dossier fields capturing `allow_incomplete` and staged parity
- heading contamination detection using a `1KI`-style fixture
- split-word editorial candidate detection using `1CH` / `2SA` style cases
- inline verse-number leakage detection using a `2CH.5:14` style case
- dashboard status correctness when dossiers are incomplete vs refreshed

## Handoff
**To:** `ark`  
**Ask:** Use this memo as the active historical-books planning brief and reset the next session to recovery/hardening work rather than new extraction.
