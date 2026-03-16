# Senior PM Optimization Review — Foundation for Wikilinks Engineering

**Author:** `ark`
**Type:** `decision`
**Status:** `draft — awaiting human ratification`
**Scope:** Project-wide optimization audit and wikilinks foundation readiness
**Date:** 2026-03-15
**Next memo:** `135`

---

## Executive Summary

This memo delivers a deep architectural review of the Orthodox Phronema Archive, conducted from the perspective of a senior PM preparing the project for its next major engineering phase: completing the wikilinks structure and function project-wide. The review covers all seven project surfaces (canon, study, reference, pipeline, metadata, schemas, governance) and produces a prioritized optimization plan organized into three tiers: blockers, foundation hardening, and wikilinks-ready engineering.

**Bottom line:** The project is architecturally mature and operationally disciplined. Canon is complete (76/76 promoted), footnote cleanup is done (76/76 verified), the R1 extraction pipeline works, and 6,094 study-domain backlink shards are generated. However, three ratification blockers and several structural debts must be resolved before the wikilinks layer can be engineered with confidence across the full project surface.

---

## Current State Snapshot

| Surface | State | Health |
|---|---|---|
| Canon (76 books) | All promoted, checksummed, V1-V12 swept | Strong |
| Study articles (76 files) | 30% have wikilinks; 53 books have zero article-level cross-references | Weak — primary wikilinks gap |
| Study footnotes (76 files) | 97% wikilinked, all 7 validation components passed | Strong |
| Lectionary notes (15 files) | Only 20% of canon covered | Incomplete |
| Reference layer (21 files) | JSON+MD pairs for glossary (201 terms), lectionary (401 entries), variants (1,309 entries), cross-refs (375 entries) | Solid |
| Pipeline (V1-V12 + D1-D5) | Fully operational, no active TODOs/FIXMEs | Strong |
| Metadata (6,256 files) | Study backlinks complete; patristic/liturgical empty (intentional) | Partial |
| Schemas (anchor_registry v1.7.4) | 31 CVC corrections applied, frozen | Locked |
| Knowledge graph (281 entities) | Current, synced with ops board | Healthy |
| Governance (14 active memos) | 3 awaiting ratification (Memo 88 is critical blocker) | Blocked |

---

## Part 1 — Blockers (Must Resolve Before Wikilinks Engineering)

### 1.1 Memo 88 Ratification (Critical Path)

Memo 88 is the constitutional document for Phase 3. It locks the three-layer architecture (canonical flat-file, domain-sharded backlinks, DuckDB query layer), five closed adjudications, and the frozen decision set. Every downstream wikilinks engineering decision depends on this memo being ratified.

**What it governs:**

- ADJ-1: Backlink filename format (hyphen separator, `PSA.44-10.json`)
- ADJ-2: Wikilink syntax scope (`[[BOOK.CH:V]]` everywhere outside canon)
- ADJ-3: Domain-sharded rollout (pre-sharded from day one)
- ADJ-4: Canon directory structure (`canon/OT/`, `canon/NT/`)
- ADJ-5: V11/V12 are informational, not promotion gates

**Ask:** Ratify Memo 88 as the governing Phase 3 document. Without this, no wikilinks engineering can proceed with architectural certainty.

### 1.2 Memo 91 — OT Canon Lock

Seventeen V7-only books plus EST disposition need ratification. This locks the OT canon surface so wikilinks can target stable anchors. If anchors shift post-wikilink engineering, the entire backlink layer becomes stale.

**Ask:** Ratify Memo 91 so that OT anchor targets are frozen.

### 1.3 Memo 51 — Historical Residual Ratification (JDG, 1SA, 2SA)

Three books with historical residuals (parser-era gaps) need formal disposition. These residuals affect V4 gap coverage, which in turn affects whether wikilinks pointing at these anchors resolve to actual content or to known gaps.

**Ask:** Ratify Memo 51 to close the residual ledger for these three books.

---

## Part 2 — Foundation Hardening (Pre-Wikilinks Optimization)

### 2.1 Study Article Wikilink Coverage: 30% to 100%

This is the single largest gap for project-wide wikilinks. Only 23 of 76 article files contain any wikilinks. Fifty-three books have zero article-level cross-references, meaning the study articles layer is effectively disconnected from the anchor graph.

**Current state:**

- Articles WITH wikilinks (23): GEN, EXO, LEV, NUM, DEU, JER, JOB, DAN, EZK, 2MA, MAT, MRK, LUK, JOH, ACT, ROM, 1CO, EPH, JAS, 1JN, 2PE, REV, TIT
- Articles WITHOUT wikilinks (53): All remaining books
- All `canon_anchors_referenced` arrays are empty (reverse mapping not populated)

