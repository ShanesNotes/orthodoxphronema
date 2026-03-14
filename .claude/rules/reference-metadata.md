---
paths:
  - reference/**
  - metadata/**
---

## Reference & Metadata Layers

These directories contain derived and curated content that builds on the canon substrate.

`reference/` — Human-curated OSB reference material:
- glossary.json / glossary.md
- lectionary.md / lectionary.yaml
- liturgical-crossrefs.json
- source-abbreviations, textual-variants, ot-books-compared
- Introductory articles (how-to-read-the-bible, introducing-orthodoxy, etc.)

`metadata/` — Machine-generated linkage and analysis:
- anchor_backlinks/ — reverse index from study content to canon anchors
- pericope_index/ — reading boundary indexes
- graph/ — citation and linkage graph structures
- embedding_documents/ — vector embedding source documents
- agent_ingestion/ — structured intake for experimental agents

Rules:
- Reference content is curated; treat edits carefully
- Metadata is regenerable from source data; prefer regeneration over manual fixes
- Both layers reference canon via `[[BOOK.CH:V]]` wikilink anchors
- Neither layer may modify canon files
