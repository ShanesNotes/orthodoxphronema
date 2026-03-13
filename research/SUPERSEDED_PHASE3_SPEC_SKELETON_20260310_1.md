# MEMO: ORTHODOX PHRONEMA ARCHIVE — PHASE 3 HYPERLINKING SPEC SKELETON
**Date:** 2026-03-10 (updated same-day after Grok Layer 3 implementation memo)
**Author:** Claude (reconciliation & synthesis)
**Updated by:** Claude (ADJ-1, ADJ-4 closed via Grok/Harper live-repo verification)
**File path:** `memos/PHASE3_SPEC_SKELETON_20260310.md`
**Status:** DRAFT — ADJ-1 and ADJ-4 closed. ADJ-2, ADJ-3, ADJ-5 remain open. One technical flag pending Ark review.
**Inputs reconciled:**
- `GROK_ENGINEERING_AUDIT_20260310.md` (Benjamin / Harper / Lucas / Grok)
- `GEMINI_BACKLINK_SCHEMA_20260310.md` (Gemini 3.1 Pro)
- `GROK-PHASE3_LAYER3_IMPLEMENTATION_20260310.md` (Benjamin / Harper / Grok)
- Project knowledge base: README, ARK_BRIEFING_PACKET, live reports, pericope_index artifacts

---

## 0. RECONCILIATION STATUS SUMMARY

| Topic | Status |
|---|---|
| Flat-file canon as immutable source of truth | ✅ Closed |
| `metadata/` as home for all derived artifacts | ✅ Closed |
| Domain-sharded backlink JSON structure | ✅ Closed |
| Regeneratable derived graph (DuckDB) | ✅ Closed |
| Per-anchor JSON as DuckDB input source | ✅ Closed |
| Write-path choreography / Ark bottleneck | ✅ Closed |
| Anchor filename format — ADJ-1 | ✅ CLOSED: hyphen (`PSA.44-10.json`) |
| `canon/` directory structure — ADJ-4 | ✅ CLOSED: `canon/OT/` and `canon/NT/` confirmed live |
| `[[BOOK.CH:V]]` wikilink syntax scope — ADJ-2 | ✅ CLOSED (revised): everywhere outside canon — phronema, notes, and articles all use `[[BOOK.CH:V]]`, including internal cross-refs within footnotes |
| Monolithic vs pre-sharded rollout — ADJ-3 | ✅ CLOSED: pre-sharded from day one |
| V11 / V12 gate definition — ADJ-5 | ✅ CLOSED: informational only, not promotion gates; Phase 3 not blocked |
| Technical flag: `INSERT OR REPLACE` in regeneration script | ⚠️ REVIEW REQUIRED |

---

## 1. ALIGNMENT AUDIT (FINAL)

### 1A. Directly Compatible

1. **Flat-file Markdown canon as immutable source of truth.** Affirmed by all three collaborator documents independently. No divergence.
2. **`metadata/` as the location for all derived artifacts.** Grok proposes `metadata/graph/`; Gemini proposes `metadata/anchor_backlinks/`. Distinct subdirectories, no competition. Pattern confirmed by existing `metadata/pericope_index/`.
3. **Domain-sharded backlink structure.** All three collaborators converge: separate `liturgical/`, `patristic/`, `study/` subdirectories. Adopted.
4. **Backlink artifacts are regeneratable derived outputs.** Unanimous. Never hand-authored. A missing or corrupted backlink file is a pipeline error, not content loss.
5. **Anchor logical identifier format.** `PSA.44:10` (uppercase, colon separator) is the frozen logical format across all layers. Filename escaping (hyphen) is a filesystem convention only and does not affect the logical identifier.

### 1B. Complementary (Both Adopted)

1. **Gemini = read-path schema; Grok = write-path integrity.** Non-overlapping. Both required.
2. **Layer 2 JSON files are the input source for Layer 3 DuckDB.** Explicit handoff confirmed in Grok's implementation. Layer 2 is authoritative; Layer 3 is derived.
3. **Grok addresses Ark bottleneck; Gemini is silent on it.** Single-writer constraint remains in force. Performance observation noted; no relaxation of write safety adopted.
4. **Grok's contamination risk analysis extends Gemini's validation checklist.** Maps to existing V-gate system. Both incorporated into Phase 3 gate extension.

### 1C. Closed Conflicts

