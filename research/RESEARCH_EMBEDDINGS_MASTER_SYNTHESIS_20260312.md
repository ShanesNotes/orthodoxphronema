# MEMO: ORTHODOX PHRONEMA ARCHIVE — EMBEDDING LAYER MASTER SYNTHESIS
**Date:** 2026-03-12  
**Author:** Claude (strategic synthesis)  
**Contributors:** Grok/Lucas/Benjamin/Harper (Prompts 1–3), Gemini Deep Research (embedding architecture validation)  
**Proposed file path:** `memos/RESEARCH_EMBEDDINGS_MASTER_SYNTHESIS_20260312.md`  
**Status:** Archival-grade. Governing document for the archive's embedding layer. Synthesizes all session research. No changes to canon, schemas Layer 1, or established invariants.  
**Supersedes:** Individual session memos (Prompts 1–3) — those remain as source documents; this memo is the consolidated authority.  
**Inputs reconciled:**
- `memos/RESEARCH_EMBEDDINGS_STRATEGIC_20260312.md` (Grok Prompt 1)
- `memos/RESEARCH_EMBEDDINGS_SCHEMAS_20260312.md` (Grok Prompt 2)
- Gemini Deep Research: *Technical Validation and Domain Adaptation Framework* (March 2026)
- `memos/RESEARCH_FINE_TUNING_CRITICAL_ANALYSIS_20260312.md` (Grok Prompt 3 — critical review)

---

## 0. GOVERNING PRINCIPLE (FORMALIZED)

> **Embedding units are defined by theological coherence (OSB pericope boundary), not token count. Footnote enrichment is co-embedded within the pericope but field-separated in the derived document to preserve regenerability and auditability. All embedding artifacts are derived and regeneratable from canon. Nothing generated at embedding time is stored in or alters canon.**

This principle is now canonical for the archive's embedding layer. It closes the gap identified in session planning and integrates all subsequent research.

---

## 1. ARCHITECTURAL DECISIONS — CLOSED

The following decisions are confirmed by multi-source research alignment. They are not open for further debate without explicit human adjudication.

### 1.1 Pericope as Primary Embedding Unit — CONFIRMED

OSB section headings define the atomic embedding chunk. This is validated on four independent grounds:

- **Theological:** OSB headings are liturgically and exegetically native — they represent how the Church has always read and heard scripture, not arbitrary editorial divisions.
- **Mathematical:** BM25 and SPLADE both normalize for variable document length via `b` and `avgdl` parameters. Variable pericope size is not a retrieval problem.
- **Prior art:** SanghaGPT (Vietnamese Buddhist RAG) uses explicit semantic boundary chunking that respects textual coherence — the closest operational analogue. No system reviewed contradicts pericope-level coherence.
- **Architectural:** The pericope index (`metadata/pericope_index/BOOK.json`) already exists. Embedding at pericope level is zero-migration from the existing navigation layer.

**Rejected alternatives:** Fixed token windows (fragments the living unit the Church reads together); individual verse embedding (loses contextual signal; requires hybrid indexing with no advantage over pericope+verse fallback).

### 1.2 Field-Separated Co-Embedding — CONFIRMED

Embedding documents combine three fields but store them separately for auditability. Multi-vector late fusion at query time with explicit weighting:

| Field | Vector Weight | Rationale |
|---|---|---|
| `scripture_text` | **70%** | OSB-primacy invariant; scripture is the substrate |
| `footnotes_array` | **20%** | Patristic footnotes are OSB-native phronema — they enrich, not contaminate |
| `phronema_context` | **10%** | Liturgical/typological context; surfaces annotation without injecting non-OSB framing |

**Critical enforcement:** In footnote-dense books (Genesis, Gospels), without this weighting a single-vector approach will favor footnote content over scripture text — a direct violation of the OSB-primacy invariant. The 70/20/10 split is non-negotiable.

**Never co-embedded:** Modern editorial commentary; cross-references from non-Orthodox traditions; lexical glosses not present in OSB footnotes; auxiliary witness text (Brenton, Rahlfs) unless explicitly tagged as such.

### 1.3 Hybrid BM25 + Dense Retrieval Architecture — CONFIRMED

A dense-only approach on a small corpus (~31k verses) is prone to missing exact liturgical matches. The hybrid architecture satisfies the high-precision requirement:

