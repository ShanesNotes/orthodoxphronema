# Claude Code Harness Optimization — Synthesized Report v2

**Date:** 2026-03-14
**Sources:** Anthropic Skills PDF (Cherny, 33pp), Grok research synthesis, Claude Code docs, deep web research, live project audit
**Scope:** Full harness optimization — not just CLAUDE.md, but every native file Claude Code recognizes

---

## Part 1: Corrections & Clarifications

### AGENTS.md is NOT Claude Code Native

Your instinct was correct. `AGENTS.md` is a **Codex CLI convention** (OpenAI). Claude Code does not auto-discover or auto-load it. There's an open feature request (anthropics/claude-code#34235) but it isn't implemented.

Your AGENTS.md is an exceptional document — 414 lines of well-structured multi-agent protocol. The fix isn't to delete it; it's to **bridge it into Claude Code's native system** using `@` imports in CLAUDE.md and by porting the agent definitions into `.claude/agents/*.md` (which IS native).

### .claudeignore Does NOT Exist

My first report recommended creating a `.claudeignore` file. That was wrong — `.claudeignore` is NOT a native Claude Code feature. It's a community feature request (anthropics/claude-code#579, #29455). There's a community hook workaround (`li-zhixin/claude-ignore`) but no built-in support.

**Workaround:** Use `claudeMdExcludes` in `.claude/settings.local.json` or configure permission deny rules in `.claude/settings.json` to restrict file access patterns.

### Grok Output Assessment

The uploaded Grok research (Cherney-style CLAUDE.md) has solid structural instincts but several inaccuracies:

**What Grok got right:**
- Skills 2.0 progressive disclosure model (confirmed by the actual Cherny PDF)
- SKILL.md with YAML frontmatter structure
- Emphasis on `## CRITICAL` sections and trigger descriptions with negative exclusions
- Concise CLAUDE.md target (under 200 lines)
- Repository directory rules mapping

**What Grok got wrong:**
- `@skill:ScriptureValidationSkill` is not valid syntax — skills are invoked by Claude automatically based on description matching, or via `/skill-name` slash commands
- The 4-agent names (Harper/Benjamin/Lucas) are Grok fabrications that don't match your actual team (Ark/Ezra/Photius/Cowork)
- Suggests `fd / rg` as explore commands — these work but aren't part of the harness
- Skill names like `ScriptureValidationSkill` use PascalCase — the Cherny PDF is explicit that names MUST be kebab-case only, no capitals

---

## Part 2: Complete Native Claude Code Filesystem

Here is every file Claude Code auto-discovers and loads, verified against current docs:

```
project-root/
├── CLAUDE.md                          # Main instructions (auto-loaded every session)
│                                      # Supports @path/to/file imports (recursive, max 5 hops)
│
├── .claude/
│   ├── CLAUDE.md                      # Alternative location (either root or here, not both)
│   ├── settings.json                  # Project config — SHARED via git
│   │                                  # Contains: permissions, hooks, MCP servers
│   ├── settings.local.json            # Personal overrides — GITIGNORED
│   │                                  # Contains: local permissions, claudeMdExcludes
│   │
│   ├── rules/                         # Path-scoped instruction files (AUTO-LOADED)
│   │   └── *.md                       # YAML frontmatter with `paths:` glob patterns
│   │                                  # Global rules (no paths field) = always in context
│   │                                  # Scoped rules = indexed, loaded when relevant
│   │
│   ├── agents/                        # Custom subagent definitions (NATIVE)
│   │   └── *.md                       # YAML frontmatter: name, description, tools, model
│   │                                  # Become available as subagents Claude can spawn
│   │
│   ├── skills/                        # Custom skills (NATIVE)
│   │   └── skill-name/
│   │       ├── SKILL.md               # Required — YAML frontmatter + instructions
│   │       ├── scripts/               # Optional — executable code
│   │       ├── references/            # Optional — docs loaded on demand
│   │       └── assets/                # Optional — templates, fonts, icons
│   │
│   └── hooks/                         # Hook scripts (referenced FROM settings.json)
│       └── *.sh                       # Not auto-discovered — must be wired in settings
│
├── .mcp.json                          # MCP server configuration (AUTO-LOADED)
│
└── subdirectory/
    └── CLAUDE.md                      # Lazy-loaded when Claude accesses this directory

User-level (applies to ALL projects):
~/.claude/
├── CLAUDE.md                          # User-level instructions
├── settings.json                      # User-level config
├── rules/                             # User-level rules
├── agents/                            # User-level agents
└── projects/<project>/memory/
    ├── MEMORY.md                      # Auto-memory index (first 200 lines loaded)
    └── [topic].md                     # Topic-specific memory files
```

