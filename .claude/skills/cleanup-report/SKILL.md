---
name: cleanup-report
description: Generate a structured cleanup report after stabilization or recovery work on a staged book. Use when Photius completes recovery work, after editorial fixes, or when someone asks for a "cleanup report", "recovery summary", or "stabilization status". Do NOT use for validation-only runs (use validate-book) or promotion (use promote-book).
allowed-tools: "Bash(python3:*) Read Grep Write"
metadata:
  author: Orthodox Phronema Archive
  version: 1.0.0
  category: reporting
---

# Cleanup Report Generator

## Instructions

### Step 1: Identify Scope
Determine which book(s) were worked on and the type of cleanup:
- Structural recovery (verse boundaries, chapter splits)
- Editorial fixes (fused words, OCR artifacts, spacing)
- Article bleed removal
- Footnote marker cleanup

### Step 2: Run Before/After Validation
```bash
# Run validators on the current state
python3 pipeline/validate/run_validators.py staging/validated/{OT,NT}/BOOK.md
```

Compare against the previous validation results if available in `reports/`.

### Step 3: Generate Report
Follow the pattern established in `memos/archive/phase2_cleanup_reports/`.
Note: companion content also exists in `study/articles/` and `study/footnotes/` — check if study layer files need updating alongside staging companions.

```markdown
# BOOK Cleanup Report

## Summary
- Book: [BOOK code]
- Date: [YYYY-MM-DD]
- Agent: [Photius/Ark]
- Type: [structural/editorial/bleed/footnote]

## Changes Applied
[List each fix with evidence]

## Validation Results
| Validator | Before | After |
|-----------|--------|-------|
| V1-V8    | ...    | ...   |

## Remaining Issues
[Categorized list]

## Artifacts
- [ ] Dossier refreshed (or deferred: [reason])
- [ ] Dashboard refreshed (or deferred: [reason])

## Next Owner
[Ark/Ezra/Human + specific action needed]
```

### Step 4: Save Report
Save to `memos/08_BOOK_cleanup_report.md` following existing naming conventions.

## Common Issues
- If before/after comparison unavailable, note this explicitly rather than omitting
- Always include the evidence-package fields even if some are "N/A"
