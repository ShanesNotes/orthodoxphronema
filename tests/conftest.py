"""
conftest.py — Fixtures for osb_extract and validate_canon.
"""
from __future__ import annotations

import pytest

from pipeline.parse import osb_extract as _osb_extract
from pipeline.validate import validate_canon as _validate_canon


@pytest.fixture(scope="session")
def osb_extract():
    return _osb_extract


@pytest.fixture(scope="session")
def validate_canon():
    return _validate_canon
