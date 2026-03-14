# CLAUDE.md Optimization Report — Orthodox Phronema Archive

**Date:** 2026-03-14
**Prepared for:** Shane (ShanesNotes)
**Scope:** Review current CLAUDE.md harness and recommend structural + ecosystem optimizations

---

## Executive Summary

Your current CLAUDE.md is functional but undersized at 34 lines — it's essentially a stub that points to ARK_BRIEFING_PACKET.md (88 lines) and AGENTS.md (414 lines). The problem is that **Claude Code loads CLAUDE.md directly into context but doesn't automatically chase file references** unless you use the `@` import syntax or the `.claude/rules/` directory. This means your agents are likely re-reading 500+ lines of briefing material every session from disk reads rather than having it primed automatically.

Meanwhile, several high-leverage features of the Claude Code harness are completely unused: `.claudeignore`, `settings.json` (you only have `settings.local.json`), `.claude/rules/` (empty directory exists), hooks, and skills.

The recommendations below are ordered by impact-to-effort ratio.

---

## 1. Current State Audit

### What You Have

| File | Lines | Role | Auto-loaded? |
|------|-------|------|-------------|
| `CLAUDE.md` | 34 | Entry point, identity, session protocol | Yes |
| `ARK_BRIEFING_PACKET.md` | 88 | Mission, non-negotiables, architecture | No — must be read manually |
| `AGENTS.md` | 414 | Multi-agent protocol, ownership, workflows | No — must be read manually |
| `.claude/settings.local.json` | ~35 | Permissions (allow-list only) | Yes |
| `.claude/rules/` | empty | Path-scoped rules | Yes (but nothing in it) |
| `.claude/status.sh` | 1 | Status bar script | Utility only |
| `.claudeignore` | missing | Context exclusion | N/A |

### What's Missing

- **`.claude/settings.json`** — project-level settings (committable, shared across agents)
- **`.claudeignore`** — context window is being polluted with PDFs, src.texts, staging raw files
- **`.claude/rules/*.md`** — path-scoped rules for different pipeline stages
- **Hooks** — no pre/post validation automation
- **Skills** — no custom slash commands for your pipeline operations
- **@ imports** — CLAUDE.md doesn't pull in briefing packet or agents protocol

---

## 2. Critical Fixes (Do These First)

### 2a. Add `.claudeignore`

Your repo has massive directories that waste context tokens. Create this immediately:

```
# Source PDFs — never need to be in context
src.texts/
*.pdf

# Raw staging — only validated matters
staging/raw/

# Build artifacts
*.pyc
__pycache__/
.pytest_cache/
node_modules/

# Large generated reports (read explicitly when needed)
reports/*.json

# Git internals
.git/

# Memos archive (historical, read explicitly)
memos/archive/
```

**Impact:** Reduces context consumption significantly. Your `src.texts/` directory alone contains dozens of subdirectories with README files that get indexed unnecessarily.

### 2b. Restructure CLAUDE.md with @ Imports

The key insight: Claude Code supports `@path/to/file.md` imports that get pulled into context automatically. Your current CLAUDE.md says "read ARK_BRIEFING_PACKET.md" but that requires a manual Read tool call every session.

**Proposed new CLAUDE.md structure:**

```markdown
# ARK SYSTEM DIRECTIVES

You are Ark — planning/architecture lead for the Orthodox Phronema Archive.
Repo: /home/ark/orthodoxphronema
Hardware: Full Linux access, RTX 4060 Ti 8GB, passwordless sudo.

## Mission & Architecture
@ARK_BRIEFING_PACKET.md

## Agent Protocol & Ownership
@AGENTS.md

## Session Protocol
- Confirm you have loaded the briefing packet and agent protocol above.
- For substantial changes: write/update a memo in `memos/` BEFORE implementing.
- Before promoting any book: confirm Ezra audit recorded or explicitly waived.
- Before widening parser allowlists on V4 books under 100 missing anchors:
  run `python3 pipeline/validate/pdf_edge_case_check.py staging/validated/{OT,NT}/BOOK.md`
- Use plan mode for multi-step changes with non-trivial rollback risk.
- When ambiguous: open as "Open Questions" in the relevant memo.

## IMPORTANT Directives
- YOU MUST use one-verse-per-line in canon/.
- YOU MUST check for study-article leakage before promotion.
- YOU MUST reference AGENTS.md for ownership boundaries.
- Never bypass Ezra audit for canon promotion.
- Prefer /compact when context > 60%.
```

**Key changes:**
- `@` imports auto-load the briefing packet and agents protocol
- `IMPORTANT` and `YOU MUST` markers increase adherence (documented best practice)
- Concise — under 30 lines of direct content, with imports handling the rest

### 2c. Create `.claude/settings.json`

Move from `settings.local.json` (user-only) to a proper project `settings.json` that all agents share:

```json
{
  "permissions": {
    "deny": [
      "Bash(rm -rf /home/ark/orthodoxphronema/canon/*)"
    ],
    "allow": [
      "Bash(python3:*)",
      "Bash(git:*)",
      "Bash(jq:*)",
      "Bash(wc:*)",
      "Bash(ls:*)",
      "Bash(grep:*)",
      "Read(/home/ark/**)"
    ]
  }
}
```

