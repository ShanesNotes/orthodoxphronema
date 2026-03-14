---
name: canon-spell-audit
description: >
  Detection-only spelling audit for canon and staging files. Wraps
  pipeline/tools/spell_audit.py with the biblical names allowlist. Use when the
  user wants to: check spelling in a specific book, audit spelling across the
  corpus, build or update the allowlist, or investigate flagged words. Also
  trigger for "spell check", "unknown words", "aspell audit". This is read-only
  and never modifies files.
allowed-tools: "Bash(python3:*) Read Grep Glob"
metadata:
  author: Orthodox Phronema Archive
  version: 1.0.0
  category: audit
  delegates-to: skills/canon-spell-audit
---

# Canon Spell Audit — Bridge Skill

This is a Claude Code discovery bridge. The full implementation lives at `skills/canon-spell-audit/`.

**Before doing any work**, read the canonical SKILL.md:
```
Read skills/canon-spell-audit/SKILL.md
```

Key entry point: `pipeline/tools/spell_audit.py`
Allowlist: `schemas/biblical_names.txt`
