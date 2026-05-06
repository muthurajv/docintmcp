from __future__ import annotations
from server.extractors.base import BaseExtractor


class ExtractorRegistry:
    def __init__(self):
        self._extractors: dict[str, BaseExtractor] = {}

    def register(self, extractor: BaseExtractor) -> None:
        self._extractors[extractor.model_type] = extractor

    def get(self, model_type: str) -> BaseExtractor | None:
        return self._extractors.get(model_type)

    def list_models(self) -> list[str]:
        return list(self._extractors.keys())


registry = ExtractorRegistry()
