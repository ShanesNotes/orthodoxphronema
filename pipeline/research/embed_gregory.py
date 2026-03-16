#!/usr/bin/env python3
"""
Gregory of Nyssa 'Life of Moses' Embedding Pipeline
=====================================================
Embeds each section of the Life of Moses using Gemini embedding-2-preview.
Text-only embedding (no diagrams in this source).

Uses section-level chunking aligned to Gregory's own structural divisions
(Book I historia, Book II theoria sections by theophanic episode).

Usage:
    python3 pipeline/research/embed_gregory.py
    python3 pipeline/research/embed_gregory.py --dry-run
    python3 pipeline/research/embed_gregory.py --sections book2_burning_bush,book2_darkness

Environment:
    GEMINI_API_KEY  — required
"""

import json
import os
import sys
import re
import time
import math
import argparse
import hashlib
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "pipeline" / "research" / "gregory_chapter_manifest.json"
OUTPUT_DIR = REPO_ROOT / "metadata" / "embeddings" / "gregory"
PDF_PATH = REPO_ROOT / "src.texts" / "Gregory-of-Nyssa-The-Life-of-Moses.pdf"

DEFAULT_MODEL = "gemini-embedding-2-preview"
DEFAULT_DIMENSIONS = 768
DEFAULT_TASK_TYPE = "RETRIEVAL_DOCUMENT"
BATCH_DELAY_SECONDS = 1.5


def load_manifest():
    with open(MANIFEST_PATH) as f:
        return json.load(f)


def extract_section_text(pdf_path, start_page, end_page):
    """Extract and lightly clean text from a page range."""
    import fitz
    doc = fitz.open(str(pdf_path))
    text_parts = []
    for page_num in range(start_page - 1, min(end_page, len(doc))):
        page = doc[page_num]
        text_parts.append(page.get_text())
    doc.close()

    text = "\n".join(text_parts).strip()

    # Light cleanup: strip page number markers like -41- or -xii-
    text = re.sub(r'\n\s*-\d+-\s*\n', '\n', text)
    text = re.sub(r'\n\s*-[xivlc]+-\s*\n', '\n', text, flags=re.IGNORECASE)

    # Strip superscript footnote numbers (Unicode superscripts and bare numbers after spaces)
    # These appear as small numbers like ⁷⁴ or as regular digits after text
    text = re.sub(r'[⁰¹²³⁴⁵⁶⁷⁸⁹]+', '', text)
    # Also strip patterns like " 74 " that are footnote refs in the middle of text
    text = re.sub(r'\s\d{1,3}\s(?=[A-Z])', ' ', text)

    # Collapse multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def compute_text_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def embed_text(client, text, section_title, model, dimensions, task_type):
    """Embed text with section title context."""
    from google.genai import types

    # Prepend section title for context
    content = f"Gregory of Nyssa, Life of Moses — {section_title}\n\n{text}"

    result = client.models.embed_content(
        model=model,
        contents=content,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=dimensions
        )
    )
    return result.embeddings[0].values


def normalize_embedding(values):
    norm = math.sqrt(sum(v * v for v in values))
    if norm == 0:
        return values
    return [v / norm for v in values]


