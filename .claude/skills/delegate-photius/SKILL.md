---
name: delegate-photius
description: >
  Delegate tasks to Photius (Gemini CLI, Flash 3.0) for batch text processing,
  OCR cleanup, evidence packaging, and staging recovery. Use when a task involves
  repetitive file processing across many books, pattern-matching cleanup, or when
  Ark wants to offload bounded execution work. Trigger for "delegate to photius",
  "have photius do this", "batch process", "run photius on", or any task that
  matches Photius's strengths (batch ops, cleanup, evidence collection).
  Do NOT use for architectural decisions, canon promotion, or parser changes.
allowed-tools: "Bash(gemini:*) Read Grep Glob"
metadata:
  author: Orthodox Phronema Archive
  version: 1.0.0
  category: delegation
  external-agent: gemini-cli
  model: gemini-3-flash
---

# Delegate to Photius (Gemini CLI)

Photius runs on Gemini CLI (Flash 3.0). This skill enables Ark to delegate
bounded execution tasks to Photius non-interactively.

## How Delegation Works

Gemini CLI supports headless mode via `--prompt` flag. Ark constructs a task
prompt that includes:
1. The specific work to be done
2. File paths and scope boundaries
3. Output expectations (memo, report, file changes)
4. Completion handshake requirements

## Delegation Command

```bash
# Non-interactive delegation with structured output
gemini --prompt "TASK_PROMPT_HERE" \
  --approval-mode yolo \
  --output-format json \
  2>&1 | tee /tmp/photius_run_$(date +%Y%m%d_%H%M%S).log

# With sandbox for safer execution
gemini --prompt "TASK_PROMPT_HERE" \
  --sandbox \
  --approval-mode auto_edit \
  --output-format json \
  2>&1 | tee /tmp/photius_run_$(date +%Y%m%d_%H%M%S).log
```

## Task Prompt Template

Every delegation prompt to Photius should include:

```
You are Photius, operating per GEMINI.md and AGENTS.md.
Working directory: /home/ark/orthodoxphronema

TASK: [specific task description]
SCOPE: [files/directories in scope]
BOUNDARIES: [what NOT to touch]

Expected outputs:
- [file changes, memo, report, etc.]

Completion handshake:
- Write a memo to memos/ documenting changes
- Run validation on affected files
- List files changed, verification results, and remaining drift
```

## Photius Strengths (delegate these)
- Batch text cleanup across 5+ books
- OCR artifact detection and classification
- Footnote structural repair (F1-F4 patterns)
- Evidence collection and packaging
- Repetitive validation sweeps
- Split-word and fused-word repair
- Report generation and dashboard refresh

## Escalate Back to Ark (don't delegate these)
- Parser architecture changes
- Validation rule changes
- Promotion gate decisions
- Schema modifications
- Ambiguous architectural tradeoffs

## After Delegation
1. Check Photius's output log for completion handshake
2. Review any file changes with `git diff`
3. Run validation on affected files
4. If Photius deferred any completion surfaces, handle them or note as stale

## Control Documents
- `GEMINI.md` — Photius's full system directives (read by Gemini CLI at session start)
- `AGENTS.md` — shared agent protocol (ownership, boundaries, handoff rules)
