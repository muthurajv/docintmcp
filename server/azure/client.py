import io
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

from server.config import settings
from shared.exceptions import AzureAnalysisError

_client: DocumentIntelligenceClient | None = None


def get_client() -> DocumentIntelligenceClient:
    global _client
    if _client is None:
        _client = DocumentIntelligenceClient(
            endpoint=settings.azure_document_intelligence_endpoint,
            credential=AzureKeyCredential(settings.azure_document_intelligence_key),
        )
    return _client


def analyze_pdf(model_id: str, pdf_bytes: bytes) -> dict:
    client = get_client()
    try:
        poller = client.begin_analyze_document(
            model_id=model_id,
            body=io.BytesIO(pdf_bytes),
            content_type="application/pdf",
        )
        result = poller.result()
        return result.as_dict()
    except HttpResponseError as exc:
        raise AzureAnalysisError(model_id, str(exc)) from exc
