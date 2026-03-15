# Orthodox Phronema Agent Protocol

## Team
```text
human: ShanesNotes
ark: architecture_codebase_engineering_promotion_owner        [Claude Code / Opus]
ezra: strategic_lead_audit_throughput_shared_engineering_owner [Codex CLI 5.4 — MCP-delegatable]
photius: parsing_staging_recovery_cleanup_specialist           [Gemini CLI Flash 3.0 — Bash-delegatable]
cowork: pm_workflow_optimization_research_synthesis            [Claude Cowork]
repo: /home/ark/orthodoxphronema
```

## Core Principle
```text
Single writer, explicit handoff, durable evidence.
```

Ark remains the sole default writer and committer for canon-affecting and core pipeline work.
Photius operates as a bounded writer for staged recovery, cleanup tooling, and evidence packaging.
Ezra functions as the standing strategic, audit, and throughput layer.
Human adjudicates ambiguity, promotion, and role changes.

## Ownership
| Area | Owner | Notes |
|---|---|---|
| Architecture | Ark | Pipeline design, sequencing, long-horizon decisions |
| Core pipeline | Ark | `pipeline/parse/`, `pipeline/validate/`, `pipeline/promote/`, `schemas/` |
| Canon / Promotion | Ark + Human | `canon/` writes, promotion execution |
| Staged recovery | Photius | `staging/validated/` structural/editorial fixes (evidence-packaged) |
| Cleanup tooling | Photius | `pipeline/cleanup/` bounded tools; batch tools (5+ books) require Ark review |
| Evidence packaging | Photius | `memos/`, `reports/` for recovery evidence and dossier regeneration |
| Commits / Git | Ark (default) | Photius may commit to staging with distinct authorship |
| Audit / Review | Ezra | Findings-first review, regressions, risk analysis |
| Strategic direction / throughput | Ezra | sequencing, blocker management, technical direction, live ops board |
| Shared engineering triage | Ezra | May take high-leverage engineering lanes when that is the fastest safe unblocker |
| Workflow / Protocol docs | Ezra or Ark on request | Non-canon coordination docs only |
| Human ratification | Human | Ambiguous source cases and promotion approval |

## Ezra Default Mode (Codex 5.4, Sunset Path)
```text
platform: OpenAI Codex CLI 5.4
delegation: MCP server (codex mcp-server) in .mcp.json, or codex exec for batch tasks
control_doc: AGENTS.md (this file)
claude_agent_def: .claude/agents/ezra.md
delegation_skill: .claude/skills/delegate-ezra/SKILL.md
default_mode: strategic_lead
default_git_access: denied
default_scope: analyze | validate | diff | report | memo_draft | delivery_ops | triage | sequencing | blocker_management | technical_direction | release_readiness | selective_engineering
```

Ezra may update coordination docs only when the human explicitly requests it.
Examples:
- `AGENTS.md`
- `memos/ezra-audit-log.md`
- memo templates
- non-canon workflow notes

Ezra may take direct implementation work when the human explicitly requests an expanded lane or when Ezra is already operating inside a human-ratified leadership lane.
Default high-leverage Ezra coding lanes:
- workflow-critical unblockers
- high-leverage refactors
- cross-agent integration fixes
- release-readiness blockers that would otherwise idle Ark or Photius

Ezra should not absorb routine staged cleanup that clearly belongs to Photius or routine core-pipeline ownership that already belongs cleanly to Ark.
Ezra does not edit canon-affecting code or scripture artifacts unless the human explicitly changes that rule.

## Ezra Delivery Ops
```text
cadence: per_session_ops_loop
live_coordination_surface: memos/ezra_ops_board.md
source_of_live_state: reports/book_status_dashboard.json
```

