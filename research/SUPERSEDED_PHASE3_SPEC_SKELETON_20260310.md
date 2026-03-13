# MEMO: ORTHODOX PHRONEMA ARCHIVE — PHASE 3 HYPERLINKING SPEC SKELETON
**Date:** 2026-03-10  
**Author:** Claude (reconciliation & synthesis)  
**File path (proposed):** `memos/PHASE3_SPEC_SKELETON_20260310.md`  
**Status:** DRAFT — governing skeleton; not a full spec. Flagged conflicts require human adjudication before this document is promoted.  
**Inputs reconciled:**
- `GROK_ENGINEERING_AUDIT_20260310.md` (Benjamin / Harper / Lucas / Grok)
- `GEMINI_BACKLINK_SCHEMA_20260310.md` (Gemini 3.1 Pro)
- Project knowledge base: README, ARK_BRIEFING_PACKET, live reports, pericope_index artifacts

---

## 0. RECONCILIATION STATUS SUMMARY

| Topic | Status |
|---|---|
| Flat-file canon as immutable source of truth | ✅ Directly compatible |
| `metadata/` as home for all derived artifacts | ✅ Directly compatible |
| Domain-sharded backlink JSON structure | ✅ Directly compatible |
| Regeneratable derived graph (DuckDB) | ✅ Complementary to Gemini layer |
| Per-anchor JSON as DuckDB input source | ✅ Complementary (explicit handoff needed) |
| Write-path choreography / Ark bottleneck | ✅ Complementary (Grok only; Gemini silent) |
| Anchor filename format (colons vs dots) | ⚠️ CONFLICT — requires adjudication |
| `[[BOOK.ch:v]]` syntax vs canonical `BOOK.CH:V` | ⚠️ CONFLICT — requires adjudication |
| Monolithic vs pre-sharded schema rollout | ⚠️ CONFLICT — requires adjudication |
| `canon_uri` directory path | ⚠️ CONFLICT — requires verification |

---

## 1. ALIGNMENT AUDIT

### 1A. Directly Compatible — Can Be Merged Without Conflict

**1. Flat-file Markdown canon as immutable source of truth.**  
Both documents independently affirm this. Grok: "Keep Markdown + frozen [[BOOK.ch:v]] anchors and minimal JSON sidecars as the immutable, Git-native source of truth." Gemini: "treats the scripture text as an immutable node and everything else as directed edges." No divergence. This is already the established invariant per README and ARK briefing.

**2. `metadata/` as the location for all derived artifacts.**  
Grok proposes `metadata/` for the DuckDB derived graph layer. Gemini proposes `metadata/anchor_backlinks/` for per-anchor JSON files. These are not in competition — they occupy different subdirectories within the same parent. The existing `metadata/pericope_index/` pattern confirms this directory is already the home for generated navigation artifacts.

**3. Domain-sharded backlink structure.**  
Gemini's hardening strategy (separating `liturgical/`, `patristic/`, `study/` into subdirectories) is consistent with the graph architecture Grok describes (typed edges). Both converge on: do not co-locate heterogeneous relationship types in a single per-anchor blob. This decision can be adopted as-is.

**4. Backlink artifacts are regeneratable derived outputs.**  
Neither document proposes that backlink files are authored by hand or that they carry canonical status. Both treat them as pipeline-generated. This aligns with the existing sidecar pattern (`BOOK_footnote_markers.json`, etc.) and the principle that `canon/` files stay minimal.

**5. Gemini's `anchor_id` format matches the established anchor convention.**  
`PSA.44:10` in Gemini's schema correctly uses the repo's `BOOK.CH:V` format. No conflict on the logical anchor identifier itself.

---

### 1B. Complementary — Address Different Layers; Both Should Be Adopted

**1. Gemini = read-path schema; Grok = write-path integrity.**  
Gemini designs the backlink JSON structure for efficient querying (what shape does `PSA.44.10.json` take? how do we prevent patristic bloat?). Grok designs the pipeline gate that validates graph completeness before promotion (no dangling references, backlink completeness, DuckDB integrity checks). These operate at different phases of the same workflow and are not substitutes. Both must be adopted.

