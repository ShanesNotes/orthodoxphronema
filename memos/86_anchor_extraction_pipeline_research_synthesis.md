# Research Synthesis: Structured Anchor Reference Extraction Pipeline — 2026-03-11

**Author:** `ark`
**Type:** `decision`
**Status:** `draft`
**Scope:** R1 extraction pipeline — Phase 2/3 boundary
**Workstream:** `phase3-design`
**Phase:** `3`
**Supersedes:** `none`
**Superseded by:** `none`
**Source document:** `research/GEMINI_ANCHOR_EXTRACTION_PIPELINE_20260311.md`

## Context

Gemini delivered a deep research report on the engineering specification for a structured anchor reference extraction pipeline (the R1 pipeline). This pipeline is the critical bridge between Phase 2 (flat-file canon) and Phase 3 (DuckDB-powered citation graph). It scans the Markdown companion files in `canon/` and extracts every scripture reference — both frozen syntax (`[[GEN.1:1]]`) and bare syntax (`GEN.1:1`) — into typed JSONL records that feed the downstream graph layer.

The report is comprehensive engineering specification, not advisory. It contains directly implementable architecture: Pydantic schemas, AST+regex hybrid parsing strategy, zone exclusion rules, and output format contracts. This memo synthesizes the actionable decisions and tasks.

## Objective

- Ratify the R1 pipeline architecture as specified.
- Generate bounded Cowork tasks for implementation.
- Flag risks and open questions requiring human adjudication before code is written.

## Files / Artifacts

- `research/GEMINI_ANCHOR_EXTRACTION_PIPELINE_20260311.md` — full source report
- `pipeline/` — target directory for implementation artifacts

## Findings — Architecture Summary

### 1. Dual-Syntax Extraction

The pipeline must handle two distinct reference syntaxes with zero false positives:

- **Frozen syntax:** `[[BOOK.CH:V]]` — explicitly bracketed wikilinks. The inner token is the anchor ID.
- **Bare syntax:** `BOOK.CH:V` — unbracketed references appearing in prose. Must be extracted only when not inside a frozen link, code block, YAML frontmatter, or HTML element.

The report specifies an AST-first approach: parse Markdown into an abstract syntax tree, identify and exclude structural zones (frontmatter, code fences, HTML blocks), then apply regex extraction only within validated prose zones. This prevents the false-positive contamination that a regex-only approach would produce.

### 2. SBL Morphology Constraint

All anchor IDs must conform to the SBL standard pattern: `^[A-Z0-9]{2,4}\.\d+:\d+$`. The report specifies the complete book code registry (2–4 uppercase alphanumeric characters) already established in `research/PROJECT-KNOWLEDGE.md`. No new codes are introduced.

### 3. Output Schema (R1 Payload)

The R1 pipeline emits strictly typed JSONL with exactly six fields per record:

| Field | Type | Description |
|---|---|---|
| `source_file` | `string` | Relative path to the Markdown file |
| `line_number` | `integer` | Physical line number of the match |
| `raw_match` | `string` | Exact string as found in source |
| `anchor_id` | `string` | Normalized SBL reference |
| `reference_type` | `enum` | `frozen` or `bare` |
| `context` | `string` | Surrounding paragraph text |

This schema is the contract between R1 and the DuckDB ingestion layer (see memo 87). No fields may be added or renamed without updating both sides.

### 4. Zone Exclusion Rules

The AST parser must exclude extraction from:
- YAML frontmatter blocks (delimited by `---`)
- Fenced code blocks (` ``` `)
- Inline code spans (`` ` ``)
- HTML comment blocks (`<!-- -->`)
- HTML element attributes

Failure to enforce zone exclusion produces false positives that silently corrupt the citation graph.

### 5. Spatial Deduplication

When a frozen link `[[GEN.1:1]]` appears in prose, both the frozen syntax and the inner bare token `GEN.1:1` occupy the same character span. The AST parser must detect this overlap and emit only the frozen record, suppressing the bare duplicate. The report specifies an interval-overlap algorithm for this.

## Decisions

| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| AST+regex hybrid, not regex-only | Regex-only cannot distinguish structural zones from prose; produces false positives in code blocks and frontmatter | Low — AST parsing is well-understood; Python `mistune` or `markdown-it-py` are mature | Revert to regex-only with manual zone annotation (high labor cost) |
| Pydantic for output validation | Enforces R1 schema contract at emit time; catches drift before JSONL hits DuckDB | Low | Raw dict output with post-hoc validation (weaker guarantees) |
| JSONL output format (not CSV, not Parquet) | Human-readable, line-diffable, Git-friendly; DuckDB ingests natively via `read_json_auto` | None at current scale (~31k anchors) | Parquet conversion deferred per memo 87 threshold analysis |
| Frozen-priority deduplication | Frozen links carry explicit authorial intent; bare tokens inside frozen spans are artifacts | None — this is the only semantically correct behavior | N/A |

## Summary of Actions for Cowork

| # | Task | Owner | Destination | Dependencies |
|---|---|---|---|---|
| 1 | Implement R1 Python extractor: AST parser + regex extraction + zone exclusion | Cowork | `pipeline/extract/r1_extractor.py` | None |
| 2 | Define Pydantic output model for R1 JSONL records (six fields per schema above) | Cowork | `pipeline/extract/models.py` | None |
| 3 | Implement spatial deduplication (frozen-priority interval overlap) | Cowork | Within `r1_extractor.py` | Task 1 |
| 4 | Build SBL regex validator: `^[A-Z0-9]{2,4}\.\d+:\d+$` applied to all emitted `anchor_id` values | Cowork | Within `models.py` or validator module | Task 2 |
| 5 | Create hallucinated reference dimension table (max chapters/verses per book) | Cowork | `pipeline/extract/canon_dimensions.json` | Book code registry in PROJECT-KNOWLEDGE |
| 6 | Write test suite: known-good extractions from representative canon files (GEN, PSA, MAT at minimum) | Cowork | `pipeline/extract/tests/` | Tasks 1–4 |
| 7 | Run R1 across full `canon/OT/` and validate output counts against known anchor density | Cowork | `metadata/r1_output/` | Tasks 1–6 |

**Cowork execution instruction:** Read `research/GEMINI_ANCHOR_EXTRACTION_PIPELINE_20260311.md`. Execute tasks 1–7 in order. Do not improvise implementation details beyond what the source report and this memo specify. If you encounter an ambiguity, file a question in `memos/` rather than resolving it independently.

## Open Questions

- **AST library selection:** The report references both `mistune` and `markdown-it-py`. Which library should R1 use? Recommendation: `markdown-it-py` (closer to CommonMark spec, plugin-extensible). Awaiting human ratification or Cowork can evaluate both and report findings.
- **Output directory structure:** Should R1 JSONL be emitted as a single file (`metadata/r1_output/anchors.jsonl`) or domain-sharded per testament (`metadata/r1_output/OT/`, `metadata/r1_output/NT/`)? The DuckDB memo (87) assumes glob ingestion, so either structure works. Recommendation: single file for simplicity at current scale.
- **NT applicability:** R1 is specified against `canon/OT/` (49 promoted books). Should it also run against `staging/validated/NT/` (27 staged books) now, or defer until NT stabilization is complete? Recommendation: defer NT until at least MAT/HEB/EPH instability is resolved per `ezra_ops_board.md`.

## Handoff

**To:** `human`
**Ask:** Ratify this memo. Resolve open questions (or accept recommendations). Once ratified, Cowork can execute tasks 1–7.

---

**End of memo.**
