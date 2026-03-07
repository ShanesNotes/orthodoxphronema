# Docling Probe — Genesis Verse Pages (p102-112)
**Author:** Ark | **Date:** 2026-03-06 | **Status:** COMPLETE — ready to lock extraction strategy

---

## What Was Probed

Pages 102–112. Per the ground truth, Genesis text spans pages 49–188 (navigation index through p101, verse text from p102). Genesis footnotes are at pages 4120–4354.

Raw files: `staging/raw/probe/probe_markdown_p102-112.md`, `probe_structure_p102-112.json`

---

## Finding 1 — Verse Text Is Present and High Quality

Genesis 1:1 ("In the beginning God made heaven and earth.") appears at element index 3. Text quality is excellent. The SAAS OT translation is clean and fully readable. This is not a scan — it is a typeset PDF and Docling handles it well.

---

## Finding 2 — Verse Structure: Multiple Verses per TextItem, Numbers Inline

**This is the most important structural finding.**

Verse numbers are **not** separate elements. They are embedded inline within `TextItem` blocks, with multiple verses grouped into one element. Example (element 3):

```
"1 In the beginning God made heaven and earth. †ω  2 The earth was invisible and
unfinished; and darkness was over the deep. The Spirit of God was hovering over the
face of the water. †  3 Then God said, 'Let there be light'; and there was light. †
4 God saw the light; it was good; ..."
```

**Verse boundaries within a TextItem** are marked by: ` N ` (space, number, space) where N is the next verse number, often preceded by a footnote marker (`†`, `ω`, `†ω`).

**Chapter boundaries** follow a different convention:

At the start of a new chapter, the TextItem begins with the **chapter number** (not verse 1). Verse 1 of that chapter is the text immediately following the chapter number — it has no explicit "1" prefix. Example (element 32):

```
"2 Thus heaven and earth and all their adornment were finished. †  2 And on the
seventh day God finished the works He made..."
```

Here the leading `2` is **Genesis chapter 2**. "Thus heaven..." is Gen 2:1. Then " 2 And on the seventh day" is Gen 2:2. Then " 3 Then God blessed" is Gen 2:3.

This is standard typeset Bible convention: the chapter number appears as a lead-in (drop cap in print), and verse 1 is implicit.

**Extraction implication:** The parser must track the current chapter and handle chapter-start TextItems differently from mid-chapter TextItems.

---

## Finding 3 — Footnote Markers: Three Types, All Inline

Footnote references appear inline within verse text. Three marker types observed:

| Marker | Example context | Type |
|--------|----------------|------|
| `†` | `"heaven and earth. †  2 The earth..."` | Standard footnote (text note in footnote pages) |
| `ω` | `"the water. ω  15 Let them..."` | Cross-reference / alternate reading |
| `†ω` | `"In the beginning God made heaven and earth. †ω  2 The earth..."` | Both types present |

The markers appear **after** the verse text they annotate, before the next verse number.

**The actual footnote text is not on these pages.** It is in the footnote section (Genesis: pages 4120–4354). The inline markers are anchors only.

**Extraction rule for Scripture files:**
- Strip `†`, `ω`, `†ω` from the verse text body for the canon file.
- Record each marker occurrence as `{book}.{chapter}:{verse}` → `{marker_type}` in a footnote-marker index. This index is used when extracting the footnote pages to pair each footnote to its verse anchor.

---

## Finding 4 (CRITICAL) — Study Articles Are Interleaved with Verse Text

This is the core purity challenge. Study articles appear **mid-chapter**, breaking the verse sequence. Two clear examples in 10 pages:

**Example A — "THE HOLY TRINITY" (between Gen 1:28 and Gen 1:29):**

```
[verses 1–28 in elements 3–8]
→ SectionHeaderItem: "T H E  H O L Y  T R I N I T Y"    ← article starts
→ TextItem: "T he Holy Trinity is revealed both..."
→ [7 more article TextItems]
→ SectionHeaderItem: "THE INCARNATE SON FULLY REVEALS THE HOLY TRINITY"
→ [2 more article TextItems]
→ TextItem: "29 Then God said, 'Behold, I have given you..."  ← verse resumes at 1:29
```

