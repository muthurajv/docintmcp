import io
from dataclasses import dataclass

from pypdf import PdfReader, PdfWriter

from shared.exceptions import PDFChunkError


@dataclass
class PDFChunk:
    index: int
    total: int
    start_page: int  # 0-based, inclusive
    end_page: int    # 0-based, inclusive
    pdf_bytes: bytes


def chunk_pdf(
    pdf_bytes: bytes,
    chunk_size: int = 5,
    overlap: int = 1,
) -> list[PDFChunk]:
    """Split a PDF into overlapping page-range chunks.

    For a 15-page PDF with chunk_size=5, overlap=1:
      chunk 0: pages 0-4
      chunk 1: pages 4-8
      chunk 2: pages 8-12
      chunk 3: pages 12-14
    """
    if chunk_size < 1:
        raise PDFChunkError("chunk_size must be >= 1")
    if overlap < 0 or overlap >= chunk_size:
        raise PDFChunkError("overlap must be >= 0 and < chunk_size")

    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
    except Exception as exc:
        raise PDFChunkError(f"Failed to parse PDF: {exc}") from exc

    total_pages = len(reader.pages)
    if total_pages == 0:
        raise PDFChunkError("PDF has no pages.")

    step = chunk_size - overlap
    starts = list(range(0, total_pages, step))

    # Compute chunk boundaries
    boundaries: list[tuple[int, int]] = []
    for start in starts:
        end = min(start + chunk_size - 1, total_pages - 1)
        boundaries.append((start, end))
        if end == total_pages - 1:
            break

    chunks: list[PDFChunk] = []
    for idx, (start, end) in enumerate(boundaries):
        writer = PdfWriter()
        for page_num in range(start, end + 1):
            writer.add_page(reader.pages[page_num])

        buf = io.BytesIO()
        writer.write(buf)

        chunks.append(PDFChunk(
            index=idx,
            total=len(boundaries),
            start_page=start,
            end_page=end,
            pdf_bytes=buf.getvalue(),
        ))

    return chunks
