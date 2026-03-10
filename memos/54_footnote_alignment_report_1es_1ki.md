# Memo 54 — Footnote Alignment Victory (1ES) and 1KI Structural Diagnostic

**Date:** 2026-03-10
**From:** Photius
**To:** Human (Shane), Ark, Ezra
**Status:** Completed Run; 1ES aligned; 1KI escalated.

## Executive Summary
I have successfully demonstrated the "huge cleanup" and "footnote anchor location verification" requested. By refining the `refine_notes.py` tool with monotonicity and book-boundary logic, I have achieved **perfect footnote alignment for 1 Esdras (1ES)**.

However, the audit of **3 Kingdoms (1KI)** has revealed a massive structural crisis: the Scripture extraction follows MT chapter boundaries while the OSB source content (and the OSB Notes section) follow a different LXX structure.

## Actions Executed

### 1. 1 Esdras (1ES) — 100% Aligned
- **Marker Recovery:** Manually recovered 10 missing `†` markers in `1ES.md` (e.g., 8:1, 9:3, 9:42) using `pdftotext` verification.
- **Refined Extraction:** Re-ran `refine_notes.py` with the new monotonic parser.
- **Verification:** `verify_footnotes.py` now reports **PASS** for 1ES.
- **Result:** All 27 Scripture markers now link to the correct 27 OSB annotations.

### 2. 3 Kingdoms (1KI) — Structural Diagnostic
- **Systematic Shift:** Confirmed that Chapters 10, 11, 12, 13, 14, and 15 in `1KI.md` are mis-chaptered.
    - Example: The "Queen of Sheba" (OSB 10:1) was absorbed into Chapter 9.
    - Example: "Lover of women" (OSB 11:1) was absorbed into Chapter 10.
- **Registry Desync:** The `_footnote_markers.json` for 1KI is stale and contains anchors that no longer exist in the `.md` file.
- **Partial Fix:** Executed a structural realignment for Chapters 10 and 11.

### 3. Tooling Improvements
- **`refine_notes.py`**: Now ignores inline references (e.g., "(see 3:14)") by enforcing strictly increasing verse anchors.
- **`reindex_markers.py`**: New utility to rebuild the footnote marker index directly from validated Markdown.

## Evidence Pack
- **Aligned Footnotes:** `staging/validated/OT/1ES_footnotes.md`
- **Corrected Markers:** `staging/validated/OT/1ES_footnote_markers.json`
- **1KI Diagnostic:** PDF Page 948 (Ch 10) vs `1KI.md` Line 1045.

## Recommendations
- **Ezra:** Halt promotion of 1KI. It is structurally unsound despite the "Pass" in the dashboard.
- **Ark:** We need a "Structural Reset" script for 1KI that re-partitions the entire book based on OSB chapter headers. I have the "Start Phrases" ready for this task.
- **Photius:** Continue Batch B marker recovery once structural boundaries are locked.

## Final Note
Footnote alignment is the "stress test" for our Scripture substrate. 1ES has passed; 1KI has failed and requires architecture-level repair.
