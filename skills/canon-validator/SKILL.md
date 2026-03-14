---
name: canon-validator
description: >
  Post-correction validation skill for Orthodox Phronema Archive files. Runs the
  full V1-V12 validation suite, purity audit, and coordination surface checks
  to verify that corrections haven't introduced regressions. Use this skill after
  any proofreading or correction pass, before canon promotion, or when the user
  asks to: validate a book, check for regressions, verify canon integrity, run
  the validation suite, check promotion readiness, or audit a book. Also trigger
  for "did we break anything", "regression check", "pre-promotion check", or
  "validation gate".
---

# Canon Validator

Runs the full validation pipeline to verify file integrity after corrections.
This is the "did we break anything?" safety net.

## When to Use

- After running `canon-proofreader` to apply corrections
- Before promoting a book from staging to canon
- After any manual edits to canon or staging files
- As part of the Ezra audit workflow

## Validation Suite

### V1-V12 Checks (validate_canon.py)

The master validation script runs 12 checks:

| Check | Description |
|-------|-------------|
| V1 | Anchor uniqueness — no duplicate BOOK.CH:VS anchors |
| V2 | Chapter count — correct number for the book |
| V3 | Chapter sequence — sequential with no gaps |
| V4 | Verse sequence — monotonically increasing within chapters |
| V5 | No article bleed — study article text must not appear in canon |
| V6 | Frontmatter present — required YAML fields exist |
| V7 | Completeness — total anchors match registry verse counts |
| V8 | Heading integrity — no fragment headings |
| V9 | Embedded verse detection |
| V10 | Absorbed content (Brenton cross-reference) |
| V11 | Split-word artifacts (Docling column-split) |
| V12 | Inline verse-number leakage |

```bash
# Single book
python3 pipeline/validate/validate_canon.py canon/OT/01_GEN.md

# Strict mode (all warnings become errors)
python3 pipeline/validate/validate_canon.py canon/OT/01_GEN.md --strict

# Batch validate entire testament
python3 pipeline/tools/batch_validate.py --dir canon/OT
python3 pipeline/tools/batch_validate.py --dir canon/NT
```

### Purity Audit

Checks for residual OCR artifacts, study article leakage, and formatting
inconsistencies:

```bash
python3 pipeline/validate/purity_audit.py canon/OT/01_GEN.md
```

### Coordination Surface Checks

Verifies cross-book consistency (anchor registry alignment, cross-references):

```bash
python3 pipeline/validate/check_coordination_surfaces.py
```

### PDF Edge Case Check

For books with known V4 residual gaps under 100 missing anchors:

```bash
python3 pipeline/validate/pdf_edge_case_check.py staging/validated/OT/BOOK.md
```

## Recommended Workflow

After a proofreading pass:

1. **Run batch validate** on all modified files
   ```bash
   python3 pipeline/tools/batch_validate.py --dir canon/OT
   python3 pipeline/tools/batch_validate.py --dir canon/NT
   ```

2. **Run purity audit** on any book that had corrections applied
   ```bash
   for f in canon/OT/*.md canon/NT/*.md; do
     python3 pipeline/validate/purity_audit.py "$f"
   done
   ```

3. **Check for new V4 gaps** if verse text was modified
   ```bash
   python3 pipeline/validate/validate_canon.py canon/OT/01_GEN.md --strict
   ```

4. **Document results** in a memo for Ezra audit
   ```bash
   # The batch validator outputs a summary; capture it
   python3 pipeline/tools/batch_validate.py --dir canon/OT 2>&1 | \
     tee reports/post_proofread_validation.txt
   ```

## Interpreting Results

- **PASS** — All checks passed, file is ready for promotion
- **WARN** — Non-blocking issues that should be reviewed
- **FAIL** — Blocking issues that must be resolved before promotion

Common post-proofreading warnings:
- V4 verse gaps — usually pre-existing, not caused by proofreading
- V11 split-word residuals — if new ones appear, the proofreader may have
  introduced a regression

## Key Files

- `pipeline/validate/validate_canon.py` — Master validation (V1-V12)
- `pipeline/validate/checks.py` — Individual check functions
- `pipeline/validate/purity_audit.py` — OCR residue and leakage audit
- `pipeline/validate/check_coordination_surfaces.py` — Cross-book consistency
- `pipeline/validate/pdf_edge_case_check.py` — V4 edge cases
- `pipeline/tools/batch_validate.py` — Batch runner
- `schemas/anchor_registry.json` — Ground truth for verse counts
