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
allowed-tools: "Bash(gemini:*) Bash(tee:*) Read Grep Glob"
metadata:
  author: Orthodox Phronema Archive
  version: 2.0.0
  category: delegation
  external-agent: gemini-cli
  model: gemini-3-flash
---

# Delegate to Photius (Gemini CLI Flash 3.0)

Photius runs on Google's Gemini CLI with the Flash 3.0 model — fast, high-throughput,
optimized for execution over deep reasoning. GEMINI.md at the repo root is the
canonical control document, auto-loaded by Gemini CLI.

## Delegation Commands

```bash
# Non-interactive delegation (preferred for automation)
gemini --prompt "TASK_PROMPT_HERE" \
  --approval-mode auto_edit \
  --output-format json \
  2>&1 | tee /tmp/photius_run_$(date +%Y%m%d_%H%M%S).log

# Sandboxed execution (safer for untested tasks)
gemini --prompt "TASK_PROMPT_HERE" \
  --sandbox \
  --approval-mode auto_edit \
  --output-format json \
  2>&1 | tee /tmp/photius_run_$(date +%Y%m%d_%H%M%S).log

# Full YOLO mode (auto-approve everything — use for trusted batch cleanup)
gemini --prompt "TASK_PROMPT_HERE" \
  --approval-mode yolo \
  --output-format text \
  2>&1 | tee /tmp/photius_run_$(date +%Y%m%d_%H%M%S).log

# Interactive handoff (Photius takes over the terminal)
gemini -i "TASK_PROMPT_HERE"
```

### Approval Modes

| Mode | Behavior | Use For |
|------|----------|---------|
| `default` | Prompts for approval on each action | First-time tasks, untested workflows |
| `auto_edit` | Auto-approves edit tools, prompts for others | Standard cleanup runs |
| `yolo` | Auto-approves everything | Trusted batch operations on evidence-backed tasks |
| `plan` | Read-only mode | Analysis, evidence collection, report generation |

### Output Formats

| Format | Flag | Use For |
|--------|------|---------|
| Text | `--output-format text` | Human-readable logs |
| JSON | `--output-format json` | Programmatic consumption, piping to jq |
| Stream JSON | `--output-format stream-json` | Real-time monitoring |

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
- Batch text cleanup across 5+ books (fused words, split words, punctuation)
- OCR artifact detection and classification
- Footnote structural repair (F1-F4 patterns via text-cleaner --profile footnotes)
- Evidence collection and packaging (counts, examples, before/after)
- Repetitive validation sweeps across books
- Split-word and fused-word repair (aspell-gated detection)
- Report generation and dashboard refresh
- Search-and-replace across many files with format enforcement

## Escalate Back to Ark (don't delegate these)
- Parser architecture changes (`pipeline/parse/`)
- Validation rule changes (`pipeline/validate/`)
- Promotion gate decisions (`pipeline/promote/`)
- Schema modifications (`schemas/`)
- Ambiguous architectural tradeoffs
- Canon file edits (promotion only)

## Common Delegation Patterns

### Batch Footnote Cleanup
```bash
gemini --prompt "You are Photius per GEMINI.md. Run text-cleaner with --profile footnotes on study/footnotes/OT/. Apply F1-F4 structural fixes. Write a memo documenting all changes with before/after examples. Run validation after." \
  --approval-mode auto_edit \
  2>&1 | tee /tmp/photius_footnote_cleanup.log
```

### Evidence Collection Sweep
```bash
gemini --prompt "You are Photius per GEMINI.md. For each book in canon/OT/, count total anchors, check for V5 article bleed, and report results as JSON to reports/sweep_$(date +%Y%m%d).json." \
  --approval-mode plan \
  --output-format json \
  2>&1 | tee /tmp/photius_sweep.log
```

### Batch Validation Run
```bash
gemini --prompt "You are Photius per GEMINI.md. Run python3 pipeline/tools/batch_validate.py --dir canon/OT and python3 pipeline/tools/batch_validate.py --dir canon/NT. Capture results to reports/batch_validation_$(date +%Y%m%d).txt. Summarize any FAIL or WARN results." \
  --approval-mode auto_edit \
  2>&1 | tee /tmp/photius_validate.log
```

## After Delegation
1. Check Photius's output log for completion handshake block
2. Review any file changes with `git diff`
3. Run validation on affected files if Photius didn't
4. If Photius deferred any completion surfaces, handle them or note as stale
5. If changes look good, commit with Photius attribution

## Control Documents
- `GEMINI.md` — Photius's full system directives (auto-loaded by Gemini CLI)
- `AGENTS.md` — shared agent protocol (read at session start per GEMINI.md instructions)
- `.claude/agents/photius.md` — Claude Code native agent definition
