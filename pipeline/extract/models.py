"""
models.py — Typed records for narrow R1 extraction.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import re

RE_ANCHOR_ID = re.compile(r"^[A-Z0-9]{2,4}\.\d+:\d+$")
REFERENCE_TYPES = {"frozen", "bare", "wikilink", "wikilink_range"}


@dataclass(frozen=True)
class ReferenceRecord:
    source_file: str
    line_number: int
    raw_match: str
    anchor_id: str
    reference_type: str
    context: str

    def validate(self) -> None:
        if self.reference_type == "frozen":
            object.__setattr__(self, "reference_type", "wikilink")
        if self.reference_type not in REFERENCE_TYPES:
            raise ValueError(f"invalid reference_type: {self.reference_type!r}")
        if self.line_number < 1:
            raise ValueError(f"invalid line_number: {self.line_number!r}")
        if not RE_ANCHOR_ID.fullmatch(self.anchor_id):
            raise ValueError(f"invalid anchor_id: {self.anchor_id!r}")
        if not self.source_file:
            raise ValueError("source_file must be non-empty")
        if not self.raw_match:
            raise ValueError("raw_match must be non-empty")
        if not self.context:
            raise ValueError("context must be non-empty")

    def to_dict(self) -> dict:
        self.validate()
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=True, sort_keys=True)
