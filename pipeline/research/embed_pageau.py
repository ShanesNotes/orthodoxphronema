#!/usr/bin/env python3
"""
Pageau 'Language of Creation' Embedding Pipeline
=================================================
Embeds each chapter of the Language of Creation PDF using Gemini embedding-2-preview.
Produces multimodal embeddings (text + diagrams) at chapter granularity.

Usage:
    # Embed all chapters
    python3 pipeline/research/embed_pageau.py

    # Embed specific chapter range
    python3 pipeline/research/embed_pageau.py --chapters 5-13

    # Dry run (extract text, no API calls)
    python3 pipeline/research/embed_pageau.py --dry-run

    # Use text-only model instead
    python3 pipeline/research/embed_pageau.py --model gemini-embedding-001

Environment:
    GEMINI_API_KEY  — required, your Google AI API key

Output:
    metadata/embeddings/pageau/chapters.jsonl  — one JSON object per chapter
    metadata/embeddings/pageau/manifest.json   — run metadata and stats
"""

import json
import os
import sys
import time
import argparse
import hashlib
from pathlib import Path
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "pipeline" / "research" / "pageau_chapter_manifest.json"
OUTPUT_DIR = REPO_ROOT / "metadata" / "embeddings" / "pageau"
PDF_FILENAME = "The-Language-of-Creation-Cosmic-Symbolism-in-Genesis-A-Commentary.pdf"

# Search multiple locations for the PDF
PDF_SEARCH_PATHS = [
    REPO_ROOT / "src.texts" / PDF_FILENAME,
    REPO_ROOT / "research" / PDF_FILENAME,
    Path.home() / "orthodoxphronema" / "src.texts" / PDF_FILENAME,
]

DEFAULT_MODEL = "gemini-embedding-2-preview"
DEFAULT_DIMENSIONS = 768
DEFAULT_TASK_TYPE = "RETRIEVAL_DOCUMENT"
BATCH_DELAY_SECONDS = 1.5  # rate limit courtesy delay between API calls
MAX_PAGES_PER_EMBED = 6    # gemini-embedding-2-preview PDF page limit


def find_pdf():
    """Locate the Language of Creation PDF."""
    for p in PDF_SEARCH_PATHS:
        if p.exists():
            return p
    # Also check if passed via env
    env_path = os.environ.get("PAGEAU_PDF_PATH")
    if env_path and Path(env_path).exists():
        return Path(env_path)
    return None


def load_manifest():
    """Load the chapter manifest with page boundaries."""
    with open(MANIFEST_PATH) as f:
        return json.load(f)


def extract_chapter_text_pdftotext(pdf_path, start_page, end_page):
    """Extract text from a page range using pdftotext (if available)."""
    import subprocess
    try:
        result = subprocess.run(
            ["pdftotext", "-f", str(start_page), "-l", str(end_page),
             "-layout", str(pdf_path), "-"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def extract_chapter_text_pymupdf(pdf_path, start_page, end_page):
    """Extract text using PyMuPDF (fitz) — 0-indexed pages."""
    try:
        import fitz
        doc = fitz.open(str(pdf_path))
        text_parts = []
        # PDF pages are 1-indexed in manifest, 0-indexed in fitz
        for page_num in range(start_page - 1, min(end_page, len(doc))):
            page = doc[page_num]
            text_parts.append(page.get_text())
        doc.close()
        return "\n".join(text_parts).strip()
    except ImportError:
        return None


def extract_chapter_pdf_bytes(pdf_path, start_page, end_page):
    """Extract a page range as PDF bytes for multimodal embedding."""
    try:
        import fitz
        src = fitz.open(str(pdf_path))
        dst = fitz.open()
        # fitz uses 0-indexed pages
        for page_num in range(start_page - 1, min(end_page, len(src))):
            dst.insert_pdf(src, from_page=page_num, to_page=page_num)
        pdf_bytes = dst.tobytes()
        dst.close()
        src.close()
        return pdf_bytes
    except ImportError:
        return None


def get_part_for_chapter(manifest, ch_num):
    """Look up which Part a chapter belongs to."""
    for part in manifest["parts"]:
        if ch_num in part["chapters"]:
            return {"part": part["part"], "title": part["title"]}
    # Chapter 0 (Introduction) is before Part I
    if ch_num == 0:
        return {"part": "Intro", "title": "Introduction"}
    return {"part": "unknown", "title": "unknown"}


def get_symbolic_topics(manifest, ch_num):
    """Look up symbolic topic tags for a chapter."""
    topics = []
    st = manifest.get("symbolic_topics", {})
    for category_name, category in st.items():
        if category_name.startswith("_"):
            continue
        for topic_name, chapters in category.items():
            if ch_num in chapters:
                topics.append(f"{category_name}:{topic_name}")
    return topics


def embed_text_only(client, text, model, dimensions, task_type):
    """Embed using text-only mode."""
    from google.genai import types
    result = client.models.embed_content(
        model=model,
        contents=text,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=dimensions
        )
    )
    return result.embeddings[0].values


def embed_multimodal_pdf(client, pdf_bytes, chapter_title, model, dimensions, task_type):
    """Embed PDF pages as multimodal content (text + diagrams)."""
    from google.genai import types

    # Build a multimodal content object: text context + PDF bytes
    parts = [
        types.Part(text=f"Chapter: {chapter_title}"),
        types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")
    ]

    result = client.models.embed_content(
        model=model,
        contents=[types.Content(parts=parts)],
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=dimensions
        )
    )
    return result.embeddings[0].values


