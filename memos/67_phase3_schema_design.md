# Phase 3 Schema Design — Backlink + Patristic + Liturgical — 2026-03-10

**Author:** `ark`
**Type:** `decision`
**Status:** `draft`
**Scope:** `schemas/, metadata/anchor_backlinks/`

## Context
- OT extraction is nearly complete (45/49 promoted, 4 holdouts in final cleanup).
- Phase 3 requires metadata infrastructure: backlinks, patristic sources, liturgical references.
- Prior art: `memos/BACKLINK-SCHEMA.md` (Gemini), `memos/GROK_ENGINEERING_AUDIT_20260310.md` (Grok).
- Both external audits converge on domain-sharded per-anchor files to prevent hot-verse bloat.

## Objective
- Define 3 new JSON schemas for Phase 3 metadata layers.
- Create directory structure under `metadata/anchor_backlinks/`.
- Build generation and validation tooling.
- **Invariant:** Canon files (`canon/`) and validation pipeline remain untouched.

## Proposed Schema: `schemas/anchor_backlinks.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Anchor Backlink Entry",
  "description": "Domain-specific backlinks for a single canon anchor.",
  "type": "object",
  "required": ["anchor_id", "canon_uri", "domain", "links"],
  "properties": {
    "anchor_id": {
      "type": "string",
      "pattern": "^[A-Z0-9]+\\.\\d+:\\d+$",
      "description": "Canon anchor (e.g. GEN.1:1)"
    },
    "canon_uri": {
      "type": "string",
      "description": "Relative path to canon file + anchor fragment"
    },
    "domain": {
      "type": "string",
      "enum": ["liturgical", "patristic", "study"],
      "description": "Backlink domain shard"
    },
    "links": {
      "type": "array",
      "items": { "$ref": "#/$defs/backlink_entry" }
    }
  },
  "$defs": {
    "backlink_entry": {
      "type": "object",
      "required": ["type", "source_ref"],
      "properties": {
        "type": { "type": "string" },
        "source_ref": { "type": "string" },
        "entity": { "type": "string" },
        "service": { "type": "string" },
        "usage": { "type": "string" },
        "author": { "type": "string" },
        "work": { "type": "string" },
        "note_id": { "type": "string" },
        "file": { "type": "string" }
      }
    }
  }
}
```

## Proposed Schema: `schemas/patristic_source_metadata.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Patristic Source Metadata",
  "type": "object",
  "required": ["source_id", "author", "work", "tradition"],
  "properties": {
    "source_id": { "type": "string" },
    "author": { "type": "string" },
    "work": { "type": "string" },
    "tradition": { "type": "string", "enum": ["eastern", "western", "syriac", "coptic"] },
    "century": { "type": "integer" },
    "language": { "type": "string" },
    "edition": { "type": "string" },
    "notes": { "type": "string" }
  }
}
```

## Proposed Schema: `schemas/liturgical_reference.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Liturgical Reference",
  "type": "object",
  "required": ["ref_id", "context_type", "entity"],
  "properties": {
    "ref_id": { "type": "string" },
    "context_type": { "type": "string", "enum": ["feast", "fast", "service", "akathist", "prokeimenon", "reading"] },
    "entity": { "type": "string" },
    "calendar": { "type": "string", "enum": ["fixed", "moveable", "triodion", "pentecostarion"] },
    "date_or_week": { "type": "string" },
    "service": { "type": "string" },
    "usage": { "type": "string" },
    "source_reference": { "type": "string" }
  }
}
```

## Directory Structure

```
metadata/anchor_backlinks/
├── liturgical/    # e.g. liturgical/PSA.44.10.json
├── patristic/     # e.g. patristic/GEN.1.1.json
└── study/         # e.g. study/GEN.1.1.json
```

File naming: `{ANCHOR_ID_DOT_SEPARATED}.json` (e.g. `GEN.1.1.json` for `GEN.1:1`).

## Tooling (to build)

- `pipeline/metadata/generate_anchor_backlinks.py` — scan study articles → backlink entries
- `pipeline/metadata/validate_backlink_graph.py` — referential integrity (all anchors exist in canon)

## Decisions

| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Domain-sharded files | Prevents hot-verse bloat (PSA.50, JOH.1:1) | More files on disk | Merge to single-file later |
| Dot-separated filenames | Colons invalid in filenames on some OS | Minor naming convention | Rename script |
| `tradition` enum on patristic | Scopes early ingest to Eastern sources | May need expansion | Add enum values |
| Separate liturgical schema | Calendar structure differs from patristic | Two schemas to maintain | Merge if overlap grows |

## Open Questions
- Should backlink files include a `text_tradition` field (LXX vs MT numbering)?
- Should we version backlink entries (for future correction tracking)?
- How to handle anchors that map to different verse numbers across traditions (e.g. PSA LXX vs MT)?

## Handoff
**To:** `human`
**Ask:** Ratify schema design before implementation. Flag any domain adjustments needed.
