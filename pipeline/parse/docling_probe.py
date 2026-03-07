"""
Docling probe — extract a page range from the OSB PDF and write
structured output to staging/raw/probe/ for inspection.

Usage:
    python3 pipeline/parse/docling_probe.py --pages 1-10
    python3 pipeline/parse/docling_probe.py --pages 45-70

Output files in staging/raw/probe/ (named by page range):
    probe_markdown_pN-M.md    — Markdown export
    probe_structure_pN-M.json — element type/label summary
    probe_text_pN-M.txt       — plain text export
"""

import argparse
import json
from pathlib import Path

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

REPO_ROOT = Path(__file__).parent.parent.parent
PDF_PATH  = REPO_ROOT / "src.texts" / "the_orthodox_study_bible.pdf"
PROBE_OUT = REPO_ROOT / "staging" / "raw" / "probe"


def run_probe(pdf_path: Path, start_page: int, end_page: int, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = f"p{start_page}-{end_page}"

    print(f"[probe] Source : {pdf_path}")
    print(f"[probe] Pages  : {start_page}-{end_page}")
    print(f"[probe] Output : {out_dir}")
    print("[probe] Initialising Docling converter ...")

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    pipeline_options.do_table_structure = True

    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )

    print(f"[probe] Converting ...")
    result = converter.convert(str(pdf_path), page_range=(start_page, end_page))
    doc = result.document

    # Markdown
    md_path = out_dir / f"probe_markdown_{tag}.md"
    md_text = doc.export_to_markdown()
    md_path.write_text(md_text, encoding="utf-8")
    print(f"[probe] Markdown  : {md_path}  ({len(md_text):,} chars)")

    # Structure summary
    summary = []
    for i, item in enumerate(doc.iterate_items()):
        elem = item[0] if isinstance(item, tuple) else item
        entry = {"i": i, "type": type(elem).__name__}
        text = getattr(elem, "text", None)
        if callable(text):
            text = None
        if text:
            entry["text"] = str(text)[:160].replace("\n", " ")
        lbl = getattr(elem, "label", None)
        if lbl is not None and not callable(lbl):
            entry["label"] = str(lbl)
        summary.append(entry)
        if i >= 3000:
            summary.append({"note": "truncated"})
            break

    json_path = out_dir / f"probe_structure_{tag}.json"
    json_path.write_text(
        json.dumps({"page_range": f"{start_page}-{end_page}", "elements": summary},
                   indent=2, ensure_ascii=False, default=str),
        encoding="utf-8"
    )
    print(f"[probe] Structure : {json_path}  ({len(summary)} elements)")

    # Plain text
    txt_path = out_dir / f"probe_text_{tag}.txt"
    txt_path.write_text(doc.export_to_text(), encoding="utf-8")
    print(f"[probe] Text      : {txt_path}")

    print("[probe] Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Docling probe on OSB PDF")
    parser.add_argument("--pages", type=str, default="1-10",
                        help="Page range, e.g. '1-10' or '45-70'")
    parser.add_argument("--pdf", type=str, default=str(PDF_PATH))
    args = parser.parse_args()

    if "-" in args.pages:
        start, end = [int(x) for x in args.pages.split("-", 1)]
    else:
        start, end = 1, int(args.pages)

    run_probe(Path(args.pdf), start, end, PROBE_OUT)