**Optimization plan:**

1. Run the R1 extractor against all 76 article files to identify bare references that could be converted to wikilinks
2. Use Photius for batch wikilink normalization (same pattern as Memo 122 full rollout)
3. For articles with "(No study articles extracted...)" placeholder text (e.g., RUT), flag as extraction gaps — these need parser re-extraction from the OSB PDF article pages
4. Populate `canon_anchors_referenced` arrays in article frontmatter after wikilink insertion
5. Target: 76/76 articles with wikilinks before wikilinks engineering begins

**Effort estimate:** Medium. The footnote cleanup waves (Memos 126-133) proved this batch pattern works at scale with Ezra + Photius.

### 2.2 Parser Recovery Debt (DEU, NUM, 1CH)

Three books have known parser-level issues that affect anchor integrity:

| Book | Issue | Impact on Wikilinks |
|---|---|---|
| DEU | 29:1 mega-line (7,281 chars), content duplication (29:1-28 + 30:1-20 fused into one line), 30:20 embedded not separate | Wikilinks targeting DEU.29:x or DEU.30:x resolve to corrupted fused content. Staging has clean separation — re-promote. Registry CVC corrected 19→20 (v1.7.5). All gates now pass. |
| NUM | 1:1 truncated, 6:27 missing from promoted canon | Missing anchors create dead wikilinks |
| 1CH | 1:43-54 removed by Ezra audit (duplicate content), registry corrected 54 to 42 | Wikilinks targeting 1CH.1:43-54 are now orphaned; need cleanup |

**Optimization plan:**

1. DEU: Re-promote from staging (mega-line already separated, 30:20 recovered). Verify registry CVC for ch30 (19 vs 20 verses) before promotion.
2. NUM: Re-promote from staging (1:1 full text and 6:27 already recovered there). Staging has fixes; canon is stale.
3. 1CH: Audit all existing wikilinks pointing at 1CH.1:43-54. Redirect or remove orphaned references. Verify registry CVC (54 to 42) is propagated through pipeline.
4. Re-promote all three books through full V1-V12 + D1-D5 gate sequence.

**Effort estimate:** High per-book, but only three books. Surgical, not systemic.

### 2.3 Dossier Refresh Cycle ~~(71 Stale Dossiers)~~ COMPLETED

**Status: DONE (2026-03-15).** All 76 dossiers refreshed to registry v1.7.4 via `batch_dossier.py`. Dashboard regenerated. Results:
- 61 books: `dry-run` (would-promote, all gates pass)
- 15 books: `blocked` (unresolved residuals or editorial candidates: 1MA, 1SA, 2SA, 3MA, EST, EZK, HOS, JDG, JER, JOB, LAM, NEH, PRO, SIR, WIS)
- NUM: V7 at 98.8% (confirms missing verses)
- DEU: V7 at 100.1% (one extra verse vs registry — CVC correction needed)

### 2.4 Registry CVC Final Reconciliation

Registry v1.7.5 includes 32 CVC corrections (DEU ch30: 19→20 applied 2026-03-15), but a handful of chapters in EXO, TOB, JDT, 2KI, SIR, ZEC, NAH, and BAR still have pending alignment corrections documented in Memo 128. These affect V7 completeness checks, which in turn affect confidence in anchor coverage.

**Optimization plan:**

1. Complete the remaining CVC corrections documented in Memo 128
2. Bump registry to v1.7.6+ with changelog
3. Run full V7 sweep to confirm all 76 books align with registry
4. Target: zero V7 warnings (or all warnings ratified with evidence)

**Effort estimate:** Low-medium. Most corrections are already documented; just need application.

---

## Part 3 — Wikilinks-Ready Engineering

### 3.1 Wikilink Audit and Normalization (Full Surface)

Before building the wikilinks structure project-wide, every existing wikilink must be audited for correctness:

**Scope:**

- 2,957 wikilinks in footnotes (97% coverage)
- 138 wikilinks in articles (30% coverage, expanding per 2.1)
- Unknown count in reference layer files
- R1 JSONL output (10,660 records across 76 books)

**Audit dimensions:**

1. **Anchor resolution:** Does every `[[BOOK.CH:V]]` resolve to a real anchor in canon? Cross-check against `anchor_registry.json` dimensions.
2. **Range validity:** Do range references like `[[PSA.18:1]]-4` correctly compute end verse? Verify end verse exists in registry.
3. **Bare reference conversion:** How many bare references (e.g., "Genesis 1:1") remain unconverted? These are wikilink candidates.
4. **Orphaned wikilinks:** After parser recovery (2.2), which wikilinks point at anchors that no longer exist or have moved?
5. **Cross-domain consistency:** Do study, patristic, and liturgical domains use identical anchor syntax?

