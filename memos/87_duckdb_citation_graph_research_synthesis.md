# Research Synthesis: DuckDB-Powered Theological Citation Graph — 2026-03-11

**Author:** `ark`
**Type:** `decision`
**Status:** `draft`
**Scope:** DuckDB analytical layer — Phase 3 graph backend
**Workstream:** `phase3-design`
**Phase:** `3`
**Supersedes:** `none`
**Superseded by:** `none`
**Source document:** `research/GEMINI_DUCKDB_CITATION_GRAPH_20260311.md`

## Context

Gemini delivered a deep research report on the architectural blueprint for the DuckDB-powered citation graph — the Phase 3 analytical layer that sits atop the R1 extraction pipeline (memo 86). This report covers duckpgq stability, FTS+graph query composition, directory ingestion, graph integrity validation, and the JSONL-vs-Parquet storage decision.

The report is more advisory than the R1 pipeline spec. Its most critical finding is not an implementation pattern but a **risk assessment**: duckpgq is a community-tier research extension with documented failure modes that require defensive engineering. This memo synthesizes the actionable decisions, the risk register, and the bounded Cowork tasks.

## Objective

- Ratify the DuckDB schema and ingestion architecture.
- Establish a formal risk register for duckpgq.
- Generate bounded Cowork tasks for schema creation and validation hardening.
- Confirm the JSONL-direct-ingestion decision at current scale.

## Files / Artifacts

- `research/GEMINI_DUCKDB_CITATION_GRAPH_20260311.md` — full source report
- `pipeline/graph/` — target directory for DuckDB schema and scripts
- Memo 86 (R1 pipeline) — upstream dependency; R1 output is DuckDB's input

---

## Section 1 — duckpgq Risk Register

This is the highest-priority finding. The duckpgq extension is the mechanism for graph traversal queries over the citation data. It is **not production-hardened** and requires explicit defensive posture.

### Risk: Community-Tier Extension Status

**Severity:** Medium
**Description:** duckpgq is classified as a DuckDB Community Extension maintained by the CWI Database Architectures group. It is explicitly documented as an ongoing research project. It lacks the Long-Term Support and stability guarantees of DuckDB Core extensions. The maintainers have issued disclaimers regarding incomplete features and occasional instability.

**Mitigation:** Treat duckpgq as an exploratory analytical tool, not a hardened transactional layer. All graph query results used in downstream pipeline stages must be independently validatable against the flat-file canon. Never place duckpgq in the critical path of a synchronous user-facing application without fallback.

### Risk: Silent Empty-Set on Schema Drift

**Severity:** High
**Description:** The `CREATE PROPERTY GRAPH` statement establishes rigid `SOURCE KEY` and `DESTINATION KEY` constraints. If the upstream R1 JSONL introduces even minor `anchor_id` format mutations (e.g., `GEN.1:1` → `GEN_1_1`), the edge mappings silently fail to bind. Subsequent `GRAPH_TABLE` queries return empty result sets **without error**. This is the most dangerous failure mode — it produces silent data loss with no diagnostic signal.

**Mitigation:** Mandatory schema validation at the ingestion boundary. Every R1 record must pass the SBL regex gate (`^[A-Z0-9]{2,4}\.\d+:\d+$`) before entering DuckDB. The ingestion script must assert non-zero edge counts after `CREATE PROPERTY GRAPH` execution and halt with an explicit error if the assertion fails.

### Risk: CTE Scoping Bugs in Graph Algorithms

**Severity:** Medium
**Description:** Graph algorithm functions (`local_clustering_coefficient`, `pagerank`) sporadically fail with `csr_cte does not exist` errors. This is a documented bug in duckpgq's CTE binding logic where the dynamically generated CSR structure drops out of scope during execution.

**Mitigation:** Wrap all graph algorithm invocations in try-catch exception handling. Pipeline scripts must degrade gracefully: if an algorithm fails, log the error and continue with available data rather than halting the entire pipeline. Do not use graph algorithm outputs as pipeline gates.

### Risk: Parser Conflicts with Mixed Query Syntax

**Severity:** Low
**Description:** Complex subqueries mixing core DuckDB SQL with PGQ visual `MATCH` syntax can confuse the runtime parser hierarchy.

**Mitigation:** Isolate all graph queries into discrete, encapsulated CTEs. Never nest PGQ syntax inside complex subqueries. Use the two-step CTE pattern (see Section 2).

---

## Section 2 — Ratified Architecture Decisions

### 2.1 Two-Step CTE Pattern for FTS+Graph Composition

FTS (`match_bm25`) and graph traversal (`GRAPH_TABLE`) cannot be syntactically composed into a single query. The ratified pattern is:

1. **CTE Phase 1 — Lexical filter:** Execute `match_bm25` against the `context` column; project a truncated set of `source_file` primary keys.
2. **Phase 2 — Graph traversal + join:** Execute `GRAPH_TABLE` path-finding; `INNER JOIN` graph output against the FTS CTE.

This is non-negotiable. Attempting unified composition will produce parser failures.

### 2.2 Dynamic Directory Ingestion via Recursive Glob

Reject brittle `UNION ALL` patterns and non-compliant Hive partitioning. The ratified ingestion pattern:

```sql
SELECT *, split_part(filename, '/', -2) AS taxonomy_domain
FROM read_json_auto('metadata/anchor_backlinks/*/*.json', filename=true)
```

This auto-discovers new domain subdirectories without script modification. The `split_part` extraction preserves the domain folder name as a queryable column.

### 2.3 JSONL Direct Ingestion — No Parquet Conversion

