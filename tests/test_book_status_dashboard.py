"""
test_book_status_dashboard.py — Status ladder and dashboard generation.
"""
from __future__ import annotations

import json
from pathlib import Path

from pipeline.tools import generate_book_status_dashboard as _dashboard_mod


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _write_markdown(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\nbook: TST\n---\n" + body,
        encoding="utf-8",
    )


def test_determine_status_promotion_ready():
    dashboard = _dashboard_mod
    dossier = {
        "validation": {
            "V1": {"status": "PASS"},
            "V2": {"status": "PASS"},
            "V3": {"status": "PASS"},
            "V4": {"status": "PASS"},
            "V5": {"status": "PASS"},
            "V6": {"status": "PASS"},
            "V7": {"status": "WARN"},
            "V8": {"status": "PASS"},
            "V9": {"status": "PASS"},
        }
    }
    editorial = {"total_candidates": 0, "by_category": {}}
    residuals = {
        "ratified_by": "human",
        "ratified_date": "2026-03-08",
        "residuals": [
            {
                "anchor": "GEN.25:34",
                "classification": "osb_source_absent",
                "blocking": False,
                "ratified": True,
            }
        ],
    }

    status, reasons = dashboard.determine_status(dossier, editorial, residuals, False, True)
    assert status == "promotion_ready"
    assert any("promotion gate conditions are satisfied" in reason for reason in reasons)


def test_determine_status_editorially_blocked():
    dashboard = _dashboard_mod
    dossier = {
        "validation": {
            "V1": {"status": "PASS"},
            "V2": {"status": "PASS"},
            "V3": {"status": "PASS"},
            "V4": {"status": "PASS"},
            "V5": {"status": "PASS"},
            "V6": {"status": "PASS"},
            "V7": {"status": "PASS"},
            "V8": {"status": "PASS"},
            "V9": {"status": "PASS"},
        }
    }
    editorial = {"total_candidates": 3, "by_category": {"chapter_open_dropcap": 2, "truncation": 1}}

    status, reasons = dashboard.determine_status(dossier, editorial, None, False, True)
    assert status == "structurally_passable"
    assert any(
        "3 editorial candidate(s) remain: chapter_open_dropcap=2, truncation=1" in reason
        for reason in reasons
    )


def test_determine_status_v11_warning_blocks_editorially_clean():
    dashboard = _dashboard_mod
    dossier = {
        "validation": {
            "V1": {"status": "PASS"},
            "V2": {"status": "PASS"},
            "V3": {"status": "PASS"},
            "V4": {"status": "PASS"},
            "V5": {"status": "PASS"},
            "V6": {"status": "PASS"},
            "V7": {"status": "WARN"},
            "V8": {"status": "PASS"},
            "V9": {"status": "PASS"},
            "V11": {"status": "WARN"},
        }
    }
    editorial = {"total_candidates": 0, "by_category": {}}

    status, reasons = dashboard.determine_status(dossier, editorial, None, False, True)
    assert status == "structurally_passable"
    assert any("validation still reports editorial issues: V11" in reason for reason in reasons)


def test_determine_status_stale_dossier_blocks_promotion_ready():
    dashboard = _dashboard_mod
    dossier = {
        "validation": {
            "V1": {"status": "PASS"},
            "V2": {"status": "PASS"},
            "V3": {"status": "PASS"},
            "V4": {"status": "PASS"},
            "V5": {"status": "PASS"},
            "V6": {"status": "PASS"},
            "V7": {"status": "PASS"},
            "V8": {"status": "PASS"},
            "V9": {"status": "PASS"},
        }
    }
    editorial = {"total_candidates": 0, "by_category": {}}

    status, reasons = dashboard.determine_status(dossier, editorial, None, False, False)
    assert status == "editorially_clean"
    assert any("checksum does not match current staged file" in reason for reason in reasons)


def test_dossier_refresh_priority_escalates_ready_books():
    dashboard = _dashboard_mod
    assert dashboard.dossier_refresh_priority("STALE", "promotion_ready", "dry-run") == "high"
    assert dashboard.dossier_refresh_priority("STALE", "editorially_clean", "dry-run") == "high"
    assert dashboard.dossier_refresh_priority("STALE", "extracting", "blocked") == "low"
    assert dashboard.dossier_refresh_priority("FRESH", "promotion_ready", "dry-run") == "none"


