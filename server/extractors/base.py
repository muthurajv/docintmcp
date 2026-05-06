from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    model_type: str

    @abstractmethod
    def extract(self, raw_result: dict) -> dict:
        """Transform raw Azure DI result dict into a clean formatted dict."""
        ...

    def get_model_id(self, custom_model_id: str | None = None) -> str:
        return self.model_type
