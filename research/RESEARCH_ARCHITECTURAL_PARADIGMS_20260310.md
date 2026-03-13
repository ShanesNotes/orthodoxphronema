# MEMO: RESEARCH FINDINGS — ARCHITECTURAL PARADIGMS FOR STRUCTURED TEXTUAL CORPORA
**Date:** 2026-03-10
**Author:** Claude (synthesis from Gemini deep research report)
**Source document:** `research/Architectural_Paradigms.md` (Gemini 3.1 Pro, deep research)
**File path (proposed):** `memos/RESEARCH_ARCHITECTURAL_PARADIGMS_20260310.md`
**Status:** Archival-grade. No changes to canon, schemas, or invariants proposed.

---

## Purpose

This memo documents findings from the Gemini deep research report on architectural paradigms for structured textual corpora, filtered for relevance to the Orthodox Phronema Archive. It distinguishes between findings that confirm existing decisions (record only) and findings that contain new actionable signal. The full source report is preserved in `research/Architectural_Paradigms.md`.

---

## Section 1 — Confirmed Decisions (No Action Required)

The following architectural choices, already established and operational, are independently validated by the external research. They are recorded here to close these questions permanently against future challenge.

### 1.1 JSON Sidecar Architecture is Correct for This Data Profile

The report conducts a rigorous comparison of native graph databases (Neo4j, FalkorDB, Memgraph) against domain-sharded JSON sidecar approaches. Its conclusion supports the archive's architecture on four grounds specific to this project's data profile:

- **Low write concurrency.** Graph databases are optimized for massive parallel writes (social networks, fraud detection, live recommendation engines). The archive is read-heavy and mutation-averse. The infrastructural overhead of a graph database runtime is over-engineering for this problem.
- **Git as the provenance layer.** Storing backlinks as discrete JSON files makes every relationship change version-controlled, diff-able, and secured by SHA-256 checksums. A graph database would require a proprietary auditing layer to replicate what Git provides natively.
- **Filesystem as pseudo-database.** Domain-sharding backlinks into per-anchor files (e.g., `metadata/anchor_backlinks/GEN.1.1.json`) repurposes the OS filesystem's native B-tree or hash indexing as a high-performance key-value store. Direct anchor lookup is O(1) via file path resolution — no database index scan required.
- **Platform independence and durability.** Graph databases require proprietary query languages (Cypher, Gremlin) and continuously maintained runtimes. A flat-file JSON and Markdown repository is parseable by any programming language, servable via CDN or static site generators, and accessible in failure states with a text editor.

**Decision confirmed:** Flat-file Markdown + domain-sharded JSON sidecars + regeneratable DuckDB derived layer is the correct architecture. A native graph database is not warranted at any anticipated scale of this archive.

### 1.2 Deliberate Divergence from TEI / CTS URN Standards is Correct

The report addresses the Text Encoding Initiative (TEI) and Canonical Text Services (CTS) URN standards used in major digital humanities projects. Its analysis confirms that these standards were engineered for multi-institutional consortia attempting to unify disparate global libraries with high source variability and critical edition encoding requirements.

The Orthodox Phronema Archive operates as a bounded, single-source archive rooted exclusively in the Orthodox Study Bible. The complexity of TEI's XML encoding environment and CTS's API-dependent server infrastructure introduces fragility and operational overhead that is disproportionate to the archive's requirements. The archive's frozen anchor format (`BOOK.CH:V`) and deterministic directory structure achieve comparable relational density while delivering superior offline usability, mathematical auditability, and long-term durability.

**Decision confirmed:** The archive's custom anchor format is the correct choice. CTS URN adoption is not warranted. This question is closed.

### 1.3 Docling + pdftotext Hybrid Extraction Strategy is Correct

The report conducts an in-depth analysis of pdftotext (Poppler-based, heuristic coordinate mapping) versus Docling (IBM Research, DocLayNet + TableFormer neural models). It identifies pdftotext as categorically inadequate for structured archival work due to its inability to distinguish body text from footnotes, headers, and margin annotations — exactly the contamination risk this archive guards against.

The live dossiers already reflect the correct posture: Docling as primary extraction engine, pdftotext deployed surgically as a verse-recovery fallback (confirmed in TOB.13:2, TOB.14:1, 2CH.33:1 resolved entries). The report validates this as the state-of-the-art approach.

**Decision confirmed.** However, this hybrid policy currently exists only implicitly in individual dossier resolved entries. See Section 2.3 below for the one action this finding generates.

---

## Section 2 — New Signal (Actionable)

