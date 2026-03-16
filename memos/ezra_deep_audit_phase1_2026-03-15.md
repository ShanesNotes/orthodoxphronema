# Ezra Deep Audit — Phase 1 Findings
**Date:** 2026-03-15
**Auditor:** Ezra (claude-sonnet-4-6)
**Scope:** Task 1A: Mega-Line Corpus Triage | Task 1B: Companion Divergence Spot-Check

---

## Task 1A: Mega-Line Classification

### Summary Table

| Book | Line | Length | Classification | Embedded Verses | Article Titles Found |
|---|---|---|---|---|---|
| LEV | 466 | 16,457 | article_bleed + verse_fusing | ~69 | SACRIFICE, THE OLD COVENANT |
| LEV | 531 | 8,179 | article_bleed + verse_fusing | ~34 | SACRIFICE, THE OLD COVENANT |
| LEV | 770 | 5,709 | article_bleed + verse_fusing | ~25 | THE FEAST OF WEEKS — PENTECOST |
| EXO | 445 | 8,422 | verse_fusing | ~47 | none |
| EXO | 716 | 7,928 | article_bleed + verse_fusing | ~29 | IMAGES AND IMAGERY |
| JOS | 287 | 10,409 | verse_fusing | ~54 | none |
| 1CH | 426 | 8,105 | verse_fusing | ~77 | none |

### Per-Line Detail

---

#### LEV line 466 — 16,457 chars
**Classification: article_bleed + verse_fusing (BLOCKING)**

This is the worst case in the corpus. The line begins with a valid scripture anchor `LEV.14:1` and runs through what should be verses 14:2 through 16:10, but the entire SACRIFICE study article is embedded inline starting after verse 16:10. The article text begins:

> `...to let it go as the scapegoat into the desert. SACRIFICE In the Book of Leviticus...`

The SACRIFICE article continues through its full theological treatment (THE OLD COVENANT section, New Covenant section, patristic citations, Heb 4:14, Jn 1:29, etc.) before the line terminates. Embedded verse numbers counted: ~69 (verse markers from LEV.14:2 through LEV.16:10 are all run together in this fused blob). This line contains at minimum two chapter's worth of content (ch.14 and part of ch.15 and ch.16).

The article text in canon is a V5 (article bleed) violation. It is confirmed: the SACRIFICE article that should appear only in `LEV_articles.md` has been physically embedded in the canon file.

**Note:** Lines immediately following (467 onward) correctly show `LEV.14:2`, `LEV.14:3`, etc. as individual verses. This means the mega-line 466 is a parser failure that deposited a full multi-chapter run plus the article into a single line, while the parser also emitted the correctly-split verses. There is structural duplication: the fused blob exists AND the proper one-verse-per-line sequence exists below it.

---

#### LEV line 531 — 8,179 chars
**Classification: article_bleed + verse_fusing (BLOCKING)**

Begins at `LEV.15:1` and contains the same SACRIFICE article text. This is a second instance of the same failure pattern — the parser emitted a fused run of LEV ch.15 + the SACRIFICE article body again. Embedded verse numbers: ~34. The same SACRIFICE / THE OLD COVENANT text appears verbatim.

The lines immediately following (532+) correctly show `LEV.15:2`, `LEV.15:3`, etc. Again: dual-track failure — fused blob AND correct one-verse-per-line sequence below it.

**The SACRIFICE article appears in both line 466 and line 531.** This means the article is duplicated in the canon blob — it was emitted twice by the parser.

---

#### LEV line 770 — 5,709 chars
**Classification: article_bleed + verse_fusing (BLOCKING)**