- **Sparse component:** Corpus-fitted BM25 with parameters `k₁ = 1.6`, `b = 0.8`, custom vocabulary extension for Greek-derived theological terms.
- **Dense component:** Bi-encoder (GTE-Qwen or NV-Embed) for semantic reranking, utilizing field-separated vectors for late fusion.
- **Corpus-fitted IDF:** BM25 IDF statistics computed solely from the archive corpus — not from general English. This ensures Orthodox theological vocabulary (theotokos, hypostasis, troparion, prokeimenon) receives appropriate term weight rather than being treated as rare noise.

### 1.4 Instruction-Prefix Conditioning — CONFIRMED WITH SPECIFICATION

Instruction-tuned models (NV-Embed, GTE-Qwen, Nemotron-8B) reshape embedding geometry based on task prefix. Three distinct instruction types are required — not two as originally proposed:

**Document ingestion instruction:**
> "Represent this pericope from the Orthodox Study Bible, including the Septuagint scripture and its patristic footnotes, for authoritative theological retrieval."

**Scripture/patristic query instruction:**
> "Represent this Orthodox Christian theological query to find relevant scripture and patristic commentary from the Septuagint tradition."

**Liturgical query instruction (new — not in prior memos):**
> "Represent this liturgical query to find relevant scripture pericopes, feast assignments, and patristic commentary from the Orthodox Study Bible tradition."

The third instruction type is necessary because liturgical queries (e.g., "what do we sing at the Entrance of the Theotokos") do not resolve to scripture references directly — they require traversal through the phronema annotation layer. Conflating liturgical queries with scripture queries risks retrieval failure.

**Model hierarchy (by domain adaptation capability):**

| Model | Architecture | Domain Adaptation | Recommendation |
|---|---|---|---|
| Nemotron-8B | Bidirectional Llama-3.1 | Very High | Primary candidate |
| NV-Embed | Latent Attention Layer | High | Primary candidate |
| GTE-Qwen | Bidirectional Decoder-only | High | Primary candidate |
| E5-Large-Instruct | Encoder-only | Moderate | Fallback only |

### 1.5 Synthetic Fine-Tuning and SPLADE — REJECTED AS PRIMARY PATH

**Benjamin's critical engineering verdict is adopted.** The proposed synthetic fine-tuning direction conflicts with the archive's core invariants:

| Proposal | Decision | Rationale |
|---|---|---|
| LLM-generated synthetic query pairs | **Rejected as primary** | General LLMs inject Protestant/secular framing — defeats OSB-primacy |
| Full bi-encoder fine-tuning | **Rejected as primary** | Binary model artifacts cannot be Git-diffed or reconstructed from canon — violates regenerability invariant |
| SPLADE as primary sparse retrieval | **Rejected** | Requires BERT fine-tuning; 3–24× latency overhead; domain overfitting risk; corpus-fitted BM25 matches or beats SPLADE at this corpus size |
| LoRA/QLoRA on GTE-Qwen/NV-Embed | **Experimental branch only** | Technically feasible on Apple Silicon M-series; permitted only on isolated staging branch with human adjudication of every synthetic pair and explicit non-canonical marker |

**The faithful route:** Corpus-fitted BM25 + custom tokenizer extension + instruction-prefix dense retrieval. Zero training required. Fully regeneratable. Auditable.

---

## 2. SCHEMAS — ADOPTED

### 2.1 Enhanced Pericope JSON

Extends existing `metadata/pericope_index/BOOK.json`. Zero-migration confirmed by Harper — existing `start_anchor`/`end_anchor` pattern preserved.

```json
{
  "book_code": "PSA",
  "book_name": "Psalms",
  "testament": "OT",
  "pericopes": [
    {
      "heading": "The Song of the Bride",
      "start_anchor": "PSA.44:1",
      "end_anchor": "PSA.44:17",
      "chapter": 44,
      "liturgical_assignment": {
        "feast": "Entrance of the Theotokos",
        "service": "Vespers",
        "rank": "Great",
        "tone": null
      },
      "patristic_summary": "St. John Chrysostom: royal psalm of Christ and Church (OSB footnote reference)",
      "embedding_status": "ready",
      "notes_anchors": ["PSA.44:1:fn1", "PSA.44:5:fn2"],
      "phronema_refs": ["[[JOH.3:29]]", "[[REV.21:2]]"],
      "alt_versification": {
        "mt_parallel": "PSA.45",
        "note": "LXX Psalm 44 = MT Psalm 45 — Bride/Bridegroom psalm"
      }
    }
  ]
}
```

