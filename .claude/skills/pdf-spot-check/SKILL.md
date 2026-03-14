---
name: pdf-spot-check
description: Perform targeted PDF source verification for scripture edge cases using pdftotext against the OSB PDF. Use when V4 shows small residual gaps (under 100 missing anchors), for drop-cap recovery verification, or when someone asks to "check against the PDF", "verify source", or "spot-check". Do NOT use for full book extraction (that's the parser pipeline) or for validation runs (use validate-book).
allowed-tools: "Bash(python3:*) Bash(pdftotext:*) Read Grep"
metadata:
  author: Orthodox Phronema Archive
  version: 1.0.0
  category: verification
---

# PDF Spot-Check

## Instructions

### Step 1: Identify Target Verses
Determine which verses need source verification:
- From V4 gap report: missing anchors list
- From drop-cap candidates: `BOOK_dropcap_candidates.json`
- From manual request: specific verse references

### Step 2: Locate Source Pages
Use the page mapping or anchor registry to find the relevant OSB PDF pages:
```bash
python3 pipeline/validate/pdf_edge_case_check.py staging/validated/{OT,NT}/BOOK.md
```

### Step 3: Extract and Compare
For each target verse, extract the raw text from the source PDF page:
```bash
pdftotext -f PAGE -l PAGE src.texts/osb.pdf /tmp/page_check.txt
```

Compare the extracted text against the staged verse content.

### Step 4: Document Findings
For each verse checked, record:
- Verse reference (e.g., GEN.1:1)
- OSB PDF page number
- Expected text (from staged file)
- Actual text (from PDF extraction)
- Verdict: MATCH / MISMATCH / AMBIGUOUS
- If ambiguous: describe the issue (drop-cap, OCR artifact, line break)

### Step 5: Recommend Action
- All match → Gaps are likely versification differences, document as known
- Mismatches found → Route to Photius for staged recovery with evidence
- Ambiguous cases → Route to Human for source adjudication

## Common Issues
- Drop-cap verses: first letter may be on a separate line or missing from OCR
- Verse spanning page breaks: check both pages
- Footnote markers inline: may cause false gaps
