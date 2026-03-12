# EXTRACTION POLICY — Orthodox Phronema Archive

**Effective:** 2026-03-11
**Authority:** Memo 88 (Phase 3 Ratified Spec), Frozen Decision #8
**Owner:** Ark
**Status:** Active

---

## 1. Primary Extraction Engine: Docling

Docling (IBM Research — DocLayNet + TableFormer neural models) is the **mandatory primary extraction engine** for all books entering the pipeline. No exceptions.

Docling is required because it provides layout-aware parsing that distinguishes body text from footnotes, headers, margin annotations, and structural elements. This distinction is critical to the archive's zero-contamination invariant: commentary must never bleed into scripture, and footnote content must never be misclassified as verse text.

### Docling Configuration Requirements

- Input: OSB PDF pages for the target book
- Output: Structured Markdown with layout classification
- All extraction runs must log the Docling version used in the book's processing metadata
- Extraction output goes to `staging/raw/` before any validation

## 2. Recovery Fallback: pdftotext (Poppler)

pdftotext is authorized **only** as a verse-recovery instrument under the following strict conditions:

### Authorization Criteria (all must be met)

1. **V-gate failure confirmed.** A specific anchor (e.g., `TOB.13:2`) has been flagged as missing by V1–V9 validation after Docling extraction.
2. **Manual review attempted.** The missing verse has been visually confirmed as present in the source PDF but missed by Docling's layout model.
3. **Surgical application.** pdftotext is run against the specific page(s) containing the missing verse, not against the entire book.

### Logging Requirement

Every pdftotext recovery use must be recorded in the book's `BOOK_residuals.json` under the classification `pdftotext_recovery`, with:
- The specific anchor(s) recovered
- The PDF page number(s) targeted
- The date of recovery
- The pdftotext version used

### What pdftotext Cannot Do

- pdftotext **may not** be used as a primary extraction tool for any book, partial or complete
- pdftotext **may not** be used to extract footnotes, commentary, or study article content
- pdftotext output **may not** be committed to canon without passing the same V1–V9 gate that Docling output passes

## 3. No Other Extraction Tools Authorized

No extraction tool beyond Docling (primary) and pdftotext (recovery fallback) is authorized for use on this archive. This includes but is not limited to:

- PyMuPDF / fitz
- pdfplumber
- Camelot / Tabula
- Adobe PDF Services API
- Any LLM-based direct PDF extraction (GPT-4V, Claude vision, etc.)

Introduction of a new extraction tool requires a formal memo and human ratification before any code is written or any extraction run is performed.

## 4. Applicability

This policy applies to:
- All OT and NT scripture extraction (Phase 1/2)
- All phronema content extraction (Phase 3+)
- All footnote and study article extraction
- Any future corpus expansion

## 5. Violation Handling

An extraction run that uses an unauthorized tool or uses pdftotext outside the recovery criteria above is a **pipeline integrity violation**. The affected output must be quarantined (not promoted) and the violation logged in a memo before remediation.

---

**Referenced by:** Memo 88 (Phase 3 Ratified Spec), Memo `RESEARCH_ARCHITECTURAL_PARADIGMS_20260310` (Action #3)