**2. Per-anchor JSON files (Gemini) as the source that DuckDB (Grok) indexes.**  
The natural handoff: the backlink JSON files in `metadata/anchor_backlinks/` are the human-readable, Git-diffable, plain-text source of truth for linkage. DuckDB ingests these files to enable O(1) traversal queries that flat files cannot support (multi-hop, backlink completeness checks, high-degree node analytics). This is the hybrid model Grok recommends, with Gemini's schema defining the input format.

**3. Grok addresses the Ark bottleneck; Gemini is silent on it.**  
The single-writer enforcement for `canon/` serializes all promotion-touching operations. At Phase 3 scale (10k+ link insertions + backlink regeneration across 76 books), this becomes a rate-limiter. Gemini's schema does not engage with write choreography at all. Grok's concern is valid and uncontested. The resolution (parallel reads, serialized writes only for canon-touching operations) needs to be specified in the pipeline design but does not affect the schema layer Gemini designed.

**4. Grok's contamination risk analysis (Benjamin) extends Gemini's validation checklist.**  
Gemini identifies three contamination risks (footnote bleed, anchor misalignment, auxiliary witness contamination). These map directly to the V-gate system already operational in the repo (V1–V9 confirmed in live reports; V11/V12 marked MISSING on many books). Gemini's theoretical framework and Grok's first-principles audit are independently consistent with each other and with what the live pipeline already enforces. Both can be incorporated into the Phase 3 validation gate extension.

---

### 1C. In Tension — Conflicts Requiring Human Adjudication

**CONFLICT 1: Anchor filename format (colons vs dots in filenames)**  
_Gemini proposes:_ `metadata/anchor_backlinks/PSA.44.10.json` — using dots as separators in filenames.  
_Canonical anchor format:_ `PSA.44:10` — colons separate chapter and verse in the logical identifier and in canon files.  
_Tension:_ Colons are not valid in filenames on Windows and cause issues in some Unix shell contexts. Gemini silently substitutes dots, but this creates a divergence between the logical anchor ID (`PSA.44:10`) and the filename (`PSA.44.10.json`), which requires a mapping layer and introduces ambiguity (is `.44.10` chapter 44 verse 10, or chapter 44.10?).  
_Options for adjudication:_  
- (A) Adopt dots in filenames as canonical escape for colons; document the mapping explicitly in schema.  
- (B) Use a different separator (e.g., `PSA.44-10.json`) that is unambiguous and cross-platform.  
- (C) Use subdirectory structure to avoid the problem (`PSA/44/10.json`).  
**⚠️ FLAG: Human adjudication required. Do not begin generating backlink files until this is resolved.**

---

**CONFLICT 2: `[[BOOK.ch:v]]` wiki-link syntax vs. canonical `BOOK.CH:V` anchor format**  
_Grok proposes:_ Frozen `[[BOOK.ch:v]]` anchors as the hyperlink syntax for Phase 3 bidirectional linking.  
_Established archive format:_ Canonical anchor format in `canon/` files and all existing sidecars is `BOOK.CH:V` (uppercase, no brackets). Pericope index uses `GEN.1:1` format. Dossiers use `PRO.30:7` format.  
_Tension:_ Are `[[...]]` anchors a different artifact class (e.g., Obsidian-style wikilinks in phronema files pointing to scripture), or are they proposed as a replacement for the plain `BOOK.CH:V` format in canon? If the former, there is no conflict. If the latter, this contradicts established convention and would require migration.  
_Most likely interpretation:_ `[[BOOK.ch:v]]` is the link syntax used in phronema files (patristics, liturgics, saints) when those files reference scripture anchors — not a replacement for the anchor format in `canon/` files. But this is not stated explicitly by Grok.  
**⚠️ FLAG: Clarify scope of `[[...]]` syntax. Is it confined to phronema-layer files only, or does it also appear in footnotes/articles layers? The answer determines whether backlink JSON needs to store the bracket form or the bare form of the reference.**

---