---

## 3. High-Impact Additions

### 3a. Path-Scoped Rules in `.claude/rules/`

These fire automatically when Claude touches files matching the glob pattern. This is where your validation contracts and ownership boundaries become *enforced* rather than merely documented.

**`.claude/rules/canon-protection.md`**
```yaml
---
paths: canon/**/*.md
---
IMPORTANT: Canon files are immutable post-promotion.
- Never modify canon files without explicit Human + Ark approval.
- Verify Ezra audit is complete before any promotion write.
- One-verse-per-line format is mandatory.
- Study article text must NEVER appear in canon scripture files.
- Footnote markers are stripped from canon and indexed separately.
```

**`.claude/rules/staging-validated.md`**
```yaml
---
paths: staging/validated/**/*.md
---
Before modifying validated books:
- Check anchor integrity (V1 uniqueness).
- Verify chapter count (V2) and sequence (V3).
- Confirm no article bleed (V5).
- Evidence-package all fixes: source page ref, affected anchors, validator before/after, rationale.
- Photius has bounded write access here; Ark has full access.
```

**`.claude/rules/pipeline-core.md`**
```yaml
---
paths: pipeline/**/*.py
---
Pipeline code is Ark-owned. Changes require:
- A memo in memos/ documenting the rationale.
- Validation run before and after.
- Batch tools (5+ books) require architecture review.
Preferred parser: Docling for scripture, pdftotext for notes/footnotes.
```

**`.claude/rules/memos.md`**
```yaml
---
paths: memos/*.md
---
Memos are durable evidence artifacts. Every substantial memo must include:
- Files changed
- Verification run
- Artifacts refreshed (or explicitly deferred with named stale surface)
- Remaining known drift
- Next owner
Use template: memos/_template_work_memo.md
```

### 3b. Hooks for Automated Validation

Add to `.claude/settings.json`:

```json
{
  "hooks": [
    {
      "event": "PreToolUse",
      "type": "command",
      "matcher": "Edit|Write",
      "command": "bash .claude/hooks/pre-edit-guard.sh \"$TOOL_INPUT_FILE\"",
      "timeout": 10
    },
    {
      "event": "PostToolUse",
      "type": "command",
      "matcher": "Edit|Write",
      "command": "bash .claude/hooks/post-edit-validate.sh \"$TOOL_INPUT_FILE\"",
      "timeout": 30
    }
  ]
}
```

**`.claude/hooks/pre-edit-guard.sh`** (blocks edits to canon without confirmation):
```bash
#!/bin/bash
FILE="$1"
if [[ "$FILE" == *"/canon/"* ]]; then
  echo "BLOCKED: Attempted edit to canon file: $FILE"
  echo "Canon files require explicit Human + Ark promotion approval."
  exit 2  # Exit code 2 = block the operation
fi
exit 0
```

**`.claude/hooks/post-edit-validate.sh`** (runs validation after staging edits):
```bash
#!/bin/bash
FILE="$1"
if [[ "$FILE" == *"/staging/validated/"* && "$FILE" == *.md ]]; then
  BOOK=$(basename "$FILE" .md)
  echo "Running validation on $BOOK..."
  python3 pipeline/validate/run_validators.py "$FILE" --quick 2>&1 | tail -5
fi
exit 0
```

### 3c. Custom Skills for Pipeline Operations

Create project-specific skills that become slash commands:

**`.claude/skills/validate-book/SKILL.md`**
```yaml
---
name: validate-book
description: Run the full validation suite on a staged book. Use when checking a book's readiness for promotion or after cleanup work.
---

To validate a book:
1. Identify the book file at staging/validated/{OT,NT}/BOOK.md
2. Run: python3 pipeline/validate/run_validators.py staging/validated/{OT,NT}/BOOK.md
3. Check all 8 validators: V1 (anchors), V2 (chapter count), V3 (chapter sequence), V4 (verse gaps), V5 (article bleed), V6 (frontmatter), V7 (completeness), V8 (heading integrity)
4. Report results with pass/fail per validator
5. If V4 gaps remain high, recommend parser work before cleanup
6. If V4 missing anchors <= 100, recommend PDF spot-check over allowlist widening
```

**`.claude/skills/promote-book/SKILL.md`**
```yaml
---
name: promote-book
description: Execute the promotion gate for a validated book. Use after Ezra audit and Human ratification.
---

Promotion checklist (ALL required):
1. Confirm Ark implementation complete
2. Confirm validation run recorded (check reports/)
3. Confirm Ezra audit complete or explicitly waived (check memos/ezra-audit-log.md)
4. Confirm Human ratification of ambiguous cases
5. Execute promotion from the SAME staged file that was validated
6. Refresh affected dossier and dashboard after promotion
7. Write completion memo with: files changed, verification run, artifacts refreshed, remaining drift, next owner
```