**ADJ-1 — Backlink filename separator: CLOSED**
Resolution: **Hyphen escape.** `PSA.44:10` → `PSA.44-10.json`
Source: Harper live-repo verification (`metadata/anchor_backlinks/` does not yet exist; hyphen adopted as founding convention per Grok implementation).
Rationale: Unambiguous, cross-platform. Does not conflict with the dot separating book code from chapter.

**ADJ-4 — `canon/` directory structure: CLOSED**
Resolution: `canon/OT/BOOK.md` and `canon/NT/BOOK.md` (subdivided by testament).
Source: Harper live-repo verification.
`canon_uri` format locked: `canon/{OT|NT}/BOOK.md#BOOK.CH:V`
Example: `canon/OT/PSA.md#PSA.44:10`

---

## 2. PHASE 3 SPEC SKELETON

### Layer 1 — Canonical Flat-File Layer (immutable; Git-native)

**Description:** The unchangeable substrate. Phase 3 does not alter this layer's content.

**Directory structure (confirmed live):**
```
canon/
  OT/
    GEN.md, EXO.md, PSA.md ... (promoted OT books)
  NT/
    MAT.md ... (promoted NT books)
staging/validated/{OT,NT}/
  BOOK.md
  BOOK_footnote_markers.json
  BOOK_editorial_candidates.json
  BOOK_residuals.json
phronema/
  patristics/*.md       # structure TBD
  liturgics/*.md        # structure TBD
  saints/*.md           # structure TBD
notes/BOOK_footnotes.md
articles/BOOK_articles.md
```

**Phase 3 interactions:**
- Phronema, notes, and articles files contain outbound `[[BOOK.CH:V]]` references (scope TBD — ADJ-2 open).
- Phase 3 generates zero writes to `canon/`.
- Single-writer Ark enforcement remains in force for any operation touching `canon/`.

**Invariants:**
- OSB sole source; no auxiliary witness text injected.
- One-verse-per-line in canon files.
- Commentary never bleeds into scripture files.
- V11 and V12 must be resolved before Phase 3 begins (ADJ-5 open).

---

### Layer 2 — Domain-Sharded Backlink Schema (derived; regeneratable)

**Description:** Per-anchor JSON files recording all inbound links from phronema, footnotes, and articles. Human-readable, Git-diffable, tool-agnostic. Write output of the Phase 3 extraction pipeline; read input for Layer 3.

**Directory structure (ADJ-1 closed):**
```
metadata/
  anchor_backlinks/
    liturgical/
      PSA.44-10.json
    patristic/
      PSA.44-10.json
    study/
      PSA.44-10.json
```

**Per-file schema (Gemini base; updated for closed adjudications):**
```json
{
  "anchor_id": "PSA.44:10",
  "canon_uri": "canon/OT/PSA.md#PSA.44:10",
  "text_tradition": "LXX",
  "generated_at": "<ISO-8601 timestamp>",
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

**Generation rules:**
- Never hand-authored. Always pipeline-generated.
- Pre-sharded by domain from day one (ADJ-3 recommendation — awaiting human sign-off).
- Missing or corrupted file = pipeline error, not content loss. Regenerate from source.

**Handoff to Layer 3:** After any hyperlinking batch, `pipeline/graph/regenerate_graph.py` ingests all files under `metadata/anchor_backlinks/` and rebuilds DuckDB.

---

### Layer 3 — Regeneratable Derived Graph (DuckDB)

**Description:** Embedded, file-based graph store populated entirely from Layer 2. Enables O(1) backlink queries, multi-hop traversals, and pre-promotion integrity validation. Not canonical — always reconstructible.

**Location:** `metadata/graph/phronema_graph.duckdb`

**Schema (from `pipeline/graph/schema.sql` — Grok, ready to commit):**

```sql
CREATE TABLE IF NOT EXISTS nodes (
    anchor_id TEXT PRIMARY KEY,
    book_code TEXT NOT NULL,
    chapter INTEGER NOT NULL,
    verse INTEGER NOT NULL,
    testament TEXT NOT NULL CHECK (testament IN ('OT', 'NT')),
    text_tradition TEXT DEFAULT 'LXX',
    canon_uri TEXT NOT NULL UNIQUE,
    book_name TEXT
);