Rules:
- Ezra maintains `memos/ezra_ops_board.md` as the human-readable live queue.
- `reports/book_status_dashboard.json` remains the machine-readable source of current book state.
- Memos preserve rationale, decisions, and substantial handoffs; they should not become the only live status surface.
- Ezra leads with prioritization and routing first, and codes second only when direct intervention is the highest-leverage move.
- After any Ark or Photius session that changes staged, validation, or promotion-affecting state, Ezra should:
  1. read the new memo/report/dashboard deltas
  2. refresh `memos/ezra_ops_board.md`
  3. publish concise next actions for Ark, Photius, and Human
- Human-facing ratification asks should be capped at 3 open items at a time.

Ezra lane-selection order:
1. unblock Ark or Photius if shared state or interface drift is stalling them
2. package Human decisions into tight packets
3. remove contradictions between dashboard, dossiers, memos, and staged state
4. take one high-leverage engineering lane if delegation would be slower or less safe
5. keep long-horizon work visible without letting it displace the release train

Default WIP limits:
- Ark: 1 core engineering lane at a time
- Photius: 2 active cleanup/recovery lanes max, or 1 batch-tool lane plus 1 book lane
- Ezra: 1 active audit/release queue + 1 active ops board + at most 1 active engineering lane

## Photius Default Mode (Gemini CLI Flash 3.0)
```text
platform: Google Gemini CLI (Flash 3.0)
delegation: gemini --prompt for non-interactive tasks, gemini -i for interactive
control_doc: GEMINI.md
claude_agent_def: .claude/agents/photius.md
delegation_skill: .claude/skills/delegate-photius/SKILL.md
default_mode: bounded_write
default_git_access: staging_only
default_scope: parse_analysis | staged_recovery | cleanup_tooling | evidence_packaging
```

Photius may write without additional approval when work is evidence-backed:
- `staging/validated/` — structural and editorial recovery
- `pipeline/cleanup/` — bounded parsing-residue tools
- `memos/` — evidence packaging and handoff
- `reports/` — dossier and dashboard regeneration

Photius must NOT edit without explicit human instruction:
- `canon/` — promotion is Ark + Human only
- `pipeline/parse/` — parser architecture stays with Ark
- `pipeline/validate/` — validation semantics stay with Ark
- `pipeline/promote/` — promotion gate stays with Ark
- `schemas/` — registry is a controlled source of truth (propose corrections, Ark applies)
- `AGENTS.md`, workflow policy files, git history/tags

Evidence-packaged commit requirement for staged fixes:
- Source page reference (OSB PDF page number)
- Affected anchors (verse list)
- Validator result (before/after)
- Brief rationale

Cleanup script review gate:
- Single-book targeted fixes: ship immediately
- Batch tools (5+ books): require Ark architecture review before corpus-wide use

## Cowork Default Mode
```text
default_mode: pm_and_research_synthesis
default_git_access: denied
default_scope: project_board | memo_index | research_curation | workflow_optimization | synthesis
control_doc: PROJECT_BOARD.md
```

Cowork operates as the project management and workflow optimization layer.
Cowork maintains:
- `PROJECT_BOARD.md` as the official PM surface
- `memos/INDEX.md` as the memo-governance overlay
- `research/` as the canonical home for non-governing advisory/spec artifacts

Cowork may write without additional approval:
- `PROJECT_BOARD.md` — project board updates
- `memos/INDEX.md` — memo classification updates
- `research/` — external AI output synthesis and relocation

Cowork must NOT edit without explicit human instruction:
- `canon/`, `staging/`, `pipeline/`, `schemas/` — implementation artifacts
- `AGENTS.md` — protocol authority changes (Cowork may propose, but Human ratifies)
- Numbered memos — governance artifacts owned by Ark/Ezra/Photius unless Human explicitly assigns one
- `memos/ezra_ops_board.md` — Ezra's live dispatch surface

Cowork's official standing surfaces are `PROJECT_BOARD.md` and `memos/INDEX.md`.
Other Cowork-authored planning, research, or synthesis outputs are non-governing by default. They become governing only when:
- Human explicitly ratifies them, or
- A numbered memo by Ark/Ezra/Photius adopts specific findings

## External AI Agent Protocol

External AI agents that are not named team members produce valuable input but are not part of the standing governance structure.

