---
name: canon-validator
description: >
  Full V1-V12 validation suite, purity audit, and coordination surface checks.
  Use after any proofreading or correction pass, before canon promotion, when
  the user asks to: validate a book, check for regressions, verify canon
  integrity, run the validation suite, check promotion readiness, or audit a
  book. Also trigger for "did we break anything", "regression check",
  "pre-promotion check", or "validation gate".
allowed-tools: "Bash(python3:*) Read Grep Glob"
metadata:
  author: Orthodox Phronema Archive
  version: 2.0.0
  category: validation
  delegates-to: skills/canon-validator
---

# Canon Validator — Bridge Skill

This is a Claude Code discovery bridge. The full implementation lives at `skills/canon-validator/`.

**Before doing any work**, read the canonical SKILL.md:
```
Read skills/canon-validator/SKILL.md
```

Key entry points:
- `pipeline/validate/validate_canon.py` — V1-V12 master validation
- `pipeline/validate/purity_audit.py` — OCR residue and leakage audit
- `pipeline/validate/check_coordination_surfaces.py` — cross-book consistency
- `pipeline/validate/pdf_edge_case_check.py` — V4 edge cases
- `pipeline/tools/batch_validate.py` — batch runner
