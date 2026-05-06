from server.extractors.base import BaseExtractor
from server.extractors.registry import registry
from server.azure.formatter import format_confidence, format_pages_summary


def _serialize_field(field: dict) -> dict:
    """Recursively serialize any field type to a JSON-safe dict."""
    if not field:
        return {}

    value_key = next((k for k in field if k.startswith("value")), None)
    raw_value = field.get(value_key) if value_key else None

    if isinstance(raw_value, dict) and value_key == "valueObject":
        raw_value = {k: _serialize_field(v) for k, v in raw_value.items()}
    elif isinstance(raw_value, list) and value_key == "valueArray":
        raw_value = [_serialize_field(v) for v in raw_value]

    return {
        "type": field.get("type"),
        "value": raw_value,
        "content": field.get("content"),
        "confidence": format_confidence(field.get("confidence")),
    }


class CustomExtractor(BaseExtractor):
    model_type = "custom"

    def get_model_id(self, custom_model_id: str | None = None) -> str:
        if not custom_model_id:
            raise ValueError("custom_model_id is required for model_type='custom'")
        return custom_model_id

    def extract(self, raw_result: dict) -> dict:
        docs = raw_result.get("documents", [])
        extracted_docs = []

        for doc in docs:
            fields = {
                name: _serialize_field(field)
                for name, field in doc.get("fields", {}).items()
            }
            extracted_docs.append({
                "doc_type": doc.get("docType"),
                "fields": fields,
                "confidence": format_confidence(doc.get("confidence")),
            })

        return {
            "model": self.model_type,
            "pages": format_pages_summary(raw_result),
            "documents": extracted_docs,
        }


registry.register(CustomExtractor())
