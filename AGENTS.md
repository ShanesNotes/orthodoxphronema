# Orthodox Phronema Agent Protocol

## Team
```text
human: ShanesNotes
ark: planning_architecture_implementation_owner
ezra: audit_risk_workflow_owner
repo: /home/ark/orthodoxphronema
```

## Core Principle
```text
Single writer, explicit handoff, durable evidence.
```

Ark remains the sole default writer and committer for canon-affecting work.
Ezra functions as the standing audit and workflow layer.
Human adjudicates ambiguity, promotion, and role changes.

## Ownership
| Area | Owner | Notes |
|---|---|---|
| Architecture | Ark | Pipeline design, sequencing, long-horizon decisions |
| Implementation | Ark | `pipeline/`, `staging/validated/`, `canon/`, `schemas/` |
| Commits / Git | Ark | Sole default committer |
| Audit / Review | Ezra | Findings-first review, regressions, risk analysis |
| Workflow / Protocol docs | Ezra or Ark on request | Non-canon coordination docs only |
| Human ratification | Human | Ambiguous source cases and promotion approval |

## Ezra Default Mode
```text
default_mode: read_only
default_git_access: denied
default_scope: analyze | validate | diff | report | memo_draft
```

Ezra may update coordination docs only when the human explicitly requests it.
Examples:
- `AGENTS.md`
- `memos/ezra-audit-log.md`
- memo templates
- non-canon workflow notes

Ezra does not edit canon-affecting code or scripture artifacts unless the human explicitly changes that rule.

## Repo Workflow
```text
parse -> cleanup -> validate -> audit -> human_ratify -> promote
```

Detailed flow:
1. Ark plans and, for substantial changes, writes a memo in `memos/`
2. Ark implements code and staged artifact changes
3. Cleanup runs in place on the staged `BOOK.md`
4. Validation runs on that same staged `BOOK.md`
5. Ezra audits the change set or artifact
6. Human reviews only ambiguous cases / promotion decisions
7. Ark promotes from the same staged `BOOK.md`

## Artifact Policy
```text
One staged scripture artifact per book.
```

Rules:
- Staged scripture source of truth: `staging/validated/{OT,NT}/BOOK.md`
- Do not maintain persistent parallel artifacts like `BOOK_clean.md` in steady-state workflow
- Use sidecars for ambiguity, not parallel scripture files
- Use git history, memos, and reports for auditability

Examples of acceptable sidecars:
- `BOOK_dropcap_candidates.json`
- `BOOK_residue_audit.json`
- `BOOK_footnote_markers.json`

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
6. When residual V4 missing-anchor counts are small, source-PDF spot checks are better than broad allowlist growth.
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
Minimum recurring checks:
- `V1` anchor uniqueness
- `V2` chapter count
- `V3` chapter sequence
- `V4` verse sequence / gap detection
- `V5` article bleed
- `V6` frontmatter
- `V7` completeness
- `V8` heading integrity

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

Memo goals:
- preserve rationale
- show evidence
- reduce copy/paste loss between Ark, Ezra, and Human

## Handoff Protocol
Default handoff medium:
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
- anchor_registry.json remains a controlled source of truth
- changes to canonical workflow should prefer tightening invariants over convenience
```
