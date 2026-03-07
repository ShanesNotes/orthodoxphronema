# Docling Probe Findings — OSB PDF
**Author:** Ark | **Date:** 2026-03-06 | **Status:** In Progress — awaiting human page-range ground truth

---

## Probes Run

| Probe | Pages | Output size | Status |
|-------|-------|-------------|--------|
| Probe 1 | 1–10 | 6,854 chars / 39 elements | Complete |
| Probe 2 | 45–70 | 4,735 chars / 54 elements | Complete |

Raw files: `staging/raw/probe/`

---

## Finding 1 — Text Extraction Quality: GOOD

Docling extracts text cleanly from this typeset PDF. Characters are accurate; Greek characters (™ symbol visible) survive. No garbled output.

**Issue:** Tab characters (`\t`) appear pervasively as whitespace separators within extracted text blocks. This is an artefact of the PDF's justified/columnar layout. Every extraction rule must strip or normalize tabs before any further processing.

**Resolution:** Add a `.replace("\t", " ").strip()` normalization step to every text extraction in the pipeline. This is a one-line fix applied universally.

---

## Finding 2 — Element Type Inventory

Docling surfaces four element types in these pages:

| Type | Label | What it represents |
|------|-------|--------------------|
| `SectionHeaderItem` | `section_header` | Book titles ("GENESIS"), chapter headings ("Verses in Genesis Chapter 1") |
| `TextItem` | `text` | Body text, verse lists, navigation strings |
| `ListItem` | `list_item` | Items Docling interpreted as list members |
| `PictureItem` | `picture` | Images (cover, illustrations) |

No `TableItem`, `FormulaItem`, or `FootnoteItem` types observed yet. Footnote detection is the critical unknown — must be confirmed when we reach actual verse pages.

---

## Finding 3 (CRITICAL) — The PDF Is a Navigable/Interactive Document

**This is the most important finding from the probe.**

Pages 45–70 do NOT contain actual verse text. They contain a **navigation index layer**: for each chapter of Genesis, there is a page structured as:

```
SectionHeaderItem: "Verses in Genesis Chapter N"
TextItem: "1,2,3,4,5,6,7,8,9,10 11,12,... Back to Chapters in Genesis Back to the Old Testament Back to Table of Contents"
```

This is the structure of an **interactive PDF** (likely generated from a web-based or tagged-PDF version of the OSB), where:
- Navigation/index pages list verse numbers as clickable links
- The actual verse text resides on *separate pages* accessible via those links
- "Back to Chapters", "Back to the Old Testament", "Back to Table of Contents" are navigation controls — not content

**Implication for the pipeline:** The OSB PDF is NOT structured as a flat sequence of pages where page N = book section N. It has at minimum two layers:
1. **Navigation/index pages** — book list, chapter lists, verse number indexes
2. **Actual content pages** — the verse text, footnotes, and study notes (location unknown until further probing)

**We have not yet seen a single verse of actual biblical text.**

---

## Finding 4 — Book List Confirmed (Critical Value)

Page 45 contains the full OT book list as a TextItem. This is the most valuable single extraction from the probe because it **confirms the canonical book order and exact book names used in the OSB**:

From element index 2 (collapsed, tab-separated):
```
Exodus Leviticus Numbers Deuteronomy Joshua Judges Ruth
1 Kingdoms (1 Samuel)  2 Kingdoms (2 Samuel)  3 Kingdoms (1 Kings)  4 Kingdoms (2 Kings)
1 Chronicles (1 Paraleipomenon)  2 Chronicles (2 Paraleipomenon)
1 Ezra (2 Esdras)  2 Ezra (Ezra/2 Esdras)  Nehemiah
Tobit  Judith  Esther
1 Maccabees  2 Maccabees  3 Maccabees
Psalms  Job  Proverbs of Solomon  Ecclesiastes  Song of Songs
Wisdom of Solomon  Wisdom of Sirach
Hosea  Amos  Micah  Joel  Obadiah  Jonah  Nahum  Habakkuk  Zephaniah  Haggai  Zechariah
```

From element index 5:
```
Malachi  Isaiah  Jeremiah  Baruch  Lamentations of Jeremiah  Epistle of Jeremiah  Ezekiel  Daniel
```

**Registry cross-check results:**