### What Does NOT Exist Natively

| Claimed File | Reality |
|---|---|
| `.claudeignore` | NOT native. Feature request only. |
| `AGENTS.md` | NOT native. Codex CLI convention. |
| `.claude/commands/*.md` | NOT native / deprecated. |
| `.claude/README.md` | NOT auto-discovered. |
| `.claude/REVIEW.md` | Only for Code Review feature, not general. |

---

## Part 3: Your Current State vs Full Harness

| Native Feature | Your Status | Impact |
|---|---|---|
| `CLAUDE.md` with `@` imports | Have CLAUDE.md but no imports | Briefing packet requires manual Read every session |
| `.claude/settings.json` (shared) | **Missing** — only have settings.local.json | Hooks, shared permissions, MCP config unavailable |
| `.claude/rules/*.md` | **Empty directory exists** | No auto-enforced path-scoped rules |
| `.claude/agents/*.md` | **Missing entirely** | Agents (Ezra/Photius/Cowork) have no native definitions |
| `.claude/skills/*/SKILL.md` | **Missing entirely** | No pipeline skills, no slash commands |
| `.mcp.json` | **Missing** | No MCP server integration |
| Hook scripts | **Missing** | No automated validation gates |
| Nested `CLAUDE.md` files | **Not used** | Pipeline/staging subdirs could have scoped instructions |

---

## Part 4: What To Build — Priority Order

### 4a. CLAUDE.md Rewrite (with @ imports)

Your current CLAUDE.md is 34 lines that ask agents to read other files manually. The `@` import syntax makes this automatic. Keep the file under 200 lines of direct content — let imports handle the rest.

Key structural changes from the Cherny PDF patterns:
- Put CRITICAL/IMPORTANT rules near the top (they get more weight)
- Use `## CRITICAL` headers for zero-exception invariants
- Keep behavioral rules as ALWAYS/NEVER lists (proven pattern from Cherny guide)
- Reference the briefing packet and agents protocol via `@` instead of "please read"

### 4b. `.claude/agents/` — Port Your Agent Definitions

This is the biggest unlock that neither my first report nor Grok identified. Claude Code natively supports custom subagent definitions in `.claude/agents/*.md`. Your AGENTS.md contains everything needed — it just needs to be ported into the native format.

Each agent file uses YAML frontmatter:

**`.claude/agents/ezra.md`** example structure:
```yaml
---
name: ezra
description: Strategic lead, audit, throughput, and shared engineering. Use for validation audits, risk analysis, release readiness, delivery ops, and blocker management.
tools: Read, Grep, Glob, Bash
model: sonnet
---

[Ezra's specific instructions, scope, default mode, lane selection, WIP limits]
```

**`.claude/agents/photius.md`** example structure:
```yaml
---
name: photius
description: Parsing, staging recovery, cleanup specialist. Use for staged scripture structural/editorial fixes, cleanup tooling, evidence packaging, and dossier regeneration.
tools: Read, Grep, Glob, Bash, Edit, Write
model: sonnet
---

[Photius scope, evidence-packaging requirements, cleanup gates]
```

Benefits: Claude can now spawn these as actual subagents with constrained tool access, model selection, and scoped instructions — rather than relying on a human to open separate terminal sessions.

### 4c. `.claude/rules/` — Path-Scoped Auto-Enforcement

These fire automatically when Claude touches files matching the glob. No manual reading required.

