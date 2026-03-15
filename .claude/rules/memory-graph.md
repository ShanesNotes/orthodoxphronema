# Memory Knowledge Graph Convention

## Graph-as-Index Pattern

The Memory MCP (`memory` server) maintains a persistent knowledge graph at
`metadata/memory/knowledge_graph.jsonl`. It serves as a **lightweight index into
memos and canon**, not a replacement for either.

### How It Works

1. **Orientation queries first.** At session start or when context is needed,
   query the graph (`search_nodes`) for the relevant entity rather than reading
   full memo files. This typically costs 200–500 tokens vs 5,000–15,000 for a
   memo read.

2. **Targeted memo reads.** Each `governing_memo` entity stores its file path
   in observations. After finding the right entity, read only the specific memo
   you need.

3. **Write-through.** When creating or updating a memo, also update the graph
   entity's observations. The memo remains the source of truth; the graph is
   the index.

### Entity Types

| Type | Examples | Purpose |
|---|---|---|
| `canon_book` | GEN, PSA, REV | 76 books with path, line count, category, testament |
| `canon_collection` | OT_Canon, NT_Canon | Collection-level rollups |
| `project` | Orthodox_Phronema_Archive | Top-level project state |
| `governing_memo` | memo_validation_spec | Pointer to active governing memo file |
| `study_article` | GEN_articles | OSB study articles — one per book, linked via `companion_of` |
| `study_footnote` | GEN_footnotes | OSB footnotes — cleanup tier tracked in observations |
| `study_lectionary` | GEN_lectionary | OSB lectionary notes — 15 books covered so far |
| `study_collection` | Study_Layer | Rollup of the entire study surface |

### Relation Types

| Relation | Meaning |
|---|---|
| `belongs_to` | Book → Collection |
| `part_of` | Collection → Project |
| `governs` | Memo → what it governs |
| `companion_of` | Study file → Canon book |

### Cleanup Tier Tracking

Each `study_footnote` entity carries a `Cleanup tier:` observation reflecting
the current state from `reports/footnote_review/dashboard.json`:

- `complete` — all components verified
- `clean (marker alignment pending)` — patristic/wikilinks done, markers not
- `structurally clean (patristic pending)` — structure ok, patristic entities unresolved
- `structurally clean (wikilinks/patristic pending)` — structure ok, more work needed
- `mechanically clean only` — basic OCR cleanup done
- `needs full cleanup` — untouched

**After cleaning a book's footnotes**, update the entity:
```
add_observations: { entity: "BOOK_footnotes", observations: ["Cleanup tier: complete", "Cleaned: 2026-03-14"] }
```

### Adding New Entities

When a new governing memo is ratified or a significant project milestone occurs:

```
add_observations: { entity: "existing_entity", observations: ["new fact"] }
create_entities: [{ name: "new_entity", entityType: "type", observations: [...] }]
create_relations: [{ from: "a", to: "b", relationType: "relation" }]
```

### Storage

- File: `metadata/memory/knowledge_graph.jsonl`
- Format: One JSON object per line (`{"type":"entity",...}` or `{"type":"relation",...}`)
- Env var: `MEMORY_FILE_PATH` set in `.mcp.json`
- Not in `.gitignore` — the graph is version-controlled alongside the repo

### Current Stats

- 260 entities (76 books + 76 articles + 76 footnotes + 15 lectionary + 3 structural + 1 study collection + 13 governing memos)
- 252 relations (78 book→collection + 2 collection→project + 6 memo→governs + 152 companion→book + 14 misc)
