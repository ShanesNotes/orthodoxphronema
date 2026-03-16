# Phase 3 Ratified Specification — 2026-03-11

**Author:** `ark`
**Type:** `decision`
**Status:** `ratified`
**Scope:** Phase 3 hyperlinking architecture — governing document
**Workstream:** `phase3-design`
**Phase:** `3`
**Supersedes:** `research/PHASE3_SPEC_SKELETON_20260310.md`, `research/PHASE3_SPEC_SKELETON_20260310_1.md`
**Superseded by:** `none`
**Inputs reconciled:**
- `research/GROK_ENGINEERING_AUDIT_20260310.md`
- `research/GEMINI_BACKLINK_SCHEMA_20260310.md`
- `research/GROK_PHASE_3_LAYER_3_IMPLEMENTATION.md`
- `memos/86_anchor_extraction_pipeline_research_synthesis.md` (R1 pipeline)
- `memos/87_duckdb_citation_graph_research_synthesis.md` (DuckDB + duckpgq risk register)
- `research/RESEARCH_ARCHITECTURAL_PARADIGMS_20260310.md`

---

## Purpose

This memo consolidates the Phase 3 architecture into a single ratified reference document. It merges the two spec skeleton drafts (2026-03-10 and 2026-03-10_1), incorporates all five closed adjudications, and integrates the R1 pipeline and DuckDB memos (86, 87) by reference. This is the constitutional document for Phase 3. Cowork, Ezra, and all downstream agents should reference this memo — not the superseded skeleton files — for architectural decisions.

---

## Frozen Architectural Decisions

All five adjudications are closed. Combined with the eight pre-existing invariants, the complete frozen decision set is:

### Core Invariants (Closed Prior to Phase 3)

1. **OSB sole source.** No external text injected into canon.
2. **Canon immutability.** `canon/{OT|NT}/` files are read-only after promotion. Phase 3 generates zero writes to canon.
3. **Single-writer Ark.** Any operation touching `canon/` requires Ark as single writer. Not relaxed.
4. **Flat-file primacy.** Markdown + Git is the source of truth. DuckDB is derived only.
5. **Idempotent pipelines.** All transformations are reconstructible from source.
6. **Source purity.** Patristic and liturgical content never originates from non-OSB sources.
7. **One-verse-per-line.** Invariant in all canon files.
8. **Docling primary / pdftotext recovery-only.** Codified in `pipeline/EXTRACTION_POLICY.md`.

### Closed Adjudications

| ADJ | Decision | Rationale |
|---|---|---|
| **ADJ-1** | Backlink filename separator: **hyphen** (`PSA.44-10.json`) | Unambiguous, cross-platform. Dot separates book from chapter; hyphen separates chapter from verse in filenames. |
| **ADJ-2** | `[[BOOK.CH:V]]` wikilink syntax: **everywhere outside canon** — phronema, notes, articles, internal cross-refs within footnotes | Uniform extraction scope. R1 extractor scans all non-canon Markdown. No syntax ambiguity between file types. |
| **ADJ-3** | Domain-sharded rollout: **pre-sharded from day one** (`liturgical/`, `patristic/`, `study/`) | Mid-phase migration is high-risk. DuckDB layer already assumes this structure. Implementation cost is minimal. |
| **ADJ-4** | Canon directory structure: **`canon/OT/`** and **`canon/NT/`** (subdivided by testament) | Live-repo verified. `canon_uri` format locked: `canon/{OT|NT}/BOOK.md#BOOK.CH:V` |
| **ADJ-5** | V11/V12: **informational only**, not promotion gates | Phase 3 initiation not blocked by V11/V12 backfill. These checks remain useful for reporting but are not gatekeepers. |

---

## Three-Layer Architecture

### Layer 1 — Canonical Flat-File Layer (immutable; Git-native)

The unchangeable substrate. Phase 3 does not alter this layer.

```
canon/
  OT/  GEN.md, EXO.md, PSA.md ... (49 promoted)
  NT/  (empty; 27 books in staging/validated/NT/)
staging/validated/{OT,NT}/
  BOOK.md
  BOOK_footnote_markers.json
  BOOK_editorial_candidates.json
  BOOK_residuals.json
phronema/
  patristics/*.md
  liturgics/*.md
  saints/*.md
notes/BOOK_footnotes.md
articles/BOOK_articles.md
```

Phase 3 interactions: phronema, notes, and articles files contain outbound `[[BOOK.CH:V]]` references. R1 extractor (memo 86) scans these files and emits JSONL. Canon files are never scanned for outbound references — they are targets only.

### Layer 2 — Domain-Sharded Backlink Schema (derived; regeneratable)

Per-anchor JSON files recording all inbound links. Human-readable, Git-diffable. Write output of the Phase 3 extraction pipeline; read input for Layer 3.

```
metadata/
  anchor_backlinks/
    liturgical/  PSA.44-10.json
    patristic/   PSA.44-10.json
    study/       PSA.44-10.json
```

Per-file schema:

