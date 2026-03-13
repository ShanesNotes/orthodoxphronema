from __future__ import annotations

from pipeline.reference.reference_aliases import (
    build_biblical_alias_map,
    canonical_biblical_code,
    canonical_patristic_entity,
    load_reference_aliases,
)


def test_reference_aliases_schema_loads():
    data = load_reference_aliases()
    assert data["version"] == 1
    assert data["biblical"]
    assert data["patristic_future"]


def test_biblical_alias_resolution_handles_osb_abbreviations_and_greek():
    assert canonical_biblical_code("Mt") == "MAT"
    assert canonical_biblical_code("Matt") == "MAT"
    assert canonical_biblical_code("Μτ") == "MAT"
    assert canonical_biblical_code("Jn") == "JOH"
    assert canonical_biblical_code("1Co") == "1CO"
    assert canonical_biblical_code("2Pt") == "2PE"
    assert canonical_biblical_code("4Kg") == "2KI"


def test_biblical_alias_map_contains_canonical_entries():
    alias_map = build_biblical_alias_map()
    assert alias_map["mat"] == "MAT"
    assert alias_map["matt"] == "MAT"
    assert alias_map["john"] == "JOH"
    assert alias_map["1 corinthians"] == "1CO"


def test_patristic_aliases_resolve_to_entity_not_anchor():
    entity = canonical_patristic_entity("Athan")
    assert entity is not None
    assert entity["canonical"] == "ATHANASIUS"
    assert "context_hint" in entity
    assert canonical_patristic_entity("St. John Chrysostom")["canonical"] == "JOHN_CHRYSOSTOM"
