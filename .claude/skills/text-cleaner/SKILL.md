---
name: text-cleaner
description: >
  General-purpose OCR/extraction artifact cleanup toolkit. Fixes fused words,
  split words, punctuation spacing, doubled text, footnote marker residue, and
  spelling errors across any corpus type (scripture, patristic, liturgical, etc.).
  Use when the user mentions: cleaning extracted text, fixing OCR errors, post-extraction
  cleanup, corpus cleanup, "swiss cheese errors", "fused words", "split words", or
  text-quality improvement. Do NOT use for validation-only (use canon-validator) or
  spelling-only audit (use canon-spell-audit).
allowed-tools: "Bash(python3:*) Read Grep Glob"
metadata:
  author: Orthodox Phronema Archive
  version: 2.0.0
  category: cleanup
  delegates-to: skills/text-cleaner
---

# Text Cleaner — Bridge Skill

This is a Claude Code discovery bridge. The full implementation lives at `skills/text-cleaner/`.

**Before doing any work**, read the canonical SKILL.md:
```
Read skills/text-cleaner/SKILL.md
```

Key references in that directory:
- `CORPUS_CONTRACT.md` — onboarding contract for new text sources
- `scripts/clean.py` — multi-pass cleaner (P1-P8 + F1-F4)
- `scripts/scan.py` — deep fused-token scanner
- `scripts/fix.py` — curated fused-token fixer
- `scripts/manifest.py` — batch manifest generator
- `profiles/` — corpus-specific YAML configs (canon, footnotes, patristic, staging, default)
- `references/error_patterns.md` — detailed error category examples
