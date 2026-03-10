"""
test_batch_tools.py — Tests for batch pipeline tools: book discovery, dashboard generation, status classification.
"""
from __future__ import annotations

import json
from pathlib import Path

from pipeline.common.text import discover_staged_books, discover_staged_paths

import pipeline.tools.generate_book_status_dashboard as dashboard_mod


class TestDiscoverStagedBooks:
    """Verify book discovery logic from staging directory."""

    def test_discovers_books_from_staging(self, tmp_path, monkeypatch):
        """Should find .md files in testament subdirectories, excluding companions."""
        ot_dir = tmp_path / "OT"
        ot_dir.mkdir()
        (ot_dir / "GEN.md").write_text("---\n---\nGEN.1:1 text\n", encoding="utf-8")
        (ot_dir / "EXO.md").write_text("---\n---\nEXO.1:1 text\n", encoding="utf-8")
        (ot_dir / "GEN_notes.md").write_text("notes\n", encoding="utf-8")
        (ot_dir / "GEN_dropcap_candidates.json").write_text("{}", encoding="utf-8")

        import pipeline.common.text as text_mod
        monkeypatch.setattr(text_mod, "STAGING_ROOT", tmp_path)

        codes = discover_staged_books()
        assert "GEN" in codes
        assert "EXO" in codes
        # Companion files should be excluded
        assert "GEN_notes" not in codes

    def test_filter_by_book_code(self, tmp_path, monkeypatch):
        """Book filter should restrict discovery to specified codes."""
        ot_dir = tmp_path / "OT"
        ot_dir.mkdir()
        (ot_dir / "GEN.md").write_text("text\n", encoding="utf-8")
        (ot_dir / "EXO.md").write_text("text\n", encoding="utf-8")
        (ot_dir / "LEV.md").write_text("text\n", encoding="utf-8")

        import pipeline.common.text as text_mod
        monkeypatch.setattr(text_mod, "STAGING_ROOT", tmp_path)

        all_codes = discover_staged_books(tmp_path)
        codes = [c for c in all_codes if c in ["GEN", "LEV"]]
        assert codes == ["GEN", "LEV"]

    def test_empty_staging_returns_empty(self, tmp_path, monkeypatch):
        """Empty staging directory should return empty list."""
        import pipeline.common.text as text_mod
        monkeypatch.setattr(text_mod, "STAGING_ROOT", tmp_path)

        codes = discover_staged_books()
        assert codes == []

    def test_discover_staged_paths_returns_path_objects(self, tmp_path, monkeypatch):
        """discover_staged_paths should return Path objects."""
        ot_dir = tmp_path / "OT"
        ot_dir.mkdir()
        (ot_dir / "GEN.md").write_text("text\n", encoding="utf-8")

        import pipeline.common.text as text_mod
        monkeypatch.setattr(text_mod, "STAGING_ROOT", tmp_path)

        paths = discover_staged_paths()
        assert len(paths) == 1
        assert isinstance(paths[0], Path)
        assert paths[0].stem == "GEN"


class TestDashboardStatusClassification:
    """Verify determine_status returns correct status and reasons."""

    def test_promoted_status(self):
        """Book with canon artifact should be classified as promoted."""
        status, reasons = dashboard_mod.determine_status(
            dossier=None, editorial=None, residuals=None,
            promoted_exists=True, staged_matches_dossier=False,
        )
        assert status == "promoted"
        assert "canon artifact exists" in reasons[0]

    def test_extracting_no_dossier(self):
        """Book with no dossier should be classified as extracting."""
        status, reasons = dashboard_mod.determine_status(
            dossier=None, editorial=None, residuals=None,
            promoted_exists=False, staged_matches_dossier=False,
        )
        assert status == "extracting"

    def test_extracting_hard_failures(self):
        """Book with hard validation failures should be extracting."""
        dossier = {
            "validation": {
                "V1": {"status": "FAIL"},
                "V2": {"status": "PASS"},
                "V3": {"status": "PASS"},
                "V9": {"status": "PASS"},
            }
        }
        status, reasons = dashboard_mod.determine_status(
            dossier=dossier, editorial=None, residuals=None,
            promoted_exists=False, staged_matches_dossier=True,
        )
        assert status == "extracting"

    def test_structurally_passable_with_editorial(self):
        """Book passing validation but with editorial candidates is structurally_passable."""
        dossier = {
            "validation": {
                k: {"status": "PASS"}
                for k in dashboard_mod.PASSISH_VALIDATION_KEYS
            }
        }
        editorial = {"total_candidates": 3}
        status, reasons = dashboard_mod.determine_status(
            dossier=dossier, editorial=editorial, residuals=None,
            promoted_exists=False, staged_matches_dossier=True,
        )
        assert status == "structurally_passable"

    def test_editorially_clean_no_editorial(self):
        """Book passing validation with no editorial candidates is editorially_clean."""
        dossier = {
            "validation": {
                k: {"status": "PASS"}
                for k in dashboard_mod.PASSISH_VALIDATION_KEYS
            }
        }
        status, reasons = dashboard_mod.determine_status(
            dossier=dossier, editorial=None, residuals=None,
            promoted_exists=False, staged_matches_dossier=True,
        )
        assert status in ("editorially_clean", "promotion_ready")

    def test_promotion_ready_all_clear(self):
        """Book with all gates satisfied should be promotion_ready."""
        dossier = {
            "validation": {
                k: {"status": "PASS"}
                for k in dashboard_mod.PASSISH_VALIDATION_KEYS
            }
        }
        status, reasons = dashboard_mod.determine_status(
            dossier=dossier, editorial=None, residuals=None,
            promoted_exists=False, staged_matches_dossier=True,
        )
        assert status == "promotion_ready"


