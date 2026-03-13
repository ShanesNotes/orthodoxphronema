# Memo 71 — OT Closeout Overnight Dispatch

**Author:** Cowork
**Type:** operational dispatch
**Status:** superseded
**Workstream:** ot-closeout
**Phase:** 1
**Supersedes:** none
**Superseded by:** 72

## Context

Human is going offline. Four OT holdouts remain: PRO, SIR, JOB, PSA. This memo dispatches overnight work to Ezra and Photius so that when Human returns, the promotion queue is as close to ratification-ready as possible.

## Ezra Tasks (Long-Horizon, Autonomous)

### Task 1: PRO Residual Ratification Packet

**Goal:** Package PRO for human residual ratification so it can promote immediately after sign-off.

**Current state:**
- Status: `editorially_clean`, decision: `dry-run`
- V1-V9 PASS (V7 WARN is non-blocking)
- 0 editorial candidates
- 130 unratified residuals — all classified `docling_issue` ("Verse not captured by Docling extraction")
- Known major gap: PRO.31 (entire chapter, 31 verses — the virtuous wife acrostic)

**Steps:**
1. Read `staging/validated/OT/PRO_residuals.json` — group residuals by chapter and classify the gap pattern (scattered vs. contiguous).
2. Spot-check 3-5 representative missing verses against the OSB PDF using `pdftotext` to confirm they are genuine Docling extraction failures, not content errors.
3. Assess PRO.31 specifically — is the entire chapter absent from PRO.md, or partially present? If absent, note whether `pdftotext` recovery is feasible or if this is a deferred gap.
4. Draft a ratification packet memo section for PRO that presents:
   - Total residual count and classification
   - Evidence of spot-check verification
   - Recommendation: ratify as accepted extraction gaps (non-blocking) or flag specific verses for recovery attempt
   - Clear yes/no ask for Human
5. Run `python3 pipeline/validate/batch_validate.py staging/validated/OT/PRO.md` to confirm current validation state.

### Task 2: SIR Residual Ratification Packet

**Goal:** Same as PRO — package SIR for human ratification.

**Current state:**
- Status: `editorially_clean`, decision: `dry-run`
- V1-V6 PASS, V7 WARN, V8-V9 PASS
- 0 editorial candidates
- 63 unratified residuals — all `docling_issue`, mostly chapter-opening verses (drop-cap losses)

**Steps:**
1. Read `staging/validated/OT/SIR_residuals.json` — group by chapter, identify the drop-cap pattern.
2. Spot-check 3-5 chapter-opening verses against OSB PDF to confirm drop-cap loss classification.
3. Draft ratification packet section for SIR.
4. Run validation to confirm current state.

### Task 3: JOB Editorial Candidate Resolution + Residual Triage

**Goal:** Resolve the 4 editorial candidates blocking JOB's promotion readiness, then prepare residual packet.

**Current state:**
- Status: `structurally_passable`, decision: `dry-run`
- V4 WARN, V7 WARN
- 4 editorial candidates (chapter-open drop-caps):
  - JOB.1:1 — token `here`, confidence 0.7 (ambiguous)
  - JOB.2:1 — token `hen`, confidence 0.7, replacement suggested: "Then again as it so happened..."
  - JOB.3:1 — token `fter`, confidence 0.95, replacement: "After this, Job opened his mouth"
  - JOB.12:1 — token `ut`, confidence 0.95, replacement: "But Job answered and said:"
- 43 unratified residuals

**Steps:**
1. For the two high-confidence candidates (JOB.3:1 at 0.95, JOB.12:1 at 0.95): verify the suggested replacements against OSB PDF using `pdftotext`. If confirmed, apply the fix to `staging/validated/OT/JOB.md` and update `JOB_editorial_candidates.json` status to `resolved`.
2. For the two lower-confidence candidates (JOB.1:1 at 0.7, JOB.2:1 at 0.7): verify against OSB PDF. If the correct text is recoverable, apply. If ambiguous, leave as `pending` and flag for Human.
3. Re-run validation after any edits.
4. Group the 43 residuals by pattern and draft ratification section.
5. Regenerate the promotion dossier for JOB if editorial candidates were resolved.

### Task 4: Consolidated Ratification Ask

**Goal:** Combine PRO, SIR, and JOB findings into a single ratification memo (or append to this one) so Human can review and sign off on all three at once.

**Deliverable:** A clear decision table:
| Book | Residuals | Pattern | Recommendation | Human action needed |
|---|---|---|---|---|
| PRO | 130 | Docling gaps + PRO.31 total loss | Ratify as accepted gaps | Yes/No |
| SIR | 63 | Drop-cap chapter openers | Ratify as accepted gaps | Yes/No |
| JOB | 43 + 0-4 editorial | Drop-cap + scattered | Ratify after editorial resolution | Yes/No |

## Photius Tasks (Text Processing, Non-Reasoning)

### Task: PSA V4 Warning Investigation

**Goal:** Identify what's causing the V4 validation warning on PSA so it can be addressed.

**Current state:**
- Status: `editorially_clean` but decision: `blocked`
- V4 WARN (verse completeness or sequence issue)
- 0 editorial candidates, 0 residuals
- Custom extractor (`psa_extract.py`) produced 151 chapters, 2473 verses

**Steps:**
1. Run `python3 pipeline/validate/batch_validate.py staging/validated/OT/PSA.md` and capture the V4 warning details.
2. Identify which verses or chapters are triggering the warning.
3. Classify the failures: missing verses, sequence gaps, title absorption, or numbering issues.
4. If the fix is a text-level cleanup (split-word, heading removal, anchor normalization) — apply it.
5. If the fix requires parser changes or architectural decisions — document findings and hand off to Ark.
6. Write a brief run report to `memos/` with findings and completion handshake.

**Note:** PSA uses LXX numbering (Psalms 1-151). V4 warnings may relate to the LXX/MT numbering divergence. Check whether the validator is expecting MT numbering and flagging LXX-specific verses as gaps.

## Priority Order

1. **Ezra: PRO packet** (closest to promotion, smallest decision surface)
2. **Ezra: SIR packet** (same pattern as PRO, can batch)
3. **Ezra: JOB editorial resolution** (requires PDF verification, highest effort)
4. **Photius: PSA V4 investigation** (diagnostic, may surface structural work)

## Completion

When done, update `memos/ezra_ops_board.md` with results and mark this memo's status as `closed` with a completion handshake block.