Create these four files:

**`.claude/rules/canon.md`** — triggers on `canon/**`
**`.claude/rules/staging.md`** — triggers on `staging/validated/**`
**`.claude/rules/pipeline.md`** — triggers on `pipeline/**`
**`.claude/rules/memos.md`** — triggers on `memos/*.md`

Each with YAML frontmatter containing the relevant invariants from your AGENTS.md ownership table and validation contract.

### 4d. `.claude/skills/` — Pipeline Skills (Cherny Patterns)

Following the actual Cherny PDF patterns (not the Grok approximation). Three key patterns apply to your project:

**Pattern 1 — Sequential Workflow Orchestration** (for promotion gate):
```
validate → audit → ratify → promote
```

**Pattern 3 — Iterative Refinement** (for cleanup cycles):
```
cleanup → validate → identify issues → fix → re-validate → repeat until threshold
```

**Pattern 5 — Domain-Specific Intelligence** (for scripture validation):
```
Specialized knowledge about OSB format, verse anchors, article bleed detection
```

Concrete skills to create:

| Skill | Name | Cherny Pattern |
|---|---|---|
| Validate a book | `validate-book` | Sequential orchestration |
| Run promotion gate | `promote-book` | Sequential + domain intelligence |
| Cleanup report | `cleanup-report` | Iterative refinement |
| PDF edge-case check | `pdf-spot-check` | Domain intelligence |
| Dossier refresh | `refresh-dossier` | Sequential orchestration |

Each SKILL.md must follow the Cherny rules:
- `name`: kebab-case only, no spaces/capitals
- `description`: MUST include WHAT + WHEN + negative exclusions
- Under 1024 characters for description
- No XML angle brackets in frontmatter
- Instructions: specific and actionable, not vague
- Include error handling and examples
- Keep SKILL.md under 5,000 words; move detailed docs to `references/`

### 4e. `.claude/settings.json` — Shared Project Config

Create this to enable hooks and shared permissions. Your existing `settings.local.json` remains for personal overrides.

The hooks system supports 24 events including `PreToolUse` (can block operations), `PostToolUse`, `SessionStart`, `PreCompact`, `PostCompact`, and more.

### 4f. `.mcp.json` — MCP Server Configuration

