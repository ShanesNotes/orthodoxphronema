# Architecture

Technical reference for the Orthodox Phronema Archive.

## Design Thesis

The archive is built on an immutable scripture substrate with dense, traceable linkage outward. Canon text is extracted once from a single authoritative source (the Orthodox Study Bible), validated mechanically, and locked. All commentary, footnotes, study articles, and cross-references live in separate files that point back into canon via stable anchors. Nothing modifies canon after promotion.

## Substrate Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Storage | Git | Full history, diffable text, offline-first |
| Format | Markdown + YAML frontmatter | Human-readable, tooling-agnostic |
| Verse layout | One verse per line | Grep-friendly, clean diffs, anchor-addressable |
| Anchor format | `BOOK.CH:V` | Compact, unique, regex-parseable |
| Book codes | SBL abbreviations | `GEN`, `EXO`, `PSA`, `MAT`, `REV`, etc. |
| Numbering | Septuagint (LXX) | Matches the Orthodox canon (e.g. Psalm numbering) |
| Source authority | OSB canonical, Brenton auxiliary | One source of truth; Brenton used only for cross-reference |

## Pipeline Architecture

The pipeline has five composable stages. Each stage reads the output of the previous one and writes to a well-defined location.

```
src.texts/  ──▶  staging/raw/  ──▶  staging/validated/  ──▶  canon/     ──▶  metadata/
           Parse          Cleanup           Validate+Promote         Extract/Graph
                                        │
                                        └──▶  study/       (footnotes, articles, lectionary-notes)
                                        └──▶  reference/   (essays, glossary, lectionary, prayers)
```

### Stage 1: Parse (`pipeline/parse/`)

Extracts raw text from OSB PDFs using Docling.

- `osb_extract.py` — main extraction driver
- `psa_extract.py` — specialized Psalms extractor (LXX numbering)
- `article_tracker.py` — identifies and separates study article boundaries
- `chapter_tracker.py` — tracks chapter/heading structure during extraction
- `docling_probe.py` — PDF structure probing utilities

Output: `staging/raw/{OT,NT}/BOOK.md` with YAML frontmatter.

### Stage 2: Cleanup (`pipeline/cleanup/`)

Structural repair and content separation. 20+ modules handling:

- Footnote marker extraction and reindexing
- Article/commentary removal from scripture body
- OCR artifact repair (split words, fused lines)
- Chapter and verse structure normalization
- Heading cleanup and deduplication

Output: `staging/validated/{OT,NT}/BOOK.md` plus companion sidecars (`_footnotes.md`, `_articles.md`, `_residuals.json`, `_editorial_candidates.json`, `_footnote_markers.json`).

### Stage 3: Validate (`pipeline/validate/`)

Composable V-checks in `checks.py`, orchestrated by `validate_canon.py`.

| Check | Name | What it verifies |
|---|---|---|
| V1 | Anchor uniqueness | No duplicate `BOOK.CH:V` anchors |
| V2 | Chapter count | Matches registry expected count |
| V3 | Chapter sequence | Chapters are sequential, no gaps |
| V4 | Verse sequence | Verses monotonically increase within chapters |
| V5 | Article bleed | No study-article text leaked into canon |
| V6 | Frontmatter | Required YAML fields present |
| V7 | Completeness | Anchor count matches registry verse totals |
| V8 | Heading integrity | No fragment/repeated/orphan headings |
| V9 | Embedded verses | Missing verses not hidden inside adjacent lines |
| V10 | Absorbed content | Brenton cross-check for fused verse content |
| V11 | Split words | Docling column-split OCR artifacts |
| V12 | Inline leakage | Verse's own number leaked into text body |

### Stage 4: Promote (`pipeline/promote/`)

Promotion gates in `gates.py`, executed by `promote.py`. A book must pass every gate to move from `staging/validated/` to `canon/`.

| Gate | Name | What it enforces |
|---|---|---|
| D1 | Editorial | No unresolved editorial candidates |
| D2 | Freshness | Staged text unchanged since last dossier |
| D3 | Sidecar fields | Residuals use `classification` not `class` |
| D4 | Absorbed content | No residuals describing fused/absorbed content |
| D5 | Ratification | Non-empty residuals require human sign-off |
| V4 | Verse coverage | All V4 gaps documented in residuals sidecar |
| V7 | Completeness | Completeness issues require `--allow-incomplete` |

On success, `promote.py` copies the book to `canon/`, writes a SHA-256 checksum into frontmatter, and sets `status: promoted`.

### Stage 5: Extract and Graph (`pipeline/extract/`, `pipeline/graph/`, `pipeline/reference/`)

Builds a queryable reference graph from the companion layer.

1. **Wikilink parser** (`pipeline/reference/wikilinks.py`): Parses `[[BOOK.CH:V]]` references from companion files using regex (`WIKILINK_RE`, `BARE_RE`).
2. **R1 extractor** (`pipeline/extract/r1_extractor.py`): Produces typed `ReferenceRecord` JSONL output to `metadata/r1_output/`.
3. **Backlink builder** (`pipeline/graph/build_backlinks.py`): Generates per-domain backlink shards in `metadata/anchor_backlinks/`.
4. **Graph materialization** (`pipeline/graph/regenerate_graph.py`): Loads into DuckDB using `schema.sql`.
5. **Downstream agent export** (`pipeline/metadata/build_noah_queue.py`, `pipeline/metadata/export_noah_bundle.py`): Emits read-only pericope session queues and Obsidian-friendly bundle files for external agent consumers.

