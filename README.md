# Orthodox Phronema Archive

A versioned, local-first archive of the 76-book Orthodox canon extracted from the Orthodox Study Bible (OSB). Scripture text is stored as plain Markdown with stable verse anchors. Commentary, footnotes, and study articles live in companion files that link back into canon via wikilinks. The entire corpus is validated, checksummed, and queryable through a DuckDB reference graph.

## Core Invariants

1. **Scripture purity** — `canon/` files contain only scripture text. No commentary, footnotes, or study articles inline.
2. **76-book scope** — the Orthodox canon (49 OT + 27 NT, including deuterocanonical books).
3. **Anchor traceability** — every reference resolves to a canon anchor (`BOOK.CH:V`).
4. **Gated promotion** — no content enters `canon/` without passing all V-checks and D-gates.

## Canon Format

```markdown
---
book_code: GEN
book_name: "Genesis"
testament: OT
canon_position: 1
source: "Orthodox Study Bible (OSB), Thomas Nelson 2008"
status: promoted
checksum: "93854d94..."
---

## Chapter 1

GEN.1:1 In the beginning God made heaven and earth.
GEN.1:2 The earth was invisible and unfinished; ...
```

One verse per line. SBL book codes. Septuagint numbering.

## Pipeline

```
src.texts/  ──▶  staging/raw/  ──▶  staging/validated/  ──▶  canon/  ──▶  metadata/
           Parse          Cleanup           Validate+Promote        Extract/Graph
```

| Stage | What it does |
|---|---|
| **Parse** | Docling PDF extraction into raw Markdown |
| **Cleanup** | Structural repair, footnote separation, OCR fix (20+ modules) |
| **Validate** | 12 composable V-checks (`pipeline/validate/checks.py`) |
| **Promote** | 7 D-gates + checksum lock (`pipeline/promote/gates.py`) |
| **Graph** | R1 extraction → backlink shards → DuckDB materialization |

## Validation Contract

| Check | Verifies |
|---|---|
| V1 | Anchor uniqueness |
| V2 | Chapter count matches registry |
| V3 | Chapter sequence (no gaps) |
| V4 | Verse sequence (monotonic) |
| V5 | No article bleed into canon |
| V6 | Required frontmatter fields |
| V7 | Completeness vs. registry totals |
| V8 | Heading integrity |
| V9 | No embedded/hidden verses |
| V10 | Brenton cross-reference for absorbed content |
| V11 | Split-word OCR artifacts |
| V12 | Inline verse-number leakage |

Promotion gates (D1-D5 + V4/V7) enforce editorial resolution, freshness, sidecar hygiene, absorbed-content checks, and human ratification before any book reaches `canon/`.

## Reference Graph

- **Wikilink parser** — `[[BOOK.CH:V]]` syntax parsed from companion files
- **R1 extractor** — typed `ReferenceRecord` JSONL output (~4,558 wikilinks across 76 books)
- **Backlink shards** — per-domain reverse index in `metadata/anchor_backlinks/`
- **DuckDB** — `archive_nodes` + `archive_edges` tables for graph queries

## Repository Structure

| Directory | Purpose |
|---|---|
| `canon/` | Promoted, validated scripture (76 files: `OT/`, `NT/`) |
| `staging/` | Pre-promotion work area (`raw/`, `validated/`) with companion sidecars |
| `pipeline/` | All pipeline code: `parse/`, `cleanup/`, `validate/`, `promote/`, `extract/`, `graph/`, `reference/` |
| `metadata/` | Generated artifacts: `r1_output/`, `anchor_backlinks/`, `pericope_index/`, `graph/` |
| `articles/` | OSB introductions, essays, appendices (separated from scripture) |
| `notes/` | Companion footnote files by testament |
| `schemas/` | JSON schemas for validation |
| `reports/` | Validation audit trail and dashboards |
| `src.texts/` | Raw source documents (immutable after intake) |
| `tests/` | 341 tests (pytest) |
| `memos/` | Internal planning and coordination memos |
| `research/` | Reference material and research notes |

## Status

- **Phase 1** — Complete. All 76 books extracted, validated, and promoted to `canon/`.
- **Phase 2** — Active. Companion layer normalization (wikilinks, footnote reindexing, purity audits).
- **Phase 3** — Scaffold built. Reference graph (R1 JSONL, backlink shards, DuckDB schema) operational.

## Tooling

| Tool | Role |
|---|---|
| Docling | PDF extraction (primary parser) |
| pdftotext | Fallback text extraction |
| DuckDB | Reference graph storage and queries |
| pytest | Test suite (341 tests) |
| Python | >= 3.11 |

Install optional dependencies:

```bash
pip install -e ".[extract]"   # docling
pip install -e ".[graph]"     # duckdb
pip install -e ".[dev]"       # pytest
```

## Further Reading

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for detailed pipeline internals, validation contract, graph schema, and design rationale.