**Tooling:**

- `pipeline/reference/audit_wikilinks.py` — existing tool, run project-wide
- `pipeline/reference/wikilinks.py` — shared parser with `WIKILINK_RE`, `BARE_RE`, `CHAPTER_RANGE_RE`
- `pipeline/extract/r1_extractor.py` — regenerate R1 JSONL after audit corrections

**Deliverable:** A `wikilink_audit_v2.json` report covering all surfaces, with per-book pass/fail/warn status and a manifest of required corrections.

### 3.2 Backlink Layer Completion (Layer 2)

Current state: 6,094 study-domain backlink shards. Patristic and liturgical domains are intentionally empty.

**Phase 3 wikilinks engineering requires:**

1. **Study domain:** Regenerate after article wikilink expansion (2.1). Current 6,094 shards will grow significantly once 53 article files gain wikilinks.
2. **Patristic domain:** Populate from footnote patristic citations. The 53 source abbreviations in `source-abbreviations.json` provide the entity taxonomy. Each patristic citation in footnotes that references a canon anchor becomes a backlink shard.
3. **Liturgical domain:** Populate from lectionary cross-references. The 375 entries in `liturgical-crossrefs.json` and 15 lectionary-note files provide the source material.

**Architecture per Memo 88:**

```
metadata/anchor_backlinks/
  study/       → regenerate (expanded)
  patristic/   → new (populate from footnote patristic citations)
  liturgical/  → new (populate from lectionary + liturgical cross-refs)
```

**Each shard:**

```json
{
  "anchor_id": "GEN.1:1",
  "canon_uri": "canon/OT/GEN.md#GEN.1:1",
  "domain": "study|patristic|liturgical",
  "links": [{ "source_file": "...", "line_number": N, "raw_match": "...", "reference_type": "wikilink", "context": "..." }]
}
```

### 3.3 R1 Extractor Enhancement

The current R1 extractor handles `[[BOOK.CH:V]]` wikilinks and bare `Book CH:V` references. For full project-wide wikilinks, it needs:

1. **Patristic entity extraction:** Recognize `(BasilG)`, `(JohnChr)` etc. as source attributions tied to the surrounding anchor context. Map these to the `source-abbreviations.json` taxonomy.
2. **Liturgical context extraction:** Recognize liturgical calendar references ("read during Vespers on Great and Holy Saturday") and map them to the `liturgical-crossrefs.json` entries.
3. **Range expansion:** Currently records `[[PSA.18:1]]-4` as a single reference. Should expand to individual anchors (PSA.18:1, PSA.18:2, PSA.18:3, PSA.18:4) for complete backlink coverage.
4. **Cross-reference chain tracking:** When a footnote references multiple anchors in sequence (e.g., "cf. [[GEN.1:1]], [[JOH.1:1]], [[COL.1:15]]"), record the co-occurrence pattern for the graph layer.

### 3.4 Glossary Wikilink Integration

The glossary (`reference/glossary.json`, 201 terms) contains scripture references in prose form (e.g., "uses in Mk 14:36, Rom 8:15") but does not use wikilink syntax.

**Plan:**

1. Parse all 201 glossary entries for scripture references
2. Convert bare references to `[[BOOK.CH:V]]` wikilink syntax
3. Generate backlink shards for glossary-to-canon cross-references
4. This creates a new reference-domain backlink surface

### 3.5 Lectionary Coverage Expansion

Only 15 of 76 books have lectionary notes, and only 42 books appear in the daily personal reading lectionary. This creates gaps in the liturgical backlink domain.

**Plan:**

1. Audit `reference/lectionary.json` (401 entries) against canon books — identify which of the 42 books already have backlink-ready structured references
2. For the 15 books with lectionary notes: convert all references to wikilinks, generate liturgical backlink shards
3. Document the 34-book lectionary gap as a known limitation (these books are not referenced in the OSB lectionary — this is a source limitation, not an engineering gap)

### 3.6 Knowledge Graph Wikilinks Surface

After all wikilink engineering is complete, update the knowledge graph to reflect the new cross-reference density:

1. Add `wikilink_count` observation to each `canon_book` entity
2. Add `inbound_link_count` per domain (study, patristic, liturgical) to each entity
3. Create new relation type `cross_references` for high-density anchor pairs
4. Update `study_article` entities with wikilink status (was empty, now populated)

---

## Part 4 — Proposed Execution Order

### Tier 0: Ratification (Human Action Required)

