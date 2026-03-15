# Planning Prompt — Footnote Cleanup Lane + Graph Learning Layer

> **Purpose:** Paste this into a Claude Code CLI session to initialize a focused
> cleanup sprint that simultaneously captures graph-traversal insights for DuckDB
> engineering.
>
> **Usage:** `claude` → paste the prompt block below

---

## Prompt

```
I need you to pick up the footnote cleanup lane on the Orthodox Phronema Archive.
Before you begin, load your briefing by reading these files:

1. CLAUDE.md (project directives + @imports)
2. AGENTS.md (agent protocol)
3. .claude/rules/memory-graph.md (knowledge graph convention)

Then orient via the memory graph — use the `memory` MCP server:
- search_nodes("Study_Layer") → get the cleanup rollup
- search_nodes("patristic pending") → find the next books to clean
- search_nodes("mechanically clean only") → find deeper-work books

**Your two concurrent objectives:**

### 1. Footnote Cleanup (the work)

Clean footnotes book-by-book in canonical order. For each book:
- Read the footnote file (path from the graph entity)
- Run spellchecker MCP against it (check_file)
- Apply the text-cleaner skill for structural/patristic/wikilink cleanup
- Validate with canon-validator skill
- Update the memory graph entity: add_observations → new cleanup tier + date
- Commit the cleaned file + updated graph

Priority order:
- First: 13 "structurally clean (patristic pending)" books (lowest friction)
- Then: 10 "mechanically clean only" books
- Then: 2 "needs full cleanup" books

### 2. Graph Traversal Observations (the meta-learning)

As you work, you are also a sensor. Pay attention to:
- Which graph queries save you the most time vs reading files
- Where the graph is missing information you need (gaps)
- What entity shapes or relation types would help a 7B model navigate
- Where wikilinks create useful jump paths vs dead ends
- What structured metadata (YAML frontmatter, anchor density, cross-ref counts)
  would make DuckDB queries more powerful
- How pericope boundaries, liturgical cross-refs, and patristic citations
  form natural graph edges

After every 5 books cleaned, write a short "graph observations" entry in:
  memos/graph_traversal_observations.md

Format:
  ## Observation batch N (date)
  - What worked: ...
  - What was missing: ...
  - DuckDB schema implications: ...
  - Proposed new entity/relation types: ...

This memo becomes first-class input for the DuckDB engineering phase.

### Constraints
- Never edit canon/ files
- Memos are the source of truth; the graph is the index
- Use the Ezra audit log convention: record what you changed and why
- If you hit ambiguity, open it in the observations memo rather than guessing
```

---

## What This Achieves

The cleanup work is real and needed. But wrapping it in the graph-learning
layer means every book cleaned is also a data point for how the project's
structured access layer should work. By the time the 76 footnotes are clean,
we'll have a rich observations memo that directly informs:

- DuckDB table schemas (what columns matter for navigation)
- YAML frontmatter standards (what metadata should live in each file)
- Wikilink topology decisions (which cross-ref patterns are load-bearing)
- The query interface a limited model would actually use

The memory graph is the prototype. The DuckDB layer is the production system.
The cleanup sprint bridges them.