**`.claude/skills/cleanup-report/SKILL.md`**
```yaml
---
name: cleanup-report
description: Generate a cleanup report for a book after stabilization work. Use after Photius recovery or editorial fixes.
---

Generate report following the pattern in memos/archive/phase2_cleanup_reports/:
1. Read the staged book file
2. Run validators and capture before/after
3. Document all fixes applied with evidence
4. List remaining issues by category
5. State whether dossier/dashboard were refreshed
6. Name the next owner and recommended action
```

---

## 4. Open-Source Ecosystem Opportunities

Based on deep research, these external resources are directly relevant to your project:

### 4a. Production-Ready Skill Libraries

**Anthropic Official Skills** — `github.com/anthropics/skills`
Your Cowork environment already has the core skills (docx, pdf, xlsx, pptx). But for Claude Code sessions (Ark, Ezra, Photius), you could install additional skills for structured document processing.

**levnikolaevich/claude-code-skills** — Full delivery workflow skills including research, planning, implementation, testing, code review, and quality gates. The quality gate skill pattern maps well to your promotion gate.

**sickn33/antigravity-awesome-skills** — 1000+ agentic skills. Look specifically at validation, document processing, and batch operations skills.

### 4b. MCP Servers Worth Investigating

For your text processing pipeline:

- **Filesystem MCP** — structured file operations with validation
- **Git MCP** — programmatic git operations (could enforce commit message standards)
- **SQLite MCP** — if you ever want to query your anchor_registry or dashboard data via SQL instead of JSON
- **Custom validation MCP** — wrap your Python validators as an MCP server so they're available as tools

### 4c. Agent Orchestration Frameworks

**ruflo** (`github.com/ruvnet/ruflo`) — Multi-agent orchestration platform. Relevant because you already have a multi-agent setup (Ark/Ezra/Photius/Cowork) but coordinate via memos. Ruflo could formalize the handoff protocol.

**claude-pipeline** (`github.com/aaddrick/claude-pipeline`) — Multi-agent pipeline with built-in quality gates. Their gate pattern (Analysis → Planning → Generation → Audit → Healing → Documentation) maps directly to your parse → cleanup → validate → audit → ratify → promote workflow.

### 4d. Community CLAUDE.md Patterns

**claude-code-showcase** (`github.com/ChrisWiles/claude-code-showcase`) — The most comprehensive real-world example of hooks + skills + agents + commands working together. Worth studying for your settings.json structure.

**claude-code-ultimate-guide** (`github.com/FlorianBruniaux/claude-code-ultimate-guide`) — Production templates and agentic workflow guides.

---

## 5. Proposed Final Directory Structure

```
.claude/
├── settings.json            # Shared project settings (hooks, permissions, MCP)
├── settings.local.json      # Your existing personal permissions
├── rules/
│   ├── canon-protection.md  # Auto-enforced on canon/** edits
│   ├── staging-validated.md # Auto-enforced on staging/validated/** edits
│   ├── pipeline-core.md     # Auto-enforced on pipeline/** edits
│   └── memos.md             # Auto-enforced on memos/** writes
├── skills/
│   ├── validate-book/
│   │   └── SKILL.md         # /validate-book slash command
│   ├── promote-book/
│   │   └── SKILL.md         # /promote-book slash command
│   └── cleanup-report/
│       └── SKILL.md         # /cleanup-report slash command
├── hooks/
│   ├── pre-edit-guard.sh    # Blocks unauthorized canon edits
│   └── post-edit-validate.sh # Auto-validates after staging edits
├── status.sh                # Existing status script
└── worktrees/               # Existing worktree config

CLAUDE.md                    # Restructured with @ imports (~25 lines + imported content)
ARK_BRIEFING_PACKET.md       # Unchanged (auto-imported)
AGENTS.md                    # Unchanged (auto-imported)
.claudeignore                # NEW: excludes src.texts/, staging/raw/, archives
```

---

## 6. Priority Implementation Order

1. **Create `.claudeignore`** — 5 min, immediate context savings
2. **Restructure `CLAUDE.md` with @ imports** — 10 min, eliminates manual reads
3. **Populate `.claude/rules/`** — 20 min, auto-enforces your validation contracts
4. **Create `.claude/settings.json`** with hooks — 15 min, automated safety gates
5. **Create pipeline skills** — 30 min, standardizes slash commands
6. **Explore external frameworks** — ongoing research, adopt incrementally

---

## Sources

- Anthropic Official Docs: docs.anthropic.com/en/docs/claude-code/
- Claude Code Memory System: docs.anthropic.com/en/docs/claude-code/memory
- Claude Code Best Practices: code.claude.com/docs/en/best-practices
- Anthropic Skills Repo: github.com/anthropics/skills
- awesome-claude-code: github.com/hesreallyhim/awesome-claude-code
- claude-code-showcase: github.com/ChrisWiles/claude-code-showcase
- claude-code-ultimate-guide: github.com/FlorianBruniaux/claude-code-ultimate-guide
- claude-pipeline: github.com/aaddrick/claude-pipeline
- ruflo orchestration: github.com/ruvnet/ruflo
