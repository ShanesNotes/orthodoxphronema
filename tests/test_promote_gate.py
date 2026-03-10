"""
test_promote_gate.py — Promotion gate tests (D1-D5 hardening + per-entry ratification).
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from pipeline.promote import promote as _promote_mod

REPO_ROOT = Path(__file__).parent.parent


def _load_promote():
    return _promote_mod


def _make_staged_file(tmp: Path, book_code: str = "TST") -> Path:
    """Create a minimal staged file with a V4 gap (v3→v5)."""
    staged_dir = tmp / "staging" / "validated" / "OT"
    staged_dir.mkdir(parents=True)
    path = staged_dir / f"{book_code}.md"
    path.write_text(
        "---\n"
        f"book_code: {book_code}\n"
        "book_name: Test Book\n"
        "testament: OT\n"
        "canon_position: 1\n"
        "source: test\n"
        "parse_date: 2026-01-01\n"
        "status: staged\n"
        "promote_date: \"\"\n"
        "checksum: \"\"\n"
        "---\n"
        "## Chapter 1\n"
        f"{book_code}.1:1 verse one\n"
        f"{book_code}.1:2 verse two\n"
        f"{book_code}.1:3 verse three\n"
        f"{book_code}.1:5 verse five\n",
        encoding="utf-8",
    )
    return path


def _make_sidecar(tmp: Path, entries: list[dict], book_code: str = "TST",
                  ratified_date: str | None = "2026-03-08") -> Path:
    """Create a residuals sidecar JSON."""
    sidecar_dir = tmp / "staging" / "validated" / "OT"
    sidecar_dir.mkdir(parents=True, exist_ok=True)
    path = sidecar_dir / f"{book_code}_residuals.json"
    sidecar = {
        "book_code": book_code,
        "registry_version": "1.1.0",
        "ratified_by": "human",
        "ratified_date": ratified_date,
        "residuals": entries,
    }
    path.write_text(json.dumps(sidecar, indent=2), encoding="utf-8")
    return path


def _make_registry(tmp: Path, book_code: str = "TST") -> Path:
    """Create a minimal anchor registry for the test book."""
    schemas_dir = tmp / "schemas"
    schemas_dir.mkdir(parents=True, exist_ok=True)
    path = schemas_dir / "anchor_registry.json"
    registry = {
        "registry_version": "1.1.0",
        "books": [
            {"code": book_code, "name": "Test Book", "testament": "OT", "position": 1}
        ],
    }
    path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    return path


def _make_residual_classes(tmp: Path) -> Path:
    """Create residual class taxonomy with one ratified class and one ordinary class."""
    schemas_dir = tmp / "schemas"
    schemas_dir.mkdir(parents=True, exist_ok=True)
    path = schemas_dir / "residual_classes.json"
    data = {
        "version": "1.0.0",
        "classes": [
            {
                "name": "osb_source_absent",
                "requires_per_entry_ratification": True,
            },
            {
                "name": "docling_issue",
                "requires_per_entry_ratification": False,
            },
            {
                "name": "policy_exception",
                "requires_per_entry_ratification": True,
            },
        ],
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def _make_editorial_candidates(tmp: Path, total: int = 0,
                               book_code: str = "TST") -> Path:
    """Create an editorial candidates sidecar JSON."""
    sidecar_dir = tmp / "staging" / "validated" / "OT"
    sidecar_dir.mkdir(parents=True, exist_ok=True)
    path = sidecar_dir / f"{book_code}_editorial_candidates.json"
    data = {
        "book": book_code,
        "file": f"staging/validated/OT/{book_code}.md",
        "generated": "2026-03-09",
        "total_candidates": total,
        "candidates": [{"anchor": f"{book_code}.1:1"}] * total,
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def _make_dossier(tmp: Path, body_checksum: str,
                  book_code: str = "TST") -> Path:
    """Create a previous promotion dossier with a specific checksum."""
    reports_dir = tmp / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / f"{book_code}_promotion_dossier.json"
    data = {
        "book_code": book_code,
        "body_checksum": body_checksum,
        "decision": "dry-run",
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def _setup_promote(tmp_path):
    """Set up promote module with tmp_path overrides."""
    _make_registry(tmp_path)
    _make_residual_classes(tmp_path)
    promote = _load_promote()
    promote.STAGING_ROOT = tmp_path / "staging" / "validated"
    promote.CANON_ROOT = tmp_path / "canon"
    promote.REPORTS_ROOT = tmp_path / "reports"
    promote.REGISTRY = tmp_path / "schemas" / "anchor_registry.json"
    promote.RESIDUAL_CLASSES = tmp_path / "schemas" / "residual_classes.json"
    return promote


class TestPerEntryRatification:
    """Tests for the osb_* per-entry ratification gate in promote.py."""

    def test_osb_entry_ratified_passes(self, tmp_path):
        """osb_source_absent entry with ratified:true should not block."""
        _make_staged_file(tmp_path)
        _make_sidecar(tmp_path, [
            {
                "anchor": "TST.1:4",
                "classification": "osb_source_absent",
                "description": "test",
                "blocking": False,
                "ratified": True,
            }
        ])

        _make_registry(tmp_path)
        _make_residual_classes(tmp_path)
        promote = _load_promote()
        promote.STAGING_ROOT = tmp_path / "staging" / "validated"
        promote.CANON_ROOT = tmp_path / "canon"
        promote.REPORTS_ROOT = tmp_path / "reports"
        promote.REGISTRY = tmp_path / "schemas" / "anchor_registry.json"
        promote.RESIDUAL_CLASSES = tmp_path / "schemas" / "residual_classes.json"

        # promote_book should NOT exit 3 for ratified osb_ entries
        # We use --dry-run + --allow-incomplete, so the only blocker
        # would be the per-entry gate.
        try:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        except SystemExit as e:
            # exit 0 = success (dry-run), any other code is a failure
            assert e.code == 0, f"Expected exit 0 (dry-run), got exit {e.code}"

    def test_osb_entry_unratified_blocks(self, tmp_path):
        """osb_source_absent entry with ratified:false should block (exit 3)."""
        _make_staged_file(tmp_path)
        _make_sidecar(tmp_path, [
            {
                "anchor": "TST.1:4",
                "classification": "osb_source_absent",
                "description": "test",
                "blocking": False,
                "ratified": False,
            }
        ])

        _make_registry(tmp_path)
        _make_residual_classes(tmp_path)
        promote = _load_promote()
        promote.STAGING_ROOT = tmp_path / "staging" / "validated"
        promote.CANON_ROOT = tmp_path / "canon"
        promote.REPORTS_ROOT = tmp_path / "reports"
        promote.REGISTRY = tmp_path / "schemas" / "anchor_registry.json"
        promote.RESIDUAL_CLASSES = tmp_path / "schemas" / "residual_classes.json"

        with pytest.raises(SystemExit) as exc_info:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        assert exc_info.value.code == 3

    def test_docling_issue_no_per_entry_needed(self, tmp_path):
        """docling_issue entries should NOT require per-entry ratification."""
        _make_staged_file(tmp_path)
        _make_sidecar(tmp_path, [
            {
                "anchor": "TST.1:4",
                "classification": "docling_issue",
                "description": "parser failure",
                "blocking": False,
                # No 'ratified' field at all — should still pass
            }
        ])

        _make_registry(tmp_path)
        _make_residual_classes(tmp_path)
        promote = _load_promote()
        promote.STAGING_ROOT = tmp_path / "staging" / "validated"
        promote.CANON_ROOT = tmp_path / "canon"
        promote.REPORTS_ROOT = tmp_path / "reports"
        promote.REGISTRY = tmp_path / "schemas" / "anchor_registry.json"
        promote.RESIDUAL_CLASSES = tmp_path / "schemas" / "residual_classes.json"

        try:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        except SystemExit as e:
            assert e.code == 0, f"Expected exit 0 (dry-run), got exit {e.code}"

    def test_taxonomy_required_entry_ratification_blocks_non_osb_class(self, tmp_path):
        """Per-entry ratification follows residual taxonomy, not only osb_* prefix."""
        _make_staged_file(tmp_path)
        _make_sidecar(tmp_path, [
            {
                "anchor": "TST.1:4",
                "classification": "policy_exception",
                "description": "test",
                "blocking": False,
                "ratified": False,
            }
        ])

        _make_registry(tmp_path)
        _make_residual_classes(tmp_path)
        promote = _load_promote()
        promote.STAGING_ROOT = tmp_path / "staging" / "validated"
        promote.CANON_ROOT = tmp_path / "canon"
        promote.REPORTS_ROOT = tmp_path / "reports"
        promote.REGISTRY = tmp_path / "schemas" / "anchor_registry.json"
        promote.RESIDUAL_CLASSES = tmp_path / "schemas" / "residual_classes.json"

        with pytest.raises(SystemExit) as exc_info:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        assert exc_info.value.code == 3


class TestEditorialCandidatesGate:
    """D1: Editorial candidates must be resolved before promotion."""

    def test_editorial_candidates_zero_passes(self, tmp_path):
        """Book with 0 editorial candidates should pass."""
        _make_staged_file(tmp_path)
        _make_sidecar(tmp_path, [
            {"anchor": "TST.1:4", "classification": "docling_issue",
             "description": "parser failure", "blocking": False}
        ])
        _make_editorial_candidates(tmp_path, total=0)
        promote = _setup_promote(tmp_path)
        try:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        except SystemExit as e:
            assert e.code == 0, f"Expected exit 0, got {e.code}"

    def test_editorial_candidates_nonzero_blocks(self, tmp_path):
        """Book with unresolved editorial candidates should block."""
        _make_staged_file(tmp_path)
        _make_sidecar(tmp_path, [
            {"anchor": "TST.1:4", "classification": "docling_issue",
             "description": "parser failure", "blocking": False}
        ])
        _make_editorial_candidates(tmp_path, total=3)
        promote = _setup_promote(tmp_path)
        with pytest.raises(SystemExit) as exc_info:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        assert exc_info.value.code == 3


class TestDossierFreshness:
    """D2: Stale dossier checksum blocks non-dry-run promotion."""

    def test_stale_dossier_blocks_promote(self, tmp_path):
        """Promotion should block when dossier checksum doesn't match staged text."""
        _make_staged_file(tmp_path)
        _make_sidecar(tmp_path, [
            {"anchor": "TST.1:4", "classification": "docling_issue",
             "description": "parser failure", "blocking": False}
        ])
        _make_dossier(tmp_path, body_checksum="stale_checksum_that_wont_match")
        promote = _setup_promote(tmp_path)
        with pytest.raises(SystemExit) as exc_info:
            promote.promote_book("TST", dry_run=False, allow_incomplete=True)
        assert exc_info.value.code == 3

    def test_dry_run_skips_freshness_check(self, tmp_path):
        """Dry-run should not check dossier freshness."""
        _make_staged_file(tmp_path)
        _make_sidecar(tmp_path, [
            {"anchor": "TST.1:4", "classification": "docling_issue",
             "description": "parser failure", "blocking": False}
        ])
        _make_dossier(tmp_path, body_checksum="stale_checksum_that_wont_match")
        promote = _setup_promote(tmp_path)
        try:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        except SystemExit as e:
            assert e.code == 0, f"Expected exit 0, got {e.code}"