**Field notes:**
- `patristic_summary` must be brief and strictly sourced to OSB footnotes — never interpretive expansion beyond what the OSB states.
- `liturgical_assignment` draws only from existing metadata or Menaion cross-reference files — never external calendars.
- `embedding_status` extended from binary to state machine — see Section 2.4.
- `alt_versification` is **new** — absent from Grok and Gemini outputs, added here. Required to prevent silent retrieval failure on non-LXX queries (see Risk Register §4).

### 2.2 Phronema Annotation YAML Frontmatter

For files in `phronema/saints/`, `phronema/feasts/`, `phronema/typology/`.

```yaml
---
entity_type: feast                        # saint | feast | typology | patristic
entity_name: Entrance of the Theotokos
primary_anchors:
  - PSA.44:1
  - PSA.44:10
liturgical_context:
  service: Vespers
  rank: Great                             # Great | Vigil | Polyeleos | Doxology | 6-verse | Simple
  tone: 8                                 # 1-8 or null for non-tonal services
  calendar_type: fixed                    # fixed | moveable
  date_fixed: "Nov 21"                    # null if moveable
  paschal_offset: null                    # integer days from Pascha if moveable
canonical_sources:
  - OSB_footnote_PSA.44:1
  - Menaion_Nov21
phronema_links:
  - "[[PSA.44:1]]"
  - "[[JOH.3:29]]"
embedding_ready: true
query_instruction: liturgical             # scripture | patristic | liturgical
---
```

**Field notes:**
- `canonical_sources` must list only OSB or established Orthodox witnesses (Synaxarion, Menaion, Triodion). No patristic author names without explicit OSB footnote tie-in.
- `calendar_type` + `paschal_offset` handle moveable feasts — absent from Grok schema, added here to prevent ambiguity in the liturgical calendar layer.
- `query_instruction` maps the file to the correct embedding instruction type at generation time — ensures liturgical phronema files use the liturgical query instruction, not the scripture instruction.

### 2.3 Footnote-Enriched Embedding Document

Derived at runtime. Never committed to canon or staging. Regeneratable from Schema 2.1 + `notes/BOOK_footnotes.md`.

```json
{
  "document_id": "PSA.44:1-17",
  "pericope_heading": "The Song of the Bride",
  "book_code": "PSA",
  "testament": "OT",
  "scripture_text": "PSA.44:1 My heart overflows with a good word...\nPSA.44:2 My tongue is the pen of a swift writer.",
  "footnotes": [
    {
      "anchor": "PSA.44:1:fn1",
      "text": "St. John Chrysostom interprets this as...",
      "source": "OSB",
      "father": "John Chrysostom"
    }
  ],
  "liturgical_context": {
    "feast": "Entrance of the Theotokos",
    "service": "Vespers",
    "rank": "Great",
    "tone": null
  },
  "phronema_context": {
    "summary": "Patristic reading as royal psalm of Christ and Church",
    "anchors": ["[[PSA.44:1]]"],
    "query_instruction_type": "scripture"
  },
  "alt_versification": {
    "mt_parallel": "PSA.45"
  },
  "embedding_instructions": {
    "document": "Represent this pericope from the Orthodox Study Bible, including the Septuagint scripture and its patristic footnotes, for authoritative theological retrieval.",
    "vector_weights": {
      "scripture_text": 0.70,
      "footnotes_array": 0.20,
      "phronema_context": 0.10
    }
  },
  "generated_at": "<ISO-8601 timestamp>",
  "generator_version": "<pipeline semver>",
  "source_canon_uri": "canon/OT/PSA.md#PSA.44:1"
}
```

### 2.4 Embedding Status State Machine

The binary `ready`/`pending` flag from Grok is insufficient. Extended to a four-state model:

| Status | Meaning |
|---|---|
| `pending` | Pericope exists; footnotes not yet reconciled |
| `footnotes_ready` | Footnotes reconciled; liturgical assignment not yet verified |
| `ready` | All fields complete; cleared for embedding document generation |
| `excluded` | Pericope excluded from embedding (e.g., textual note sections, appendices) |

---

## 3. OPEN ENGINEERING PROBLEMS

Labeled proposals only. None are active work until human ratification.

