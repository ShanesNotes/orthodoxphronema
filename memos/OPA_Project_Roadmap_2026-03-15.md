# Orthodox Phronema Archive — Project Status & Roadmap

**March 15, 2026**
Prepared by Ark (PM Agent) for Shane McCusker
Governing Document: Memo 134 | Session: Wikilinks Foundation Sprint

> *"Informing matter with meaning and expressing meaning with matter."*
> — Matthieu Pageau, *The Language of Creation*

---

## 1. Executive Summary

The Orthodox Phronema Archive is building a machine-readable corpus of the Orthodox Study Bible with a layered system of wikilinks, study materials, and a symbolic anchor layer informed by patristic theology. The project has reached a critical inflection point: the scripture foundation is substantially complete (76/76 books promoted to canon), the companion layer (articles, footnotes, lectionary notes) is maturing, and a new symbolic dimension has emerged from the integration of Matthieu Pageau's *Language of Creation* and St. Gregory of Nyssa's *Life of Moses*.

This document captures the current state of all three workstreams, the architectural vision for the symbolic anchor layer, and a prioritized roadmap for the next phase of engineering.

---

## 2. Project State Snapshot

| Component | Detail | Status |
|---|---|---|
| Canon Scripture (76 books) | 76/76 promoted, registry v1.7.6 | ✅ Complete |
| Validation Pipeline (V1–V13) | All gates operational | ✅ Complete |
| Study Articles (76 books) | Extracted, in staging | 🔄 In Progress |
| Study Footnotes (76 books) | Tiered cleanup underway | 🔄 In Progress |
| Lectionary Notes (15 books) | Extracted, needs expansion | 🔄 In Progress |
| Anchor Registry | Frozen, 76-book SBL codes | ✅ Complete |
| Pericope Index | Built for GEN, needs expansion | 🔄 In Progress |
| Knowledge Graph | ~280 entities, ~280 relations | 🔄 In Progress |
| Pageau Embeddings | 85/85 chapters, 768-dim multimodal | ✅ Complete |
| Gregory Embeddings | 33/33 sections, 768-dim text | ✅ Complete |
| Symbolic Anchor Layer | Schema designed, awaiting build | 📋 Planned |
| Wikilinks System | Design complete, build pending | 📋 Planned |
| Jethro's Council (Evaluation) | Architecture defined, soul.md pending | 📋 Planned |

---

## 3. The Three Lanes

All forward progress organizes into three braided workstreams. They are not independent — lane 1 is the foundation that lanes 2 and 3 build on, and discoveries in lane 3 refine what we need from lane 1.

### Lane 1: Scripture Source Purity

The OSB PDF scan has been the most labor-intensive dimension of this project. OCR artifacts, fused words, drop-cap failures, footnote contamination, and article bleed have required a multi-phase pipeline (parse → validate → cleanup → promote) with 13 validation gates. The bulk work is done: all 76 books are promoted and the 15 previously blocked books have been re-staged and dry-run validated.

**What Remains:** Content-level proofreading across the full canon. V-checks catch structural defects but not semantic ones. Lesson learned #20: audit pass does not mean content purity. The canon-proofreader and canon-spell-audit skills exist for this work. Priority should go to the Pentateuch and Psalms, as these are the most heavily cross-referenced books and any errors propagate through the entire graph.

**Lane 1 Action Items:**

