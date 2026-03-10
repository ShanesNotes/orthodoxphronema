"""Article mode tracking — encapsulates the 4-rule article exit logic."""

from __future__ import annotations

from pipeline.common.types import ArticleRecord


class ArticleTracker:
    """Tracks study article accumulation and exit logic.

    OSB study articles contain numbered paragraphs (sub-points) that begin
    with a digit + uppercase letter — the same pattern as verse/chapter leads.
    This class implements the 4-rule sequential sub-point tracking that
    distinguishes article content from verse resumption.
    """

    def __init__(self):
        self._title: str = ""
        self._after_anchor: str = ""
        self._body: list[str] = []
        self._subpoint_seq: int = 0

    @property
    def active(self) -> bool:
        """True if currently accumulating an article."""
        return bool(self._title)

    def start(self, title: str, after_anchor: str) -> None:
        """Begin a new article (flushes any current one first)."""
        self._title = title
        self._after_anchor = after_anchor
        self._body = []
        self._subpoint_seq = 0

    def flush(self) -> ArticleRecord | None:
        """Flush the current article and return it, or None if empty."""
        if not self._title:
            return None
        record = ArticleRecord(
            title=self._title,
            after_anchor=self._after_anchor,
            body=list(self._body),
        )
        self._title = ""
        self._after_anchor = ""
        self._body = []
        self._subpoint_seq = 0
        return record

    def is_subpoint(self, num: int, current_verse: int) -> bool:
        """Return True if num is a sequential sub-point (article content).

        Rule 1: seq >= 1 AND num == seq + 1 AND num <= current_verse → stay
        Rule 3: seq == 0 AND num == 1 AND current_verse >= 1 → first sub-point
        """
        # Rule 1 — Sequential continuation
        if (self._subpoint_seq >= 1
                and num == self._subpoint_seq + 1
                and num <= current_verse):
            self._subpoint_seq = num
            return True

        # Rule 3 — First sub-point
        if self._subpoint_seq == 0 and num == 1 and current_verse >= 1:
            self._subpoint_seq = 1
            return True

        return False

    def is_exit_signal(self, num: int, current_verse: int, current_chapter: int) -> bool:
        """Return True if num signals article exit (verse or chapter resumption).

        Rule 2: num > current_verse OR num == current_chapter + 1
        """
        return num > current_verse or num == current_chapter + 1

    def add_body(self, text: str) -> None:
        """Add a paragraph to the article body."""
        self._body.append(text)

    def add_subheading(self, text: str) -> None:
        """Add a sub-heading to the article body."""
        self._body.append(f"\n#### {text}\n")

    def reset_subpoint_seq(self) -> None:
        """Reset sub-point counter (non-sequential number encountered)."""
        self._subpoint_seq = 0
