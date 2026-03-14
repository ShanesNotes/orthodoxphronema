---
name: refresh-dossier
description: Regenerate the promotion dossier and book status dashboard after staged scripture changes. Use after cleanup work, recovery sessions, or whenever someone asks to "refresh the dossier", "update the dashboard", or "regenerate reports". Do NOT use for validation (use validate-book) or promotion (use promote-book).
allowed-tools: "Bash(python3:*) Read Grep Write"
metadata:
  author: Orthodox Phronema Archive
  version: 1.0.0
  category: reporting
---

# Refresh Dossier & Dashboard

## Instructions

### Step 1: Identify Stale Surfaces
Check what changed since last refresh:
```bash
git log --oneline -10 -- staging/validated/ reports/
```

Identify which books have changed staged state since their last dossier generation.

### Step 2: Regenerate Book Dossier
For each affected book, regenerate the promotion dossier:
```bash
python3 pipeline/metadata/generate_dossier.py staging/validated/{OT,NT}/BOOK.md
```

If the dossier generator doesn't exist, manually compile:
- Current validation status (run validate-book)
- Ezra audit status (check memos/ezra-audit-log.md)
- Known residual issues
- Promotion readiness assessment

### Step 3: Refresh Dashboard
Regenerate the machine-readable book status:
```bash
python3 pipeline/metadata/refresh_dashboard.py
```

This updates `reports/book_status_dashboard.json`.

### Step 4: Document the Refresh
Update the relevant memo or create a note confirming:
- Which dossiers were refreshed
- Which dashboard entries changed
- Any surfaces intentionally left stale (with reason)

## IMPORTANT
- If a refresh is intentionally deferred, you MUST name the stale surface explicitly
- Use precise vocabulary: "stale dossier", "stale dashboard", "stale memo"
- After refresh, Ezra's ops board should be updated to reflect new state