class TestSidecarFieldNormalization:
    """D3: Sidecar using 'class' instead of 'classification' should block."""

    def test_class_field_blocks(self, tmp_path):
        """Residual entry with 'class' field (not 'classification') should block."""
        _make_staged_file(tmp_path)
        sidecar_dir = tmp_path / "staging" / "validated" / "OT"
        sidecar_dir.mkdir(parents=True, exist_ok=True)
        sidecar_path = sidecar_dir / "TST_residuals.json"
        sidecar = {
            "book_code": "TST", "registry_version": "1.1.0",
            "ratified_by": "human", "ratified_date": "2026-03-09",
            "residuals": [
                {"anchor": "TST.1:4", "class": "docling_issue",
                 "description": "test", "blocking": False}
            ],
        }
        sidecar_path.write_text(json.dumps(sidecar, indent=2), encoding="utf-8")
        promote = _setup_promote(tmp_path)
        with pytest.raises(SystemExit) as exc_info:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        assert exc_info.value.code == 3


class TestAbsorbedContentGate:
    """D4: Residuals describing absorbed/fused content should block."""

    def test_absorbed_description_blocks(self, tmp_path):
        """Residual mentioning 'absorbed' in description should block."""
        _make_staged_file(tmp_path)
        _make_sidecar(tmp_path, [
            {"anchor": "TST.1:4", "classification": "docling_issue",
             "description": "Verse content absorbed parenthetically into TST.1:3",
             "blocking": False}
        ])
        promote = _setup_promote(tmp_path)
        with pytest.raises(SystemExit) as exc_info:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        assert exc_info.value.code == 3

    def test_fused_into_description_blocks(self, tmp_path):
        """Residual mentioning 'fused into' should block."""
        _make_staged_file(tmp_path)
        _make_sidecar(tmp_path, [
            {"anchor": "TST.1:4", "classification": "docling_issue",
             "description": "Text fused into preceding verse",
             "blocking": False}
        ])
        promote = _setup_promote(tmp_path)
        with pytest.raises(SystemExit) as exc_info:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        assert exc_info.value.code == 3

    def test_neutral_description_passes(self, tmp_path):
        """Residual without absorbed keywords should pass."""
        _make_staged_file(tmp_path)
        _make_sidecar(tmp_path, [
            {"anchor": "TST.1:4", "classification": "docling_issue",
             "description": "Verse missing from extraction due to parser failure",
             "blocking": False}
        ])
        promote = _setup_promote(tmp_path)
        try:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        except SystemExit as e:
            assert e.code == 0, f"Expected exit 0, got {e.code}"