**CONFLICT 3: Rollout order — monolithic schema first vs. pre-sharded from day one**  
_Gemini:_ Presents a monolithic `PSA.44.10.json` with all domains inside, then proposes sharding as a hardening strategy. The framing implies: start monolithic, migrate later.  
_Grok / Hybrid model:_ Implies typed edges from the start; DuckDB schema would likely reflect domain separation natively.  
_Tension:_ If we start monolithic and Grok's DuckDB layer is built to query a sharded structure, a migration will be required after an indeterminate number of files are generated. Migrating partially-generated backlink files mid-Phase 3 is high-risk and violates the provenance-first principle.  
**⚠️ FLAG: Recommend pre-sharded from day one to avoid mid-phase migration. But this must be decided before any backlink files are generated. Human sign-off required.**

---

**CONFLICT 4: `canon_uri` path format in Gemini schema**  
_Gemini proposes:_ `"canon_uri": "orthodoxphronema/canon/OT/PSA.md#PSA.44:10"`  
_Live repo structure (per project knowledge):_ Canon files are in `canon/` directly (e.g., per pericope_index references and book_status_dashboard). There is no confirmed `canon/OT/` or `canon/NT/` subdivision in the project knowledge.  
_Tension:_ If the live repo uses `canon/PSA.md` (flat), Gemini's `canon/OT/PSA.md` path is wrong and all generated `canon_uri` values would be invalid.  
**⚠️ FLAG: Verify live `canon/` directory structure before committing to `canon_uri` format. If OT/NT subdirectories exist, Gemini is correct. If not, the schema must be corrected before any backlink files are committed.**

---

## 2. PHASE 3 SPEC SKELETON

This skeleton defines the three-layer architecture and the handoff points between them. It is not a full spec — implementation details, agent assignments, and validation gate definitions are deferred.

### Layer 1 — Canonical Flat-File Layer (immutable; Git-native)

**Description:** The unchangeable substrate. Phase 3 does not alter this layer's content, only reads from it.

**Artifacts:**
```
canon/{OT,NT}/BOOK.md          # Promoted scripture; anchor format: BOOK.CH:V
staging/validated/{OT,NT}/BOOK.md
staging/validated/{OT,NT}/BOOK_footnote_markers.json
staging/validated/{OT,NT}/BOOK_editorial_candidates.json
staging/validated/{OT,NT}/BOOK_residuals.json
phronema/patristics/*.md        # [TBD structure]
phronema/liturgics/*.md         # [TBD structure]
phronema/saints/*.md            # [TBD structure]
notes/BOOK_footnotes.md
articles/BOOK_articles.md
```

**Phase 3 interactions:**
- Phronema files and footnote/article files will contain outbound `[[BOOK.CH:V]]` references (scope TBD — see Conflict 2).
- Canon files are read-only. Phase 3 generates no writes to `canon/`.
- Single-writer Ark enforcement remains in force for any operation that touches `canon/`.

**Invariants carried forward:**
- OSB sole source; no auxiliary witness text injected.
- One-verse-per-line in canon files.
- Commentary never bleeds into scripture files.
- All promoted books pass V1–V9 (V11, V12 must be defined and gated before Phase 3 begins — currently MISSING on most books per live dashboard).

---

### Layer 2 — Domain-Sharded Backlink Schema (derived; regeneratable)

**Description:** Per-anchor JSON files recording all inbound links from phronema, footnotes, and articles. Human-readable, Git-diffable, tool-agnostic. These are the write output of the Phase 3 hyperlinking pipeline and the read input for Layer 3.

**Proposed directory structure (pending Conflict 1 and Conflict 3 adjudication):**
```
metadata/
  anchor_backlinks/
    liturgical/
      PSA.44.10.json        # ← filename format TBD (Conflict 1)
    patristic/
      PSA.44.10.json
    study/
      PSA.44.10.json
```

**Proposed per-file schema (based on Gemini; modified):**
```json
{
  "anchor_id": "PSA.44:10",
  "canon_uri": "canon/PSA.md#PSA.44:10",    // ← path TBD (Conflict 4)
  "text_tradition": "LXX",
  "generated_at": "<ISO-8601 timestamp>",
  "generator_version": "<pipeline semver>",
  "links": [
    {
      "source_file": "phronema/liturgics/theotokos_entrance.md",
      "source_anchor": "FEAT.NOV21.MATINS",   // ← phronema anchor format TBD
      "link_type": "prokeimenon",
      "service": "Matins",
      "entity": "Entrance of the Theotokos"
    }
  ]
}
```

