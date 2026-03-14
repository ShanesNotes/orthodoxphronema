---
name: canon-proofreader
description: >
  Convenience wrapper for proofreading canon scripture files. Delegates to
  text-cleaner with --profile canon. Use when the user mentions: proofreading
  canon, fixing scripture errors, correcting text in canon/, running a correction
  pass, or text-quality improvement on biblical scripture. For footnote/article
  cleanup, use text-cleaner directly with --profile footnotes.
allowed-tools: "Bash(python3:*) Read Grep Glob"
metadata:
  author: Orthodox Phronema Archive
  version: 2.0.0
  category: cleanup
  delegates-to: skills/canon-proofreader
---

# Canon Proofreader — Bridge Skill

This is a Claude Code discovery bridge. The full implementation lives at `skills/canon-proofreader/`.

**Before doing any work**, read the canonical SKILL.md:
```
Read skills/canon-proofreader/SKILL.md
```

This skill is a **thin wrapper** around `text-cleaner` with `--profile canon`.
New work should use text-cleaner directly. See `skills/text-cleaner/SKILL.md`.
