---
paths:
  - skills/**
---

## Project Skills — Executable Toolkits

The `skills/` directory contains project-specific skills with executable scripts, profiles, and reference data.

Current skills:
- `text-cleaner/` — corpus-agnostic OCR/extraction cleanup (P1-P8, D1-D6, F1-F4)
- `canon-proofreader/` — thin wrapper delegating to text-cleaner with --profile canon
- `canon-validator/` — V1-V12 validation suite, purity audit, coordination checks
- `canon-spell-audit/` — detection-only aspell audit with biblical names allowlist

These are bridged into `.claude/skills/` for Claude Code native discovery. The bridge skills contain frontmatter for triggering and a pointer back here.

Rules:
- Scripts here are Ark-owned; structural changes require Ark review
- Profile YAML files (in text-cleaner/profiles/) configure per-corpus behavior
- The `references/` subdirectories contain domain knowledge (error patterns, allowlists)
- CORPUS_CONTRACT.md defines the onboarding protocol for new text sources
- All scripts expect to be run from the repo root: `python3 skills/text-cleaner/scripts/clean.py`
