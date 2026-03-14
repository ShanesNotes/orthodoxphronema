---
paths:
  - study/**
---

## Study Layer — Companion Content

The `study/` directory contains non-scripture companion content separated from the canon substrate:
- `study/articles/{OT,NT}/` — study articles per book (76 files)
- `study/footnotes/{OT,NT}/` — verse-linked footnotes per book (76 files)
- `study/lectionary-notes/{OT,NT}/` — lectionary reading notes (growing)

Rules:
- Study content NEVER appears in `canon/` files
- Study files reference canon via wikilink anchors: `[[BOOK.CH:V]]`
- These are separate from the staging sidecars (which also contain articles/footnotes during pre-promotion work)
- Photius may edit study files for cleanup and formatting fixes
- Structural changes to the study layer require Ark review
