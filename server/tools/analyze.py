import base64
import json
import uuid

from mcp.server.fastmcp import FastMCP

from server.azure.client import analyze_pdf
from server.extractors.registry import registry
from server.storage.result_store import result_store
from shared.exceptions import ExtractorNotFoundError, AzureAnalysisError


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def analyze_document(
        pdf_b64: str,
        model_type: str,
        model_id: str = "",
    ) -> str:
        """Analyze a PDF chunk using Azure Document Intelligence.

        Args:
            pdf_b64: Base64-encoded PDF bytes.
            model_type: One of prebuilt-read, prebuilt-document, prebuilt-layout,
                        prebuilt-invoice, prebuilt-receipt, prebuilt-idDocument, custom.
            model_id: Required only when model_type is 'custom'.

        Returns:
            JSON string with result_id, raw_json, formatted_json.
        """
        extractor = registry.get(model_type)
        if extractor is None:
            raise ExtractorNotFoundError(model_type)

        resolved_model_id = extractor.get_model_id(model_id or None)
        pdf_bytes = base64.b64decode(pdf_b64)

        raw = analyze_pdf(resolved_model_id, pdf_bytes)
        formatted = extractor.extract(raw)

        result_id = str(uuid.uuid4())
        payload = {
            "result_id": result_id,
            "model_type": model_type,
            "raw_json": raw,
            "formatted_json": formatted,
        }
        result_store.put(result_id, payload)

        return json.dumps({
            "result_id": result_id,
            "model_type": model_type,
            "formatted_json": formatted,
        })
