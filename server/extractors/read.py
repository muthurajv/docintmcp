from server.extractors.base import BaseExtractor
from server.extractors.registry import registry
from server.azure.formatter import format_pages_summary, format_confidence


class ReadExtractor(BaseExtractor):
    model_type = "prebuilt-read"

    def extract(self, raw_result: dict) -> dict:
        paragraphs = [
            {
                "content": p.get("content"),
                "role": p.get("role"),
                "confidence": format_confidence(p.get("confidence")),
            }
            for p in raw_result.get("paragraphs", [])
        ]

        styles = []
        for style in raw_result.get("styles", []):
            styles.append({
                "is_handwritten": style.get("isHandwritten"),
                "confidence": format_confidence(style.get("confidence")),
            })

        return {
            "model": self.model_type,
            "full_text": raw_result.get("content", ""),
            "pages": format_pages_summary(raw_result),
            "paragraphs": paragraphs,
            "styles": styles,
            "language": raw_result.get("languages", [{}])[0].get("locale") if raw_result.get("languages") else None,
        }


registry.register(ReadExtractor())
