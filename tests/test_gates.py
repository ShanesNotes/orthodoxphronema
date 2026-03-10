"""Tests for pipeline/promote/gates.py — individual promotion gate functions."""

from __future__ import annotations

import json
from pathlib import Path

from pipeline.promote.gates import (
    gate_absorbed_content,
    gate_completeness,
    gate_editorial,
    gate_errors,
    gate_freshness,
    gate_ratification,
    gate_sidecar_fields,
    gate_v4_coverage,
)


# ── D1: Editorial gate ──────────────────────────────────────────────────────

def test_editorial_no_file():
    r = gate_editorial(Path("/nonexistent"))
    assert r.passed


def test_editorial_zero_candidates(tmp_path):
    p = tmp_path / "editorial.json"
    p.write_text(json.dumps({"total_candidates": 0}))
    r = gate_editorial(p)
    assert r.passed


def test_editorial_blocks(tmp_path):
    p = tmp_path / "editorial.json"
    p.write_text(json.dumps({"total_candidates": 3}))
    r = gate_editorial(p)
    assert not r.passed
    assert r.exit_code == 3


# ── D2: Freshness gate ──────────────────────────────────────────────────────

def test_freshness_no_dossier():
    r = gate_freshness(Path("/nonexistent"), "abc123", dry_run=False)
    assert r.passed


def test_freshness_dry_run_skips(tmp_path):
    p = tmp_path / "dossier.json"
    p.write_text(json.dumps({"body_checksum": "old"}))
    r = gate_freshness(p, "new", dry_run=True)
    assert r.passed


def test_freshness_stale_blocks(tmp_path):
    p = tmp_path / "dossier.json"
    p.write_text(json.dumps({"body_checksum": "old"}))
    r = gate_freshness(p, "new", dry_run=False)
    assert not r.passed
    assert r.exit_code == 3


def test_freshness_matching_passes(tmp_path):
    p = tmp_path / "dossier.json"
    p.write_text(json.dumps({"body_checksum": "same"}))
    r = gate_freshness(p, "same", dry_run=False)
    assert r.passed


# ── Error gate ───────────────────────────────────────────────────────────────

def test_errors_empty_passes():
    r = gate_errors([])
    assert r.passed


def test_errors_blocks():
    r = gate_errors(["V1 duplicate anchor"])
    assert not r.passed
    assert r.exit_code == 1


# ── D3: Sidecar fields ──────────────────────────────────────────────────────

def test_sidecar_fields_none():
    r = gate_sidecar_fields(None)
    assert r.passed


def test_sidecar_fields_correct():
    sidecar = {"residuals": [{"anchor": "TST.1:1", "classification": "docling_issue"}]}
    r = gate_sidecar_fields(sidecar)
    assert r.passed


def test_sidecar_fields_class_blocks():
    sidecar = {"residuals": [{"anchor": "TST.1:1", "class": "docling_issue"}]}
    r = gate_sidecar_fields(sidecar)
    assert not r.passed
    assert r.exit_code == 3


# ── V4 coverage ──────────────────────────────────────────────────────────────

def test_v4_no_gaps():
    r = gate_v4_coverage([], None, "TST")
    assert r.passed


def test_v4_gaps_no_sidecar():
    r = gate_v4_coverage(
        ["V4   Missing verses in ch.1: jumps from 2 to 4"],
        None, "TST",
    )
    assert not r.passed


def test_v4_gaps_covered():
    sidecar = {"residuals": [
        {"anchor": "TST.1:3", "classification": "docling_issue", "blocking": False},
    ]}
    r = gate_v4_coverage(
        ["V4   Missing verses in ch.1: jumps from 2 to 4"],
        sidecar, "TST",
    )
    assert r.passed


# ── D4: Absorbed content ────────────────────────────────────────────────────

def test_absorbed_none():
    r = gate_absorbed_content(None)
    assert r.passed


def test_absorbed_neutral():
    sidecar = {"residuals": [
        {"anchor": "TST.1:1", "description": "parser failure"},
    ]}
    r = gate_absorbed_content(sidecar)
    assert r.passed


def test_absorbed_blocks():
    sidecar = {"residuals": [
        {"anchor": "TST.1:1", "description": "content absorbed into TST.1:2"},
    ]}
    r = gate_absorbed_content(sidecar)
    assert not r.passed
    assert r.exit_code == 3


# ── D5: Ratification ────────────────────────────────────────────────────────

def test_ratification_no_sidecar():
    r = gate_ratification(None, set())
    assert r.passed


def test_ratification_human_passes():
    sidecar = {
        "ratified_by": "human", "ratified_date": "2026-01-01",
        "residuals": [{"anchor": "TST.1:1", "classification": "docling_issue"}],
    }
    r = gate_ratification(sidecar, set())
    assert r.passed


def test_ratification_ark_blocks():
    sidecar = {
        "ratified_by": "ark", "ratified_date": "2026-01-01",
        "residuals": [{"anchor": "TST.1:1", "classification": "docling_issue"}],
    }
    r = gate_ratification(sidecar, set())
    assert not r.passed


def test_ratification_per_entry_blocks():
    sidecar = {
        "ratified_by": "human", "ratified_date": "2026-01-01",
        "residuals": [
            {"anchor": "TST.1:1", "classification": "osb_source_absent", "ratified": False},
        ],
    }
    r = gate_ratification(sidecar, {"osb_source_absent"})
    assert not r.passed


# ── V7: Completeness ────────────────────────────────────────────────────────

def test_completeness_no_warnings():
    r = gate_completeness([], allow_incomplete=False)
    assert r.passed


def test_completeness_warns_blocks():
    r = gate_completeness(["V7 gap of 5"], allow_incomplete=False)
    assert not r.passed
    assert r.exit_code == 2


def test_completeness_allows_incomplete():
    r = gate_completeness(["V7 gap of 5"], allow_incomplete=True)
    assert r.passed
