import base64
import uuid
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from client.config import settings
from client.llm.interpreter import interpret
from client.mcp.client import analyze_document, list_models
from client.pdf.chunker import chunk_pdf
from client.pdf.loader import load_pdf_bytes
from shared.exceptions import DocIntMCPError
from shared.models import MergedResult, ModelType

router = APIRouter(prefix="/analyze", tags=["analyze"])


def _merge_formatted(chunk_results: list[dict], model_type: str) -> dict:
    """Merge formatted JSON from multiple chunks into a single coherent dict."""
    if not chunk_results:
        return {}

    merged: dict = {"model": model_type, "pages": [], "chunks_analyzed": len(chunk_results)}

    seen_pages: set[int] = set()
    for chunk in chunk_results:
        fmt = chunk.get("formatted_json", {})
        for page in fmt.get("pages", []):
            pnum = page.get("page_number")
            if pnum not in seen_pages:
                seen_pages.add(pnum)
                merged["pages"].append(page)

    merged["pages"].sort(key=lambda p: p.get("page_number", 0))

    # Merge model-specific top-level fields from the first non-empty chunk
    for chunk in chunk_results:
        fmt = chunk.get("formatted_json", {})
        for key, value in fmt.items():
            if key in ("model", "pages"):
                continue
            if key not in merged and value:
                merged[key] = value
            elif key in merged and isinstance(merged[key], list) and isinstance(value, list):
                merged[key].extend(value)

    return merged


@router.post("", response_model=MergedResult)
async def analyze_pdf(
    file: Annotated[UploadFile, File(description="PDF file to analyze")],
    model_type: Annotated[str, Form(description="Azure DI model type")] = "prebuilt-read",
    model_id: Annotated[str, Form(description="Custom model ID (only for model_type=custom)")] = "",
    chunk_size: Annotated[int, Form(description="Pages per chunk")] = 0,
    chunk_overlap: Annotated[int, Form(description="Overlapping pages between chunks")] = 0,
) -> MergedResult:
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    effective_chunk_size = chunk_size or settings.chunk_size
    effective_overlap = chunk_overlap or settings.chunk_overlap

    try:
        pdf_bytes = await file.read()
        pdf_bytes, total_pages = load_pdf_bytes(pdf_bytes)
        chunks = chunk_pdf(pdf_bytes, effective_chunk_size, effective_overlap)
    except DocIntMCPError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    chunk_results: list[dict] = []
    raw_chunks: list[dict] = []

    for chunk in chunks:
        pdf_b64 = base64.b64encode(chunk.pdf_bytes).decode()
        try:
            result = await analyze_document(pdf_b64, model_type, model_id)
        except DocIntMCPError as exc:
            raise HTTPException(status_code=502, detail=str(exc))

        result["chunk_info"] = {
            "chunk_index": chunk.index,
            "total_chunks": chunk.total,
            "start_page": chunk.start_page,
            "end_page": chunk.end_page,
        }
        chunk_results.append(result)
        raw_chunks.append({
            "chunk_index": chunk.index,
            "start_page": chunk.start_page,
            "end_page": chunk.end_page,
            "raw_json": result.get("raw_json", {}),
        })

    merged_formatted = _merge_formatted(chunk_results, model_type)
    interpretation = interpret(model_type, merged_formatted, total_pages, len(chunks))

    return MergedResult(
        result_id=str(uuid.uuid4()),
        model_type=model_type,
        total_pages=total_pages,
        chunk_count=len(chunks),
        raw_chunks=raw_chunks,
        formatted_json=merged_formatted,
        interpretation=interpretation,
    )


@router.get("/models")
async def get_models() -> list[dict]:
    try:
        return await list_models()
    except DocIntMCPError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