CREATE TABLE IF NOT EXISTS edges (
    edge_id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_anchor TEXT NOT NULL REFERENCES nodes(anchor_id),
    source_file TEXT NOT NULL,
    source_reference TEXT,
    link_type TEXT NOT NULL,
    domain TEXT NOT NULL CHECK (domain IN ('liturgical', 'patristic', 'study')),
    entity TEXT,
    service TEXT,
    generated_at TIMESTAMP,
    metadata JSON
);
```

**V13 integrity gate (from `pipeline/graph/INTEGRITY_GATE_SPEC.md`):**
- Mandatory fail: dangling reference (edge.target_anchor absent from nodes).
- Mandatory fail: JSON parse errors in any Layer 2 file.
- Warning: high-degree nodes (>50 inbound edges) — human review report.
- Warning: zero-degree nodes — expected during incremental rollout.

**Regeneration:** Drop-and-rebuild on every run. Git conflict on binary resolved by regenerating. Layer 2 JSON is the authoritative record.

---

### Layer Interaction Map

```
[OSB PDF]
    │ Docling (primary) / pdftotext (recovery only — see EXTRACTION_POLICY.md)
    ▼
[staging/raw/]
    │ V1–V9 validation (V11, V12: ADJ-5 open)
    ▼
[staging/validated/] ←── BOOK_footnote_markers.json
    │                     BOOK_editorial_candidates.json
    │                     BOOK_residuals.json
    │ Promotion gate (single-writer Ark)
    ▼
[canon/{OT|NT}/BOOK.md]  ◄── IMMUTABLE AFTER PROMOTION
    │
    │  ← Phase 3 begins here; canon/ is read-only →
    │