**Example B — "ANCESTRAL SIN" (between Gen 3:7 and Gen 3:8):**
```
[verses 3:1–3:7 in element 39]
→ SectionHeaderItem: "A N C E S T R A L  S I N"           ← article starts
→ [8 article TextItems including numbered sub-points 1–5]
→ TextItem: "8 Then they heard the voice..."               ← verse resumes at 3:8
```

**Study article detection signals (all three must be verified before routing to article track):**

| Signal | Pattern | Confidence |
|--------|---------|-----------|
| Spaced-letter header | `SectionHeaderItem` where text matches `([A-Z] )+[A-Z]` | High — distinctive |
| Drop-cap initial | TextItem body starts with single letter then space: `"T he..."`, `"I n..."` | Medium — also occurs in some verse poetry |
| No leading verse number | TextItem text does NOT match `^\d+ [A-Z]` | Required condition |
| Follows a spaced-letter header | Appears after a confirmed article `SectionHeaderItem` | Stateful |

**Other section headers** (NOT study articles — these are narrative sub-headings within the Scripture text):

| Example | Type | Disposition |
|---------|------|-------------|
| "The Creation" | Title-case narrative heading | → Keep in Scripture file as section heading |
| "The Garden of Eden" | Title-case narrative heading | → Keep in Scripture file as section heading |
| "The Fall of Mankind" | Title-case narrative heading | → Keep in Scripture file as section heading |
| "Cain Kills Abel" | Title-case narrative heading | → Keep in Scripture file as section heading |
| "Cain's Family" | Title-case narrative heading | → Keep in Scripture file as section heading |
| "The Descendants of Adam" | Title-case narrative heading | → Keep in Scripture file as section heading |
| "T H E  H O L Y  T R I N I T Y" | Spaced-letter ALL CAPS | → Extract to articles/ |
| "A N C E S T R A L  S I N" | Spaced-letter ALL CAPS | → Extract to articles/ |
| "THE HOLY TRINITY CREATED THE WORLD" | ALL CAPS (but not spaced) | → Sub-heading within article |

**Detection rule for title-case narrative headings:**

`SectionHeaderItem` where text is title-case (not all caps, not spaced letters) → Scripture narrative heading → kept in canon file.

---

## Finding 5 — Verse Text Can Split Across Column Breaks

One TextItem in the probe splits mid-verse at a column boundary:

Element 50: `"8 Then they heard the voice of the Lord God walking in the garden that afternoon, and"`
Element 51: `"Adam and his wife hid themselves within the tree in the middle..."`

This is a mid-verse column split. The word "and" ends element 50 and the continuation begins element 51 without a verse number. The extraction script must detect and merge these fragments.

**Detection rule:** A TextItem that does not begin with a digit (verse number or chapter number) and follows a TextItem that ends without sentence-final punctuation → likely a continuation fragment; merge with previous.

---

## Finding 6 — Poetry Formatting

The "Song of Lamech" (Gen 4:23-24) appears as a TextItem with embedded line structure:

```
'Hear my voice, y ou wiv es of Lamech,
And listen carefully to my words,
Because I killed a man for wounding me...
```

Note: `"y ou"`, `"wiv es"`, `"carefully "` — these are justified spacing artifacts from the two-column PDF layout bleeding through. Word-join normalization is needed: detect adjacent fragments that look like split words.

**Detection rule:** Pattern `([a-z]) ([a-z]{2,})` within a word position → likely a split word from column justification. Apply conservative re-join.

---

## Summary: The Three Content Layers on Verse Pages

| Layer | Element type | Detection | Destination |
|-------|-------------|-----------|-------------|
| Scripture verse text | `TextItem` starting with `\d+ ` | Leading digit | `canon/` |
| Narrative section heading | `SectionHeaderItem` (Title Case, not spaced-all-caps) | Title case | `canon/` (as heading) |
| Study article | `SectionHeaderItem` (spaced ALL CAPS) + following `TextItem`s with no leading verse number | Spaced-caps header + stateful tracking | `articles/` |

---

## Recommended Extraction Architecture (Day 4 Script)

### Input
- Book text page range (from ground truth registry)
- Book footnote page range (from ground truth registry)
- Current book code and chapter tracker

### Phase 1 — Raw Element Stream

Docling output: sequence of `(element_type, label, text)` tuples.