If you decide to wrap your Python validators as an MCP server (so they're available as tools), this is where the config goes. Lower priority but worth noting as a future path.

### 4g. Nested `CLAUDE.md` Files

Place scoped instructions in subdirectories:
- `pipeline/CLAUDE.md` — parser conventions, test-on-staging rule
- `staging/validated/CLAUDE.md` — evidence-packaging requirements
- `canon/CLAUDE.md` — immutability warning, promote-script-only rule

These lazy-load when Claude accesses those directories.

---

## Part 5: ARK_BRIEFING_PACKET.md Optimization

You mentioned this should be optimized too. The briefing packet is 88 lines — reasonable length. But it's being loaded via manual `Read` calls instead of `@` imports, and some of its content overlaps with AGENTS.md.

Recommended approach:
- Keep it as a reference document for mission/first-principles/architecture
- Let CLAUDE.md import it via `@ARK_BRIEFING_PACKET.md`
- Move any operational rules that overlap with AGENTS.md out — single source of truth
- Tighten to ~60 lines focused purely on mission, invariants, and architecture

---

## Part 6: Grok Output — What to Adopt vs Discard

### Adopt (with corrections):
- The architectural invariants section (lines 9-18 of Grok output) — solid, matches your project
- Repository directory rules (lines 21-28) — accurate mapping
- Anchor/link format and scripture file format sections — correct
- Pipeline contract (line 37) — accurate
- ALWAYS/NEVER behavioral rules pattern — proven effective
- Conciseness target (under 200 lines)

### Discard:
- The Harper/Benjamin/Lucas agent names — replace with Ark/Ezra/Photius/Cowork
- `@skill:SkillName` syntax — not how skills work
- PascalCase skill names — must be kebab-case
- The "Common Commands" section referencing fd/rg — not part of the harness
- The claim about "official Anthropic Skills 2.0" branding — skills are just "skills"

### Merge carefully:
- Grok's "Memory & Self-Improvement" section has the right idea (session confirmation, lesson capture) but should be implemented via auto-memory and session hooks, not manual CLAUDE.md instructions

---

## Part 7: Open-Source Ecosystem Worth Investigating

### From the Cherny PDF directly:
- **anthropics/skills** — official example skills repo (document skills, workflow patterns)
- **skill-creator skill** — built into Claude.ai, helps generate and review skills
- **Skills API** — `/v1/skills/` endpoint for programmatic management
- **Agent SDK** — for building custom agents that leverage skills

### Community resources:
- **awesome-claude-code** (hesreallyhim) — 75+ repos, battle-tested configurations
- **antigravity-awesome-skills** (sickn33) — 1000+ skills catalog
- **claude-pipeline** (aaddrick) — multi-agent pipeline with quality gates
- **claude-code-showcase** (ChrisWiles) — comprehensive hooks/skills/agents example

### For your project specifically:
- Wrap your Python validators (`pipeline/validate/`) as an MCP server — makes them available as native tools
- The Cherny PDF's "iterative refinement" pattern maps directly to your cleanup→validate→fix→re-validate cycle
- The "domain-specific intelligence" pattern is exactly what your scripture validation needs

---

## Part 8: Implementation Checklist

### Phase 1 — Immediate (30 min)
- [ ] Rewrite CLAUDE.md with `@` imports for briefing packet and agents protocol
- [ ] Create `.claude/settings.json` (basic permissions + deny rules for canon)
- [ ] Populate `.claude/rules/` with 4 path-scoped rule files

### Phase 2 — Same Day (1-2 hours)
- [ ] Create `.claude/agents/ezra.md` from AGENTS.md Ezra section
- [ ] Create `.claude/agents/photius.md` from AGENTS.md Photius section
- [ ] Create `.claude/agents/cowork.md` from AGENTS.md Cowork section
- [ ] Create `validate-book` skill in `.claude/skills/`
- [ ] Create `promote-book` skill in `.claude/skills/`

### Phase 3 — Next Session (1-2 hours)
- [ ] Add hooks to `.claude/settings.json` (PreToolUse canon guard, PostToolUse validation)
- [ ] Create remaining skills (cleanup-report, pdf-spot-check, refresh-dossier)
- [ ] Add nested CLAUDE.md files in pipeline/, staging/validated/, canon/
- [ ] Tighten ARK_BRIEFING_PACKET.md (remove overlap with AGENTS.md)

### Phase 4 — Future
- [ ] Investigate wrapping validators as MCP server
- [ ] Test skill trigger accuracy (under/over-triggering per Cherny guide)
- [ ] Consider `.mcp.json` for external tool integrations
- [ ] Evaluate agent teams (experimental feature) for parallel Ark+Photius work

---

## Summary: The Full Native Harness

| Layer | File | Purpose | You Have It? |
|---|---|---|---|
| Instructions | `CLAUDE.md` | Core directives + `@` imports | Partial — needs rewrite |
| Instructions | `subdirectory/CLAUDE.md` | Scoped context | No |
| Rules | `.claude/rules/*.md` | Auto-enforced path constraints | Empty |
| Agents | `.claude/agents/*.md` | Native subagent definitions | No |
| Skills | `.claude/skills/*/SKILL.md` | Pipeline workflow automation | No |
| Config | `.claude/settings.json` | Shared hooks, permissions, MCP | No |
| Config | `.claude/settings.local.json` | Personal overrides | Yes |
| Integration | `.mcp.json` | MCP server connections | No |
| Memory | `~/.claude/projects/*/memory/` | Auto-accumulated knowledge | Auto (if enabled) |

You're currently using roughly 15% of the available harness. The biggest wins are the `@` imports (eliminates manual reads), `.claude/agents/` (makes your multi-agent protocol native), and `.claude/rules/` (auto-enforces your ownership boundaries).