1. Ratify Memo 88 (Phase 3 governing spec)
2. Ratify Memo 91 (OT canon lock)
3. Ratify Memo 51 (JDG/1SA/2SA historical residuals)

### Tier 1: Foundation Hardening (Ark + Ezra + Photius)

4. Registry CVC final reconciliation (v1.7.5)
5. Parser recovery: DEU, NUM, 1CH
6. ~~Dossier refresh cycle (batch)~~ DONE — 76/76 fresh at v1.7.4
7. Study article wikilink expansion (53 books, batch)

### Tier 2: Audit and Normalization

8. Full-surface wikilink audit (audit_wikilinks.py, project-wide)
9. Bare reference conversion (batch Photius operation)
10. Orphaned wikilink cleanup (post parser recovery)
11. Glossary wikilink integration

### Tier 3: Backlink Layer Engineering

12. R1 extractor enhancement (patristic, liturgical, range expansion)
13. Study backlink regeneration (expanded surface)
14. Patristic backlink population
15. Liturgical backlink population
16. Lectionary coverage documentation

### Tier 4: Verification and Graph

17. V11/V12 full sweep (backlink integrity, graph consistency)
18. Knowledge graph wikilinks surface update
19. Coordination state refresh and drift check
20. Phase 3 launch readiness gate

---

## Part 5 — Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Memo 88 ratification delayed | Medium | Critical — blocks all Phase 3 work | Escalate; present this review as evidence of readiness |
| Article wikilink expansion introduces false positives | Medium | Medium — bad cross-references in study layer | Use registry dimension validation on all normalized anchors |
| Parser recovery changes anchor set, orphaning existing backlinks | High (by design) | Medium — requires backlink regeneration | Regenerate backlinks AFTER parser recovery, not before |
| Glossary bare references are ambiguous (book name collisions) | Low | Low — false normalization | Use `canonical_biblical_code()` with alias disambiguation |
| Patristic entity extraction misattributes citations | Medium | Medium — incorrect backlinks | Validate against `source-abbreviations.json` taxonomy; human spot-check |
| CVC corrections change verse counts, invalidating existing wikilinks | Low (corrections are small) | Medium — orphaned anchors | Run orphaned-wikilink audit after each CVC bump |

---

## Part 6 — Success Criteria

The project has an "absolute pure foundation" for wikilinks engineering when:

1. All three pending memos (88, 91, 51) are ratified
2. Registry CVC has zero unresolved corrections (v1.7.5+)
3. Parser recovery debt is cleared (DEU, NUM, 1CH re-promoted)
4. ~~All 76 dossiers are fresh (generated against current registry)~~ DONE 2026-03-15
5. All 76 study articles have wikilinks (expansion from 23 to 76)
6. Full-surface wikilink audit passes with zero unresolved orphans
7. `canon_anchors_referenced` arrays are populated in all study file frontmatter
8. Glossary references are converted to wikilink syntax
9. R1 JSONL output is regenerated against the expanded wikilink surface
10. Knowledge graph reflects current wikilink density per book

---

## Appendix A — Current Wikilink Infrastructure

| Component | File | Status |
|---|---|---|
| Wikilink parser | `pipeline/reference/wikilinks.py` | Production |
| Reference aliases | `pipeline/reference/reference_aliases.py` | Production (v3) |
| Alias schema | `schemas/reference_aliases.yaml` | Locked (v3) |
| Wikilink audit | `pipeline/reference/audit_wikilinks.py` | Production |
| R1 extractor | `pipeline/extract/r1_extractor.py` | Production |
| R1 data model | `pipeline/extract/models.py` | Production |
| Backlink builder | `pipeline/graph/build_backlinks.py` | Production |
| Backlink validator | `pipeline/validate/validate_phase3.py` | Production |
| Backlink schema | `schemas/anchor_backlinks.json` | Frozen |
| Source abbreviations | `reference/source-abbreviations.json` | Production (53 sources) |

## Appendix B — Governing Documents for Wikilinks

| Document | Role |
|---|---|
| Memo 88 | Phase 3 constitutional spec (pending ratification) |
| Memo 53 | Footnote workflow and link standards |
| Memo 86 | R1 extraction pipeline design |
| Memo 87 | DuckDB citation graph design |
| Memo 120 | Wikilink rollout seed (REV batch) |
| Memo 122 | Full wikilink normalization rollout |
| ADJ-2 (in Memo 88) | Wikilink syntax scope decision |
| CLAUDE.md | Anchor format (frozen: `[[GEN.1:1]]`) |

---

*This memo is draft. It becomes governing upon Human ratification and supersedes no prior memos — it synthesizes and extends them.*
