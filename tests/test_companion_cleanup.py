from __future__ import annotations

import json

from pipeline.cleanup import companion_audit as audit_mod
from pipeline.cleanup import reindex_markers as reindex_mod


def _write_marker_file(path, anchors: list[str]) -> None:
    path.write_text(
        json.dumps(
            {
                "book_code": "TST",
                "marker_count": len(anchors),
                "markers": [
                    {
                        "marker": "unknown",
                        "anchor": anchor,
                        "marker_index_in_verse": 1,
                        "marker_seq_book": idx,
                        "source": "fixture",
                    }
                    for idx, anchor in enumerate(anchors, 1)
                ],
            }
        ),
        encoding="utf-8",
    )


def test_reindex_markers_rebuilds_equal_count_anchor_mismatch(tmp_path, monkeypatch):
    staging_root = tmp_path / "staging" / "validated"
    testament_dir = staging_root / "NT"
    testament_dir.mkdir(parents=True)

    footnotes_path = testament_dir / "TST_footnotes.md"
    footnotes_path.write_text(
        "---\nbook_code: TST\n---\n\n"
        "### 1:1\n*(anchor: TST.1:1)*\n"
        "### 1:2\n*(anchor: TST.1:2)*\n",
        encoding="utf-8",
    )
    markers_path = testament_dir / "TST_footnote_markers.json"
    _write_marker_file(markers_path, ["TST.1:1", "TST.1:3"])

    monkeypatch.setattr(reindex_mod, "STAGING_ROOT", staging_root)

    result = reindex_mod.reindex_book_from_footnotes("TST", "NT")

    assert result["action"] == "reindexed"
    assert result["aligned"] is False
    payload = json.loads(markers_path.read_text(encoding="utf-8"))
    assert [marker["anchor"] for marker in payload["markers"]] == ["TST.1:1", "TST.1:2"]


def test_reindex_markers_force_rebuilds_aligned_markers(tmp_path, monkeypatch):
    staging_root = tmp_path / "staging" / "validated"
    testament_dir = staging_root / "NT"
    testament_dir.mkdir(parents=True)

    footnotes_path = testament_dir / "TST_footnotes.md"
    footnotes_path.write_text(
        "---\nbook_code: TST\n---\n\n"
        "### 1:1\n*(anchor: TST.1:1)*\n",
        encoding="utf-8",
    )
    markers_path = testament_dir / "TST_footnote_markers.json"
    _write_marker_file(markers_path, ["TST.1:1"])
    original = markers_path.read_text(encoding="utf-8")

    monkeypatch.setattr(reindex_mod, "STAGING_ROOT", staging_root)

    result = reindex_mod.reindex_book_from_footnotes("TST", "NT", force=True)

    assert result["action"] == "reindexed"
    payload = json.loads(markers_path.read_text(encoding="utf-8"))
    assert payload["markers"][0]["source"] == "reindexed_from_footnotes_md"
    assert markers_path.read_text(encoding="utf-8") != original


def test_companion_audit_detects_marker_alignment_failure(tmp_path, monkeypatch):
    staging_root = tmp_path / "staging" / "validated"
    testament_dir = staging_root / "NT"
    testament_dir.mkdir(parents=True)

    (testament_dir / "TST_footnotes.md").write_text(
        "---\n"
        "book_code: TST\n"
        "content_type: footnotes\n"
        "source: OSB-v1\n"
        "parse_date: 2026-03-13\n"
        "status: staging\n"
        "---\n\n"
        "### 1:1\n*(anchor: TST.1:1)*\n",
        encoding="utf-8",
    )
    (testament_dir / "TST_articles.md").write_text(
        "---\n"
        "book_code: TST\n"
        "content_type: article\n"
        "source: OSB-v1\n"
        "parse_date: 2026-03-13\n"
        "status: staging\n"
        "---\n\n"
        "*(No OSB study articles for this book.)*\n",
        encoding="utf-8",
    )
    _write_marker_file(testament_dir / "TST_footnote_markers.json", ["TST.1:2"])

    monkeypatch.setattr(audit_mod, "STAGING_ROOT", staging_root)
    monkeypatch.setattr(
        audit_mod,
        "load_registry",
        lambda: {"books": [{"code": "TST", "testament": "NT"}]},
    )

    report = audit_mod.run_audit()
    summary = report["summary"]
    book_report = report["books"]["TST"]

    assert summary["marker_alignment_fail"] == 1
    assert summary["empty_articles"] == 1
    assert book_report["markers"]["alignment"] == "fail"
    assert book_report["markers"]["markers_only"] == 1
    assert book_report["markers"]["footnotes_only"] == 1
