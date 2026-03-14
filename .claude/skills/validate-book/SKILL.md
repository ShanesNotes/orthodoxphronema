---
name: validate-book
description: Run the full V1-V8 validation suite on a staged scripture book and report pass/fail per validator. Use when checking a book's readiness for promotion, after cleanup work, or when someone asks to "validate", "check", or "run validators on" a book. Do NOT use for canon files (those are already promoted) or for raw/unstaged files.
allowed-tools: "Bash(python3:*) Read Grep"
metadata:
  author: Orthodox Phronema Archive
  version: 1.0.0
  category: validation
---

# Validate Book

## Instructions

### Step 1: Identify the Book
Determine the book code (SBL-standard UPPERCASE, e.g., GEN, EXO, PSA) and locate the staged file:
- OT books: `staging/validated/OT/BOOK.md`
- NT books: `staging/validated/NT/BOOK.md`

If the file does not exist, stop and report — the book may not have been extracted yet.

### Step 2: Run Full Validation Suite
```bash
python3 pipeline/validate/run_validators.py staging/validated/{OT,NT}/BOOK.md
```

If `run_validators.py` does not exist or fails, fall back to running individual validators:
```bash
python3 pipeline/validate/pdf_edge_case_check.py staging/validated/{OT,NT}/BOOK.md
```

### Step 3: Interpret Results
Report each validator with pass/fail status:

| Validator | Check | Status |
|-----------|-------|--------|
| V1 | Anchor uniqueness | ? |
| V2 | Chapter count | ? |
| V3 | Chapter sequence | ? |
| V4 | Verse sequence / gap detection | ? |
| V5 | Article bleed | ? |
| V6 | Frontmatter | ? |
| V7 | Completeness | ? |
| V8 | Heading integrity | ? |

### Step 4: Recommend Next Action
- All pass → Ready for Ezra audit and promotion
- V4 gaps high (>100 missing) → Return to parser work before cleanup
- V4 gaps small (<=100) → Recommend PDF spot-check over allowlist widening
- V5 fail → Article bleed detected, route to cleanup
- Any structural fail (V1-V3) → Route to Ark for pipeline investigation

## Common Issues
- If V4 reports missing anchors, check for lowercase-start verses (parser issue, not cleanup)
- If V5 reports bleed, check for study article headers embedded in scripture
- If V8 fails, check for heading text appearing mid-verse