**Domain separation rationale (from Gemini, adopted):** High-degree nodes (GEN.1:1, PSA.50, JHN.1:1) will accumulate hundreds of patristic citations. Sharding by domain prevents liturgical lookups from paying the cost of patristic index growth. Each domain file can be paged independently in Phase 4.

**Generation rule:** Backlink files are fully regeneratable from phronema and notes source files. They are never hand-authored. A corrupted or missing backlink file is a pipeline error, not a content loss event.

**Handoff to Layer 3:** After any hyperlinking batch, the DuckDB regeneration script ingests all files under `metadata/anchor_backlinks/` and rebuilds the derived graph.

---

### Layer 3 — Regeneratable Derived Graph (DuckDB; queryable; not canonical)

**Description:** An embedded, file-based graph store populated entirely from Layer 2 JSON files. Enables O(1) backlink queries, multi-hop traversals, and integrity validation. Not a source of truth — it is always reconstructible from Layer 2. Committed to `metadata/` as a binary artifact or as exported JSON tables.

**Proposed location:**
```
metadata/
  graph/
    phronema_graph.duckdb     # or exported as graph_nodes.json + graph_edges.json
```

**Responsibilities (from Grok, adopted):**
- Backlink completeness check: every `[[BOOK.CH:V]]` reference in phronema files has a corresponding Layer 2 entry.
- Dangling reference detection: no backlink points to an anchor that does not exist in a promoted `canon/` file.
- High-degree node analytics: identify anchors with >N references for human review prioritization.
- Multi-hop query support for Phase 4 (e.g., "all feasts that cite PSA.118 via a patristic intermediary").

**Regeneration trigger:** Any merge that modifies files under `metadata/anchor_backlinks/` or `phronema/` triggers an idempotent regeneration script. This is a pre-promotion gate extension, not a real-time operation.

**Canonical status:** None. DuckDB file is a derived artifact. Git conflict on the binary is resolved by dropping and regenerating. The Layer 2 JSON files are the authoritative record.

---

### Layer Interaction Map and Handoff Points

```
[OSB PDF]
    │ Docling extraction
    ▼
[staging/raw/]
    │ V1–V9 validation (V11, V12 pending definition)
    ▼
[staging/validated/] ←─── BOOK_footnote_markers.json
    │                      BOOK_editorial_candidates.json
    │                      BOOK_residuals.json
    │ Promotion gate (single-writer Ark)
    ▼
[canon/BOOK.md]  ◄─── IMMUTABLE AFTER PROMOTION
    │
    │  ← Phase 3 begins here; canon/ is read-only from this point →
    │
[phronema/*.md]  ──── outbound [[BOOK.CH:V]] references
[notes/*.md]     ──── outbound [[BOOK.CH:V]] references
    │
    │ Backlink extraction script (Phase 3 pipeline step)
    ▼
[metadata/anchor_backlinks/{domain}/ANCHOR.json]   ← Layer 2
    │
    │ DuckDB regeneration script (idempotent)
    ▼
[metadata/graph/phronema_graph.duckdb]              ← Layer 3
    │
    │ Integrity validation gate
    │   - No dangling references
    │   - Backlink completeness
    │   - Pericope consistency
    ▼
[PASS] → commit batch; update anchor_registry
[FAIL] → block; surface errors to human adjudication queue
```

---

## 3. OPEN CONFLICTS REQUIRING HUMAN ADJUDICATION

The following items block Phase 3 initiation. They are presented without resolution — do not proceed with implementation until each is closed.

### ADJUDICATION-1: Backlink filename separator
**Question:** What character replaces the colon in `PSA.44:10` for use in filenames?  
**Stakes:** All `metadata/anchor_backlinks/` files will be named according to this decision. Changing it mid-phase requires a bulk rename and DuckDB schema migration.  
**Options:** Dot notation (`PSA.44.10`), hyphen (`PSA.44-10`), subdirectory (`PSA/44/10.json`).  
**Recommendation (for consideration):** Hyphen (`PSA.44-10.json`) — unambiguous, cross-platform, consistent with common URI fragment escaping conventions. Does not conflict with the dot already separating book code from chapter.