Rules:
- External outputs go to `research/` only — never to `memos/`
- External outputs are non-governing by default regardless of content quality
- To adopt external findings into project policy, a numbered memo must explicitly ratify them
- External outputs use descriptive filenames: `{SOURCE}_{TOPIC}_{DATE}.md` (e.g., `GROK_ENGINEERING_AUDIT_20260310.md`)
- External outputs do not receive numbered memo prefixes

Ratification path:
1. External agent produces output → saved to `research/`
2. Team agent (Ark/Ezra/Photius) reviews and evaluates
3. If adopting findings: write a numbered memo that cites the research artifact
4. `memos/INDEX.md` updated to reflect the ratification chain

## Project Management Surfaces

```text
vision_and_kanban: PROJECT_BOARD.md
memo_governance: memos/INDEX.md
live_dispatch: memos/ezra_ops_board.md
machine_state: reports/book_status_dashboard.json
research_inputs: research/
```

Surface relationship:
- `PROJECT_BOARD.md` = management view (priorities, phases, decisions, metrics)
- `memos/ezra_ops_board.md` = tactical dispatch (next owner, blockers, session handoff)
- `memos/INDEX.md` = memo governance (current vs historical vs research)

Update cadence:
- `PROJECT_BOARD.md`: updated when lanes change status, decisions close, or metrics shift
- `memos/INDEX.md`: updated when new memos are created or governance status changes
- `ezra_ops_board.md`: updated per Ezra session loop
- `book_status_dashboard.json`: regenerated after validation/promotion state changes

## Cross-Agent Delegation Protocol

Ark (Claude Code) can delegate tasks to Ezra and Photius programmatically:

### Ezra Delegation (MCP or Exec)
```text
MCP path:   Codex registered as "ezra" MCP server in .mcp.json
             Ark calls Codex tools inline during Claude Code sessions
Exec path:  codex exec -C /home/ark/orthodoxphronema "TASK_PROMPT"
             Used for substantial standalone audit/review tasks
Skill ref:  .claude/skills/delegate-ezra/SKILL.md
```

### Photius Delegation (Bash)
```text
Exec path:  gemini --prompt "TASK_PROMPT" --approval-mode auto_edit
             Used for batch cleanup, evidence collection, report generation
Skill ref:  .claude/skills/delegate-photius/SKILL.md
Control:    GEMINI.md loaded automatically by Gemini CLI in repo root
```

### Delegation Rules
- Delegated tasks must include: scope, boundaries, output expectations, completion handshake requirements
- Ark reviews all delegated output before integration into canon-affecting state
- MCP delegation (Ezra) runs inline — Ark maintains session continuity
- Bash delegation (Photius) produces logs at /tmp/photius_run_*.log
- Both agents read AGENTS.md at session start for ownership/boundary awareness

## Repo Workflow
```text
parse -> cleanup -> validate -> audit -> human_ratify -> promote
```

Detailed flow:
1. Ark plans and, for substantial changes, writes a memo in `memos/`
2. Ark implements core pipeline and extraction changes
3. Photius performs staged recovery, structural fixes, and cleanup (evidence-packaged)
4. Cleanup runs in place on the staged `BOOK.md`
5. Validation runs on that same staged `BOOK.md`
6. Ezra audits the change set or artifact
7. Human reviews only ambiguous cases / promotion decisions
8. Ark promotes from the same staged `BOOK.md`

## Completion Handshake
```text
Work is not done when files changed. Work is done when state, evidence, and handoff agree.
```

Completion rule for substantial Ark or Photius sessions:
- If a session changes `staging/validated/`, `pipeline/cleanup/`, `reports/`, or promotion-readiness state, the session is not complete until all affected completion surfaces are handled.
- Required completion surfaces:
  - durable memo or run report in `memos/`
  - verification run or targeted check result
  - affected generated artifacts refreshed, or explicitly declared not refreshed

Minimum completion block for substantial memos:
- `Files changed`
- `Verification run`
- `Artifacts refreshed`
- `Remaining known drift`
- `Next owner`

