"""
conftest.py — Import helpers for osb_extract and validate_canon without package setup.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
EXTRACT_PATH  = REPO_ROOT / "pipeline" / "parse" / "osb_extract.py"
VALIDATE_PATH = REPO_ROOT / "pipeline" / "validate" / "validate_canon.py"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def osb_extract():
    return _load_module("osb_extract", EXTRACT_PATH)


@pytest.fixture(scope="session")
def validate_canon():
    return _load_module("validate_canon", VALIDATE_PATH)
