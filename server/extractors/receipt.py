from server.extractors.base import BaseExtractor
from server.extractors.registry import registry
from server.azure.formatter import (
    format_confidence, format_currency_field, format_string_field,
    format_date_field, format_address_field, format_pages_summary
)


def _extract_receipt_items(items_field: dict) -> list[dict]:
    items = []
    for item in items_field.get("valueArray", []):
        props = item.get("valueObject", {})
        items.append({
            "description": format_string_field(props.get("Description", {})),
            "quantity": props.get("Quantity", {}).get("valueNumber"),
            "price": format_currency_field(props.get("Price", {})),
            "total_price": format_currency_field(props.get("TotalPrice", {})),
        })
    return items


class ReceiptExtractor(BaseExtractor):
    model_type = "prebuilt-receipt"

    def extract(self, raw_result: dict) -> dict:
        docs = raw_result.get("documents", [])
        receipts = []

        for doc in docs:
            fields = doc.get("fields", {})
            receipts.append({
                "merchant_name": format_string_field(fields.get("MerchantName", {})),
                "merchant_address": format_address_field(fields.get("MerchantAddress", {})),
                "merchant_phone": format_string_field(fields.get("MerchantPhoneNumber", {})),
                "transaction_date": format_date_field(fields.get("TransactionDate", {})),
                "transaction_time": format_string_field(fields.get("TransactionTime", {})),
                "items": _extract_receipt_items(fields.get("Items", {})),
                "subtotal": format_currency_field(fields.get("Subtotal", {})),
                "total_tax": format_currency_field(fields.get("TotalTax", {})),
                "tip": format_currency_field(fields.get("Tip", {})),
                "total": format_currency_field(fields.get("Total", {})),
                "receipt_type": doc.get("docType"),
                "confidence": format_confidence(doc.get("confidence")),
            })

        return {
            "model": self.model_type,
            "pages": format_pages_summary(raw_result),
            "receipts": receipts,
        }


registry.register(ReceiptExtractor())