### 2.1 Live Analogues — SanghaGPT and mcp-otzaria-server

The research surfaces two live projects that are the closest known analogues to the archive's architecture and long-term trajectory.

**SanghaGPT** (github.com/hcmus-project-collection/sanghagpt): A RAG system for classical Vietnamese Buddhist texts. Uses Docling as its primary ingestion pipeline to parse complex theological PDFs into structured Markdown and JSONL. Applies Named Entity Recognition to extracted theological concepts and generates multilingual vector embeddings for semantic search. This is the closest operational precedent for the archive's Phase 1 ingestion approach applied to a religious corpus.

**mcp-otzaria-server**: An MCP (Model Context Protocol) server exposing a large corpus of Jewish texts to LLM queries. Integrates MCP alongside Tantivy (a Rust-based full-text search engine) to allow agentic AI workflows to dynamically query religious texts with high factual grounding. This project is direct prior art for a potential Phase 4 objective: exposing the Orthodox Phronema corpus to LLM agents via a standardized protocol.

**Action:** Gemini is tasked with a dedicated deep research scan on mcp-otzaria-server architecture (prompt issued separately). Findings to be filed in `research/` and reviewed before Phase 4 planning begins.

### 2.2 SpiritRAG — Planner-Executor Architecture for Theological Retrieval

The report documents SpiritRAG, a 7,500-document agentic question-answering system built over a UN archive of documents concerning religion and spirituality. Its architecture is a three-layer planner-executor-responder pattern: top-layer orchestrator agents interpret linguistic ambiguity and route tasks; middle-layer contracts define structured output requirements; bottom-layer execution agents run deterministic extraction scripts.

**Relevance:** This architecture maps cleanly onto the archive's existing agent structure (Ark as orchestrator, Ezra as auditor, Photius as extraction agent). The explicit contract layer between orchestration and execution is a pattern worth formalizing as Phase 3 agent choreography is defined. Currently the agent delegation model is described in the ARK briefing but the inter-agent contracts are not formally specified.

**Action:** When drafting the Phase 3 agent choreography spec, adopt the explicit contract-layer pattern. Ark should define structured output requirements (schemas, not prose) for each handoff between agents.

### 2.3 Pipeline Policy — Docling/pdftotext Hybrid Must Be Formally Documented

The Docling-primary / pdftotext-fallback policy is currently implicit — it exists in practice (evidenced by dossier resolved entries) but is not codified anywhere in `pipeline/`, `schemas/`, or `memos/`. As additional agents work the pipeline in Phase 1 completion, undocumented policies are a contamination risk: an agent unaware of the policy could deploy pdftotext as a primary extraction tool on a new book, introducing the layout-confusion failures the report documents.

**Action:** Ark to add a pipeline policy document at `pipeline/EXTRACTION_POLICY.md` (or equivalent) specifying:
- Docling is the mandatory primary extraction engine for all books.
- pdftotext is authorized only as a verse-recovery instrument for specific missing anchors confirmed by V-gate failure, with each use logged in the book's `BOOK_residuals.json` under classification `pdftotext_recovery`.
- No other extraction tools are authorized without explicit human ratification.

---

## Section 3 — Items Monitored, No Current Action

**Argument Mining Framework / Zero-shot agentic legal parsing:** The report documents emerging zero-shot modular workflows achieving F1 scores up to 0.8902 on legal corpus extraction tasks. Not directly applicable now but relevant if the archive expands to patristic texts that require argument-structure extraction (e.g., structured representation of a Church Father's exegetical reasoning chain). Flag for Phase 4 consideration.

**GraniteDocling / VLM acceleration:** Docling's Visual Language Model integration (GraniteDocling, MLX acceleration) supports scanned manuscript OCR. Not needed while the OSB PDF is the sole source, but relevant if the archive ever ingests scanned patristic manuscripts directly. No action now.

---

## Summary of Actions Generated

| # | Action | Owner | Destination |
|---|---|---|---|
| 1 | Deep research scan on mcp-otzaria-server architecture | Gemini | `research/MCP_OTZARIA_RESEARCH.md` |
| 2 | Formalize planner-executor contract layer in Phase 3 agent choreography spec | Ark | Phase 3 spec |
| 3 | Draft `pipeline/EXTRACTION_POLICY.md` — Docling/pdftotext hybrid policy | Ark / Cowork | `pipeline/` |

---

**End of memo.** Ready for `git add memos/RESEARCH_ARCHITECTURAL_PARADIGMS_20260310.md`.