At ~31,000 anchor records, Parquet conversion is an anti-pattern:
- 31,000 rows fall below the 122,880-row Parquet row group minimum, resulting in single-threaded query execution — negating Parquet's parallelization advantage.
- DuckDB's `read_json_auto` ingests 31,000 rows in fractional milliseconds.
- The JSONL format is line-diffable and Git-friendly.

**Threshold for revisiting:** When the archive organically crosses 100,000 records (approximately 3x current scale), re-evaluate Parquet conversion. Until then, JSONL is the optimal format.

### 2.4 Graph Integrity Validation (OpenAlex/OpenCitations-Derived)

The report transposes validation patterns from OpenAlex and OpenCitations to the theological pipeline. Five mandatory checks before records enter the graph:

| Check | Method | Quarantine Condition |
|---|---|---|
| SBL PID morphology | `regexp_matches(anchor_id, '^[A-Z0-9]{2,4}\.\d+:\d+$')` | Regex failure |
| Spatial deduplication | `GROUP BY source_file, anchor_id, line_number HAVING COUNT(*) > 1` | Collision count > 1 |
| Context boundary | `length(context) BETWEEN 50 AND 2000` | Out-of-bounds length |
| Hallucinated reference | `LEFT JOIN canon_dimensions` on book/chapter/verse | No matching canonical coordinate |
| Provenance consistency | Cross-reference `source_file` against Git file existence | File path not found in repo |

Records failing any check are quarantined, not silently dropped.

## Decisions

| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| duckpgq for analytical exploration only; not in critical path | Community-tier with documented instability | Low — analytical use is safe; risk is only in over-reliance | Remove duckpgq; fall back to pure SQL joins (fully functional at this scale) |
| Two-step CTE for FTS+graph | Parser cannot compose the two syntaxes | None — this is the only correct pattern | N/A |
| JSONL direct ingestion, no Parquet | Below parallelization threshold; unnecessary complexity | None at current scale | Introduce Parquet ETL at >100k records |
| Recursive glob + `filename=true` for domain ingestion | Auto-discovers new domains; eliminates hardcoded `UNION ALL` | Low — depends on stable directory naming convention | Revert to explicit `UNION ALL` if directory structure changes fundamentally |
| Five-check validation quarantine layer | Prevents silent graph corruption from schema drift, duplicates, and hallucinated references | Low — each check is deterministic and independently testable | Disable individual checks (not recommended) |

## Summary of Actions for Cowork

| # | Task | Owner | Destination | Dependencies |
|---|---|---|---|---|
| 1 | Create DuckDB schema SQL: `archive_nodes` table, `archive_edges` table, `CREATE PROPERTY GRAPH` statement | Cowork | `pipeline/graph/schema.sql` | Memo 86 R1 output schema |
| 2 | Implement ingestion script: `read_json_auto` with recursive glob, `filename=true`, `split_part` domain extraction | Cowork | `pipeline/graph/ingest.py` | Task 1 |
| 3 | Implement validation quarantine layer: five checks per Section 2.4, quarantine table for failed records | Cowork | `pipeline/graph/validate_ingestion.py` | Task 2 |
| 4 | Build canon dimensions table (max chapters/verses per book) for hallucinated reference detection | Cowork | `pipeline/graph/canon_dimensions.json` | Book code registry |
| 5 | Implement FTS index creation (`PRAGMA create_fts_index` on `context` column) | Cowork | Within `schema.sql` or separate `fts_setup.sql` | Task 1 |
| 6 | Write two-step CTE query template for FTS+graph composition | Cowork | `pipeline/graph/query_templates/fts_graph_join.sql` | Tasks 1, 5 |
| 7 | Add non-zero edge count assertion after `CREATE PROPERTY GRAPH` execution | Cowork | Within `ingest.py` | Task 1 |
| 8 | Write integration test: ingest sample R1 JSONL, run validation, execute FTS+graph query, verify non-empty results | Cowork | `pipeline/graph/tests/` | Tasks 1–7 |

**Cowork execution instruction:** Read `research/GEMINI_DUCKDB_CITATION_GRAPH_20260311.md` and memo 86. Execute tasks 1–8 in order. The duckpgq risk register (Section 1) is mandatory context — every graph algorithm call must include try-catch handling per the mitigation specifications. Do not improvise implementation details beyond what the source report and this memo specify. If you encounter an ambiguity, file a question in `memos/` rather than resolving it independently.

**Critical dependency:** Tasks 1–8 cannot be validated end-to-end until memo 86 tasks 1–6 produce actual R1 JSONL output. Cowork should build and test the DuckDB layer against synthetic/sample JSONL first, then re-validate against real R1 output once available.

## Open Questions

- **duckpgq version pinning:** Should the pipeline pin a specific duckpgq version, or track latest? Recommendation: pin to the version current at implementation time and document it in `pipeline/graph/DEPENDENCIES.md`. Upgrade only after regression testing.
- **Quarantine disposition:** What happens to quarantined records? Options: (a) log-and-skip with human review queue, (b) block pipeline until resolved, (c) emit quarantine report as a memo. Recommendation: option (a) — log to `metadata/quarantine/` with a summary report; do not block the pipeline.
- **Canon dimensions source:** The hallucinated reference table requires max chapter/verse counts for every book. Should this be hand-curated or derived programmatically from the existing `canon/` files? Recommendation: derive from canon (count actual verses per chapter) and cross-check against a known reference (e.g., BibleHub verse counts).

## Handoff

**To:** `human`
**Ask:** Ratify this memo and the duckpgq risk register. Resolve open questions (or accept recommendations). Memo 86 (R1 pipeline) should be ratified first — this memo's tasks depend on R1 output.

---

**End of memo.**
