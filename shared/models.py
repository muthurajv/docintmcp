from __future__ import annotations
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel


class ModelType(str, Enum):
    READ = "prebuilt-read"
    DOCUMENT = "prebuilt-document"
    LAYOUT = "prebuilt-layout"
    INVOICE = "prebuilt-invoice"
    RECEIPT = "prebuilt-receipt"
    ID_DOCUMENT = "prebuilt-idDocument"
    CUSTOM = "custom"


class ChunkInfo(BaseModel):
    chunk_index: int
    total_chunks: int
    start_page: int
    end_page: int


class AnalysisResult(BaseModel):
    result_id: str
    model_type: str
    raw_json: dict[str, Any]
    formatted_json: dict[str, Any]
    chunk_info: Optional[ChunkInfo] = None


class MergedResult(BaseModel):
    result_id: str
    model_type: str
    total_pages: int
    chunk_count: int
    raw_chunks: list[dict[str, Any]]
    formatted_json: dict[str, Any]
    interpretation: str


class AnalyzeClientRequest(BaseModel):
    model_type: ModelType
    model_id: Optional[str] = None
    chunk_size: Optional[int] = None
    chunk_overlap: Optional[int] = None
