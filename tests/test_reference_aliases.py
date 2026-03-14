from __future__ import annotations

from pipeline.reference.reference_aliases import (
    canonical_source_entity,
    build_biblical_alias_map,
    canonical_biblical_code,
    canonical_patristic_entity,
    load_reference_aliases,
)


def test_reference_aliases_schema_loads():
    data = load_reference_aliases()
    assert data["version"] == 2
    assert data["biblical"]
    assert data["patristic_future"]
    assert data["apostolic_future"]
    assert data["liturgical_creedal_future"]


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
    assert canonical_patristic_entity("St. John")["canonical"] == "JOHN_THEOLOGIAN"
    assert canonical_patristic_entity("JohnDm")["canonical"] == "JOHN_DAMASCENE"
    assert canonical_patristic_entity("St. Clement")["canonical"] == "CLEMENT_ROME"
    assert canonical_patristic_entity("ClemA")["canonical"] == "CLEMENT_ALEXANDRIA"
    assert canonical_patristic_entity("St. Hippolytus")["canonical"] == "HIPPOLYTUS_ROME"
    assert canonical_patristic_entity("Iren")["canonical"] == "IRENAEUS"
    assert canonical_patristic_entity("GrgTheo")["canonical"] == "GREGORY_THEOLOGIAN"
    assert canonical_patristic_entity("GrgNa")["canonical"] == "GREGORY_THEOLOGIAN"
    assert canonical_patristic_entity("St. Augustine")["canonical"] == "AUGUSTINE_HIPPO"
    assert canonical_patristic_entity("St. Jerome")["canonical"] == "JEROME"
    assert canonical_patristic_entity("AmbM")["canonical"] == "AMBROSE_MILAN"
    assert canonical_patristic_entity("HilryP")["canonical"] == "HILARY_POITIERS"
    assert canonical_patristic_entity("AphP")["canonical"] == "APHRAHAT"
    assert canonical_patristic_entity("St. Cyril")["canonical"] == "CYRIL_JERUSALEM"
    assert canonical_patristic_entity("GrgGt")["canonical"] == "GREGORY_GREAT"
    assert canonical_patristic_entity("St. Gregory the Dialogist")["canonical"] == "GREGORY_GREAT"
    assert canonical_patristic_entity("GrgPal")["canonical"] == "GREGORY_PALAMAS"
    assert canonical_patristic_entity("St. Stephen")["canonical"] == "STEPHEN_PROTOMARTYR"
    assert canonical_patristic_entity("St. Joseph")["canonical"] == "JOSEPH_BETROTHED"
    assert canonical_patristic_entity("VincLer")["canonical"] == "VINCENT_LERINS"
    assert canonical_patristic_entity("St. Photini")["canonical"] == "PHOTINI_SAMARITAN"
    assert canonical_patristic_entity("IsaacS")["canonical"] == "ISAAC_SYRIAN"
    assert canonical_patristic_entity("MaxCon")["canonical"] == "MAXIMUS_CONFESSOR"
    assert canonical_patristic_entity("AntEg")["canonical"] == "ANTONY_GREAT"
    assert canonical_patristic_entity("St. Elijah")["canonical"] == "ELIJAH_PROPHET"
    assert canonical_patristic_entity("GrgSinai")["canonical"] == "GREGORY_SINAI"
    assert canonical_patristic_entity("St. John the Forerunner")["canonical"] == "JOHN_FORERUNNER"


def test_non_patristic_source_aliases_resolve_by_section():
    assert canonical_source_entity("apostolic_future", "St. Paul")["canonical"] == "PAUL_APOSTLE"
    assert canonical_source_entity("apostolic_future", "St. Peter")["canonical"] == "PETER_APOSTLE"
    assert canonical_source_entity("apostolic_future", "St. James")["canonical"] == "JAMES_APOSTLE"
    assert canonical_source_entity("apostolic_future", "St. Jude")["canonical"] == "JUDE_APOSTLE"
    assert (
        canonical_source_entity("liturgical_creedal_future", "Creed")["canonical"]
        == "NICENE_CREED"
    )
    assert (
        canonical_source_entity("liturgical_creedal_future", "CanonAnd")["canonical"]
        == "CANON_OF_ANDREW"
    )
