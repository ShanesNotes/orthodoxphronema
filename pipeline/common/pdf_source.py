"""Shared OSB PDF extraction and search helpers."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from pipeline.common.paths import PDF_PATH, REGISTRY_PATH
from pipeline.common.patterns import RE_FOOTNOTE_MARKERS
from pipeline.common.registry import load_registry

CACHE_DIR = Path("/tmp/orthodoxphronema_pdf_cache")


def load_page_ranges(registry_path: Path | None = None) -> dict:
    """Load page_ranges from anchor_registry.json."""
    reg = load_registry(registry_path or REGISTRY_PATH)
    return reg.get("page_ranges", {})


def load_chapter_verse_counts(
    book_code: str,
    registry_path: Path | None = None,
) -> dict[int, int]:
    """Load chapter_verse_counts for a book."""
    reg = load_registry(registry_path or REGISTRY_PATH)
    for book in reg.get("books", []):
        if book["code"] == book_code:
            cvc_list = book.get("chapter_verse_counts", [])
            return {i + 1: v for i, v in enumerate(cvc_list)} if cvc_list else {}
    return {}


def ensure_pdftotext() -> str:
    exe = shutil.which("pdftotext")
    if not exe:
        raise RuntimeError("pdftotext is required for PDF source verification")
    return exe


def ensure_pdftoppm() -> str:
    exe = shutil.which("pdftoppm")
    if not exe:
        raise RuntimeError("pdftoppm is required for PDF page rendering")
    return exe


def extract_pdf_text(
    page_start: int,
    page_end: int | None = None,
    pdf_path: Path | None = None,
    *,
    layout: bool = True,
    cache_key: str | None = None,
    cache_dir: Path = CACHE_DIR,
) -> str:
    """Extract raw text from PDF page(s), optionally using a text cache."""
    pdf = pdf_path or PDF_PATH
    if not pdf.exists():
        raise FileNotFoundError(f"PDF not found: {pdf}")

    end = page_end or page_start
    cache_path: Path | None = None
    if cache_key:
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path = cache_dir / f"{cache_key}_{page_start}_{end}_{'layout' if layout else 'plain'}.txt"
        if cache_path.exists():
            return cache_path.read_text(encoding="utf-8", errors="ignore")

    cmd = [ensure_pdftotext()]
    if layout:
        cmd.append("-layout")
    cmd.extend(["-f", str(page_start), "-l", str(end), str(pdf)])

    if cache_path is not None:
        cmd.append(str(cache_path))
        subprocess.run(cmd, check=True, timeout=30)
        return cache_path.read_text(encoding="utf-8", errors="ignore")

    cmd.append("-")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(f"pdftotext failed: {result.stderr}")
    return result.stdout


def is_navigation_page(text: str) -> bool:
    lower = text.lower()
    return (
        "back to table of contents" in lower
        or "chapters in " in lower
        or "verses in " in lower
    )


def normalize_pdf_search_text(text: str) -> str:
    text = RE_FOOTNOTE_MARKERS.sub("", text)
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)
    text = re.sub(r"[^A-Za-z0-9]+", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def estimate_chapter_page_range(
    book_code: str,
    chapter: int,
    page_ranges: dict | None = None,
    cvc: dict[int, int] | None = None,
    *,
    nav_fraction: float = 0.38,
    margin: int = 3,
) -> tuple[int, int]:
    """Estimate the page range for a chapter inside a book-level text span."""
    ranges = page_ranges or load_page_ranges()
    book_range = ranges.get(book_code, {}).get("text", [])
    if not book_range or len(book_range) < 2:
        raise ValueError(f"No page range for {book_code} in registry")

    book_start, book_end = book_range
    total_pages = book_end - book_start + 1
    text_start = book_start + int(total_pages * nav_fraction)
    text_pages = book_end - text_start + 1

    cvc = cvc or load_chapter_verse_counts(book_code)
    if not cvc or text_pages <= 0:
        return book_start, book_end

    total_verses = sum(cvc.values())
    if total_verses == 0:
        return text_start, book_end

    verses_before = sum(cvc.get(c, 0) for c in range(1, chapter))
    verses_in_ch = cvc.get(chapter, 0)
    frac_start = verses_before / total_verses
    frac_end = (verses_before + verses_in_ch) / total_verses

    est_start = max(text_start, text_start + int(frac_start * text_pages) - margin)
    est_end = min(book_end, text_start + int(frac_end * text_pages) + margin)
    return est_start, est_end