Begins at `LEV.22:1` and embeds the "THE FEAST OF WEEKS — PENTECOST" article. The article header appears as `T H E F E A S T O F W E E K S— PENTECOST` (spaced OCR artifact from the OSB PDF's formatted header). Embedded verse count: ~25 (LEV ch.22 and ch.23 verses). Lines following (771+) correctly show `LEV.22:2`, `LEV.22:3`, etc.

---

#### EXO line 445 — 8,422 chars
**Classification: verse_fusing only (no article bleed)**

Begins at `EXO.13:1` and runs through what should be chapters 13, 14, and into chapter 15:1 (the Song of Moses). No all-caps article header is present. The line contains section heading text ("The Feast of Unleavened Bread", "Pillar of Cloud, Pillar of Fire", "Crossing the Red Sea", "The Song of Moses") run together with scripture — these are chapter sub-headings from the OSB PDF that were absorbed into the fused line by the parser. Embedded verse count: ~47. Lines following (446+) correctly show `EXO.13:2`, `EXO.13:3`, etc.

This is pure verse fusing across at least 3 chapters. No study article content.

---

#### EXO line 716 — 7,928 chars
**Classification: article_bleed + verse_fusing (BLOCKING)**

Begins at `EXO.21:1` and embeds the "IMAGES AND IMAGERY" study article in full. The article starts after `EXO.21:6` scripture text and runs for thousands of characters through the full iconoclasm / Seventh Ecumenical Council discussion before resuming with `EXO.21:7`. Embedded verse count: ~29. Lines following (717+) correctly show `EXO.21:2`, `EXO.21:3`, etc.

The article discusses the Second Commandment, icons, cherubim, King Solomon's temple, and the AD 787 Council — clearly study article content.

---

#### JOS line 287 — 10,409 chars
**Classification: verse_fusing only (no article bleed)**

Begins at `JOS.10:1` and runs through chapters 10, 11, and into chapter 12 (The Victories of Moses). Section titles embedded: "The Sun Stands Still", "Victory in the Southland", "Victory in the North", "A Summary of Conquest", "The Victories of Moses". No all-caps study article headers. Embedded verse count: ~54. Lines following (288+) correctly show `JOS.10:2`, `JOS.10:3`, etc.

This is pure verse fusing spanning 3 chapters (JOS 10–12). The parser emitted a single blob before splitting the verses correctly below.

---

#### 1CH line 426 — 8,105 chars
**Classification: verse_fusing only (no article bleed)**

Begins at `1CH.8:1` and runs through chapters 8, 9, and into chapter 10. Section titles embedded: "The Return from Captivity to Jerusalem", "The Priests in Jerusalem", "The Levites in Jerusalem", "Gatekeepers of the Levites", "Other Work of the Levites", "Family Line of King Saul", "The Death of Saul and His Sons". No study article headers. Embedded verse count: ~77. Lines following (427+) correctly show `1CH.8:2`, `1CH.8:3`, etc.

This is pure verse fusing spanning 3 chapters (1CH 8–10). Same dual-track pattern.

---

### Key Pattern Observed Across All 7 Cases

All seven mega-lines share a structural signature: the parser emitted a fused multi-verse blob on a single line AND also emitted the correct one-verse-per-line sequence immediately below it on subsequent lines. This means:

1. The canon file currently contains duplicate content: the fused blob + the correctly-split verses exist simultaneously.
2. The V5 check should have caught the article bleed cases (LEV.466, LEV.531, LEV.770, EXO.716) — the fact that these are in promoted canon suggests V5 did not fire, likely because the article text is embedded inside a line that begins with a valid scripture anchor, so the per-line check may only inspect whether the line looks like a scripture verse.
3. The correct remediation is to delete the fused mega-lines entirely (keeping the properly split verses below), then re-promote through the pipeline. This is a staged recovery operation, not a parser fix — the parser has already emitted the correct output on the lines that follow.

---

## Task 1B: Companion Divergence Spot-Check

### Pair 1: GEN footnotes

| Metric | staging/validated/OT/GEN_footnotes.md | study/footnotes/OT/GEN_footnotes.md |
|---|---|---|
| Total lines | 2,247 | 1,669 |
| Blank lines | 1,015 (45%) | 437 (26%) |
| Content lines | 1,232 | 1,232 |

**Nature of divergence:** Pure whitespace. Both files have exactly 1,232 content lines. The staging version has 578 extra blank lines — these are the intra-paragraph OCR blank-line artifacts documented in Lesson Learned #14 (footnote OCR blank-line artifacts, ~45% of lines). The study version has been cleaned: blank lines between sentences within a footnote paragraph have been collapsed. No content difference exists between the two.

**Which is better:** `study/footnotes/OT/GEN_footnotes.md` — the blank lines have been collapsed while preserving section separators (blank lines between footnote entries remain). The content is identical; staging just has the artifact-inflated version.

---

### Pair 2: LEV articles

| Metric | staging/validated/OT/LEV_articles.md | study/articles/OT/LEV_articles.md |
|---|---|---|
| Total lines | 26 | 26 |

**Nature of divergence:** Both files are 26 lines. Content is nearly identical but the study version has more complete wikilink conversion. Specific differences:

- staging `LEV_articles.md` line 20: `Lv 17:11` (bare abbreviation, not wikilinked)
- study `LEV_articles.md` line 20: `[[LEV.17:11]]` (wikilinked)
- staging line 20: `Lv 16:2-34` (bare)
- study line 20: `[[LEV.16:2]]-34` (wikilinked)
- staging line 20: `Lv 16:21` (bare)
- study line 20: `[[LEV.16:21]]` (wikilinked)
- staging line 20: `Is 53:11` (bare), `Is 53:5` (bare)
- study line 20: `[[ISA.53:11]]`, `[[ISA.53:5]]` (wikilinked)
- staging line 26: `Pr 15:8`, `1Kg 15:22`, `1PE.2:5` partially wikilinked
- study line 26: `[[PRO.15:8]]`, `[[1SA.15:22]]`, `[[1PE.2:5]]` fully wikilinked

**Which is better:** `study/articles/OT/LEV_articles.md` — it has more complete wikilink coverage (bare scripture refs converted to wikilinks). The staging version lags behind in wikilink conversion. No content corrections — purely wikilink density difference.

---

### Pair 3: MAT footnotes

| Metric | staging/validated/NT/MAT_footnotes.md | study/footnotes/NT/MAT_footnotes.md |
|---|---|---|
| Total lines | 4,009 | 2,569 |
| Blank lines | 2,001 (50%) | 561 (22%) |
| Content lines | 2,008 | 2,008 |

**Nature of divergence:** Same pattern as GEN, amplified. Both files have exactly 2,008 content lines. The staging version has 1,440 extra blank lines — the intra-paragraph OCR blank-line artifact. MAT has the largest raw line count (4,009) and therefore the largest raw divergence (1,440 lines), but it is entirely whitespace noise, not content. The study version has been cleaned.

**Which is better:** `study/footnotes/NT/MAT_footnotes.md` — cleaner, identical content, no artifact blanks.

---

## Source-of-Truth Policy Recommendations

### For Companion Files (footnotes, articles)

**Finding:** The study layer (`study/footnotes/`, `study/articles/`) is consistently cleaner than the staging layer (`staging/validated/`) for companion files. Content is identical; the study versions have:
1. Blank-line artifacts removed (footnotes)
2. More complete wikilink coverage (articles)

**Recommendation:** The study layer should be declared the authoritative source-of-truth for companion content after the initial cleanup pass. Staging companions are the pre-cleanup artifacts; study companions are the post-cleanup state. Workflow should be:
- Staging companions = raw extract (pre-cleanup)
- Study companions = cleaned/linked version (canonical companion)

When making further wikilink or content corrections, apply to study layer. Staging companions should be considered read-only historical artifacts unless a structural re-extraction is needed.

### For Canon Scripture Files

**Finding:** Canon mega-lines contain fused content blobs that exist alongside correctly-split verses. The fused blobs include both verse fusing (all 7 cases) and article bleed (4 of 7 cases). The V5 check failed to catch these because they are embedded within lines that begin with valid scripture anchors.

**Immediate remediation path:**
1. Identify all 82 mega-lines (>1000 chars) across the 19 affected books
2. Classify each as article_bleed, verse_fusing, or mixed
3. For each: the correctly-split verses exist below the mega-line; the fix is to delete the fused mega-line from the staged file
4. For article_bleed cases: verify the article content is present in the companion articles file before deleting from canon
5. Re-run V1–V12 validation on each corrected staged file
6. Re-promote through the standard pipeline

**V5 check hardening:** V5 should be extended to scan for all-caps article headers (SACRIFICE, IMAGES AND IMAGERY, PENTECOST, etc.) anywhere within a line, not just at line-start. Lines beginning with a valid anchor can still contain article bleed.

---

## Blocking vs Non-Blocking Summary

| Issue | Blocking? | Count |
|---|---|---|
| Article bleed in promoted canon (LEV ×3, EXO ×1) | BLOCKING | 4 lines |
| Verse fusing in promoted canon (EXO ×1, JOS ×1, 1CH ×1) | Non-blocking for content, blocking for anchor reliability | 3 lines |
| Staging companion blank-line inflation | Non-blocking (study layer is authoritative and clean) | Corpus-wide |
| Study articles lagging wikilink coverage vs study layer | Non-blocking (already corrected in study) | Staging only |

**Highest priority:** The 4 article-bleed canon lines in LEV and EXO. These are V5 violations in promoted canon — study article text in the scripture substrate. The fact that they passed promotion indicates either (a) V5 was not run at promotion time, or (b) the check does not inspect content embedded after a valid anchor prefix on the same line.

---

*Report written by Ezra / claude-sonnet-4-6 — 2026-03-15*
