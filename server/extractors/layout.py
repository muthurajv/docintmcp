from server.extractors.base import BaseExtractor
from server.extractors.registry import registry
from server.azure.formatter import format_pages_summary, format_tables, format_confidence


class LayoutExtractor(BaseExtractor):
    model_type = "prebuilt-layout"

    def extract(self, raw_result: dict) -> dict:
        sections = []
        for section in raw_result.get("sections", []):
            sections.append({
                "content": section.get("content"),
                "elements": section.get("elements", []),
            })

        paragraphs = []
        for p in raw_result.get("paragraphs", []):
            paragraphs.append({
                "role": p.get("role"),
                "content": p.get("content"),
                "confidence": format_confidence(p.get("confidence")),
            })

        figures = []
        for fig in raw_result.get("figures", []):
            figures.append({
                "caption": fig.get("caption", {}).get("content"),
                "elements": fig.get("elements", []),
            })

        return {
            "model": self.model_type,
            "full_text": raw_result.get("content", ""),
            "pages": format_pages_summary(raw_result),
            "tables": format_tables(raw_result),
            "sections": sections,
            "paragraphs": paragraphs,
            "figures": figures,
        }


registry.register(LayoutExtractor())
