# First 14-Day Execution Plan
**Author:** Ark | **Date:** 2026-03-06 | **Status:** Proposed

---

## Governing Principles

- **Bounded:** Each day's work has a defined endpoint. No open-ended exploration.
- **Low-risk:** Nothing touches `canon/` until Day 10 at the earliest.
- **Rollback-ready:** Every step that produces artifacts writes to `staging/` or `pipeline/`, never canon. Rollback is always `git reset` or directory delete.
- **Inspect before scale:** We process Genesis first. Nothing is automated at scale until Genesis is clean and human-reviewed.

---

## Phase A: Foundation (Days 1–4)

### Day 1 — Repository Structure
**Tasks:**
1. Create the full directory tree per the Folder Contract.
2. Add `.gitkeep` files in empty directories so they are tracked.
3. Add a `.gitignore` excluding `staging/` from commits (staging is ephemeral).
4. Update `README.md` with project overview.
5. Commit: `chore: scaffold repository structure per folder contract`

**Decision:** `staging/` is gitignored because it is transient. Validated and promoted files are what we version.

**Rationale:** Clean structure before any parsing prevents future reorganization.

**Risks:** None — no content files touched.

**Rollback:** `git reset --hard HEAD~1`

**Owner:** Ark

---

### Day 2 — Schema and Registry Files
**Tasks:**
1. Write `schemas/scripture_frontmatter.json` (JSON Schema draft-7).
2. Write `schemas/notes_frontmatter.json`.
3. Write `schemas/anchor_registry.json` — initial 76-book registry with all codes, book names, and canon positions.
4. **Human action required:** Review and ratify the anchor registry. No anchors may be written to parsed files until this is signed off.
5. Commit: `feat: add validation schemas and 76-book anchor registry`

**Decision:** Lock the registry before parsing begins. Changing book codes post-parse requires a corpus-wide migration.

**Risks:** Human may want to amend book codes (especially for deuterocanonical books where conventions vary). This is expected and manageable at this stage.

**Rollback:** Schema files are in `schemas/`; amending before any parse has been run is zero-cost.

**Owner:** Ark (draft) + Human (ratification)

---

### Day 3 — Docling Parse Probe
**Tasks:**
1. Run Docling on `src.texts/the_orthodox_study_bible.pdf` — first 10 pages only.
2. Inspect raw output structure (JSON/Markdown) in `staging/raw/probe/`.
3. Document findings: How does Docling segment verses? Are footnotes structurally separated? What markers exist for chapter headings?
4. Write `memos/06_docling_probe_findings.md` with findings and recommended extraction strategy.
5. Do NOT write any canon files yet.

**Decision:** Probe before pipeline. The OSB is a complex typeset document. We do not assume Docling output is usable without inspection.

**Rationale:** One bad assumption about PDF structure, acted on at scale, produces 76 corrupted files. One probe on 10 pages costs one day and saves weeks.

**Risks:** Docling may struggle with the OSB's two-column layout, footnote formatting, or Greek text. This is the moment to discover that, not after processing the full document.

**Rollback:** `staging/raw/probe/` is gitignored. No impact.

**Owner:** Ark

---

### Day 4 — Extraction Script v1
**Tasks:**
1. Based on probe findings, write `pipeline/parse/docling_parse.py`.
2. Script takes: input PDF path, target book name, output directory.
3. Output: structured JSON with fields: `book_code`, `chapter`, `verse`, `text`, `footnotes[]`, `raw_line`.
4. Run on Genesis only.
5. Inspect output manually — every chapter heading, every verse, every footnote separation.
6. Document anomalies in `memos/07_genesis_parse_notes.md`.
7. Do NOT write markdown files yet.

**Risks:** The parser may need significant tuning. Genesis is ~50 chapters — a manageable manual inspection.

**Rollback:** Script is in `pipeline/`; output is in `staging/`. Both are disposable.

**Owner:** Ark

---

## Phase B: Validation Suite (Days 5–7)

### Day 5 — Write Validation Scripts
**Tasks:**
1. Write `pipeline/validate/check_schema.py`
2. Write `pipeline/validate/check_purity.py`
3. Write `pipeline/validate/check_anchors.py`
4. Write `pipeline/validate/check_completeness.py`
5. Write a test harness with synthetic pass/fail fixtures for each check.
6. All checks must produce structured output suitable for the report format.
7. Commit: `feat: add validation pipeline scripts with test fixtures`

**Risks:** Validation logic may have false positives on legitimate verse text patterns. The test fixtures catch this before real data is processed.

**Rollback:** Scripts do not touch data. Safe to iterate freely.

**Owner:** Ark

---

### Day 6 — Run Validation on Genesis JSON
**Tasks:**
1. Convert Genesis JSON (from Day 4) to two staging markdown files: `GEN.md` (scripture only) and `GEN_notes.md` (footnotes only).
2. Run V1–V4 on `GEN.md`.
3. Run V1 + V6 on `GEN_notes.md`.
4. Produce validation report.
5. Fix any validation failures by adjusting the extraction script (not the output files manually).
6. Iterate until Genesis passes all checks.

**Decision:** Fix the pipeline, not the output. Manual edits to staging files create a process that does not scale.

**Risks:** Multiple iteration rounds may be needed. This is expected and acceptable — better now than at book 40.

**Rollback:** All changes are in `staging/` and `pipeline/`. Canon untouched.

