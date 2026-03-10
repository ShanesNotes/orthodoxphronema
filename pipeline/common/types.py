"""Structured data types for the Orthodox Phronema pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict


@dataclass
class VerseRecord:
    """A single extracted verse."""
    anchor: str
    chapter: int
    verse: int
    text: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class HeadingRecord:
    """A narrative heading (e.g. 'The Creation')."""
    after_anchor: str
    heading: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ArticleRecord:
    """A study article extracted from the OSB."""
    title: str
    after_anchor: str
    body: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class FootnoteMarker:
    """A footnote marker occurrence."""
    marker: str
    ownership: str       # "inline_body" | "boundary_trailing" | "lc_split_first_segment"
    anchor: str = ""
    page: int | None = None
    raw_excerpt: str = ""
    element_index: int | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ResidualEntry:
    """A residual (missing/problematic verse) in a sidecar file."""
    anchor: str
    classification: str
    description: str
    blocking: bool = False
    ratified: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CheckResult:
    """Result of a single validation check (V1, V2, etc.)."""
    name: str          # "V1", "V2", etc.
    status: str        # "PASS", "WARN", "FAIL"
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    data: dict = field(default_factory=dict)

    @property
    def messages(self) -> list[str]:
        return [*self.errors, *self.warnings]


@dataclass
class ValidationResult:
    """Aggregate validation result for a book."""
    book_code: str
    checks: list[CheckResult] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def check(self, name: str) -> CheckResult | None:
        for check in self.checks:
            if check.name == name:
                return check
        return None

    @property
    def status_map(self) -> dict[str, str]:
        return {check.name: check.status for check in self.checks}

    @property
    def errors(self) -> list[str]:
        result = []
        for c in self.checks:
            result.extend(c.errors)
        return result

    @property
    def warnings(self) -> list[str]:
        result = []
        for c in self.checks:
            result.extend(c.warnings)
        return result

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0