[phronema/*.md]  ──── outbound [[BOOK.CH:V]] references (scope: ADJ-2)
[notes/*.md]     ──── outbound references (syntax: ADJ-2)
    │
    │ Backlink extraction script (pipeline/graph/extract_backlinks.py — TBD)
    ▼
[metadata/anchor_backlinks/{domain}/BOOK.CH-V.json]   ← Layer 2
    │
    │ pipeline/graph/regenerate_graph.py (idempotent; drop-and-rebuild)
    ▼
[metadata/graph/phronema_graph.duckdb]                 ← Layer 3
    │
    │ V13 integrity gate
    │   - No dangling references
    │   - No JSON parse errors
    │   - High-degree node report
    ▼
[PASS] → commit batch; update anchor_registry
[FAIL] → block; surface to human adjudication queue
```

---

## 3. OPEN CONFLICTS REQUIRING HUMAN ADJUDICATION

### ADJ-2 — Scope of `[[BOOK.CH:V]]` wikilink syntax
**Question:** Is `[[...]]` syntax confined to phronema-layer `.md` files, or does it also appear in `notes/` and `articles/` files?
**Stakes:** Determines the scope of the backlink extraction script and the operational definition of "backlink completeness" in the V13 gate. The extractor must know which files to scan and which syntax to expect.
**Recommendation:** Adopt `[[BOOK.CH:V]]` in phronema files only. Notes and articles use bare `BOOK.CH:V` references. Extractor handles both syntaxes; distinction documented in `CLAUDE.md` or `pipeline/EXTRACTION_POLICY.md`.
**Blocking:** Backlink extraction script cannot be written to a final spec until this is closed.

---

### ADJ-3 — Pre-sharded rollout from day one
**Question:** Generate domain-sharded backlink files from the very first extraction run, or begin monolithic and migrate later?
**Stakes:** A mid-phase schema migration is high-risk. The DuckDB schema already walks domain subdirectories. A monolithic start would require migration before Layer 3 could be wired.
**Recommendation:** Pre-sharded from day one. Implementation cost is minimal; migration risk avoided is significant. Grok's `regenerate_graph.py` already assumes this structure.
**Blocking:** First backlink extraction run must not begin until confirmed.

---

### ADJ-5 — V11 and V12 gate definition
**Question:** V11 and V12 are `MISSING` on the majority of promoted books (GEN, EXO, LEV, EZR, and others). Are these gates defined but unimplemented, or entirely undefined?
**Stakes:** Phase 3 should not begin on books with undefined validation gates. If V11/V12 are intended as Phase 2 tagging validators or Phase 3 anchor-registry validators, they must be operational before the first hyperlinking batch.
**Recommendation:** Ark to report current V11/V12 status. Block Phase 3 initiation until they are either (a) defined, implemented, and passing on all promoted books, or (b) explicitly scoped as Phase 3 pre-conditions with their current absence formally acknowledged.
**Blocking:** Phase 3 initiation gate.

---

## 4. TECHNICAL FLAG — ARK REVIEW REQUIRED

### FLAG: `INSERT OR REPLACE` in `regenerate_graph.py`

Grok's regeneration script uses `INSERT OR REPLACE INTO nodes` when scanning canon files, but the script also drops and rebuilds the entire schema on every run before insertion. This creates a latent inconsistency:

**Current behavior:** Drop-and-rebuild makes `INSERT OR REPLACE` a no-op — there are never pre-existing rows to replace. Harmless in current form.

**Latent risk:** If the regeneration strategy is ever changed to incremental updates rather than full rebuild, `INSERT OR REPLACE` would silently overwrite existing nodes rather than surfacing duplicate anchors. A malformed canon file containing two lines matching the same anchor (e.g., two `PSA.44:10` entries from an OCR defect) would be silently collapsed rather than flagged as a pipeline error.

**The one-verse-per-line invariant means this should never occur** — but the gate should make violations visible, not silent.

**Recommended fix:** Replace `INSERT OR REPLACE` with `INSERT INTO`. Add a pre-population duplicate anchor scan over canon files. Log any duplicate found as a V13 mandatory fail, not a silent overwrite.

**Owner:** Ark / Cowork. Low priority but should be fixed before first full-corpus regeneration run.

---

## 5. NEXT ACTIONS

| # | Action | Owner | Blocker | Status |
|---|---|---|---|---|
| 1 | Close ADJ-2 (wikilink syntax scope) | Human | — | Open |
| 2 | Close ADJ-3 (pre-sharded rollout) | Human | — | Open |
| 3 | Close ADJ-5 (V11/V12 definition) | Ark + Human | — | Open |
| 4 | Fix `INSERT OR REPLACE` flag in `regenerate_graph.py` | Ark / Cowork | — | Open |
| 5 | Write `pipeline/EXTRACTION_POLICY.md` (Docling/pdftotext hybrid) | Ark | ADJ-2 | Open |
| 6 | Write `pipeline/graph/extract_backlinks.py` (Layer 2 producer) | Ark | ADJ-2 | Blocked |
| 7 | Wire `regenerate_graph.py` into promotion gate; test on single book | Ark / Cowork | ADJ-3, ADJ-5 | Blocked |
| 8 | Commit this memo as governing Phase 3 document | Human | ADJ-2,3,5 | Pending |
| 9 | Complete Phase 1 (55 books remaining) | Ark / Cowork | — | In progress |
| 10 | Gemini: MCP-Otzaria deep research | Gemini | — | In progress |
| 11 | Harper: Grokipedia patristic entity schema verification | Harper | External | Pending |

---

## 6. FROZEN ARCHITECTURAL DECISIONS

The following are closed and may not be reopened without a formal memo and human ratification.

1. OSB is the sole scripture source. No external text injected into canon.
2. `canon/{OT|NT}/` files are immutable after promotion. Phase 3 generates zero writes.
3. Single-writer Ark for any canon-touching operation. Not relaxed.
4. Flat-file Markdown + Git is the primary source of truth. DuckDB is derived only.
5. All pipeline transformations are idempotent and reconstructible from source.
6. Patristic and liturgical content never originates from Grokipedia or any non-OSB source.
7. **Backlink filename format: hyphen escape (`BOOK.CH-V.json`). Frozen. (ADJ-1)**
8. **`canon_uri` format: `canon/{OT|NT}/BOOK.md#BOOK.CH:V`. Frozen. (ADJ-4)**
9. **Domain-sharded directory structure: `liturgical/`, `patristic/`, `study/`. Frozen.**
10. Docling is the mandatory primary extraction engine. pdftotext is recovery-only.
11. **`[[BOOK.CH:V]]` syntax: everywhere outside `canon/`. Phronema, notes, and articles all use `[[BOOK.CH:V]]`, including internal cross-references within footnotes. Canon files remain untouched. Frozen. (ADJ-2, revised)**
12. **Backlink rollout: pre-sharded from day one (`liturgical/`, `patristic/`, `study/`). No monolithic phase. Frozen. (ADJ-3)**
13. **V11/V12: informational checks only, not promotion gates. Phase 3 start not blocked by backfill. Frozen. (ADJ-5)**

---

**End of skeleton.** ADJ-2, ADJ-3, ADJ-5 remain open and three remaining items block formal commit. All other architectural questions are closed.