Artifact refresh rule:
- If staged scripture changes and a promotion dossier exists for that book, refresh or explicitly defer the dossier.
- If dashboard-visible book state changed, refresh or explicitly defer `reports/book_status_dashboard.json`.
- If a refresh is intentionally deferred, the memo must say so plainly and name the stale surface.

Stale-state vocabulary:
- `stale dossier` = staged scripture changed but the dossier was not regenerated
- `stale dashboard` = generated dashboard was not refreshed after dossier/staged state changed
- `stale memo` = memo claims no longer match current repo artifacts

Owner expectations:
- Ark must refresh or explicitly defer impacted dossier/dashboard state after structural, parser, validator, promote, or staged-book work.
- Photius must leave a run memo and either refresh affected reports or explicitly state that report refresh was not performed.
- Ezra should name the exact stale surface and whether it is blocking, misleading, or harmless drift, not just say `stale`.

## Artifact Policy
```text
One staged scripture artifact per book.
```

Rules:
- Staged scripture source of truth: `staging/validated/{OT,NT}/BOOK.md`
- Do not maintain persistent parallel artifacts like `BOOK_clean.md` in steady-state workflow
- Use sidecars for ambiguity, not parallel scripture files
- Use git history, memos, and reports for auditability
- Standard non-scripture companions may sit beside the staged scripture file without becoming a second scripture source of truth

Examples of acceptable sidecars:
- `BOOK_dropcap_candidates.json`
- `BOOK_residue_audit.json`
- `BOOK_footnote_markers.json`

Standard non-scripture companions (staging):
- `BOOK_articles.md`
- `BOOK_footnotes.md`

Promoted study layer (`study/`):
- `study/articles/` — promoted study articles
- `study/footnotes/` — promoted footnotes (per-testament subdirs: OT/, NT/)
- `study/lectionary-notes/` — lectionary cross-references

## Non-Scripture Companion Workflow
```text
Single scripture file, explicit companion layers.
```

Standard staged companion set:
- `BOOK.md` — staged scripture source of truth
- `BOOK_articles.md` — study articles / commentary blocks
- `BOOK_footnotes.md` — verse-linked footnotes from the OSB notes section
- `BOOK_footnote_markers.json` — scripture-side footnote marker trace

Rules:
- `BOOK_notes.md` is legacy / transitional; new work should target `BOOK_articles.md` and `BOOK_footnotes.md`
- Article and footnote companions may expand context and linkage, but they do not create a second staged scripture artifact
- Footnote verification compares `BOOK_footnotes.md` against `BOOK_footnote_markers.json`
- Footnote mismatch results may route work to Photius staged recovery, Ezra audit triage, or Ark parser changes depending on root cause

Named footnote mismatch classes:
- parser false positives
- missing inline markers
- versification drift

## Extraction Method Selection
```text
Choose the extractor that preserves the substrate, not the one with the prettiest generic output.
```

Rules:
- Scripture pages: `Docling` remains the primary extractor
- Scripture edge cases: `pdftotext` is the sanctioned verifier / targeted fallback for drop-caps, marker misses, and other hard OCR edge cases
- Notes and footnotes pages: `pdftotext` is the primary extractor
- `Docling` may still be used on notes pages for debugging page shape, but not as the default footnote extractor
- Footnote verification may expose scripture extraction defects, but it does not silently relax canon-promotion requirements

## Source Authority
| Source | Role |
|---|---|
| OSB PDF | Canonical source |
| Brenton text files | Auxiliary witness only |
| LLM inference | Proposal / ranking layer only |

Rules:
- OSB remains authoritative for canon text
- Brenton may assist with bounded micro-corrections and confidence scoring
- Brenton must not rewrite verses wholesale or decide anchor structure
- Ambiguous drop-caps are resolved by OSB image/PDF review, not Brenton alone

