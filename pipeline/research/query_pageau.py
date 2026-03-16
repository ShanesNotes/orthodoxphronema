#!/usr/bin/env python3
"""
Pageau Embedding Query Tool
============================
Semantic search over the embedded Language of Creation chapters.
Used by agents at runtime to retrieve symbolic grammar context.

Usage:
    # Semantic search
    python3 pipeline/research/query_pageau.py "burning bush fire that doesn't consume"

    # Search with top-k control
    python3 pipeline/research/query_pageau.py "seed and flesh exchange" --top-k 5

    # Filter by part
    python3 pipeline/research/query_pageau.py "time and space" --part IV

    # Filter by symbolic topic
    python3 pipeline/research/query_pageau.py "heaven earth polarity" --topic polarities:heaven_earth

    # Output as JSON (for agent consumption)
    python3 pipeline/research/query_pageau.py "microcosm pattern" --json

Environment:
    GEMINI_API_KEY  — required for query embedding
"""

import json
import os
import sys
import math
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EMBEDDINGS_PATH = REPO_ROOT / "metadata" / "embeddings" / "pageau" / "chapters.jsonl"

DEFAULT_MODEL = "gemini-embedding-2-preview"
DEFAULT_DIMENSIONS = 768
QUERY_TASK_TYPE = "RETRIEVAL_QUERY"


def load_embeddings():
    """Load all chapter embeddings from JSONL."""
    chapters = []
    with open(EMBEDDINGS_PATH) as f:
        for line in f:
            if line.strip():
                obj = json.loads(line)
                if obj.get("embedding") and isinstance(obj["embedding"], list):
                    chapters.append(obj)
    return chapters


def embed_query(client, query, model, dimensions):
    """Embed a query string for retrieval."""
    from google.genai import types
    result = client.models.embed_content(
        model=model,
        contents=query,
        config=types.EmbedContentConfig(
            task_type=QUERY_TASK_TYPE,
            output_dimensionality=dimensions
        )
    )
    values = result.embeddings[0].values
    # Normalize
    if dimensions < 3072:
        norm = math.sqrt(sum(v * v for v in values))
        if norm > 0:
            values = [v / norm for v in values]
    return values


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def search(query_embedding, chapters, top_k=3, part_filter=None, topic_filter=None):
    """Rank chapters by cosine similarity to query."""
    scored = []
    for ch in chapters:
        # Apply filters
        if part_filter and ch.get("part") != part_filter:
            continue
        if topic_filter and topic_filter not in ch.get("symbolic_topics", []):
            continue

        sim = cosine_similarity(query_embedding, ch["embedding"])
        scored.append({
            "chapter_number": ch["chapter_number"],
            "chapter_title": ch["chapter_title"],
            "part": ch["part"],
            "part_title": ch["part_title"],
            "page_range": ch["page_range"],
            "symbolic_topics": ch.get("symbolic_topics", []),
            "similarity": round(sim, 4),
            "text_excerpt": ch.get("text_excerpt", ""),
        })

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]


def main():
    parser = argparse.ArgumentParser(description="Query Pageau embeddings")
    parser.add_argument("query", type=str, help="Search query")
    parser.add_argument("--top-k", type=int, default=3, help="Number of results")
    parser.add_argument("--part", type=str, default=None, help="Filter by part (I-VI)")
    parser.add_argument("--topic", type=str, default=None, help="Filter by symbolic topic")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL)
    parser.add_argument("--dimensions", type=int, default=DEFAULT_DIMENSIONS)
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    # Check dependencies
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    if not EMBEDDINGS_PATH.exists():
        print(f"ERROR: No embeddings found at {EMBEDDINGS_PATH}", file=sys.stderr)
        print("  Run embed_pageau.py first to generate embeddings.", file=sys.stderr)
        sys.exit(1)

    # Load embeddings
    chapters = load_embeddings()
    if not chapters:
        print("ERROR: No valid embeddings found", file=sys.stderr)
        sys.exit(1)

    # Embed query
    from google import genai
    client = genai.Client(api_key=api_key)
    query_vec = embed_query(client, args.query, args.model, args.dimensions)

    # Search
    results = search(query_vec, chapters, args.top_k, args.part, args.topic)

    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"\nQuery: \"{args.query}\"")
        print(f"Results: {len(results)} (from {len(chapters)} chapters)\n")
        for i, r in enumerate(results, 1):
            print(f"  {i}. Ch {r['chapter_number']}: {r['chapter_title']}")
            print(f"     Part {r['part']}: {r['part_title']}")
            print(f"     Pages: {r['page_range'][0]}-{r['page_range'][1]}")
            print(f"     Similarity: {r['similarity']}")
            if r['symbolic_topics']:
                print(f"     Topics: {', '.join(r['symbolic_topics'])}")
            print(f"     Excerpt: {r['text_excerpt'][:200]}...")
            print()


if __name__ == "__main__":
    main()
