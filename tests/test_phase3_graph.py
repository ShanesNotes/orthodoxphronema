from __future__ import annotations

import json
from pathlib import Path

from pipeline.graph import build_backlinks as backlinks_mod
from pipeline.graph import regenerate_graph as graph_mod
from pipeline.validate import validate_phase3 as validate_mod


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n"
    path.write_text(payload, encoding="utf-8")


def _write_registry(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "books": [
                    {
                        "code": "PSA",
                        "testament": "OT",
                        "chapter_verse_counts": [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


def test_build_backlinks_shards_and_domains(tmp_path):
    registry = tmp_path / "schemas" / "anchor_registry.json"
    _write_registry(registry)
    input_path = tmp_path / "metadata" / "r1_output" / "PSA.jsonl"
    _write_jsonl(
        input_path,
        [
            {
                "source_file": "articles/PSA_articles.md",
                "line_number": 12,
                "raw_match": "[[PSA.44:10]]",
                "anchor_id": "PSA.44:10",
                "reference_type": "frozen",
                "context": "Study context",
            },
            {
                "source_file": "phronema/liturgics/theotokos.md",
                "line_number": 7,
                "raw_match": "Ps 44:10",
                "anchor_id": "PSA.44:10",
                "reference_type": "bare",
                "context": "Liturgical context",
            },
        ],
    )

    written = backlinks_mod.build_from_paths([input_path], output_root=tmp_path / "metadata" / "anchor_backlinks", registry_path=registry)
    assert len(written) == 2

    study_payload = json.loads((tmp_path / "metadata" / "anchor_backlinks" / "study" / "PSA.44-10.json").read_text(encoding="utf-8"))
    lit_payload = json.loads((tmp_path / "metadata" / "anchor_backlinks" / "liturgical" / "PSA.44-10.json").read_text(encoding="utf-8"))
    assert study_payload["canon_uri"] == "canon/OT/PSA.md#PSA.44:10"
    assert study_payload["links"][0]["source_file"] == "articles/PSA_articles.md"
    assert lit_payload["links"][0]["source_file"] == "phronema/liturgics/theotokos.md"


def test_validate_phase3_detects_dangling_and_zero_degree(tmp_path, monkeypatch):
    registry = tmp_path / "schemas" / "anchor_registry.json"
    _write_registry(registry)

    canon_dir = tmp_path / "canon" / "OT"
    canon_dir.mkdir(parents=True)
    (canon_dir / "PSA.md").write_text(
        "---\nbook_code: PSA\n---\nPSA.44:10 text\nPSA.44:11 text\n",
        encoding="utf-8",
    )
    backlinks_root = tmp_path / "metadata" / "anchor_backlinks" / "study"
    backlinks_root.mkdir(parents=True)
    (backlinks_root / "PSA.44-10.json").write_text(
        json.dumps(
            {
                "anchor_id": "PSA.44:99",
                "canon_uri": "canon/OT/PSA.md#PSA.44:99",
                "text_tradition": "LXX",
                "generated_at": "2026-03-13T00:00:00+00:00",
                "generator_version": "phase3-backlinks-v1",
                "links": [],
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(validate_mod, "CANON_ROOT", tmp_path / "canon")
    report = validate_mod.validate_backlinks(tmp_path / "metadata" / "anchor_backlinks", registry_path=registry, book_code="PSA")
    assert report["status"] == "FAIL"
    assert any("dangling target anchor" in error for error in report["errors"])


def test_collect_graph_rows_emits_anchor_and_source_nodes(tmp_path):
    backlinks_root = tmp_path / "metadata" / "anchor_backlinks" / "study"
    backlinks_root.mkdir(parents=True)
    (backlinks_root / "PSA.44-10.json").write_text(
        json.dumps(
            {
                "anchor_id": "PSA.44:10",
                "canon_uri": "canon/OT/PSA.md#PSA.44:10",
                "text_tradition": "LXX",
                "generated_at": "2026-03-13T00:00:00+00:00",
                "generator_version": "phase3-backlinks-v1",
                "links": [
                    {
                        "source_file": "articles/PSA_articles.md",
                        "line_number": 12,
                        "raw_match": "[[PSA.44:10]]",
                        "reference_type": "frozen",
                        "context": "Study context",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    nodes, edges = graph_mod.collect_graph_rows(tmp_path / "metadata" / "anchor_backlinks")
    node_ids = {node["node_id"] for node in nodes}
    assert "anchor:PSA.44:10" in node_ids
    assert "source:articles/PSA_articles.md" in node_ids
    assert len(edges) == 1
