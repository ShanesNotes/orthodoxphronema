"""Chapter advance logic — encapsulates the 80%/60% threshold guards."""

from __future__ import annotations

from pipeline.common.config import CHAPTER_ADVANCE_THRESHOLD, CHAPTER_ADVANCE_FALLBACK


class ChapterTracker:
    """Tracks current chapter and decides when to advance to the next one.

    The 80% primary threshold prevents false chapter advances from inline verse
    numbers that happen to equal current_chapter + 1. The 60% backward-signal
    fallback catches missed advances when Docling drops >20% of verses.
    """

    def __init__(self, chapter_verse_counts: dict[int, int] | None = None,
                 max_chapters: int | None = None):
        self.current_chapter = 0
        self.current_verse = 0
        self._cvc: dict[int, int] = chapter_verse_counts or {}
        self._max_chapters: int | None = max_chapters

    def max_verse(self, ch: int) -> int:
        """Return expected verse count for chapter ch (0 if unknown)."""
        return self._cvc.get(ch, 0)

    def should_advance(self, candidate_chapter: int) -> bool:
        """Return True if candidate_chapter is a real chapter advance.

        Requires candidate_chapter == current_chapter + 1 AND one of:
          - No CVC data (max_v == 0) → allow unconditionally
          - current_verse >= 80% of max_v (primary threshold)
          - Backward signal: candidate < current_verse AND current_verse >= 60% of max_v
        """
        if candidate_chapter != self.current_chapter + 1:
            return False

        if self._max_chapters and candidate_chapter > self._max_chapters:
            return False

        max_v = self.max_verse(self.current_chapter)
        if max_v == 0:
            return True

        if self.current_verse >= int(max_v * CHAPTER_ADVANCE_THRESHOLD):
            return True

        backward_signal = (candidate_chapter < self.current_verse
                          and self.current_verse >= int(max_v * CHAPTER_ADVANCE_FALLBACK))
        if backward_signal:
            import sys
            print(f"[DEBUG] backward-signal advance: ch{self.current_chapter}→{candidate_chapter}, "
                  f"current_verse={self.current_verse}, max_v={max_v}, "
                  f"60%={int(max_v * CHAPTER_ADVANCE_FALLBACK)}", file=sys.stderr)
        return backward_signal

    def advance(self, chapter: int) -> None:
        """Advance to a new chapter, resetting the verse counter."""
        self.current_chapter = chapter
        self.current_verse = 0

    def update_verse(self, verse: int) -> None:
        """Update the current verse tracker."""
        self.current_verse = verse
