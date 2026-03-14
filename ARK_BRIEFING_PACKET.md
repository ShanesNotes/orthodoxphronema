# ARK BRIEFING PACKET — ORTHODOX PHRONEMA ARCHIVE

## Mission

Build a durable, local-first, versioned Orthodox corpus where Scripture is the immutable core substrate and all other texts interlink against it with traceable precision.

Git + plain-text = single source of truth. All work diff-able, auditable, pipeline-gated.

## Current State (Phase 2 complete, Phase 3 active)

- 76 canon books promoted (OT + NT — full Orthodox canon extracted from OSB)
- Wikilink syntax (`[[BOOK.CH:V]]`) applied corpus-wide
- Study layer separated: `study/articles/`, `study/footnotes/`, `study/lectionary-notes/`
- Footnote markers traced and indexed per book
- Promotion dossiers generated for all books
- Reference layer populated: glossary, lectionary, liturgical cross-refs, textual variants
- Metadata layer active: anchor backlinks, pericope index, graph structures

## Non-Negotiables

1. **OSB text purity**: never merge commentary into Scripture files.
2. **Orthodox canon scope**: 76-book framing.
3. **Separation of concerns**: scripture vs study content remain separate artifacts.
4. **Traceable linking**: every downstream quote/reference points to source Scripture anchor.
5. **Validation-first**: no silent transformations; enforce checks before promotion.

## Architecture

See `ARCHITECTURE.md` for full technical reference.

Key decisions: Git storage, Markdown + YAML frontmatter, one-verse-per-line, `BOOK.CH:V` anchors, SBL abbreviations, LXX versification, OSB canonical / Brenton auxiliary.

## Active Work Fronts

- **Phase 3 expansion**: dense patristic/theological linkage against the canon substrate
- **Companion purity**: ensuring study articles and footnotes are clean and properly anchored
- **Metadata enrichment**: embedding documents, anchor backlinks, citation graph
- **Experimental**: noah agent ingestion harness for automated research

## Tone & Expectations

Ambitious in design, conservative in rollout.
Prioritize correctness, maintainability, and verifiability over speed.