class TestHumanRatificationGate:
    """D5: Non-empty residual sidecars require ratified_by: human."""

    def test_ratified_by_ark_blocks(self, tmp_path):
        """ratified_by: 'ark' should block for non-empty residuals."""
        _make_staged_file(tmp_path)
        sidecar_dir = tmp_path / "staging" / "validated" / "OT"
        sidecar_dir.mkdir(parents=True, exist_ok=True)
        sidecar_path = sidecar_dir / "TST_residuals.json"
        sidecar = {
            "book_code": "TST", "registry_version": "1.1.0",
            "ratified_by": "ark", "ratified_date": "2026-03-09",
            "residuals": [
                {"anchor": "TST.1:4", "classification": "docling_issue",
                 "description": "parser failure", "blocking": False}
            ],
        }
        sidecar_path.write_text(json.dumps(sidecar, indent=2), encoding="utf-8")
        promote = _setup_promote(tmp_path)
        with pytest.raises(SystemExit) as exc_info:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        assert exc_info.value.code == 3

    def test_ratified_by_null_blocks(self, tmp_path):
        """ratified_by: null should block for non-empty residuals."""
        _make_staged_file(tmp_path)
        sidecar_dir = tmp_path / "staging" / "validated" / "OT"
        sidecar_dir.mkdir(parents=True, exist_ok=True)
        sidecar_path = sidecar_dir / "TST_residuals.json"
        sidecar = {
            "book_code": "TST", "registry_version": "1.1.0",
            "ratified_by": None, "ratified_date": "2026-03-09",
            "residuals": [
                {"anchor": "TST.1:4", "classification": "docling_issue",
                 "description": "parser failure", "blocking": False}
            ],
        }
        sidecar_path.write_text(json.dumps(sidecar, indent=2), encoding="utf-8")
        promote = _setup_promote(tmp_path)
        with pytest.raises(SystemExit) as exc_info:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        assert exc_info.value.code == 3

    def test_ratified_by_human_passes(self, tmp_path):
        """ratified_by: 'human' should pass for non-empty residuals."""
        _make_staged_file(tmp_path)
        _make_sidecar(tmp_path, [
            {"anchor": "TST.1:4", "classification": "docling_issue",
             "description": "parser failure", "blocking": False}
        ])
        promote = _setup_promote(tmp_path)
        try:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        except SystemExit as e:
            assert e.code == 0, f"Expected exit 0, got {e.code}"

    def test_empty_residuals_no_human_needed(self, tmp_path):
        """Empty residuals array should not require ratified_by: human."""
        staged_dir = tmp_path / "staging" / "validated" / "OT"
        staged_dir.mkdir(parents=True)
        path = staged_dir / "TST.md"
        path.write_text(
            "---\n"
            "book_code: TST\n"
            "book_name: Test Book\n"
            "testament: OT\n"
            "canon_position: 1\n"
            "source: test\n"
            "parse_date: 2026-01-01\n"
            "status: staged\n"
            'promote_date: ""\n'
            'checksum: ""\n'
            "---\n"
            "## Chapter 1\n"
            "TST.1:1 verse one\n"
            "TST.1:2 verse two\n"
            "TST.1:3 verse three\n",
            encoding="utf-8",
        )
        sidecar_path = staged_dir / "TST_residuals.json"
        sidecar = {
            "book_code": "TST", "registry_version": "1.1.0",
            "ratified_by": "ark", "ratified_date": None,
            "residuals": [],
        }
        sidecar_path.write_text(json.dumps(sidecar, indent=2), encoding="utf-8")
        promote = _setup_promote(tmp_path)
        try:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        except SystemExit as e:
            assert e.code == 0, f"Expected exit 0, got {e.code}"


