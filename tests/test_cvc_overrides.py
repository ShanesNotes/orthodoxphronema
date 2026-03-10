"""
test_cvc_overrides.py — Tests for CVC override loading and skip logic.
"""
from __future__ import annotations

import pytest

from pipeline.tools import verify_all_cvc as _verify_mod


@pytest.fixture(scope="module")
def verify_mod():
    return _verify_mod


def test_load_overrides_empty(verify_mod):
    """Registry with no cvc_overrides returns empty dict."""
    result = verify_mod.load_overrides({"books": []})
    assert result == {}


def test_load_overrides_with_entries(verify_mod):
    """Registry with cvc_overrides returns the entries dict."""
    reg_data = {
        "cvc_overrides": {
            "entries": {
                "1SA": {
                    "17": {"registry": 33, "brenton": 52, "reason": "LXX shorter text"}
                }
            }
        }
    }
    result = verify_mod.load_overrides(reg_data)
    assert "1SA" in result
    assert "17" in result["1SA"]


def test_is_chapter_overridden(verify_mod):
    """Chapter override lookup works for present and absent entries."""
    overrides = {
        "1SA": {
            "1": {"registry": 29, "brenton": 28, "reason": "test"},
            "17": {"registry": 33, "brenton": 52, "reason": "test"},
        }
    }
    assert verify_mod.is_chapter_overridden(overrides, "1SA", 1) is True
    assert verify_mod.is_chapter_overridden(overrides, "1SA", 17) is True
    assert verify_mod.is_chapter_overridden(overrides, "1SA", 5) is False
    assert verify_mod.is_chapter_overridden(overrides, "GEN", 1) is False


def test_is_chapter_count_overridden(verify_mod):
    """Chapter-count override lookup works for present and absent entries."""
    overrides = {
        "EZR": {
            "_chapter_count": {"registry_chapters": 10, "brenton_chapters": 23, "reason": "test"}
        },
        "1SA": {
            "17": {"registry": 33, "brenton": 52, "reason": "test"}
        },
    }
    assert verify_mod.is_chapter_count_overridden(overrides, "EZR") is True
    assert verify_mod.is_chapter_count_overridden(overrides, "1SA") is False
    assert verify_mod.is_chapter_count_overridden(overrides, "GEN") is False