## Reference Graph Schema

### Wikilink Syntax

Companion files use `[[BOOK.CH:V]]` to reference canon anchors:

```
This verse echoes the creation narrative ([[GEN.1:1]]).
See also [[PSA.103:24]]-26 for the hymnic parallel.
```

### R1 ReferenceRecord

```python
@dataclass(frozen=True)
class ReferenceRecord:
    source_file: str      # e.g. "staging/validated/OT/GEN_footnotes.md"
    line_number: int
    raw_match: str        # e.g. "[[GEN.1:1]]"
    anchor_id: str        # e.g. "GEN.1:1"
    reference_type: str   # "wikilink" | "wikilink_range" | "bare"
    context: str          # surrounding text
```

### DuckDB Tables

```sql
CREATE TABLE IF NOT EXISTS archive_nodes (
    node_id VARCHAR PRIMARY KEY,
    node_type VARCHAR NOT NULL,   -- "verse", "footnote", "article"
    label VARCHAR NOT NULL,
    domain VARCHAR,
    metadata_json JSON
);

CREATE TABLE IF NOT EXISTS archive_edges (
    edge_id VARCHAR PRIMARY KEY,
    source_node_id VARCHAR NOT NULL,
    target_node_id VARCHAR NOT NULL,
    edge_type VARCHAR NOT NULL,   -- "references", "annotates"
    metadata_json JSON
);
```

## Study Layer

Per-book study material lives in `study/`, organized by content type:

| Directory | Content |
|---|---|
| `study/footnotes/{OT,NT}/` | OSB footnotes, keyed to canon anchors via wikilinks |
| `study/articles/{OT,NT}/` | Study articles, introductions, essays separated from scripture |
| `study/lectionary-notes/{OT,NT}/` | Liturgical cross-references ("this passage is read at") |

Pipeline working artifacts remain in `staging/validated/{OT,NT}/`:

| File | Purpose |
|---|---|
| `BOOK_residuals.json` | Source-ambiguity exceptions requiring human ratification |
| `BOOK_editorial_candidates.json` | Unresolved cleanup issues (blocks promotion via D1) |
| `BOOK_footnote_markers.json` | Stripped marker trace index preserving order and context |

Canon files contain only scripture. All commentary, footnotes, and editorial apparatus live in the study layer.

## Reference Layer

Standalone reference material lives in `reference/`:

| File | Content |
|---|---|
| `introduction-to-osb.md` | Editorial introduction to the Orthodox Study Bible |
| `ot-books-compared.md` | Orthodox OT canon vs. Protestant/Catholic canon comparison |
| `source-abbreviations.md` | Patristic source abbreviation key |
| `overview-of-books.md` | Bishop Basil's overview of all 76 books |
| `introducing-orthodoxy.md` | History of the Orthodox Church essay |
| `bible-gods-revelation.md` | Bishop Joseph's essay on scripture |
| `how-to-read-the-bible.md` | Bishop Kallistos Ware's essay on the Orthodox scriptural mind |
| `glossary.md` / `glossary.json` | Theological glossary (prose + structured) |
| `lectionary.md` / `lectionary.yaml` | Full liturgical reading calendar (prose + structured) |
| `liturgical-crossrefs.json` | Verse → liturgical occasion mappings |
| `textual-variants.md` | NT textual variant notes (NU-Text, M-Text) |
| `the-seventy.md` | The 70 LXX translators |
| `prayers/morning-prayers.md` | Daily morning prayers |
| `prayers/evening-prayers.md` | Daily evening prayers |

## Downstream Agent Consumption

External downstream agents may consume scripture through derived packet exports without becoming writers to the archive.

- **Location:** `metadata/agent_ingestion/noah/`
- **Queue artifact:** `session_queue.jsonl` with deterministic pericope session ordering
- **Bundle export:** `source.md`, `prompt.md`, and `journal.md` files for one or more consecutive sessions
- **Policy:** downstream vaults are read-only consumers of archive data; they never become authoritative sources for canon or staged content

## Source Authority

| Source | Role | Policy |
|---|---|---|
| Orthodox Study Bible (OSB) | Canonical | Single authoritative source for all 76 books |
| Brenton Septuagint | Auxiliary | Cross-reference only (V10 check); never overwrites OSB |
| LLM output | Proposal-only | May suggest repairs; never written to canon without human review |

See `memos/22_osb_immutability_policy.md` for the full immutability policy.

## Separation of Concerns

Scripture/commentary separation is not a convention — it is enforced by validation:

- **V5** rejects any canon file containing known article-bleed patterns.
- **D1** blocks promotion if editorial candidates (which often contain study-article OCR debris) are unresolved.
- Companion files (`_footnotes.md`, `_articles.md`) exist specifically so commentary has a place to live that is not inside `canon/`.

This separation ensures that the scripture substrate remains stable and diffable. Commentary can evolve independently without touching canon checksums.
