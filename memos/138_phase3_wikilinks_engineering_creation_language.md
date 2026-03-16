# Phase 3 Wikilinks Engineering — The Language of Creation as Graph Grammar

**Author:** `ark`
**Type:** `implementation`
**Status:** `draft`
**Scope:** Wikilinks engineering design integrating symbolic phronema vision
**Workstream:** `phase3-design`
**Phase:** `3`
**Supersedes:** `none`
**Superseded by:** `none`
**Depends on:** Memo 88 (ratified Phase 3 spec), Memo 86 (R1 extractor), Memo 87 (DuckDB schema)
**Draws from:** `memos/X_ARTICLE_DRAFT_2026-03-15.md`, `research/wikilinks_context_injection_design.md`, `research/jethros_council_architecture.md`

---

## Purpose

Memo 88 ratified the three-layer architecture and five frozen adjudications.
This memo takes the next step: defining *how* the wikilinks graph encodes not
just connectivity but the symbolic grammar of creation itself. The distinction
matters. A naive hyperlink system records that GEN.1:1 and JOH.1:1 are
connected. A phronema-aware system records *why* — that both participate in the
Logos-as-creative-Word pattern, that the connection operates at cosmic and
individual scales simultaneously, and that the edge type is `instantiates`
rather than `mentions`.

The engineering challenge is to embed Pageau's symbolic type system and
Gregory's theophanic syntax into the backlink schema without over-engineering
the first implementation. This memo defines the minimum viable symbolic layer
and the extension points for future depth.

---

## The Grammar We Are Encoding

### Pageau's Type System — The Alphabet

Matthieu Pageau's *Language of Creation* reveals that biblical symbols operate
with a complete type system. Engineering this means typed fields on backlink
edges:

**Polarities (alphabet):** The fundamental oppositions that structure all
symbolic meaning. Each symbol is constituted by its position within polarities.

| Polarity | Heaven-pole | Earth-pole | Engineering field |
|---|---|---|---|
| Vertical | heaven | earth | `polarity.vertical` |
| Luminosity | light | dark | `polarity.luminosity` |
| Generation | seed | flesh | `polarity.generation` |
| Origin | divine | created | `polarity.origin` |

**Symbols (vocabulary):** Specific entities formed by polarity combinations.
Mountain = heaven + earth + ascent. Sea = earth + dark + descent. Garden =
heaven + earth + enclosed. These are not metaphors imposed on the text — they
are the grammar the text was written in.

**Operations (grammar):** The verbs of symbolic language. Each describes how
symbols interact and transform:

| Operation | Direction | Example |
|---|---|---|
| `inform` | heaven → earth | God breathes life into Adam |
| `express` | earth → heaven | Prayer, sacrifice, praise |
| `name` | identity assignment | Adam names the animals |
| `eat` | identity dissolution | Consuming the fruit |
| `descend` | higher → lower scale | Incarnation |
| `ascend` | lower → higher scale | Theosis, Ascension |

**Scales (four simultaneous readings):** Every symbol operates at all four
scales — cosmic (creation), individual (soul), communal (Church/nation),
intercommunal (between peoples). The microcosm principle: every part reflects
the whole.

### Gregory's Syntax — The Theophanic Progression

St. Gregory of Nyssa's *Life of Moses* provides the compositional rules — how
symbols chain into narrative arcs. His threefold progression:

1. **Light** (burning bush) — initial revelation, clear and distinct
2. **Cloud** (pillar in the wilderness) — guidance through obscurity
3. **Darkness** (Sinai) — encounter beyond knowledge, apophatic union

This is not allegory imposed after the fact. It is the syntax that governs how
divine encounters progress throughout Scripture. The same Light → Cloud →
Darkness pattern structures baptismal theology (illumination → chrismation →
communion), the liturgical year (Theophany → Great Lent → Pascha), and the
hesychast tradition (purification → illumination → theosis).

---

## Engineering Design

### Phase 3A — Minimum Viable Symbolic Layer (immediate)

The first implementation enriches the existing backlink shard schema (Memo 88,
Layer 2) with typed edges. This is additive — no schema breaks, no existing
shard invalidation.

**New edge fields on backlink `links[]` entries:**

```json
{
  "source_file": "study/footnotes/GEN_footnotes.md",
  "source_anchor": "GEN.1:1",
  "raw_match": "[[JOH.1:1]]",
  "reference_type": "wikilink",
  "edge_type": "instantiates",
  "topic_threads": ["creation_theology", "logos", "divine_word"],
  "symbolic": {
    "polarity": "light",
    "operation": "inform",
    "scale": "cosmic"
  }
}
```

