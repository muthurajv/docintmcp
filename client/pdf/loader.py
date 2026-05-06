import io
from pypdf import PdfReader
from shared.exceptions import PDFChunkError


def load_pdf_bytes(file_bytes: bytes) -> tuple[bytes, int]:
    """Validate PDF bytes and return (bytes, page_count)."""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        page_count = len(reader.pages)
    except Exception as exc:
        raise PDFChunkError(f"Failed to read PDF: {exc}") from exc

    if page_count == 0:
        raise PDFChunkError("PDF has no pages.")

    return file_bytes, page_count