**Owner:** Ark

---

### Day 7 — Write Promote Script and Report Generation
**Tasks:**
1. Write `pipeline/promote/promote.py`.
2. Script: takes a validated staging file, computes checksum, writes to `canon/`, commits with standardized message.
3. Write report generator: produces `reports/YYYY-MM-DD_validation.md` from check outputs.
4. Test on Genesis in dry-run mode (no actual write to canon).
5. Commit: `feat: add promotion script and report generator`

**Risks:** Promote script has write access to `canon/` — it must be carefully tested in dry-run mode before any live use.

**Rollback:** Promote script is not run live until Day 10+. No risk at this stage.

**Owner:** Ark

---

## Phase C: First Promotion (Days 8–10)

### Day 8 — Human Review of Genesis Staging Files
**Tasks (Human):**
1. Review `staging/validated/OT/GEN.md` — spot-check 10 verses across different chapters.
2. Review `staging/validated/OT/GEN_notes.md` — confirm notes are separated and reference correct anchors.
3. Review the Day 6 validation report.
4. Signal approval (comment in `memos/` or GitHub PR on a staging branch).

**Decision:** No promotion without human sign-off on the first book. This sets the standard for all future promotions.

**Owner:** Human

---

### Day 9 — First Canon Promotion
**Tasks:**
1. Human has approved Genesis staging files.
2. Ark runs promote script (live, not dry-run) for `GEN.md` and `GEN_notes.md`.
3. Promotion commit is made to `main`.
4. Validation report for the promotion run is committed to `reports/`.
5. Verify canon file checksum matches promote script output.

**Commit message:** `promote: Genesis (GEN) — first canon promotion, OSB v1`

**Rationale:** This is the first canonical artifact. It should be deliberate, documented, and celebrated.

**Risks:** Any error in the promote script is discovered here with only one book affected.

**Rollback:** `git revert <promotion commit>` — Genesis returns to staging, canon is clean.

**Owner:** Ark (execution) + Human (approval)

---

### Day 10 — Retrospective and Calibration
**Tasks:**
1. Ark writes `memos/08_day10_retrospective.md` covering:
   - What took longer than expected?
   - What assumptions were wrong?
   - What should change in the pipeline or validation before processing more books?
2. Human reviews retrospective.
3. Decide: process next 4 books (Exodus–Deuteronomy) with current pipeline, or adjust first?

**Decision:** Do not proceed to bulk processing until both parties are confident in the pipeline.

**Owner:** Ark (memo) + Human (decision)

---

## Phase D: Expanding the Substrate (Days 11–14)

### Days 11–13 — Process Pentateuch (Books 2–5)
**Tasks:**
1. Run Docling parse on Exodus, Leviticus, Numbers, Deuteronomy.
2. Run validation on each.
3. Fix any parse anomalies (log in `memos/` if significant).
4. Human spot-reviews at least one book.
5. Promote all four upon approval.

**Decision:** Process the Pentateuch as a batch. These books have similar structure. Any structural anomalies discovered here will inform the rest of the OT.

**Risks:** Leviticus and Numbers have distinct formatting (legal/ceremonial lists) that may stress the parser differently than narrative prose.

**Rollback:** Per-book promotion commits. Any bad book is reverted individually.

**Owner:** Ark (parse + validate + promote) + Human (review + approval)

---

### Day 14 — 14-Day Report and Plan v2
**Tasks:**
1. Ark writes `memos/09_14day_report.md`:
   - Books promoted: target is 5 (Genesis–Deuteronomy)
   - Validation pass rate
   - Pipeline performance (time per book)
   - Known issues and their status
   - Proposed scope for next 14-day plan
2. Human reviews and signals next priorities.

**Owner:** Ark (report) + Human (prioritization)

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Docling struggles with OSB PDF layout | High | High | Day 3 probe catches this early; manual override rules in parser |
| Footnotes not structurally separable | Medium | High | Treat as quarantine; flag for human-guided extraction rule |
| LXX numbering creates anchor conflicts | Medium | Medium | Anchor registry locked before parsing; Psalms handled explicitly |
| Human unavailable for review | Low | Medium | Ark continues pipeline work on staging; nothing promoted without review |
| Parse takes much longer than expected | Low | Low | Pipeline is not time-critical; quality over speed |

---

## Day-by-Day Summary

| Day | Milestone | Owner | Canon touched? |
|-----|-----------|-------|----------------|
| 1 | Directory structure scaffolded | Ark | No |
| 2 | Schemas + registry written; human ratifies | Ark + Human | No |
| 3 | Docling probe on first 10 pages | Ark | No |
| 4 | Extraction script v1; Genesis JSON output | Ark | No |
| 5 | Validation scripts written and tested | Ark | No |
| 6 | Genesis passes validation | Ark | No |
| 7 | Promote script + report generator written | Ark | No |
| 8 | Human reviews Genesis staging | Human | No |
| 9 | Genesis promoted to canon | Ark + Human | YES — first time |
| 10 | Retrospective; calibration decision | Ark + Human | No |
| 11 | Exodus and Leviticus parsed + validated | Ark | No |
| 12 | Numbers and Deuteronomy parsed + validated | Ark | No |
| 13 | Human reviews; Pentateuch promoted | Ark + Human | YES |
| 14 | 14-day report; plan v2 proposed | Ark | No |