```json
{
  "anchor_id": "PSA.44:10",
  "canon_uri": "canon/OT/PSA.md#PSA.44:10",
  "text_tradition": "LXX",
  "generated_at": "<ISO-8601>",
  "generator_version": "<pipeline semver>",
  "links": [
    {
      "source_file": "phronema/liturgics/theotokos_entrance.md",
      "source_anchor": "FEAT.NOV21.MATINS",
      "link_type": "prokeimenon",
      "service": "Matins",
      "entity": "Entrance of the Theotokos"
    }
  ]
}
```

Generation rules: never hand-authored, always pipeline-generated, pre-sharded from first run. Missing or corrupted file = pipeline error, not content loss.

### Layer 3 — Regeneratable Derived Graph (DuckDB)

Embedded, file-based graph store populated entirely from Layer 2. Enables O(1) backlink queries, multi-hop traversals, and pre-promotion integrity validation.

**Location:** `metadata/graph/phronema_graph.duckdb`

**Schema:** Defined in memo 87. Two tables (`archive_nodes`, `archive_edges`) + `CREATE PROPERTY GRAPH` statement. duckpgq for analytical exploration only — see memo 87 risk register for stability constraints.

**Regeneration:** Drop-and-rebuild on every run. Layer 2 JSON is authoritative. Binary Git conflicts resolved by regenerating.

**V13 integrity gate:**
- Mandatory fail: dangling reference (edge target absent from nodes)
- Mandatory fail: JSON parse error in any Layer 2 file
- Warning: high-degree nodes (>50 inbound edges) — human review report
- Warning: zero-degree nodes — expected during incremental rollout

---

## Layer Interaction Map

```
[OSB PDF]
    | Docling (primary) / pdftotext (recovery only — EXTRACTION_POLICY.md)
    v
[staging/raw/]
    | V1–V9 validation
    v
[staging/validated/]  <-- BOOK_footnote_markers.json
    |                     BOOK_editorial_candidates.json
    |                     BOOK_residuals.json
    | Promotion gate (single-writer Ark)
    v
[canon/{OT|NT}/BOOK.md]  <-- IMMUTABLE AFTER PROMOTION
    |
    |  <- Phase 3 begins here; canon/ is read-only ->
    |
[phronema/*.md]  ---- outbound [[BOOK.CH:V]] references
[notes/*.md]     ---- outbound [[BOOK.CH:V]] references
[articles/*.md]  ---- outbound [[BOOK.CH:V]] references
    |
    | R1 extractor (memo 86) -> JSONL
    v
[metadata/r1_output/anchors.jsonl]                       <- R1 output
    |
    | Backlink sharding script (TBD)
    v
[metadata/anchor_backlinks/{domain}/BOOK.CH-V.json]      <- Layer 2
    |
    | pipeline/graph/regenerate_graph.py (idempotent; drop-and-rebuild)
    v
[metadata/graph/phronema_graph.duckdb]                   <- Layer 3
    |
    | V13 integrity gate
    v
[PASS] -> commit batch; update anchor_registry
[FAIL] -> block; surface to human adjudication queue
```

---

## Implementation Sequencing

Phase 3 implementation is governed by three memos, executed in strict dependency order:

| Step | Memo | What it produces | Depends on |
|---|---|---|---|
| 1 | **Memo 86** — R1 Extraction Pipeline | `pipeline/extract/r1_extractor.py`, JSONL output | Canon files exist |
| 2 | **Memo 87** — DuckDB Citation Graph | `pipeline/graph/schema.sql`, ingestion + validation scripts | Memo 86 JSONL output |
| 3 | **This memo (88)** — Integration | V13 gate wired, end-to-end validation on single book | Memos 86 + 87 complete |

Step 3 integration tasks (to be specified after steps 1–2 are validated):
- Wire R1 JSONL → backlink sharding script → Layer 2 JSON production
- Wire Layer 2 → `regenerate_graph.py` → DuckDB
- Execute V13 integrity gate on a single test book (PSA recommended — highest annotation density)
- Full corpus run on all 49 promoted OT books

---

## Technical Flag — Pending

**`INSERT OR REPLACE` in `regenerate_graph.py`:** Current drop-and-rebuild makes this a no-op, but if strategy changes to incremental, it would silently collapse duplicate anchors. Fix: replace with `INSERT INTO` + pre-population duplicate anchor scan. Low priority but must be resolved before first full-corpus regeneration. Owner: Cowork (memo 87 task scope).

---

## Completion Handshake

| Item | Status | Evidence |
|---|---|---|
| Files changed | `done` | This memo created; supersedes two skeleton files |
| Verification run | `n/a` | Architectural document — no code changes |
| Artifacts refreshed | `partial` | INDEX.md updated; ops board refresh pending |
| Remaining known drift | `present` | Ops board references stale adjudication status |
| Next owner | `human` | Ratify this memo to make it governing |

## Handoff

**To:** `human`
**Ask:** Ratify this memo as the governing Phase 3 document. Once ratified, the two superseded skeleton files in `research/` can be archived. Memos 86 and 87 become executable.

---

**End of memo.**