Pre-processing on every text:
1. Normalize tabs: `.replace("\t", " ")`
2. Strip navigation artefacts: remove any element matching the nav-string patterns from probe 2 ("Back to...", comma-integer sequences)
3. Detect column-split fragments: merge continuation fragments

### Phase 2 — State Machine Classification

```
state = VERSE_MODE | ARTICLE_MODE
current_chapter = (inferred from last chapter-number marker)

for each element:
    if SectionHeaderItem AND text matches spaced-caps pattern:
        state = ARTICLE_MODE
        article_title = normalize_spaced(text)
        flush current article buffer with title
    elif SectionHeaderItem AND title-case:
        if state == VERSE_MODE:
            emit section_heading to canon stream
        else:
            emit sub_heading to article stream
    elif TextItem:
        if state == ARTICLE_MODE:
            if text starts with digit (verse number):
                state = VERSE_MODE
                # this element is a verse, fall through
            else:
                emit to article stream
                continue
        # VERSE_MODE:
        if text starts with chapter-number pattern:
            advance current_chapter
            emit verse(current_chapter, 1, text_after_chapter_number)
            split remaining inline verse numbers
        else:
            split inline verse numbers, emit verse(current_chapter, N, text)
```

### Phase 3 — Verse Splitting Within a TextItem

Within a TextItem classified as verse content:

```
verse_split_pattern = re.compile(r'(?:[\†ω ]+)?(\d+)\s+(?=[A-Z\'"])')
```

Split on this boundary. For each resulting span:
- Span N: verse number + text body + optional footnote markers
- Strip footnote markers from text body; record them as `{book}.{ch}:{verse} → marker_type`

### Phase 4 — Output Generation

**Canon file** (`canon/OT/GEN.md`):
```markdown
---
[frontmatter]
---

## Chapter 1

### The Creation

GEN.1:1 In the beginning God made heaven and earth.

GEN.1:2 The earth was invisible and unfinished; and darkness was over the deep. The Spirit of God was hovering over the face of the water.
...
```

**Notes file** (`notes/OT/GEN_notes.md`):
```markdown
---
[frontmatter]
---

## Study Articles

### The Holy Trinity
*(between GEN.1:28 and GEN.1:29)*

T he Holy Trinity is revealed both in the Old Testament and the New...
...
```

**Footnote marker index** (`staging/validated/OT/GEN_footnote_markers.json`):
```json
[
  {"anchor": "GEN.1:1", "marker": "†ω"},
  {"anchor": "GEN.1:2", "marker": "†"},
  ...
]
```
This index is used in Phase 2 footnote extraction to pair footnote text (from pages 4120-4354) to its canon anchor.

---

## Page Range Registry (Ground Truth — Committed)

The human-provided page ranges must be committed to `schemas/anchor_registry.json` as a `page_ranges` block. This is the authoritative source for the extraction script.

**Sample structure:**
```json
"page_ranges": {
  "GEN": {"text": [49, 188], "footnotes": [4120, 4354]},
  "EXO": {"text": [189, 304], "footnotes": [4355, 4532]},
  ...
}
```

---

## Open Questions (Minor — Resolve During Day 4)

| # | Question | Impact |
|---|----------|--------|
| Q1 | What pages does the Genesis book introduction occupy (within 49-188)? | Need to skip/route to articles/ |
| Q2 | Are footnote pages structured consistently across all books? | Probe EXO footnotes once GEN is clean |
| Q3 | Are chapter numbers always at the start of a TextItem, or can they appear mid-TextItem? | Edge case in chapter parsing |
| Q4 | Do any study articles span across pages in ways that break mid-article? | Only relevant at scale |

Q1 is answerable by probing pages 49-101 (navigation + introduction for Genesis, pre-verse-text). This can wait until Day 4 after the extraction script is drafted.

---

## Day 4 Action Plan

1. Commit page range ground truth to `schemas/anchor_registry.json`
2. Write `pipeline/parse/docling_parse.py` implementing the state machine above
3. Run on Genesis pages 102-188 (verse text only, first pass)
4. Manually verify output for chapters 1-3
5. Run V1-V4 validation on output
6. If clean: probe Genesis footnote pages (4120-4354) and implement footnote pairing

The extraction script should be single-book, single-pass, deterministic, and testable on small page subsets before running across all 139 Genesis verse pages.
