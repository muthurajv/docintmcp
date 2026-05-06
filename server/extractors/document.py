from server.extractors.base import BaseExtractor
from server.extractors.registry import registry
from server.azure.formatter import (
    format_pages_summary, format_tables, format_confidence, format_string_field
)


class DocumentExtractor(BaseExtractor):
    model_type = "prebuilt-document"

    def extract(self, raw_result: dict) -> dict:
        key_value_pairs = []
        for kv in raw_result.get("keyValuePairs", []):
            key_content = kv.get("key", {}).get("content")
            value_content = kv.get("value", {}).get("content") if kv.get("value") else None
            key_value_pairs.append({
                "key": key_content,
                "value": value_content,
                "confidence": format_confidence(kv.get("confidence")),
            })

        entities = []
        for entity in raw_result.get("entities", []):
            entities.append({
                "category": entity.get("category"),
                "sub_category": entity.get("subCategory"),
                "content": entity.get("content"),
                "confidence": format_confidence(entity.get("confidence")),
            })

        return {
            "model": self.model_type,
            "full_text": raw_result.get("content", ""),
            "pages": format_pages_summary(raw_result),
            "key_value_pairs": key_value_pairs,
            "tables": format_tables(raw_result),
            "entities": entities,
        }


registry.register(DocumentExtractor())