### 3.1 Versification Mapping Layer — HIGH PRIORITY

The OSB LXX versification diverges from Hebrew/MT in several books. Known divergences:

| Book | Nature of Divergence |
|---|---|
| Psalms | LXX offset by one from Psalm 9 onward (LXX PSA.9 = MT PSA.9+10 combined; LXX PSA.44 = MT PSA.45) |
| Jeremiah | LXX follows different chapter order; approximately 1/8 shorter than MT |
| Daniel | LXX includes additional sections (Prayer of Azariah, Bel and the Dragon) not in MT |
| 1–4 Kings | MT 1–2 Samuel + 1–2 Kings |

**Proposed action:** Add `alt_versification` field to pericope JSON (adopted in Schema 2.1). Build a versification mapping table in `metadata/versification/LXX_MT_MAP.json` derived from Crosswire SWORD project alternate versification tables. This is a prerequisite for a query interface — without it, "Psalm 23" queries return the wrong psalm silently.

**Owner:** Ark  
**Blocker:** None — can proceed independently of embedding pipeline.

### 3.2 BM25 Custom Tokenizer Extension — NEXT ENGINEERING STEP

Standard tokenizers split Greek-derived terms into subwords, destroying lexical signal. Required before BM25 index is built.

**Proposed action:** Prototype corpus-fitted BM25 + tokenizer extension in `pipeline/retrieval/`. Steps:
1. Extract all Greek-derived theological terms from the archive corpus (theotokos, hypostasis, troparion, prokeimenon, parakletis, etc.)
2. Extend the BM25 analyzer vocabulary with these terms as atomic tokens
3. Compute IDF statistics solely from the archive corpus
4. Initialize BM25 with `k₁ = 1.6`, `b = 0.8`
5. Validate against a test query set (manually constructed)

**Owner:** Ark / Benjamin  
**Blocker:** Footnote reconciliation must be complete before IDF statistics are computed (footnotes are part of the corpus).

### 3.3 Embedding Document Generator — DEPENDENT ON 3.2

`pipeline/embeddings/generate_chunk.py` — reads Schema 2.1 (enhanced pericope JSON) + Schema 2.2 (phronema YAML) and outputs Schema 2.3 (embedding document) for any chosen embedding model.

**Test target:** PSA.44 first. High footnote density + confirmed liturgical assignment makes it the ideal validation pericope.

**Owner:** Benjamin  
**Blocker:** Schema 2.1 finalized (this memo); tokenizer extension (3.2).

### 3.4 Experimental Fine-Tuning Branch — GATED

If pursued, strict conditions apply:
- Isolated staging branch with explicit `non-canonical` marker in all artifacts
- Every synthetic query pair routes through human adjudication before use
- Evaluation via NDCG + manual theological spot-checks — no LLM-as-judge alone
- Fine-tuned model artifacts stored in `experiments/` never in `pipeline/`
- Human sign-off required before branch is even created

**Owner:** Human ratification required before any work begins.

### 3.5 Matryoshka Embeddings — PHASE 4 FLAG

Jina-ColBERT-v2 style prunable vectors: high-fidelity for desktop, compressed for mobile/low-resource environments. Relevant if the archive becomes a reader application. Not urgent. Flag for Phase 4 planning.

### 3.6 Cross-Lingual Byzantine Greek Retrieval — PHASE 4 FLAG

Querying in Byzantine Greek to retrieve OSB English translation. Relevant once Greek witness texts (Rahlfs/Antoniades) are ingested in Phase 2. Not urgent.

---

## 4. RISK REGISTER