def normalize_embedding(values):
    """L2-normalize an embedding vector (required for dims < 3072)."""
    import math
    norm = math.sqrt(sum(v * v for v in values))
    if norm == 0:
        return values
    return [v / norm for v in values]


def compute_text_hash(text):
    """SHA-256 hash of extracted text for change detection."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def main():
    parser = argparse.ArgumentParser(description="Embed Pageau's Language of Creation")
    parser.add_argument("--chapters", type=str, default=None,
                        help="Chapter range to embed, e.g. '5-13' or '0' or '5,10,15'")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL,
                        help=f"Embedding model (default: {DEFAULT_MODEL})")
    parser.add_argument("--dimensions", type=int, default=DEFAULT_DIMENSIONS,
                        help=f"Output dimensions (default: {DEFAULT_DIMENSIONS})")
    parser.add_argument("--task-type", type=str, default=DEFAULT_TASK_TYPE,
                        help=f"Task type (default: {DEFAULT_TASK_TYPE})")
    parser.add_argument("--text-only", action="store_true",
                        help="Use text-only embedding (skip multimodal PDF)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Extract text and build metadata, but skip API calls")
    parser.add_argument("--force", action="store_true",
                        help="Re-embed chapters even if already embedded")
    args = parser.parse_args()

    # --- Locate PDF ---
    pdf_path = find_pdf()
    if pdf_path is None:
        print("ERROR: Cannot find Language of Creation PDF.")
        print(f"  Searched: {[str(p) for p in PDF_SEARCH_PATHS]}")
        print(f"  Set PAGEAU_PDF_PATH environment variable to the PDF location.")
        sys.exit(1)
    print(f"PDF found: {pdf_path}")

    # --- Load manifest ---
    manifest = load_manifest()
    chapters = manifest["chapters"]
    print(f"Manifest loaded: {len(chapters)} chapters")

    # --- Parse chapter selection ---
    if args.chapters:
        if "-" in args.chapters and "," not in args.chapters:
            start, end = args.chapters.split("-")
            selected = set(range(int(start), int(end) + 1))
        elif "," in args.chapters:
            selected = set(int(x.strip()) for x in args.chapters.split(","))
        else:
            selected = {int(args.chapters)}
        chapters = [c for c in chapters if c["ch"] in selected]
        print(f"Selected {len(chapters)} chapters: {sorted(selected)}")

    # --- Check API key ---
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key and not args.dry_run:
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        print("  Set it with: export GEMINI_API_KEY='your-key-here'")
        print("  Or use --dry-run to extract text without embedding.")
        sys.exit(1)

    # --- Initialize Gemini client ---
    client = None
    if not args.dry_run:
        from google import genai
        client = genai.Client(api_key=api_key)
        print(f"Gemini client initialized (model: {args.model}, dims: {args.dimensions})")

    # --- Load existing embeddings to skip already-done chapters ---
    output_path = OUTPUT_DIR / "chapters.jsonl"
    existing = {}
    if output_path.exists() and not args.force:
        with open(output_path) as f:
            for line in f:
                if line.strip():
                    obj = json.loads(line)
                    existing[obj["chapter_number"]] = obj.get("text_hash")
        print(f"Found {len(existing)} existing embeddings (use --force to re-embed)")

    # --- Process chapters ---
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    skipped = 0
    errors = []

    for ch_info in chapters:
        ch_num = ch_info["ch"]
        title = ch_info["title"]
        start_page = ch_info["start_page"]
        end_page = ch_info["end_page"]
        num_pages = end_page - start_page + 1

        print(f"\n--- Chapter {ch_num}: {title} (pp. {start_page}-{end_page}, {num_pages}p) ---")

        # Extract text
        text = extract_chapter_text_pymupdf(pdf_path, start_page, end_page)
        if text is None:
            text = extract_chapter_text_pdftotext(pdf_path, start_page, end_page)
        if text is None or len(text.strip()) < 50:
            print(f"  WARNING: Could not extract meaningful text, skipping")
            errors.append({"ch": ch_num, "error": "text_extraction_failed"})
            continue

        text_hash = compute_text_hash(text)
        word_count = len(text.split())
        print(f"  Extracted: {word_count} words, hash={text_hash}")

        # Skip if already embedded with same content
        if ch_num in existing and existing[ch_num] == text_hash and not args.force:
            print(f"  SKIP: Already embedded with same content hash")
            skipped += 1
            continue

        # Build metadata
        part_info = get_part_for_chapter(manifest, ch_num)
        symbolic_topics = get_symbolic_topics(manifest, ch_num)

        record = {
            "chapter_number": ch_num,
            "chapter_title": title,
            "part": part_info["part"],
            "part_title": part_info["title"],
            "page_range": [start_page, end_page],
            "num_pages": num_pages,
            "word_count": word_count,
            "text_hash": text_hash,
            "symbolic_topics": symbolic_topics,
            "text_excerpt": text[:500] + "..." if len(text) > 500 else text,
            "embedding_model": args.model,
            "embedding_dimensions": args.dimensions,
            "task_type": args.task_type,
            "embedding_mode": "text_only" if args.text_only else "multimodal_pdf",
            "embedded_at": datetime.now(timezone.utc).isoformat(),
            "embedding": None
        }

        if args.dry_run:
            print(f"  DRY RUN: Would embed {word_count} words")
            record["embedding"] = f"[dry_run_{args.dimensions}d]"
            results.append(record)
            continue

        # --- Embed ---
        try:
            if args.text_only or args.model == "gemini-embedding-001":
                # Text-only embedding
                print(f"  Embedding (text-only, {args.dimensions}d)...")
                values = embed_text_only(
                    client, text, args.model, args.dimensions, args.task_type
                )
            else:
                # Multimodal PDF embedding
                if num_pages > MAX_PAGES_PER_EMBED:
                    # Split into sub-chunks if chapter exceeds 6 pages
                    print(f"  WARNING: {num_pages} pages exceeds {MAX_PAGES_PER_EMBED} limit")
                    print(f"  Falling back to text-only for this chapter")
                    values = embed_text_only(
                        client, text, args.model, args.dimensions, args.task_type
                    )
                    record["embedding_mode"] = "text_only_fallback"
                else:
                    pdf_bytes = extract_chapter_pdf_bytes(pdf_path, start_page, end_page)
                    if pdf_bytes is None:
                        print(f"  WARNING: Could not extract PDF bytes, falling back to text")
                        values = embed_text_only(
                            client, text, args.model, args.dimensions, args.task_type
                        )
                        record["embedding_mode"] = "text_only_fallback"
                    else:
                        print(f"  Embedding (multimodal PDF, {num_pages}p, {args.dimensions}d)...")
                        values = embed_multimodal_pdf(
                            client, pdf_bytes, title, args.model, args.dimensions, args.task_type
                        )

            # Normalize if not full dimensionality
            if args.dimensions < 3072:
                values = normalize_embedding(values)

            record["embedding"] = values
            results.append(record)
            print(f"  OK: {len(values)}-dim embedding stored")

            # Rate limit courtesy
            time.sleep(BATCH_DELAY_SECONDS)

        except Exception as e:
            print(f"  ERROR: {e}")
            errors.append({"ch": ch_num, "error": str(e)})
            record["embedding"] = None
            record["error"] = str(e)
            results.append(record)

    # --- Write output ---
    if results:
        # Append mode: read existing, merge, write
        all_records = {}
        if output_path.exists():
            with open(output_path) as f:
                for line in f:
                    if line.strip():
                        obj = json.loads(line)
                        all_records[obj["chapter_number"]] = obj

        # Merge new results
        for rec in results:
            all_records[rec["chapter_number"]] = rec

        # Write sorted by chapter number
        with open(output_path, "w") as f:
            for ch_num in sorted(all_records.keys()):
                f.write(json.dumps(all_records[ch_num]) + "\n")

        print(f"\n=== Results written to {output_path} ===")
        print(f"  Total chapters in file: {len(all_records)}")

    # --- Write run manifest ---
    run_manifest = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "pdf_path": str(pdf_path),
        "model": args.model,
        "dimensions": args.dimensions,
        "task_type": args.task_type,
        "text_only": args.text_only,
        "dry_run": args.dry_run,
        "chapters_processed": len(results),
        "chapters_skipped": skipped,
        "errors": errors,
        "total_words": sum(r.get("word_count", 0) for r in results),
    }
    manifest_out = OUTPUT_DIR / "run_manifest.json"
    with open(manifest_out, "w") as f:
        json.dump(run_manifest, f, indent=2)

    # --- Summary ---
    print(f"\n{'='*60}")
    print(f"EMBEDDING PIPELINE COMPLETE")
    print(f"  Chapters embedded:  {len([r for r in results if r.get('embedding')])}")
    print(f"  Chapters skipped:   {skipped}")
    print(f"  Errors:             {len(errors)}")
    if errors:
        for e in errors:
            print(f"    Ch {e['ch']}: {e['error']}")
    print(f"  Output:             {output_path}")
    print(f"  Run manifest:       {manifest_out}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
