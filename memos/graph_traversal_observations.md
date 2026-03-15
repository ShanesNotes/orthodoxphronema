---
title: Graph Traversal Observations — Footnote Cleanup Sprint
author: Ark
date: 2026-03-14
status: active
purpose: Capture graph-navigation patterns during footnote cleanup to inform DuckDB schema engineering
---

# Graph Traversal Observations

This memo captures what works, what's missing, and what structured metadata
would make the DuckDB production layer effective. Each batch corresponds to
~5 books cleaned.

---

## Observation Batch 1 (2026-03-14) — Patristic Alias Resolution Sprint

Context: Resolved all 76 books' patristic entity verification in a single pass by
adding 18 new entities + 1 alias update to `schemas/reference_aliases.yaml` (v2→v3).
Dashboard moved from 15/76 → 25/76 complete. This batch covers the first ~13 books
(Tier 1: structurally clean, patristic pending).

### What Worked

- **Graph-first orientation was 10x faster than file reading.** Three `search_nodes`
  queries (`Study_Layer`, `patristic pending`, `mechanically clean only`) gave the
  full work queue in ~500 tokens. Reading the 76-book dashboard.json would have been
  ~15,000 tokens.
- **Entity observations as work state.** The `Cleanup tier:` observation on each
  `study_footnote` entity carried enough state to skip reading per-book reports for
  triage. Only needed per-book reports for actual cleanup work.
- **Batch resolution via schema, not per-file editing.** The unresolved patristic
  candidates were all abbreviation-to-entity mappings. Adding aliases to the schema
  resolved 17+ occurrences across 13 books simultaneously. Graph observations let
  us identify the pattern without reading each file.

### What Was Missing

- **No `unresolved_token` entity type.** The graph tracks books and their cleanup
  tiers, but doesn't track the specific unresolved tokens (CyrAl, IgnAnt, JohnCli,
  etc.). Had to read per-book JSON reports to discover them. A `patristic_token`
  entity with `appears_in` relations would have made the alias-resolution batch
  plannable from the graph alone.
- **No `reference_schema` entity.** The aliases schema (`schemas/reference_aliases.yaml`)
  is a critical coordination surface but has no graph entity. Knowing its version,
  entity count, and last-modified date from the graph would help decide whether to
  update it or read it.
- **Ambiguity detection absent.** "St. Gregory" matches GREGORY_GREAT by default,
  but in some EZK contexts it could be Gregory the Theologian. The graph has no way
  to represent "this alias is ambiguous across N entities" — a useful signal for a
  7B model navigating citations.
- **LXX as false positive.** The patristic scanner flagged "LXX" (Septuagint) in
  PSA as an unresolved patristic candidate. The graph has no concept of "known
  non-patristic tokens" or scanner exclusions. Added SEPTUAGINT as a workaround.

### DuckDB Schema Implications

- **`patristic_citations` table.** Per-book patristic citation data is rich: entity,
  alias used, line number, context snippet. This would be a powerful DuckDB table:
  ```sql
  CREATE TABLE patristic_citations (
    book_code VARCHAR,
    line_number INT,
    entity_canonical VARCHAR,    -- JOHN_CHRYSOSTOM
    matched_alias VARCHAR,       -- JohnChr
    context VARCHAR,
    citation_type VARCHAR        -- parenthetical_abbrev | prose_mention
  );
  ```
  This enables queries like "which books cite Cyril of Alexandria most?" or
  "show me all ambiguous St. Gregory citations."

- **`entity_aliases` table.** The reference_aliases.yaml should be loadable as a
  DuckDB table for join operations:
  ```sql
  CREATE TABLE entity_aliases (
    entity_canonical VARCHAR,
    alias VARCHAR,
    entity_category VARCHAR,  -- patristic | apostolic | liturgical | biblical
    context_hint VARCHAR
  );
  ```

- **`cleanup_status` view.** A denormalized view joining book metadata with
  component pass/fail status would eliminate the need to parse dashboard.json:
  ```sql
  CREATE VIEW cleanup_status AS
  SELECT book_code, testament, line_count,
         mechanical_clean, structural_clean, marker_alignment_pass,
         wikilinks_verified, patristic_entity_verified
  FROM footnote_dashboard;
  ```

### Proposed New Entity/Relation Types

| Entity Type | Purpose | Example |
|---|---|---|
| `patristic_token` | Unresolved citation abbreviation | `{name: "CyrAl", observations: ["appears in HOS(9), LUK(7), 2PE(1)"]}` |
| `reference_schema` | Schema coordination surface | `{name: "reference_aliases", observations: ["version: 3", "path: schemas/reference_aliases.yaml"]}` |

| Relation Type | Purpose | Example |
|---|---|---|
| `appears_in` | Token → Book | `CyrAl → HOS_footnotes` |
| `resolves_to` | Token → Entity | `CyrAl → CYRIL_ALEXANDRIA` |

### Cross-Cutting Observations

- The **parenthetical abbreviation pattern** `(CyrAl)`, `(GrgGt)`, `(AmbM)` is the
  dominant citation style in OSB footnotes. A regex-based extractor for `\(([A-Z][a-zA-Z]+)\)`
  would capture ~90% of patristic citations. This is a strong signal for automated
  graph construction.
- **Ephraim false positives.** The alias "Ephraim" for EPHRAIM_SYRIAN matches the
  tribe of Ephraim in OT books (JOS, HOS). The scanner correctly flags these but
  they inflate matched_entities_count. A `citation_type` field distinguishing
  parenthetical abbreviations from prose mentions would reduce noise.
- **Wikilinks are load-bearing navigation edges.** Every footnote file has 7-60
  wikilink references to canon verses. These are the primary cross-reference edges
  and should map 1:1 to DuckDB edges with `edge_type = "footnote_references"`.

---
