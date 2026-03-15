---
name: delegate-ezra
description: >
  Delegate tasks to Ezra (Codex 5.4) for strategic audit, validation review,
  risk analysis, delivery ops triage, and high-leverage engineering. Ezra runs
  as an MCP server via `codex mcp-server` — Ark can invoke Codex tools directly.
  Use when a task requires: book audit, regression check, cross-agent integration
  review, release readiness assessment, ops board refresh, or when Ark wants a
  second opinion on architectural decisions. Trigger for "delegate to ezra",
  "have ezra audit", "ezra review", "codex check", or any audit/strategic task.
  Do NOT use for routine cleanup (use delegate-photius) or canon promotion.
allowed-tools: "Bash(codex:*) Read Grep Glob"
metadata:
  author: Orthodox Phronema Archive
  version: 1.0.0
  category: delegation
  external-agent: codex-cli
  model: codex-5.4
---

# Delegate to Ezra (Codex 5.4)

Ezra runs on OpenAI Codex 5.4. Two delegation paths are available:

## Path 1: MCP Server (Preferred)

Codex is registered as an MCP server in `.mcp.json` under the name `ezra`.
When the MCP server is running, Ark can call Codex tools directly as part of
the normal Claude Code workflow. The MCP server provides:
- Code analysis and review tools
- File reading and diffing
- Structured audit output

This is the preferred path — Ark uses Ezra's tools inline without leaving
the Claude Code session.

## Path 2: Non-Interactive Exec (Batch/Heavy Tasks)

For substantial standalone tasks, use `codex exec` to run Ezra non-interactively:

```bash
# Non-interactive delegation
codex exec \
  --sandbox read-only \
  -C /home/ark/orthodoxphronema \
  "TASK_PROMPT_HERE" \
  -o /tmp/ezra_run_$(date +%Y%m%d_%H%M%S).md \
  2>&1 | tee /tmp/ezra_log_$(date +%Y%m%d_%H%M%S).log

# Full-auto mode for trusted execution
codex exec \
  --full-auto \
  -C /home/ark/orthodoxphronema \
  "TASK_PROMPT_HERE" \
  -o /tmp/ezra_output.md

# Code review mode
codex exec review \
  -C /home/ark/orthodoxphronema \
  2>&1 | tee /tmp/ezra_review.log
```

## Task Prompt Template

Every delegation prompt to Ezra should include:

```
You are Ezra, operating per AGENTS.md.
Working directory: /home/ark/orthodoxphronema

TASK: [specific task description]
SCOPE: [files/directories to review]
OUTPUT: [what to produce — findings, memo, audit log entry]

Focus on:
- Findings-first review with exact file references
- Explicit blocking vs non-blocking distinction
- Evidence-backed recommendations
```

## Ezra Strengths (delegate these)
- Book audits (pre-promotion validation review)
- Regression analysis after pipeline changes
- Cross-agent integration checks (dashboard vs dossier vs staged state)
- Release readiness assessment
- Strategic sequencing and priority recommendations
- High-leverage engineering fixes (when delegation would be slower)
- Ops board refresh after Ark/Photius sessions

## Keep with Ark (don't delegate these)
- Canon promotion execution
- Parser architecture implementation
- Schema version bumps
- Git commits to canon/

## Audit Shortcuts

These map to Ezra's documented audit protocol in AGENTS.md:

```bash
# Full book audit
codex exec -C /home/ark/orthodoxphronema \
  "Audit BOOK_NAME per AGENTS.md audit protocol. Check V1-V12, purity, coordination surfaces."

# Diff review
codex exec -C /home/ark/orthodoxphronema \
  "Compare the current state of FILE_A vs FILE_B. Report blocking issues."

# Article bleed check
codex exec -C /home/ark/orthodoxphronema \
  "Check BOOK_NAME for article bleed per V5. Report any study content in canon."

# Source PDF verification
codex exec -C /home/ark/orthodoxphronema \
  "Verify BOOK_NAME against OSB PDF using pdftotext. Report discrepancies."

# Registry integrity
codex exec -C /home/ark/orthodoxphronema \
  "Verify anchor_registry.json integrity. Check for orphans and mismatches."
```

## After Delegation
1. Review Ezra's output for findings and recommendations
2. Check if ops board needs refresh: `memos/ezra_ops_board.md`
3. If Ezra flagged blocking issues, address before proceeding
4. Update audit log if this was a formal book audit: `memos/ezra-audit-log.md`

## Control Documents
- `AGENTS.md` — shared agent protocol (Ezra section defines mode, scope, WIP limits)
- `.claude/agents/ezra.md` — Claude Code native subagent definition
