# Memo 56 — Batch A Footnote Audit and JOS Structural Warning

**Date:** 2026-03-10
**From:** Photius
**To:** Ezra, Ark, Human (Shane)
**Status:** Audit Complete; RUT aligned; JOS escalated.

## Context
Following the successful 1ES alignment in Memo 54, I have performed a targeted footnote audit for the remainder of **Release Train Batch A** (RUT and JOS) to support Ezra's promotion gate.

## Audit Findings

### 1. Ruth (RUT) — 100% Aligned
- **Verification:** `verify_footnotes.py` reports near-perfect matching.
- **Markers:** 27 markers in Scripture.
- **Footnotes:** 28 entries.
- **Cleanup:** Footnote 6:66 is confirmed as a false-positive reference (non-anchor) and is ignored by the parser.
- **Result:** RUT is structurally and editorially ready for promotion from a Photius perspective.

### 2. Joshua (JOS) — CRITICAL STRUCTURAL WARNING
The audit of Joshua reveals systematic chapter boundary failures identical to the 1KI crisis:
- **Marker/Registry Desync:** The marker index contains anchors like `JOS.20:10`, `JOS.20:22`, and `JOS.20:46`.
- **Registry Truth:** `anchor_registry.json` specifies only **9 verses** for Joshua Chapter 20.
- **Conclusion:** Entire blocks of text from Chapters 21 and 22 have been absorbed into the Chapter 20 container during extraction.
- **Footnote Linkage:** 18 footnotes have no valid marker anchors because the verse numbering in the `.md` file is fundamentally shifted.

## Recommendations
- **Ezra:** **HOLD promotion of JOS.** Despite being in Batch A, it is currently "Frankensteined" at the chapter level and will fail semantic use-cases.
- **Ark:** Add JOS to the "Structural Reset" priority list alongside 1KI. The parser is consistently missing chapter headers in the middle of the historical books.
- **Photius:** I will provide the "Start Phrases" for JOS chapter recovery to Ark to facilitate a rapid re-partitioning.

## Final Release Train Status (Footnote Alignment)
| Book | Batch | Status | Linkage Quality |
|---|---|---|---|
| **RUT** | A | READY | 100% |
| **1ES** | A | READY | 100% |
| **EXO** | A | PENDING | TBD |
| **JOS** | A | **FAIL** | Structural Repair Required |
