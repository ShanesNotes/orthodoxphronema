"""
test_promote_gate.py — Per-entry ratification gate for source-absence residuals.
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent


def _load_promote():
    spec = importlib.util.spec_from_file_location(
        "promote", REPO_ROOT / "pipeline" / "promote" / "promote.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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
        promote = _load_promote()
        promote.STAGING_ROOT = tmp_path / "staging" / "validated"
        promote.CANON_ROOT = tmp_path / "canon"
        promote.REPORTS_ROOT = tmp_path / "reports"
        promote.REGISTRY = tmp_path / "schemas" / "anchor_registry.json"

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
        promote = _load_promote()
        promote.STAGING_ROOT = tmp_path / "staging" / "validated"
        promote.CANON_ROOT = tmp_path / "canon"
        promote.REPORTS_ROOT = tmp_path / "reports"
        promote.REGISTRY = tmp_path / "schemas" / "anchor_registry.json"

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
        promote = _load_promote()
        promote.STAGING_ROOT = tmp_path / "staging" / "validated"
        promote.CANON_ROOT = tmp_path / "canon"
        promote.REPORTS_ROOT = tmp_path / "reports"
        promote.REGISTRY = tmp_path / "schemas" / "anchor_registry.json"

        try:
            promote.promote_book("TST", dry_run=True, allow_incomplete=True)
        except SystemExit as e:
            assert e.code == 0, f"Expected exit 0 (dry-run), got exit {e.code}"
