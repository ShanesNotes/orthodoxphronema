# Validation Spec — Minimum Viable + Scale Path
**Author:** Ark | **Date:** 2026-03-06 | **Status:** Proposed

---

## Core Principle

No content transitions between pipeline stages without passing all checks for that stage. Validation is a hard gate, not a best-effort lint. A partial pass is a fail.

---

## Stage 1 Checks (Staging Raw → Staging Validated)

These run after Docling parse, before any human review.

### V1 — Schema Conformance

**Decision:** Every parsed file must have a YAML frontmatter block that validates against `schemas/scripture_frontmatter.json` (or `notes_frontmatter.json` for notes).

**Check:** `pipeline/validate/check_schema.py`

**Fail behavior:** File is quarantined to `staging/quarantine/` with a dated error report. No further checks run on that file.

**Rationale:** Downstream checks depend on valid metadata. A missing book code or status field would poison all subsequent steps.

**Rollback:** Quarantined files do not touch canon. Fix the parse rule and re-run.

**Owner:** Ark

---

### V2 — Purity Check (Critical)

**Decision:** Scripture files in staging must contain zero commentary markers. The check scans for:
- Footnote reference patterns (e.g., superscript numbers, `[fn:*]` markers, `*` footnote delimiters)
- Any text block that does not parse as a verse (chapter heading, verse number, or verse text)
- Cross-reference prose inline with verse text

**Check:** `pipeline/validate/check_purity.py`

**Fail behavior:** File is flagged. Contaminated spans are logged with line numbers. File is not promoted.

**Rationale:** This is the single most important invariant. A scripture file with embedded commentary is a canonical corruption.

**Risks:** False positives if the parser includes legitimate verse-internal punctuation as footnote markers. Tuning required per source document.

**Rollback:** No impact on canon. Adjust extraction rules and re-parse.

**Owner:** Ark

---

### V3 — Anchor Integrity

**Decision:** Every verse in a scripture file must have a well-formed anchor matching the pattern `BOOK.CHAPTER:VERSE`. Book code must be in the ratified 76-book registry. Chapter and verse numbers must be sequential and complete (no gaps, no duplicates).

**Check:** `pipeline/validate/check_anchors.py`

**Fail behavior:** Missing anchors, gaps, or duplicates produce a report listing the offending lines. File is not promoted.

**Rationale:** Downstream linking is entirely dependent on anchors being present, unique, and complete. A broken anchor silently breaks every reference to it.

**Risks:** The OSB may have non-standard versification for some books (especially Psalms, Esther, Daniel). These must be handled explicitly, not assumed.

**Rollback:** Fix the parse extraction and re-run. Canon is untouched.

**Owner:** Ark

---

### V4 — Completeness Check

**Decision:** Before any promotion batch is approved, verify that the set of books present in `staging/validated/` matches the expected book list for the batch. Individual book checks (V1–V3) do not substitute for this set-level check.

**Check:** `pipeline/validate/check_completeness.py`

**Fail behavior:** Missing books are listed. Promotion is blocked until resolved.

**Rationale:** Partial imports can create a misleading sense of completeness and break searches or linkage that assumes full corpus presence.

**Rollback:** N/A — this check is purely additive; it blocks promotion, it does not modify anything.

**Owner:** Ark

---

## Stage 2 Checks (Staging Validated → Canon Promotion)

These run at promotion time, just before the promote script makes a git commit.

### V5 — Provenance Seal

**Decision:** At promotion, the promote script computes a SHA-256 checksum of the verse text body (excluding frontmatter) and writes it to the `checksum:` frontmatter field. This checksum is included in the git commit.

**Rationale:** Any future unauthorized modification to a canon file will cause checksum mismatch. This is detectable by re-running V5 at any time.

**Rollback:** If a canon file's checksum does not match, a `git log` will reveal when the mismatch was introduced. Revert to the last clean commit.

**Owner:** Ark (script) + Human (periodic integrity spot-checks)

---

### V6 — Notes Anchor Back-Reference Validation

**Decision:** All canon anchor references in notes/articles files must resolve to an existing anchor in a promoted canon file. No dangling references allowed in promoted notes.

**Check:** `pipeline/validate/check_anchors.py` (back-reference mode)

**Fail behavior:** Dangling references are listed. Notes file is not promoted.

**Rationale:** A note referencing a non-existent anchor is a broken link that is invisible to human readers but corrupts the graph.

**Owner:** Ark

---

## Scale Path — Phase 2+ Additions

As the corpus grows beyond the OSB substrate, these checks are added:

| Check | When Added | Purpose |
|-------|-----------|---------|
| V7 — Semantic Duplicate Detection | Phase 2 | Flag verses/passages with near-identical text that may represent unintentional duplication |
| V8 — Patristic Attribution Validation | Phase 2 | Ensure patristic quotes carry source metadata (author, work, section) |
| V9 — Cross-Text Link Graph Integrity | Phase 3 | Full graph traversal — every link in the corpus resolves; no orphaned nodes |
| V10 — Canon Lock Enforcement | Phase 2 | After canon is declared stable, any modification requires an explicit unlock commit with justification |
| V11 — Diff Audit | Ongoing | Every promotion commit generates a human-readable diff summary in `reports/` |

---

## Validation Report Format

Every validation run produces a dated report at `reports/YYYY-MM-DD_HHMM_validation.md`:

```
# Validation Report — 2026-03-06 17:00
Stage: staging/raw → staging/validated
Books processed: 5 (GEN, EXO, LEV, NUM, DEU)

## V1 Schema: PASS (5/5)
## V2 Purity: FAIL
  - GEN.md line 142: suspected footnote marker '^3' inline with verse text
  - GEN.md line 891: commentary-length span detected (>200 chars, no verse number)

## V3 Anchors: PASS (5/5)
## V4 Completeness: N/A (partial batch)

## Action Required:
  - Inspect GEN.md lines 142, 891 and adjust extraction rules.
  - Re-run parse for GEN only, then re-validate.
```

Reports are committed to `reports/` for audit trail.

**Owner:** Ark (automated) + Human (reads and responds to action items)