def _read_latest_dossier(tmp_path, book_code="TST"):
    """Read the dossier JSON written by a promote_book run."""
    path = tmp_path / "reports" / f"{book_code}_promotion_dossier.json"
    return json.loads(path.read_text(encoding="utf-8"))


class TestDossierSchema:
    """Dossier must record allow_incomplete and sidecar paths."""

    def test_dossier_records_allow_incomplete_true(self, tmp_path):
        """Dry-run with allow_incomplete=True records the field."""
        _make_staged_file(tmp_path)
        _make_sidecar(tmp_path, [
            {"anchor": "TST.1:4", "classification": "docling_issue",
             "description": "parser failure", "blocking": False}
        ])
        promote = _setup_promote(tmp_path)
        try:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        except SystemExit:
            pass
        dossier = _read_latest_dossier(tmp_path)
        assert dossier["allow_incomplete"] is True

    def test_dossier_records_allow_incomplete_false(self, tmp_path):
        """Dry-run without allow_incomplete records False."""
        _make_staged_file(tmp_path)
        _make_sidecar(tmp_path, [
            {"anchor": "TST.1:4", "classification": "docling_issue",
             "description": "parser failure", "blocking": False}
        ])
        promote = _setup_promote(tmp_path)
        try:
            promote.promote_book("TST", dry_run=True, allow_incomplete=False)
        except SystemExit:
            pass
        dossier = _read_latest_dossier(tmp_path)
        assert dossier["allow_incomplete"] is False

    def test_dossier_preserves_warn_and_skip_statuses(self, tmp_path):
        """Structured validation statuses should survive into the dossier."""
        _make_staged_file(tmp_path)
        _make_sidecar(tmp_path, [
            {"anchor": "TST.1:4", "classification": "docling_issue",
             "description": "parser failure", "blocking": False}
        ])
        promote = _setup_promote(tmp_path)
        try:
            promote.promote_book("TST", dry_run=True, allow_incomplete=False)
        except SystemExit:
            pass

        dossier = _read_latest_dossier(tmp_path)
        assert dossier["validation"]["V4"]["status"] == "WARN"
        assert dossier["validation"]["V7"]["status"] == "INFO"
        assert dossier["validation"]["V10"]["status"] == "SKIP"

    def test_dossier_records_staged_path(self, tmp_path):
        """Dossier should contain the staged file path."""
        _make_staged_file(tmp_path)
        _make_sidecar(tmp_path, [
            {"anchor": "TST.1:4", "classification": "docling_issue",
             "description": "parser failure", "blocking": False}
        ])
        promote = _setup_promote(tmp_path)
        try:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        except SystemExit:
            pass
        dossier = _read_latest_dossier(tmp_path)
        assert dossier["staged_path"] is not None
        assert "TST.md" in dossier["staged_path"]

    def test_dossier_records_sidecar_paths(self, tmp_path):
        """Dossier should record editorial and residuals paths."""
        _make_staged_file(tmp_path)
        _make_sidecar(tmp_path, [
            {"anchor": "TST.1:4", "classification": "docling_issue",
             "description": "parser failure", "blocking": False}
        ])
        _make_editorial_candidates(tmp_path, total=0)
        promote = _setup_promote(tmp_path)
        try:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        except SystemExit:
            pass
        dossier = _read_latest_dossier(tmp_path)
        assert dossier["residuals_path"] is not None
        assert "TST_residuals.json" in dossier["residuals_path"]
        assert dossier["editorial_candidates_path"] is not None
        assert "TST_editorial_candidates.json" in dossier["editorial_candidates_path"]
