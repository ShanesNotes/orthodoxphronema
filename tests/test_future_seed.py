from __future__ import annotations

import json
from pathlib import Path

import jsonschema

from pipeline.extract import r1_extractor as _extract_mod
from pipeline.metadata import build_future_seed as _seed_mod

REPO_ROOT = Path(__file__).parent.parent


def _load_jsonl(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def test_r1_extractor_ignores_frontmatter_and_normalizes_refs(tmp_path):
    path = tmp_path / "GEN_footnotes.md"
    path.write_text(
        "---\n"
        "book_code: GEN\n"
        "content_type: footnotes\n"
        "---\n\n"
        "### 2:7\n"
        "*(anchor: GEN.2:7)*\n\n"
        "Grace is restored in Christ (Jn 20:22) and fulfilled in [[REV.21:1]].\n\n"
        "```\n"
        "Ignore (Mk 2:27) inside code fences.\n"
        "```\n",
        encoding="utf-8",
    )

    records = _extract_mod.extract_references_from_path(path)
    anchor_ids = [record.anchor_id for record in records]
    assert anchor_ids == ["JOH.20:22", "REV.21:1"]
    assert all(record.source_file.endswith("GEN_footnotes.md") for record in records)
    assert all(record.line_number > 4 for record in records)
    assert all("GEN.2:7" not in record.raw_match for record in records)


def test_build_seed_generates_stable_genesis_outputs(tmp_path):
    mod = _seed_mod

    pericope_dir = tmp_path / "pericope"
    r1_dir = tmp_path / "r1"
    embedding_dir = tmp_path / "embedding"

    outputs = mod.build_seed(
        companion_base=REPO_ROOT / "staging" / "validated",
        pericope_out_dir=pericope_dir,
        r1_out_dir=r1_dir,
        embedding_out_dir=embedding_dir,
    )

    assert outputs["pericope_index"] == pericope_dir / "GEN.json"
    assert outputs["r1_output"] == r1_dir / "GEN.jsonl"
    assert outputs["embedding_documents"] == embedding_dir / "GEN.jsonl"

    pericope_payload = json.loads(outputs["pericope_index"].read_text(encoding="utf-8"))
    garden = next(item for item in pericope_payload["pericopes"] if item["title"] == "The Garden of Eden")

    pericope_schema = {
        "type": "object",
        "required": [
            "title",
            "start_anchor",
            "end_anchor",
            "verse_count",
            "chapter_range",
            "notes_anchors",
            "source_companions",
            "cross_ref_candidates",
            "liturgical_context",
            "alt_versification",
            "embedding_status",
            "provenance",
        ],
        "properties": {
            "title": {"type": "string"},
            "start_anchor": {"type": ["string", "null"]},
            "end_anchor": {"type": ["string", "null"]},
            "verse_count": {"type": ["integer", "null"]},
            "chapter_range": {"type": ["string", "null"]},
            "notes_anchors": {"type": "array", "items": {"type": "string"}},
            "source_companions": {"type": "array", "items": {"type": "string"}},
            "cross_ref_candidates": {"type": "array", "items": {"type": "string"}},
            "liturgical_context": {"type": ["object", "null"]},
            "alt_versification": {"type": ["object", "null"]},
            "embedding_status": {"enum": ["pending", "footnotes_ready", "ready"]},
            "provenance": {"type": ["object", "null"]},
        },
        "additionalProperties": True,
    }
    jsonschema.validate(garden, pericope_schema)

    assert garden["start_anchor"] == "GEN.2:7"
    assert garden["end_anchor"] == "GEN.2:24"
    assert garden["notes_anchors"] == ["GEN.2:7", "GEN.2:8", "GEN.2:18"]
    assert garden["source_companions"] == [
        "staging/validated/OT/GEN_footnotes.md",
        "staging/validated/OT/GEN_articles.md",
    ]
    assert "JOH.20:22" in garden["cross_ref_candidates"]
    assert "EPH.5:32" in garden["cross_ref_candidates"]
    assert garden["embedding_status"] == "footnotes_ready"
    assert garden["provenance"]["anchor_range"] == ["GEN.2:7", "GEN.2:24"]

    r1_rows = _load_jsonl(outputs["r1_output"])
    assert r1_rows
    assert any(row["anchor_id"] == "JOH.20:22" for row in r1_rows)
    assert any(row["anchor_id"] == "EPH.5:32" for row in r1_rows)
    assert all(row["raw_match"] != "GEN.2:7" for row in r1_rows)

    embedding_rows = _load_jsonl(outputs["embedding_documents"])
    assert len(embedding_rows) == 1
    seed = embedding_rows[0]
    assert seed["document_id"] == "GEN.2:7-24"
    assert seed["pericope_title"] == "The Garden of Eden"
    assert "GEN.2:7 Then God formed man" in seed["scripture_text"]
    assert seed["footnotes"]
    assert any(note["anchor"] == "GEN.2:18" for note in seed["footnotes"])
    assert "JOH.20:22" in seed["cross_ref_candidates"]
    assert seed["embedding_status"] == "footnotes_ready"
    assert seed["provenance"]["canon_source"] == "canon/OT/GEN.md"
    assert seed["provenance"]["anchor_range"] == ["GEN.2:7", "GEN.2:24"]

    first_snapshot = {
        name: path.read_text(encoding="utf-8")
        for name, path in outputs.items()
    }
    second_outputs = mod.build_seed(
        companion_base=REPO_ROOT / "staging" / "validated",
        pericope_out_dir=pericope_dir,
        r1_out_dir=r1_dir,
        embedding_out_dir=embedding_dir,
    )
    second_snapshot = {
        name: path.read_text(encoding="utf-8")
        for name, path in second_outputs.items()
    }
    assert first_snapshot == second_snapshot