def test_editorial_reason_summarizes_top_categories():
    dashboard = _dashboard_mod
    reason = dashboard.editorial_reason(
        {
            "total_candidates": 6,
            "by_category": {
                "chapter_open_dropcap": 3,
                "split_word_residue": 2,
                "truncation": 1,
                "fused_article_explicit": 1,
            },
        }
    )
    assert reason == (
        "6 editorial candidate(s) remain: "
        "chapter_open_dropcap=3, split_word_residue=2, fused_article_explicit=1"
    )


def test_build_dashboard_reads_repo_artifacts(tmp_path):
    dashboard = _dashboard_mod

    _write_json(
        tmp_path / "schemas" / "anchor_registry.json",
        {
            "registry_version": "1.2.2",
            "books": [
                {"code": "AAA", "testament": "OT"},
                {"code": "BBB", "testament": "OT"},
            ],
        },
    )
    _write_json(
        tmp_path / "schemas" / "residual_classes.json",
        {
            "classes": [
                {"name": "osb_source_absent", "requires_per_entry_ratification": True},
                {"name": "docling_issue", "requires_per_entry_ratification": False},
            ]
        },
    )
    _write_json(
        tmp_path / "reports" / "AAA_promotion_dossier.json",
        {
            "decision": "dry-run",
            "body_checksum": "abc",
            "validation": {
                "V1": {"status": "PASS"},
                "V2": {"status": "PASS"},
                "V3": {"status": "PASS"},
                "V4": {"status": "PASS"},
                "V5": {"status": "PASS"},
                "V6": {"status": "PASS"},
                "V7": {"status": "WARN"},
                "V8": {"status": "PASS"},
                "V9": {"status": "PASS"},
            },
        },
    )
    _write_json(
        tmp_path / "staging" / "validated" / "OT" / "AAA_editorial_candidates.json",
        {"total_candidates": 0, "by_category": {}},
    )
    _write_json(
        tmp_path / "staging" / "validated" / "OT" / "AAA_residuals.json",
        {
            "ratified_by": "human",
            "ratified_date": "2026-03-08",
            "residuals": [
                {
                    "anchor": "AAA.1:4",
                    "classification": "osb_source_absent",
                    "blocking": False,
                    "ratified": True,
                }
            ],
        },
    )
    _write_markdown(
        tmp_path / "staging" / "validated" / "OT" / "AAA.md",
        "AAA.1:1 Current staged text.\n",
    )
    _write_json(
        tmp_path / "reports" / "BBB_promotion_dossier.json",
        {
            "decision": "blocked",
            "body_checksum": "def",
            "validation": {
                "V1": {"status": "PASS"},
                "V2": {"status": "PASS"},
                "V3": {"status": "PASS"},
                "V4": {"status": "PASS"},
                "V5": {"status": "PASS"},
                "V6": {"status": "PASS"},
                "V7": {"status": "PASS"},
                "V8": {"status": "PASS"},
                "V9": {"status": "PASS"},
            },
        },
    )
    _write_json(
        tmp_path / "staging" / "validated" / "OT" / "BBB_editorial_candidates.json",
        {"total_candidates": 2, "by_category": {"truncation": 2}},
    )
    _write_markdown(
        tmp_path / "staging" / "validated" / "OT" / "BBB.md",
        "BBB.1:1 Current staged text.\n",
    )

    dashboard.REPO_ROOT = tmp_path
    dashboard.REGISTRY = tmp_path / "schemas" / "anchor_registry.json"
    dashboard.RESIDUAL_CLASSES = tmp_path / "schemas" / "residual_classes.json"
    dashboard.REPORTS_ROOT = tmp_path / "reports"
    dashboard.STAGING_ROOT = tmp_path / "staging" / "validated"
    dashboard.CANON_ROOT = tmp_path / "canon"

    data = dashboard.build_dashboard()
    statuses = {entry["book_code"]: entry["status"] for entry in data["books"]}
    assert statuses["AAA"] == "editorially_clean"
    assert statuses["BBB"] == "structurally_passable"
    freshness = {entry["book_code"]: entry["dossier_freshness"]["status"] for entry in data["books"]}
    priorities = {entry["book_code"]: entry["dossier_freshness"]["refresh_priority"] for entry in data["books"]}
    assert freshness["AAA"] == "STALE"
    assert priorities["AAA"] == "high"
