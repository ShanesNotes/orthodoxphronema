#!/usr/bin/env python3
"""Generate Noah's reading manifest from the anchor registry.

Reads schemas/anchor_registry.json and produces noah_manifest.json:
a flat list of every chapter-portion in canonical order, with metadata
Noah's harness needs to extract and serve each daily reading.

Usage:
    python3 experimental/noah/manifest_generator.py
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY = REPO_ROOT / "schemas" / "anchor_registry.json"
OUTPUT = Path(__file__).resolve().parent / "noah_manifest.json"


def build_manifest():
    with open(REGISTRY) as f:
        reg = json.load(f)

    portions = []
    day = 0

    for book in reg["books"]:
        code = book["code"]
        name = book["name"]
        testament = book["testament"]
        position = book["position"]
        deuterocanonical = book.get("deuterocanonical", False)
        chapters = book["chapters"]
        prefix = f"{position:02d}_{code}"
        canon_path = f"canon/{testament}/{prefix}.md"

        for ch in range(1, chapters + 1):
            day += 1
            portions.append({
                "day": day,
                "book_code": code,
                "book_name": name,
                "testament": testament,
                "canon_position": position,
                "deuterocanonical": deuterocanonical,
                "chapter": ch,
                "total_chapters": chapters,
                "canon_file": canon_path,
                "entry_filename": f"{day:04d}_{code}_{ch:02d}.md",
            })

    manifest = {
        "generated_from": "schemas/anchor_registry.json",
        "registry_version": reg["registry_version"],
        "total_days": day,
        "total_books": len(reg["books"]),
        "psalm_numbering": reg.get("psalm_numbering", "LXX"),
        "portions": portions,
    }

    with open(OUTPUT, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Manifest written: {OUTPUT}")
    print(f"  {manifest['total_books']} books, {manifest['total_days']} daily portions")
    return manifest


if __name__ == "__main__":
    build_manifest()
