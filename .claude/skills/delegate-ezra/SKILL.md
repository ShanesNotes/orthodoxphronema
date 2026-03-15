---
name: delegate-ezra
description: >
  Delegate tasks to Ezra (Codex 5.4 / gpt-5.4) for strategic audit, validation
  review, risk analysis, delivery ops triage, and high-leverage engineering.
  Ezra runs as an MCP server via `codex mcp-server` — Ark can invoke Codex tools
  directly. Use when a task requires: book audit, regression check, cross-agent
  integration review, release readiness assessment, ops board refresh, code review,
  or when Ark wants a second opinion on architectural decisions. Trigger for
  "delegate to ezra", "have ezra audit", "ezra review", "codex check", or any
  audit/strategic task. Do NOT use for routine cleanup (use delegate-photius)
  or canon promotion.
allowed-tools: "Bash(codex:*) Read Grep Glob"
metadata:
  author: Orthodox Phronema Archive
  version: 2.0.0
  category: delegation
  external-agent: codex-cli
  model-id: gpt-5.4
  context-window: 272000 (standard) / 1050000 (experimental)
  max-output: 128000
---

# Delegate to Ezra (Codex 5.4 / gpt-5.4)

Ezra runs on OpenAI's `gpt-5.4` model via the Codex CLI harness. Two delegation
paths are available.

## Path 1: MCP Server (Preferred — Inline Tools)

Codex is registered as an MCP server in `.mcp.json` under the name `ezra`.
When active, Ark can call these tools directly:

| MCP Tool | Purpose | Maps to Ezra Role |
|----------|---------|-------------------|
| `codex` | Start new conversation with Codex | General delegation |
| `codex-reply` | Continue an existing session | Multi-turn audit |
| `codex_consult` | Technical consultation / Q&A | Strategic questions |
| `codex_review` | Code review | Pre-promotion audit, regression check |
| `codex_explain` | Explain code snippets | Pipeline analysis |

This is the preferred path — Ark uses Ezra's tools inline without leaving
the Claude Code session.

## Path 2: Non-Interactive Exec (Batch/Heavy Tasks)

For substantial standalone tasks, use `codex exec`:

```bash
# Read-only audit (safe default for review tasks)
codex exec \
  --sandbox read-only \
  -C /home/ark/orthodoxphronema \
  "TASK_PROMPT_HERE" \
  -o /tmp/ezra_output_$(date +%Y%m%d_%H%M%S).md

# Full-auto with workspace write (for ops board updates, memo drafts)
codex exec \
  --full-auto \
  --sandbox workspace-write \
  -C /home/ark/orthodoxphronema \
  "TASK_PROMPT_HERE" \
  -o /tmp/ezra_output.md

# Structured JSON output (for programmatic consumption)
codex exec \
  --json \
  --sandbox read-only \
  -C /home/ark/orthodoxphronema \
  "TASK_PROMPT_HERE" \
  2>&1 | tee /tmp/ezra_log.jsonl

# Code review mode (built-in, reviews current repo state)
codex exec review \
  -C /home/ark/orthodoxphronema \
  -o /tmp/ezra_review.md
```

## Reasoning Effort Selection

Match `reasoning_effort` to task complexity. Set via `-c model_reasoning_effort=LEVEL`:

| Level | Use For | Token Cost |
|-------|---------|------------|
| `none` | Simple field extraction, structured transforms | Lowest |
| `low` | Routine checks, formatting verification, simple diffs | Low |
| `medium` | Standard audits, ops board refresh, memo drafts (default) | Moderate |
| `high` | Pre-promotion book audits, multi-file regression analysis | High |
| `xhigh` | Architecture review, cross-agent integration, strategic planning | Highest |

```bash
# Example: high-effort book audit
codex exec \
  -c model_reasoning_effort=high \
  --sandbox read-only \
  -C /home/ark/orthodoxphronema \
  "Audit GEN per AGENTS.md protocol. Run V1-V12, check purity, coordination surfaces."
```

## Task Prompt Template

Every delegation prompt to Ezra should include:

```
You are Ezra, operating per AGENTS.md.
Working directory: /home/ark/orthodoxphronema

TASK: [specific task description]
SCOPE: [files/directories to review]
OUTPUT: [what to produce — findings, memo, audit log entry]
CONSTRAINTS: Apply the SMALLEST possible change. Do NOT refactor working code.

Focus on:
- Findings-first review with exact file references
- Explicit blocking vs non-blocking distinction
- Evidence-backed recommendations
```

## Codex Config

Global config at `~/.codex/config.toml` sets:
- `model = "gpt-5.4"` — flagship model
- `project_doc_fallback_filenames = ["CLAUDE.md"]` — reads our CLAUDE.md if no local AGENTS.md
- `project_doc_max_bytes = 65536` — accommodates our full AGENTS.md
- `sandbox_mode = "workspace-write"` — default for project work

AGENTS.md is auto-injected into Codex sessions (walk-up discovery from cwd).

## Ezra Strengths (delegate these)
- Book audits (V1-V12 + purity + coordination surfaces)
- Regression analysis after pipeline changes
- Cross-agent integration checks (dashboard vs dossier vs staged state)
- Release readiness assessment
- Code review (`codex exec review`)
- Strategic sequencing and priority recommendations
- High-leverage engineering fixes
- Ops board refresh after Ark/Photius sessions

## Keep with Ark (don't delegate these)
- Canon promotion execution
- Parser architecture implementation
- Schema version bumps
- Git commits to canon/

## Audit Shortcuts

```bash
# Full book audit (high effort)
codex exec -c model_reasoning_effort=high --sandbox read-only \
  -C /home/ark/orthodoxphronema \
  "Audit GEN per AGENTS.md. Check V1-V12, purity, coordination surfaces. Report blocking issues."

# Quick diff review (medium effort)
codex exec --sandbox read-only \
  -C /home/ark/orthodoxphronema \
  "Compare staging/validated/OT/GEN.md against canon/OT/01_GEN.md. Report discrepancies."

# Article bleed check (low effort)
codex exec -c model_reasoning_effort=low --sandbox read-only \
  -C /home/ark/orthodoxphronema \
  "Check GEN for V5 article bleed. Report any study content in canon."

# Registry integrity (medium effort)
codex exec --sandbox read-only \
  -C /home/ark/orthodoxphronema \
  "Verify schemas/anchor_registry.json integrity. Check for orphans and mismatches against canon/."

# Full repo code review (high effort)
codex exec review -c model_reasoning_effort=high \
  -C /home/ark/orthodoxphronema \
  -o /tmp/ezra_review_$(date +%Y%m%d).md
```

## After Delegation
1. Review Ezra's output for findings and recommendations
2. Check if ops board needs refresh: `memos/ezra_ops_board.md`
3. If Ezra flagged blocking issues, address before proceeding
4. Update audit log for formal audits: `memos/ezra-audit-log.md`

## Control Documents
- `AGENTS.md` — shared agent protocol (auto-injected by Codex CLI)
- `CLAUDE.md` — fallback project doc (via `project_doc_fallback_filenames` config)
- `.claude/agents/ezra.md` — Claude Code native subagent definition
- `~/.codex/config.toml` — global Codex config with project defaults
