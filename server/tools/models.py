import json

from mcp.server.fastmcp import FastMCP

from server.extractors.registry import registry


_MODEL_DESCRIPTIONS = {
    "prebuilt-read": "Extract text content and reading order from documents.",
    "prebuilt-document": "Extract key-value pairs, tables, entities, and text.",
    "prebuilt-layout": "Extract layout elements: tables, sections, paragraphs, figures.",
    "prebuilt-invoice": "Extract structured invoice fields including line items and totals.",
    "prebuilt-receipt": "Extract receipt fields: merchant, items, totals.",
    "prebuilt-idDocument": "Extract identity document fields: name, DOB, document number.",
    "custom": "Use a custom-trained Azure Document Intelligence model (requires model_id).",
}


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def list_models() -> str:
        """List all supported Azure Document Intelligence model types.

        Returns:
            JSON array of objects with model_type and description.
        """
        models = [
            {"model_type": m, "description": _MODEL_DESCRIPTIONS.get(m, "")}
            for m in registry.list_models()
        ]
        return json.dumps(models)