1. Systematic spell-audit across all 76 canon books (prioritize Pentateuch, Psalms, Prophets)
2. Content-level proofreading pass on high-traffic books (GEN, EXO, PSA, ISA, JOH, ROM)
3. Footnote cleanup tier completion (dashboard at `reports/footnote_review/dashboard.json`)
4. Article wikilink audit: verify all cross-references in study articles resolve to valid anchors
5. Pericope index expansion from GEN to full OT and NT
6. Companion file promotion path: define staging → study pipeline (Lesson #18)
7. Dossier refresh for any books with stale promotion reports

### Lane 2: Deep Research & Engineering Design

Four Gemini deep research reports have been synthesized into our design artifacts. Two more are pending. The research has directly informed the wikilinks context injection design, the autoresearch hyperparameter framework, and the conciliar evaluation architecture (Jethro's Council). The key design documents are living artifacts that need to be updated as the symbolic layer matures.

**Research Synthesis Status:**

| Research Prompt | Location | Status |
|---|---|---|
| State of the Art in RAG/GraphRAG | `research/GEMINI_State of the Art...` | ✅ Complete |
| Autoresearch Pattern Deep Dive | `research/GEMINI_Autoresearch...` | ✅ Complete |
| Computational Liturgical Calendar | `research/GEMINI_Computational...` | ✅ Complete |
| Patristic Citation Networks | `research/GEMINI_Patristic Citation...` | ✅ Complete |
| Token Budget Optimization | `research/GEMINI_LLM_Multi-Hop_Retrieval_Token_Management.md` | ✅ Complete |
| Relevance Realization | `research/GEMINI_Cognitive_AI_for_Textual_Relevance.md` | ✅ Complete |

**Design Documents:**

| Document | Location | Status |
|---|---|---|
| Wikilinks Context Injection Design | `research/wikilinks_context_injection_design.md` | ✅ Complete |
| Jethro's Council Architecture | `research/jethros_council_architecture.md` | ✅ Complete |
| Senior PM Optimization Review | `memos/134_senior_pm_optimization_review.md` | ✅ Complete |
| Symbolic Anchor Layer Spec | (to be written) | 📋 Planned |
| Symbolic Lexicon Schema | (to be extracted from Pageau) | 📋 Planned |

**Lane 2 Action Items:**

1. ~~Ingest Token Budget Optimization research when Shane uploads to `/research`~~ ✅ Done 2026-03-15
2. ~~Run and ingest Relevance Realization deep research prompt (#6)~~ ✅ Done 2026-03-15
3. Update wikilinks context injection design with liturgical rank field and phase function
4. Write symbolic anchor layer specification memo (informed by Pageau + Gregory)
5. Extract symbolic lexicon JSON from Pageau embeddings (alphabet, vocabulary, grammar, operations)
6. Ratify Jethro's Council as governing memo; author soul.md files for five council members
7. Pressure-test autoresearch hyperparameters against token budget research findings

### Lane 3: The Symbolic Layer & Phronema Vision

This is the heart of the project's distinctiveness. The embedding of Pageau's *Language of Creation* (85 chapters, multimodal) and Gregory of Nyssa's *Life of Moses* (33 sections) has created a queryable symbolic reference corpus. The insight is that biblical symbols operate as a language with an alphabet (polarities: heaven/earth, light/dark, seed/flesh), a vocabulary (specific symbols formed by those polarities), and a grammar (operations: inform/express, name/eat, descend/ascend).

Gregory provides the syntax — how symbols compose into narrative chains of spiritual ascent. His threefold progression (Light → Cloud → Darkness) traces how divine knowledge deepens through sequential theophanic encounters. This is the missing "syntax" layer that connects Pageau's static symbol vocabulary into dynamic narrative arcs.

**Key principle:** The symbolic anchor layer should aim for simple, elegant solutions. The pericope is the natural retrieval unit. Symbolic anchors group pericopes by theological image, not by verse number. The system builds maximally and filters at query time via phronema mode presets.

**What We Have:** Pageau embeddings (85 chapters, 768-dim multimodal vectors at `metadata/embeddings/pageau/chapters.jsonl`). Gregory embeddings (33 sections, 768-dim text vectors at `metadata/embeddings/gregory/sections.jsonl`). Both queryable via `pipeline/research/query_pageau.py` and a forthcoming `query_gregory.py`. Chapter manifests with symbolic topic tags for filtered retrieval.

**What We Need to Build:** The symbolic lexicon (structured JSON of Pageau's alphabet, vocabulary, grammar). The symbolic anchor registry (new graph layer above verse anchors). Wikilinks in Gregory's *Life of Moses* connecting his theoria to canon anchors. A proof-of-concept symbolic anchor for a single pericope (the burning bush, Exodus 3) demonstrating the full architecture.

**Lane 3 Action Items:**

1. Build query tool for Gregory embeddings (`query_gregory.py`)
2. Extract symbolic lexicon JSON from Pageau (polarities, operations, scales)
3. Wikilink Gregory's endnotes: parse scripture references from notes (pp. 80–134)
4. Build proof-of-concept symbolic anchor: the burning bush (EXO.3:1-6)
5. Design pericope-to-symbolic-anchor mapping schema
6. Embed additional patristic sources as they become available (Maximus, Philokalia)
7. Ingest Pageau's second book when published
8. Explore PTA (Patristic Text Archive) for machine-extractable citation boundaries
9. Integrate orthocal.info API for liturgical calendar context in graph

---

## 4. Architectural Vision: The Symbolic Anchor Layer

The central architectural insight from this session is that verse-level anchors (`[[GEN.1:1]]`) are necessary but insufficient. The Church Fathers did not engage scripture at the verse level — verse numbering is a 13th/16th century projection. They engaged through symbolic images, narrative arcs, and theological movements. The symbolic anchor layer represents this patristic mode of engagement.

**Three-Layer Resolution:**

Layer 1 — Knowledge Graph (routing): Entity nodes, typed edges, topic threads. Answers the question: what is connected to what?

Layer 2 — Backlink Shards (storage): Enriched per-anchor records with verse text, pericope context, footnotes, cross-references.

Layer 3 — Pericope Bundles (delivery): The actual context payload delivered to an agent, assembled at query time from layers 1 and 2, filtered by phronema mode presets.

**The Symbolic Dimension:** Above these three layers sits the symbolic anchor layer, informed by Pageau's type system. Each symbolic anchor carries: a polarity (the heaven/earth pair it embodies), an operation (the grammar verb: inform, express, name, eat, descend, ascend), four-scale interpretations (cosmic, individual, communal, intercommunal), verse ranges, related instances and opposites, and patristic witnesses.

Gregory's *Life of Moses* provides the syntax — how symbols compose into narrative chains. His threefold ascent (Light → Cloud → Darkness) shows that symbolic anchors are not isolated nodes but form directional sequences of deepening knowledge. This is the "sentence structure" of the symbolic language.

**Design Principle:** Build maximally, filter at query time. Every discoverable connection gets a graph edge. The four phronema mode presets (quick, devotional, study, phronema) control traversal depth and token budget at read time. The graph itself is maximal; the experience is curated.

---

## 5. Embedding Infrastructure

| Source | Chunks | Words | Model | Dims | Storage |
|---|---|---|---|---|---|
| Pageau (*Language of Creation*) | 85 chapters | 57,810 | gemini-embedding-2-preview | 768 | `metadata/embeddings/pageau/` |
| Gregory (*Life of Moses*) | 33 sections | ~56,000 | gemini-embedding-2-preview | 768 | `metadata/embeddings/gregory/` |
| OSB Canon (76 books) | Pending | ~500,000+ | TBD | 768 | `metadata/embeddings/canon/` |
| OSB Footnotes | Pending | ~200,000+ | TBD | 768 | `metadata/embeddings/footnotes/` |

All embeddings use 768-dimensional vectors with RETRIEVAL_DOCUMENT task type. Pageau uses multimodal PDF embedding (text + diagrams). Gregory uses text-only. Future canon embeddings will use pericope-level chunking aligned to the pericope index. The embedding space is incompatible between gemini-embedding-001 and gemini-embedding-2-preview; all sources must use the same model.

---

## 6. Key Lessons Learned (Session)

1. The granularity mismatch is the fundamental problem: verse-level anchors don't match how the Fathers engaged scripture. The symbolic anchor layer is the solution.

2. Pageau's framework is a type system, not just a hermeneutic. The polarities, operations, and scales are machine-representable and can be encoded in a structured lexicon.

3. Gregory's "allusions" are not allusions — they are fluent readings in the symbolic language. The condescension of modern philology toward patristic engagement with scripture reflects a failure to recognize the grammar, not a deficiency in the Fathers.

4. The Fathers' own voices are the community summaries. LLM-generated theological digests are inferior to patristic commentary. The `community_summary` field in backlink shards should contain actual patristic text, not synthetic summaries.

5. Jethro's Council was architecturally fitting before we knew why — it instantiates Pageau's pattern of authority distribution (Exodus 18, the same pattern Pageau analyzes in Chapter 24).

6. Multimodal embeddings preserve Pageau's diagrams alongside text — the diagrams ARE the symbolic grammar in visual form, not mere illustrations.

7. Simple, elegant solutions should be preferred. The pericope is the natural unit. The symbolic anchor groups pericopes by theological image. The system builds maximally and filters at query time.

---

## 7. Next Session Priorities

**Immediate:** ~~Ingest Token Budget Optimization research report~~ ✅ Ingested 2026-03-15. Key findings indexed in knowledge graph. Directly informs: position-aware context assembly, adaptive budget allocation per shard relevance, synthesis checkpoint architecture (Jethro's Council), and phronema mode token budgets.

**Near-term:** Build the symbolic lexicon JSON from Pageau's framework. This is the machine-queryable type system that agents will use when constructing symbolic anchors.

**Near-term:** Build a proof-of-concept symbolic anchor for the burning bush (EXO.3:1-6) using both embedded corpora. This validates the architecture end-to-end.

**Ongoing:** Continue canon proofreading on high-traffic books. The foundation must be pure for the graph to be trustworthy.

**Ongoing:** Expand pericope index across the full canon. Pericopes are the natural retrieval unit and the building block of symbolic anchors.

---

*Glory to God for all things.*
