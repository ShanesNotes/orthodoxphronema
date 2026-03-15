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

### Relation Types

| Relation | Meaning |
|---|---|
| `belongs_to` | Book → Collection |
| `part_of` | Collection → Project |
| `governs` | Memo → what it governs |

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

- 92 entities (76 books + 3 structural + 13 governing memos)
- 84 relations (78 book→collection + 2 collection→project + 4 memo→project + memo→collection)
