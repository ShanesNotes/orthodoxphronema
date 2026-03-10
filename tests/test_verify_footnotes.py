from __future__ import annotations

from pipeline.cleanup import verify_footnotes as vf


def test_anchor_registry_error_valid_and_invalid_ranges():
    cvc = {1: 3, 2: 5}
    assert vf.anchor_registry_error("TST.1:1", "TST", cvc) is None
    assert vf.anchor_registry_error("TST.2:5", "TST", cvc) is None
    assert vf.anchor_registry_error("TST.3:1", "TST", cvc) == "invalid_chapter"
    assert vf.anchor_registry_error("TST.2:6", "TST", cvc) == "invalid_verse"


def test_anchor_registry_error_detects_wrong_book_and_malformed():
    cvc = {1: 10}
    assert vf.anchor_registry_error("GEN.1:1", "EXO", cvc) == "wrong_book_code"
    assert vf.anchor_registry_error("not-an-anchor", "EXO", cvc) == "malformed_anchor"


def test_partition_anchors_splits_valid_from_invalid():
    cvc = {1: 2}
    valid, invalid = vf.partition_anchors(
        {"TST.1:1", "TST.1:3", "BAD", "EXO.1:1"},
        "TST",
        cvc,
    )
    assert valid == {"TST.1:1"}
    assert invalid == {
        "TST.1:3": "invalid_verse",
        "BAD": "malformed_anchor",
        "EXO.1:1": "wrong_book_code",
    }