class TestDashboardHelpers:
    """Verify dashboard helper functions."""

    def test_is_pass_or_warn(self):
        """is_pass_or_warn should accept PASS and WARN, reject FAIL."""
        assert dashboard_mod.is_pass_or_warn("PASS") is True
        assert dashboard_mod.is_pass_or_warn("WARN") is True
        assert dashboard_mod.is_pass_or_warn("FAIL") is False
        assert dashboard_mod.is_pass_or_warn(None) is False

    def test_validation_map_empty_dossier(self):
        """validation_map should return empty dict for None dossier."""
        assert dashboard_mod.validation_map(None) == {}

    def test_validation_map_extracts_validation(self):
        """validation_map should extract the validation sub-dict."""
        dossier = {"validation": {"V1": {"status": "PASS"}}}
        result = dashboard_mod.validation_map(dossier)
        assert result == {"V1": {"status": "PASS"}}

    def test_editorial_summary_empty(self):
        """editorial_summary of None should return zero-count dict."""
        result = dashboard_mod.editorial_summary(None)
        assert result["total_candidates"] == 0
        assert result["by_category"] == {}

    def test_editorial_summary_with_data(self):
        """editorial_summary should reflect input data."""
        editorial = {
            "total_candidates": 5,
            "by_category": {"fused_article_explicit": 3, "truncation": 2},
        }
        result = dashboard_mod.editorial_summary(editorial)
        assert result["total_candidates"] == 5
        assert result["by_category"]["fused_article_explicit"] == 3


class TestResidualSummary:
    """Verify residual summary computation."""

    def test_empty_residuals(self):
        """Empty residuals should produce zero counts."""
        result = dashboard_mod.residual_summary(None)
        assert result["count"] == 0
        assert result["blocking_count"] == 0

    def test_blocking_residual_counted(self):
        """Blocking residuals should be counted."""
        sidecar = {
            "residuals": [
                {"anchor": "GEN.1:1", "blocking": True, "classification": "structural_fused"},
            ]
        }
        result = dashboard_mod.residual_summary(sidecar)
        assert result["count"] == 1
        assert result["blocking_count"] == 1

    def test_list_form_residuals(self):
        """Residuals passed as a bare list should still be counted."""
        residuals = [
            {"anchor": "GEN.1:1", "classification": "docling_issue"},
            {"anchor": "GEN.1:2", "classification": "docling_issue"},
        ]
        result = dashboard_mod.residual_summary(residuals)
        assert result["count"] == 2

    def test_schema_mismatch_detection(self):
        """Residuals using 'class' instead of 'classification' should be flagged."""
        sidecar = {
            "residuals": [
                {"anchor": "GEN.1:1", "class": "docling_issue"},
            ]
        }
        result = dashboard_mod.residual_summary(sidecar)
        assert result["schema_mismatch_count"] == 1


class TestDossierFreshness:
    """Verify dossier freshness status logic."""

    def test_no_dossier(self, tmp_path):
        """Missing dossier should report NO_DOSSIER."""
        result = dashboard_mod.dossier_freshness_status(None, tmp_path / "TST.md", None)
        assert result == "NO_DOSSIER"

    def test_no_staged_file(self, tmp_path):
        """Missing staged file should report NO_STAGED_FILE."""
        result = dashboard_mod.dossier_freshness_status(
            {"body_checksum": "abc"}, tmp_path / "nonexistent.md", None
        )
        assert result == "NO_STAGED_FILE"

    def test_fresh_checksum(self, tmp_path):
        """Matching checksums should report FRESH."""
        staged = tmp_path / "TST.md"
        staged.write_text("content", encoding="utf-8")
        result = dashboard_mod.dossier_freshness_status(
            {"body_checksum": "abc123"}, staged, "abc123"
        )
        assert result == "FRESH"

    def test_stale_checksum(self, tmp_path):
        """Mismatched checksums should report STALE."""
        staged = tmp_path / "TST.md"
        staged.write_text("content", encoding="utf-8")
        result = dashboard_mod.dossier_freshness_status(
            {"body_checksum": "abc123"}, staged, "def456"
        )
        assert result == "STALE"


class TestDossierRefreshPriority:
    """Verify refresh priority assignment."""

    def test_fresh_gets_none(self):
        """FRESH dossier has no refresh priority."""
        assert dashboard_mod.dossier_refresh_priority("FRESH", "extracting", None) == "none"

    def test_stale_promotion_ready_gets_high(self):
        """STALE dossier for promotion_ready book is high priority."""
        assert dashboard_mod.dossier_refresh_priority("STALE", "promotion_ready", None) == "high"

    def test_stale_structurally_passable_gets_medium(self):
        """STALE dossier for structurally_passable book is medium priority."""
        assert dashboard_mod.dossier_refresh_priority("STALE", "structurally_passable", None) == "medium"

    def test_stale_extracting_gets_low(self):
        """STALE dossier for extracting book is low priority."""
        assert dashboard_mod.dossier_refresh_priority("STALE", "extracting", None) == "low"
