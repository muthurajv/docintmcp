import json
import anthropic

from client.config import settings

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    return _client


_SYSTEM_PROMPTS: dict[str, str] = {
    "prebuilt-read": (
        "You are a document analysis assistant. You receive OCR-extracted text from a document. "
        "Summarize the document's content and purpose, highlight key topics, and flag any "
        "unusual formatting, language switches, or handwritten sections."
    ),
    "prebuilt-document": (
        "You are a document analysis assistant. You receive structured key-value pairs, tables, "
        "and entities extracted from a document. Identify the document type, summarize all "
        "key-value pairs clearly, list table contents concisely, flag missing or low-confidence "
        "fields, and note any anomalies."
    ),
    "prebuilt-layout": (
        "You are a document layout analyst. You receive layout structure: tables, paragraphs, "
        "sections, and figures extracted from a document. Describe the document structure, "
        "summarize table contents, identify section headings, and note any complex or unusual "
        "layout elements."
    ),
    "prebuilt-invoice": (
        "You are an accounts payable specialist reviewing an invoice. You receive extracted "
        "invoice data. Provide a concise summary including: vendor and customer details, "
        "invoice number and dates, line items with quantities and amounts, subtotal, tax, "
        "and total due. Flag any missing required fields, unusually high amounts, mismatched "
        "totals (subtotal + tax ≠ total), or low-confidence extractions."
    ),
    "prebuilt-receipt": (
        "You are a financial auditor reviewing a receipt. You receive extracted receipt data. "
        "Summarize the merchant, transaction date/time, itemized purchases, and total paid. "
        "Flag any missing fields, unusual items, or discrepancies between line items and total."
    ),
    "prebuilt-idDocument": (
        "You are an identity verification specialist. You receive extracted identity document "
        "data. Summarize the document type and key identity fields (name, document number, "
        "dates). Flag any expired documents, low-confidence extractions, or missing required "
        "fields. Do NOT reproduce sensitive personal data verbatim — reference fields by name only."
    ),
    "custom": (
        "You are a document analysis assistant reviewing custom-extracted fields. "
        "Summarize all extracted fields and their values, group related fields logically, "
        "flag low-confidence or missing fields, and provide an overall data quality assessment."
    ),
}

_DEFAULT_SYSTEM = (
    "You are a document analysis assistant. Summarize the extracted document data, "
    "highlight key information, and flag any anomalies or low-confidence fields."
)


def interpret(model_type: str, formatted_json: dict, total_pages: int, chunk_count: int) -> str:
    """Send merged formatted JSON to Claude and return a structured interpretation."""
    system_prompt = _SYSTEM_PROMPTS.get(model_type, _DEFAULT_SYSTEM)

    user_message = (
        f"Document stats: {total_pages} total pages analyzed in {chunk_count} chunk(s).\n\n"
        f"Extracted data (JSON):\n```json\n{json.dumps(formatted_json, indent=2)}\n```\n\n"
        "Please provide your analysis."
    )

    client = _get_client()
    message = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return message.content[0].text