### ADJUDICATION-2: Scope of `[[BOOK.CH:V]]` wikilink syntax
**Question:** Is `[[...]]` syntax confined to phronema-layer `.md` files, or does it also appear in `notes/` and `articles/` files?  
**Stakes:** Determines the scope of the backlink extraction script and the completeness definition for the integrity gate.  
**Recommendation (for consideration):** Adopt `[[BOOK.CH:V]]` in phronema files only; notes and articles continue using bare `BOOK.CH:V` anchor references. Backlink extractor handles both syntaxes. Document the distinction explicitly in `CLAUDE.md` or equivalent.

### ADJUDICATION-3: Sharded vs monolithic backlink rollout
**Question:** Do we generate domain-sharded backlink files from the start of Phase 3, or begin monolithic and migrate?  
**Stakes:** A mid-phase schema migration is high-risk and violates provenance principles.  
**Recommendation (for consideration):** Pre-sharded from day one. The cost is slightly more pipeline complexity upfront; the benefit is no migration debt.

### ADJUDICATION-4: Live `canon/` directory structure
**Question:** Are promoted canon files stored as `canon/BOOK.md` (flat) or `canon/OT/BOOK.md` and `canon/NT/BOOK.md` (subdivided)?  
**Stakes:** Determines the correct value for `canon_uri` in every Layer 2 backlink file.  
**Resolution method:** Run `ls canon/` in the live repo. This is a one-command verification — no architectural decision required, only confirmation.

### ADJUDICATION-5: V11 and V12 gate definition
**Question:** V11 and V12 appear as `MISSING` on the majority of books in the live dashboard. Are these gates defined but not yet implemented, or undefined? Phase 3 should not begin on any book where validation gates are incompletely defined.  
**Stakes:** If V11/V12 are intended as Phase 2/3 tagging validators, they must be specified and operational before the first hyperlink batch.  
**Recommendation:** Block Phase 3 initiation until V11 and V12 are either (a) defined, implemented, and passing on all promoted books, or (b) explicitly scoped as Phase 3 validators and their absence marked as an acknowledged pre-condition rather than a gap.

---

## 4. NEXT ACTIONS (PENDING ADJUDICATION)

| # | Action | Owner | Blocker |
|---|---|---|---|
| 1 | Adjudicate items 1–5 above | Human | — |
| 2 | Define V11, V12 validation gates | Ark + Human | ADJ-5 |
| 3 | Draft DuckDB schema + regeneration script prototype in `pipeline/` | Benjamin / Ark | ADJ-3, ADJ-4 |
| 4 | Draft backlink extraction script (handles both bare and `[[...]]` syntax) | Ark | ADJ-2 |
| 5 | Commit this memo as governing Phase 3 document after adjudication | Human | ADJ-1–5 |
| 6 | Verify Grokipedia public schema for patristic entity overlap | Harper | External dependency |

---

## 5. ARCHITECTURAL INVARIANTS REAFFIRMED

The following are carried forward unchanged from established decisions. Nothing in either collaborator document contradicts them.

1. OSB is the sole scripture source. No external text is injected into canon.
2. `canon/` files are immutable after promotion. Phase 3 generates zero writes to them.
3. Single-writer Ark for any operation touching `canon/`. This constraint stands despite bottleneck concerns — Grok's note on serialization is a performance observation, not a proposal to relax write safety.
4. Flat-file Markdown + Git is the primary source of truth. DuckDB is a derived index, never an authority.
5. All pipeline transformations are idempotent and reconstructible from source.
6. Patristic and liturgical content never originates from Grokipedia or any non-OSB external source. External entity schemas may be referenced for structural pattern matching only.

---

**End of skeleton.** This document is ready for human review and adjudication of the five flagged conflicts. It should not be committed to `memos/` in its current form — the open conflicts must be closed first, or explicitly annotated as deferred with a rationale.