| # | Risk | Severity | Status | Mitigation |
|---|---|---|---|---|
| R1 | Embedding model Protestant/secular bias despite instruction prefix | High | Open | Three-instruction-type model; prefer Nemotron-8B or NV-Embed; monitor via theological spot-check queries |
| R2 | BM25 tokenizer subword fragmentation of Greek-derived terms | High | Open | Custom vocabulary extension required before BM25 index built (see 3.2) |
| R3 | Versification mapping failure — silent wrong-psalm retrieval | High | Open | `alt_versification` field added to schema; mapping table required before query interface built (see 3.1) |
| R4 | Footnote length imbalance (Genesis, Gospels) | High | Mitigated | 70/20/10 late-fusion weighting enforces scripture primacy at retrieval layer |
| R5 | Synthetic data contamination if experimental branch pursued | High | Gated | Human adjudication required on every pair; branch isolation enforced |
| R6 | `phronema_context` field bleeds non-OSB framing | Medium | Mitigated | Field is strictly derived from OSB footnotes and phronema annotations; no new text permitted |
| R7 | Fine-tuned model artifacts become non-regeneratable | Medium | Mitigated by rejection | Primary path rejected; experimental only under strict conditions |
| R8 | No Orthodox vector-RAG precedent — pioneering uncharted space | Medium | Acknowledged | SanghaGPT is closest analogue; archive is establishing the precedent, not following it |
| R9 | Obsidian wikilink syntax `[[BOOK.CH:V]]` scope ambiguity | Medium | Open — ADJ-2 from Phase 3 spec | Awaiting human adjudication; not resolved by this research |

---

## 5. ARCHITECTURAL INVARIANTS REAFFIRMED

All established invariants from `README.md`, `ARK_BRIEFING_PACKET.md`, and prior memos carry forward unchanged. The embedding layer adds no new writes to `canon/`. The following are additionally confirmed by this research session:

1. All embedding documents are derived artifacts — regeneratable from canon + footnotes.
2. Nothing generated at embedding time is stored in or alters canon.
3. OSB is the sole canonical source for all embedding content — no external commentary, no auxiliary witnesses, no LLM-generated text in any production embedding document.
4. Embedding artifacts are Git-native and auditable — no black-box retrieval decisions.
5. The 70/20/10 vector weighting is a non-negotiable enforcement of the OSB-primacy invariant at the retrieval layer.

---

## 6. SUMMARY OF DECISIONS AND NEXT ACTIONS

| # | Decision / Action | Status | Owner |
|---|---|---|---|
| D1 | Pericope as primary embedding unit | **Closed** | — |
| D2 | Field-separated co-embedding, 70/20/10 weighting | **Closed** | — |
| D3 | Hybrid BM25 (corpus-fitted) + dense retrieval | **Closed** | — |
| D4 | Three-instruction-type prefix model | **Closed** | — |
| D5 | Synthetic fine-tuning and SPLADE rejected as primary | **Closed** | — |
| D6 | Enhanced pericope JSON schema (Schema 2.1) | **Closed** | — |
| D7 | Phronema YAML frontmatter (Schema 2.2) | **Closed** | — |
| D8 | Embedding document schema (Schema 2.3) | **Closed** | — |
| A1 | Build versification mapping table `metadata/versification/LXX_MT_MAP.json` | **Open** | Ark |
| A2 | Prototype BM25 + custom tokenizer in `pipeline/retrieval/` | **Open** | Ark / Benjamin |
| A3 | Prototype embedding document generator `pipeline/embeddings/generate_chunk.py`, test on PSA.44 | **Open — blocked on A2** | Benjamin |
| A4 | Human ratification before any experimental fine-tuning branch created | **Gated** | Human |
| A5 | Commit this memo as governing embedding layer document | **Pending** | Human |

---

## 7. PRIOR ART RECORD

For the archive's research provenance:

- **No Orthodox vector-RAG precedent exists** (confirmed March 2026). This archive is establishing the first known canonical LXX-based pericope-level embedding system.
- **SanghaGPT** — closest functional analogue. Vietnamese Buddhist RAG using Docling → semantic boundary chunking → metadata-enriched RAG. Confirms pericope-level coherence approach.
- **mcp-otzaria-server** — Jewish text corpus via MCP + Tantivy full-text search. Confirms Phase 4 MCP endpoint model; does not implement embeddings.
- **Latin BERT / Vulgate patristic adaptations** — reference detection in Latin patristic commentaries. Not retrieval fine-tuning; confirms absence of ready Orthodox retrieval models.
- **Digital Syriac Corpus, Coptic SCRIPTORIUM** — Eastern Christian digital corpora with NLP tooling; no retrieval or embedding layer yet.
- **Crosswire SWORD Project** — alternate versification tables for LXX-MT mapping. Prior art for A1.

---

**End of memo.** Ready for `git add memos/RESEARCH_EMBEDDINGS_MASTER_SYNTHESIS_20260312.md`.

*The archive was built to preserve the mind of the Church, not to optimize ML metrics at the cost of provenance. The embedding layer must reflect this — not merely technically, but as a matter of theological faithfulness.*