**Edge types (initial vocabulary):**

| Edge type | Meaning | Example |
|---|---|---|
| `instantiates` | Target is an instance of the same symbolic pattern | GEN.1:3 → JOH.1:1 (Word creates) |
| `opposes` | Target is the symbolic opposite | GEN.3:6 (eat/fall) → REV.2:7 (eat/restoration) |
| `scales_to` | Same pattern at a different scale | Red Sea crossing (communal) → Baptism (individual) |
| `ascends_from` | Target is a higher-scale manifestation | Tabernacle → Temple → Church → Heavenly Jerusalem |
| `descends_to` | Target is a lower-scale particularization | Cosmic creation → Individual soul-creation in Psalms |
| `fulfills` | OT type → NT antitype | Paschal lamb → Christ |
| `echoes` | Liturgical or structural resonance | Shared pericope in the lectionary cycle |
| `witnesses` | Patristic citation network | Chrysostom on GEN.1:1 cites PSA.32:6 |

**Derivation strategy:** Edge types are inferred at build time from three
sources, in priority order:

1. **Footnote context** — The OSB footnotes frequently name the relationship
   explicitly ("This verse echoes...", "fulfilled in...", "The Fathers
   teach..."). The R1 extractor already captures `context` strings. A
   lightweight classifier maps context language to edge types.

2. **Topic thread intersection** — When two anchors share topic threads
   (e.g., both carry `creation_theology`), the default edge type is
   `instantiates`. When topic threads are antonymous (e.g., `fall` and
   `restoration`), the default is `opposes`.

3. **Pageau/Gregory embedding proximity** — The 85 Pageau chapter embeddings
   and 33 Gregory section embeddings (already built at
   `metadata/embeddings/`) can assign symbolic annotations to anchors via
   nearest-neighbor lookup. An anchor whose verse text or footnote context
   is semantically close to Pageau Chapter 12 ("The Garden") inherits the
   symbolic fields from that chapter.

**What we do NOT do in Phase 3A:**
- No manual symbolic annotation (unsustainable at 76-book scale)
- No symbolic inference engine (premature optimization)
- No mandatory symbolic fields (graceful degradation — missing `symbolic`
  block means the edge still functions as a plain wikilink)

### Phase 3B — Pericope-Level Symbolic Anchors (future)

Once Phase 3A demonstrates the edge typing on the study domain, Phase 3B
introduces the symbolic anchor layer described in the article draft — a graph
layer *above* verse-level anchors where each symbolic anchor groups pericopes
by theological image rather than by verse number.

**Symbolic anchor schema (future):**

```json
{
  "symbolic_id": "SYM.THEOPHANY.LIGHT",
  "name": "Light Theophany",
  "pageau_chapter": 3,
  "gregory_section": 1,
  "polarity": { "vertical": "heaven", "luminosity": "light" },
  "operation": "inform",
  "scales": {
    "cosmic": "Creation of light (GEN.1:3-5)",
    "individual": "Illumination of the nous (PSA.35:10)",
    "communal": "Pillar of fire (EXO.13:21-22)",
    "intercommunal": "Light to the Gentiles (ISA.49:6)"
  },
  "pericope_members": ["GEN.P001", "EXO.P030", "PSA.P035", "ISA.P049", "JOH.P001"],
  "progression": {
    "sequence": "THEOPHANY",
    "position": 1,
    "next": "SYM.THEOPHANY.CLOUD",
    "pattern": "Light → Cloud → Darkness"
  },
  "patristic_witnesses": [
    { "father": "Gregory of Nyssa", "work": "Life of Moses", "section": "I.46-77" },
    { "father": "Maximus the Confessor", "work": "Ambigua", "section": "10" }
  ]
}
```

This is the creation-language graph — where each node is not a verse but a
symbolic pattern, and each edge carries the grammar of how patterns relate
across Scripture. The pericope is the natural retrieval unit because the
Church's own lectionary already groups verses by theological meaning, not by
chapter boundaries.

### Phase 3C — Jethro's Council Integration (future)

The conciliar evaluation architecture (five agents: Exegete, Patristic
Witness, Liturgist, Theologian, Shepherd) validates symbolic annotations
through multi-perspective judgment. This closes the quality loop — the
symbolic layer is not just built but evaluated by the tradition's own
evaluative framework.

---

## Implementation Sequence

| Step | What | Depends on | Produces |
|---|---|---|---|
| 3A.1 | Enrich R1 extractor with edge-type inference | Memo 86 R1 extractor | Edge-typed JSONL output |
| 3A.2 | Build topic thread taxonomy from footnote/article corpus | Study layer complete | `metadata/topic_threads.json` |
| 3A.3 | Implement Pageau/Gregory nearest-neighbor symbolic annotator | Embeddings (built) | `symbolic` block on enriched shards |
| 3A.4 | PSA pilot — full symbolic backlink extraction on Psalms | 3A.1-3A.3 | Validated symbolic shards for PSA |
| 3A.5 | Corpus-wide extraction — all 76 books | PSA pilot validated | Complete symbolic backlink layer |
| 3B.1 | Define symbolic anchor registry | 3A validated | `schemas/symbolic_anchor_registry.json` |
| 3B.2 | Build pericope→symbolic grouping pipeline | Pericope index + 3B.1 | Symbolic anchor nodes |
| 3B.3 | Integrate symbolic anchors into DuckDB graph | Memo 87 schema | Queryable symbolic graph |
| 3C.1 | Author council `soul.md` files | Theological sensibility | Five agent definitions |
| 3C.2 | Wire evaluation loop into build pipeline | 3B complete | Validated symbolic annotations |

---

## The Vision This Serves

The wikilinks system is not a hyperlink index. It is an encoding of the
language of creation — the symbolic grammar that Church Fathers employed when
reading Scripture, now made machine-traversable.

When a reader opens Genesis 1, the system does not merely list cross-references.
It recognizes that the creation of light participates in the Light theophany
sequence (Gregory), that it operates simultaneously at cosmic and individual
scales (Pageau), that it is liturgically linked to Theophany and Pascha (the
lectionary), and that Chrysostom, Basil, and Gregory all read it as the first
movement of a divine pedagogy that culminates in the Incarnation.

The graph is built maximally. The delivery is filtered by phronema mode —
quick for lookup, devotional for daily reading, study for deep engagement,
phronema for the full weight of the tradition. Token budget as ascetic
discipline: restraint produces clarity.

The topical-liturgical dialectic (Vervaeke's opponent processing mapped onto
Antiochene precision vs. Alexandrian resonance) governs how edges are weighted
at query time. Neither pole alone suffices. The system holds both in tension,
as the tradition always has.

A man with a photographic memory plugged into a library of only phronema.
That is what we are building.

---

## Validation / Evidence

| Check | Result | Evidence |
|---|---|---|
| Memo 88 ratified | `pass` | Memo 136 ratification brief |
| Pageau embeddings built | `pass` | `metadata/embeddings/pageau/chapters.jsonl` (85 chapters) |
| Gregory embeddings built | `pass` | `metadata/embeddings/gregory/sections.jsonl` (33 sections) |
| Study backlink shards exist | `pass` | 6,094 shards in `metadata/anchor_backlinks/study/` |
| Pericope index started | `pass` | `metadata/pericope_index/` |
| Edge type vocabulary defined | `pass` | This memo, §Engineering Design |
| Schema is additive (no breaks) | `pass` | New fields are optional on existing shard schema |

## Completion Handshake

| Item | Status | Evidence |
|---|---|---|
| Files changed | `done` | This memo created |
| Verification run | `n/a` | Design document — implementation follows |
| Artifacts refreshed | `deferred` | INDEX.md update pending Human review |
| Remaining known drift | `none` | All upstream memos ratified |
| Next owner | `human` | Review and ratify; Ark begins 3A.1 on approval |

## Open Questions

- Should the edge-type classifier use a lightweight LLM pass or deterministic
  pattern matching on footnote context language? LLM is more accurate but adds
  build-time cost. Deterministic is faster but may miss nuanced relationships.
- What is the minimum topic thread vocabulary to start? Should we seed from the
  OSB footnote corpus or from the Pageau chapter titles?
- Should symbolic annotations be domain-sharded like backlinks (liturgical/,
  patristic/, study/) or unified into a single symbolic/ domain?

## Handoff

**To:** `human`
**Ask:** Review the creation-language graph grammar design. Ratify to unlock
3A.1 (edge-type enrichment of R1 extractor). Ark will begin with the PSA
pilot as specified in Memo 88.

---

*The condescension of contemporary scholarship toward patristic exegesis
reflects a failure to recognize the grammar — not a deficiency in the Fathers.*
