from server.extractors.base import BaseExtractor
from server.extractors.registry import registry
from server.azure.formatter import (
    format_confidence, format_currency_field, format_string_field,
    format_date_field, format_address_field, format_pages_summary
)


def _extract_line_items(items_field: dict) -> list[dict]:
    items = []
    for item in items_field.get("valueArray", []):
        props = item.get("valueObject", {})
        items.append({
            "description": format_string_field(props.get("Description", {})),
            "quantity": props.get("Quantity", {}).get("valueNumber"),
            "unit": format_string_field(props.get("Unit", {})),
            "unit_price": format_currency_field(props.get("UnitPrice", {})),
            "amount": format_currency_field(props.get("Amount", {})),
            "product_code": format_string_field(props.get("ProductCode", {})),
            "date": format_date_field(props.get("Date", {})),
            "tax": format_currency_field(props.get("Tax", {})),
        })
    return items


class InvoiceExtractor(BaseExtractor):
    model_type = "prebuilt-invoice"

    def extract(self, raw_result: dict) -> dict:
        docs = raw_result.get("documents", [])
        invoices = []

        for doc in docs:
            fields = doc.get("fields", {})
            invoices.append({
                "vendor_name": format_string_field(fields.get("VendorName", {})),
                "vendor_address": format_address_field(fields.get("VendorAddress", {})),
                "vendor_tax_id": format_string_field(fields.get("VendorTaxId", {})),
                "customer_name": format_string_field(fields.get("CustomerName", {})),
                "customer_address": format_address_field(fields.get("CustomerAddress", {})),
                "customer_id": format_string_field(fields.get("CustomerId", {})),
                "invoice_id": format_string_field(fields.get("InvoiceId", {})),
                "invoice_date": format_date_field(fields.get("InvoiceDate", {})),
                "due_date": format_date_field(fields.get("DueDate", {})),
                "purchase_order": format_string_field(fields.get("PurchaseOrder", {})),
                "billing_address": format_address_field(fields.get("BillingAddress", {})),
                "shipping_address": format_address_field(fields.get("ShippingAddress", {})),
                "subtotal": format_currency_field(fields.get("SubTotal", {})),
                "total_tax": format_currency_field(fields.get("TotalTax", {})),
                "invoice_total": format_currency_field(fields.get("InvoiceTotal", {})),
                "amount_due": format_currency_field(fields.get("AmountDue", {})),
                "previous_unpaid_balance": format_currency_field(fields.get("PreviousUnpaidBalance", {})),
                "remittance_address": format_address_field(fields.get("RemittanceAddress", {})),
                "service_start_date": format_date_field(fields.get("ServiceStartDate", {})),
                "service_end_date": format_date_field(fields.get("ServiceEndDate", {})),
                "service_address": format_address_field(fields.get("ServiceAddress", {})),
                "items": _extract_line_items(fields.get("Items", {})),
                "confidence": format_confidence(doc.get("confidence")),
            })

        return {
            "model": self.model_type,
            "pages": format_pages_summary(raw_result),
            "invoices": invoices,
        }


registry.register(InvoiceExtractor())