## Current Lessons Learned
```text
1. Lowercase-start verse gaps belong in parse, not cleanup.
2. Deterministic cleanup rules can move earlier in the pipeline.
3. Drop-cap recovery should be OSB-residual-first and PDF-confirmed.
4. Inline footnote markers likely trail the verse they annotate.
5. Promotion must read the same staged artifact that was validated and audited.
6. Editorial cleanup must explicitly audit fused article OCR defects like `adecree`, `aephod`, and `acovenant`.
7. Footnote marker sidecars must preserve marker order and local trace context so later extraction does not require re-locating anchors.
8. `pdftotext` is preferred for OSB notes / footnotes extraction and remains a targeted verifier for scripture edge cases.
9. Footnote mismatch reports are first-class signals for parser false positives, missing markers, and versification drift.
10. When residual V4 missing-anchor counts are small, source-PDF spot checks are better than broad allowlist growth.
```

## Parser / Cleanup Boundaries
| Problem | Stage |
|---|---|
| Verse-boundary recovery | Parse |
| Study-article separation | Parse |
| Heading purity | Parse + Validate |
| Fused possessives / punctuation spacing | Parse-time normalization is acceptable |
| Bounded fused-word cleanup | Cleanup |
| Ambiguous OCR / source verification | Cleanup sidecar + human review |

## Validation Contract
Full suite (V1-V12):
- `V1` anchor uniqueness
- `V2` chapter count
- `V3` chapter sequence
- `V4` verse sequence / gap detection
- `V5` article bleed
- `V6` frontmatter
- `V7` completeness
- `V8` heading integrity
- `V9` embedded verse detection
- `V10` absorbed content (Brenton cross-reference)
- `V11` split-word artifacts (Docling column-split)
- `V12` inline verse-number leakage

Interpretation rule:
- Cleanup success does not substitute for structural success
- If `V4` gaps remain high, return to parser work before expanding cleanup complexity
- If unresolved missing-anchor count is `<= 100` for a book, prefer OSB PDF spot-check review before widening parser allowlists

## Memo Contract
Substantial changes should produce a durable memo in `memos/`.

Use:
- [`_template_work_memo.md`](/home/ark/orthodoxphronema/memos/_template_work_memo.md)

When a memo is required:
- parser refactor
- cleanup-rule expansion
- validation-rule change
- promotion-gate change
- source-authority / workflow policy change
- substantial staged recovery or dashboard/dossier affecting work

Memo goals:
- preserve rationale
- show evidence
- reduce copy/paste loss between Ark, Ezra, and Human
- make completion status explicit enough that Ezra does not need to infer whether reports or dashboard state were refreshed

## Handoff Protocol
Default handoff medium:
- `memos/ezra_ops_board.md` for live queue / next actions
- `memos/` for human-readable implementation / audit / decision notes
- `reports/` for generated validation evidence
- staged JSON sidecars for ambiguity queues

Do not add a `reviews/` folder unless the team explicitly decides existing channels are insufficient.

## Audit Request Shortcuts
```text
ezra audit BOOK
ezra diff OLD NEW
ezra check bleed BOOK
ezra verify pdf BOOK
ezra verify registry
ezra review parser change
ezra review promote gate
```

Ezra output style:
- findings first
- exact file references
- tables for comparisons when useful
- explicit distinction between blocking vs non-blocking

## Promotion Gate
Promotion should require all of:
1. Ark implementation complete
2. Validation run recorded
3. Ezra audit complete or explicitly waived
4. Human ratification of ambiguous cases
5. Ark promotion run from the same staged file

## Constraints
```text
- one-verse-per-line is mandatory
- study article text must not appear in canon scripture files
- footnote markers are stripped from canon and indexed separately
- footnote marker sidecars should retain enough local trace metadata to support later note/footnote recovery
- authored cross-text references in Markdown should use `[[BOOK.ch:v]]` syntax (example: `[[GEN.1:1]]`)
- machine-readable fields may continue storing plain canonical anchor tokens (example: `GEN.1:1`)
- anchor_registry.json remains a controlled source of truth
- changes to canonical workflow should prefer tightening invariants over convenience
```