def main():
    parser = argparse.ArgumentParser(description="Embed Gregory's Life of Moses")
    parser.add_argument("--sections", type=str, default=None,
                        help="Comma-separated section IDs to embed")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL)
    parser.add_argument("--dimensions", type=int, default=DEFAULT_DIMENSIONS)
    parser.add_argument("--task-type", type=str, default=DEFAULT_TASK_TYPE)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--skip-notes", action="store_true", default=True,
                        help="Skip the endnotes section (default: true)")
    args = parser.parse_args()

    if not PDF_PATH.exists():
        print(f"ERROR: PDF not found at {PDF_PATH}")
        sys.exit(1)
    print(f"PDF found: {PDF_PATH}")

    manifest = load_manifest()
    sections = manifest["sections"]
    print(f"Manifest loaded: {len(sections)} sections")

    # Filter sections
    if args.sections:
        selected = set(args.sections.split(","))
        sections = [s for s in sections if s["id"] in selected]
        print(f"Selected {len(sections)} sections")

    if args.skip_notes:
        sections = [s for s in sections if s.get("book") != "notes"]
        print(f"After skipping notes: {len(sections)} sections")

    # Check API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key and not args.dry_run:
        print("ERROR: GEMINI_API_KEY not set. Use --dry-run or set the key.")
        sys.exit(1)

    client = None
    if not args.dry_run:
        from google import genai
        client = genai.Client(api_key=api_key)
        print(f"Gemini client initialized (model: {args.model}, dims: {args.dimensions})")

    # Load existing
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "sections.jsonl"
    existing = {}
    if output_path.exists() and not args.force:
        with open(output_path) as f:
            for line in f:
                if line.strip():
                    obj = json.loads(line)
                    existing[obj["section_id"]] = obj.get("text_hash")

    results = []
    skipped = 0
    errors = []

    for section in sections:
        sec_id = section["id"]
        title = section["title"]
        start_page = section["start_page"]
        end_page = section["end_page"]
        num_pages = end_page - start_page + 1

        print(f"\n--- {sec_id}: {title} (pp. {start_page}-{end_page}, {num_pages}p) ---")

        text = extract_section_text(PDF_PATH, start_page, end_page)
        if not text or len(text) < 50:
            print(f"  WARNING: Insufficient text, skipping")
            errors.append({"section": sec_id, "error": "text_extraction_failed"})
            continue

        text_hash = compute_text_hash(text)
        word_count = len(text.split())
        print(f"  Extracted: {word_count} words, hash={text_hash}")

        if sec_id in existing and existing[sec_id] == text_hash and not args.force:
            print(f"  SKIP: Already embedded")
            skipped += 1
            continue

        record = {
            "section_id": sec_id,
            "section_title": title,
            "book": section.get("book", "unknown"),
            "page_range": [start_page, end_page],
            "num_pages": num_pages,
            "word_count": word_count,
            "text_hash": text_hash,
            "symbolic_relevance": section.get("symbolic_relevance", "medium"),
            "themes": section.get("themes", []),
            "paragraphs": section.get("paragraphs", ""),
            "text_excerpt": text[:500] + "..." if len(text) > 500 else text,
            "embedding_model": args.model,
            "embedding_dimensions": args.dimensions,
            "task_type": args.task_type,
            "embedded_at": datetime.now(timezone.utc).isoformat(),
            "embedding": None
        }

        if args.dry_run:
            print(f"  DRY RUN: Would embed {word_count} words")
            record["embedding"] = f"[dry_run_{args.dimensions}d]"
            results.append(record)
            continue

        try:
            print(f"  Embedding (text, {args.dimensions}d)...")
            values = embed_text(
                client, text, title, args.model, args.dimensions, args.task_type
            )
            if args.dimensions < 3072:
                values = normalize_embedding(values)

            record["embedding"] = values
            results.append(record)
            print(f"  OK: {len(values)}-dim embedding stored")
            time.sleep(BATCH_DELAY_SECONDS)

        except Exception as e:
            print(f"  ERROR: {e}")
            errors.append({"section": sec_id, "error": str(e)})
            record["error"] = str(e)
            results.append(record)

    # Write output
    if results:
        all_records = {}
        if output_path.exists():
            with open(output_path) as f:
                for line in f:
                    if line.strip():
                        obj = json.loads(line)
                        all_records[obj["section_id"]] = obj

        for rec in results:
            all_records[rec["section_id"]] = rec

        # Write sorted by section order in manifest
        section_order = {s["id"]: i for i, s in enumerate(manifest["sections"])}
        with open(output_path, "w") as f:
            for sec_id in sorted(all_records.keys(), key=lambda x: section_order.get(x, 999)):
                f.write(json.dumps(all_records[sec_id]) + "\n")

        print(f"\n=== Results written to {output_path} ===")
        print(f"  Total sections in file: {len(all_records)}")

    # Run manifest
    run_manifest = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "pdf_path": str(PDF_PATH),
        "model": args.model,
        "dimensions": args.dimensions,
        "dry_run": args.dry_run,
        "sections_processed": len(results),
        "sections_skipped": skipped,
        "errors": errors,
        "total_words": sum(r.get("word_count", 0) for r in results),
    }
    manifest_out = OUTPUT_DIR / "run_manifest.json"
    with open(manifest_out, "w") as f:
        json.dump(run_manifest, f, indent=2)

    print(f"\n{'='*60}")
    print(f"GREGORY EMBEDDING PIPELINE COMPLETE")
    print(f"  Sections embedded: {len([r for r in results if r.get('embedding')])}")
    print(f"  Sections skipped:  {skipped}")
    print(f"  Errors:            {len(errors)}")
    if errors:
        for e in errors:
            print(f"    {e['section']}: {e['error']}")
    print(f"  Output:            {output_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