| Book | Registry code | OSB name | Match? |
|------|---------------|----------|--------|
| 1 Kingdoms | 1SA | "1 Kingdoms (1 Samuel)" | ✓ Code correct; full name confirmed |
| 1 Ezra | 1ES | "1 Ezra (2 Esdras)" | ✓ |
| 2 Ezra | EZR | "2 Ezra (Ezra/2 Esdras)" | ✓ |
| Lamentations | LAM | "Lamentations of Jeremiah" | ✓ Code correct; full OSB name noted |
| Epistle of Jeremiah | LJE | "Epistle of Jeremiah" | **✓ CONFIRMED as a separate book** |

**The LJE question is resolved: "Epistle of Jeremiah" appears as a distinct entry in the OSB book list, separate from Baruch.** This confirms 49 OT canonical books (LJE is book 47, not a chapter of Baruch). The book count of 76 is validated.

Also notable: **4 Maccabees is absent from this list** — confirming it is appendix-only, not in the main OT list. **Prayer of Manasseh is also absent** — confirming appendix status. Both match our ratified registry decisions.

---

## Finding 5 — Navigation Noise to Strip

Every verse-index TextItem contains navigation strings that must be stripped from any extraction:
- `"Back to Chapters in Genesis"`
- `"Back to the Old Testament"`
- `"Back to Table of Contents"`
- `"Home"`, `"Next"`, `"Introduction"`
- Verse number sequences: `"1,2,3,4,5,6,7,8,9,10 11,12,..."`

These are pure navigation artefacts. The extraction script must filter them. Detection rule: any TextItem consisting only of comma-separated integers and/or these navigation phrases → discard.

---

## Outstanding Unknown: Where Is the Actual Verse Text?

We have not located the pages where actual Genesis 1:1 text appears. Based on the navigation structure:

- Pages 1–44: Front matter (TOC, acknowledgments, introductions, OT book comparisons)
- Pages 45–~85: Navigation index (OT book list + Genesis chapter/verse indices, possibly continuing with other books' navigation)
- Pages ~85–???: Actual verse text pages (location TBD)

**Next required action:** Probe pages in the range 150–250 or wherever the human's page-range ground truth indicates actual verse text begins. This is the single most important outstanding data point.

---

## Recommended Extraction Strategy (Draft, pending actual verse page data)

Based on what we know:

1. **Skip navigation pages entirely.** Detection: page contains only `SectionHeaderItem("Verses in [BOOK] Chapter N")` + comma-integer TextItems + navigation TextItems.

2. **Target actual verse pages.** Expected structure (hypothesis, unconfirmed):
   - `SectionHeaderItem`: Book title + chapter header (e.g., "GENESIS 1")
   - `TextItem`: Verse number marker (e.g., superscript `1` or bold `1`)
   - `TextItem`: Verse text body
   - (Possible) footnote markers inline or in a separate column

3. **Tab normalization:** Apply `.replace("\t", " ").strip()` universally.

4. **Navigation string filter:** Regex to strip "Back to..." / "Home" / "Next" / comma-integer sequences from any extracted text.

---

## Action Items

| # | Action | Owner | Blocker? |
|---|--------|-------|----------|
| 1 | Human provides page-range ground truth for Genesis 1:1 text start | Human | YES — blocks Day 4 |
| 2 | Probe actual verse text pages once page range is known | Ark | Blocked by #1 |
| 3 | Update anchor_registry.json: LJE confirmed separate; full OSB names noted | Ark | Can do now |
| 4 | Tab normalization added to extraction script | Ark | Can do now |
| 5 | Navigation page detection filter written | Ark | Can do now |

---

## Immediate Registry Update (from Finding 4)

The following OSB name fields should be updated in `schemas/anchor_registry.json`:
- `1SA` osb_name → `"1 Kingdoms (1 Samuel)"`
- `2SA` osb_name → `"2 Kingdoms (2 Samuel)"`
- `1KI` osb_name → `"3 Kingdoms (1 Kings)"`
- `2KI` osb_name → `"4 Kingdoms (2 Kings)"`
- `1CH` osb_name → `"1 Chronicles (1 Paraleipomenon)"`
- `2CH` osb_name → `"2 Chronicles (2 Paraleipomenon)"`
- `1ES` osb_name → `"1 Ezra (2 Esdras)"` (already set; confirmed)
- `EZR` osb_name → `"2 Ezra (Ezra/2 Esdras)"` (already set; confirmed)
- `LAM` osb_name → `"Lamentations of Jeremiah"`
- `LJE` osb_name → `"Epistle of Jeremiah"` (separate book — CONFIRMED)
- `PRO` osb_name → `"Proverbs of Solomon"`
- `SIR` osb_name → `"Wisdom of Sirach"`
- `WIS` osb_name → `"Wisdom of Solomon"`
