---
name: promote-book
description: Execute the full promotion gate for a validated scripture book, including pre-checks, Ezra audit verification, and promotion. Use when someone asks to "promote", "ship to canon", or "finalize" a book. Do NOT use for validation-only checks (use validate-book instead) or for books that haven't passed validation.
allowed-tools: "Bash(python3:*) Bash(git:*) Read Grep"
metadata:
  author: Orthodox Phronema Archive
  version: 1.0.0
  category: promotion
---

# Promote Book

## CRITICAL — This is a canon-affecting operation. All 5 gates must pass.

## Instructions

### Gate 1: Ark Implementation Complete
Verify the staged book at `staging/validated/{OT,NT}/BOOK.md` exists and has been through the full cleanup cycle.

### Gate 2: Validation Run Recorded
Run or confirm recent validation results:
```bash
python3 pipeline/validate/run_validators.py staging/validated/{OT,NT}/BOOK.md
```
All V1-V8 must pass. Partial pass = fail. Do not proceed.

### Gate 3: Ezra Audit
Check `memos/ezra-audit-log.md` for a recorded audit of this book.
- If audit exists and passes: proceed
- If audit exists with blocking findings: stop and report
- If no audit exists: stop and request Ezra audit or explicit Human waiver

### Gate 4: Human Ratification
If there are ANY ambiguous source cases flagged during audit, these must be Human-ratified.
Check the memo for Human sign-off on open questions.

### Gate 5: Promotion Execution
IMPORTANT: Promote from the SAME staged file that was validated and audited. Do not re-extract.

```bash
python3 pipeline/promote/promote_book.py staging/validated/{OT,NT}/BOOK.md
```

### Post-Promotion Checklist
After successful promotion:
1. Refresh the promotion dossier for this book (or explicitly defer and name the stale surface)
2. Refresh `reports/book_status_dashboard.json` (or explicitly defer)
3. Write a completion memo with: files changed, verification run, artifacts refreshed, remaining drift, next owner
4. Update `memos/ezra_ops_board.md` with the promotion completion

## Error Handling
- If promote script fails: do NOT retry without investigating. Check git status and staged file integrity.
- If validation regresses after promotion: this is a critical incident. Stop and alert Human.
