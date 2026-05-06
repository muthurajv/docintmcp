from server.extractors.base import BaseExtractor
from server.extractors.registry import registry
from server.azure.formatter import (
    format_confidence, format_string_field, format_date_field,
    format_address_field, format_pages_summary
)


class IDDocumentExtractor(BaseExtractor):
    model_type = "prebuilt-idDocument"

    def extract(self, raw_result: dict) -> dict:
        docs = raw_result.get("documents", [])
        id_docs = []

        for doc in docs:
            fields = doc.get("fields", {})
            id_docs.append({
                "document_type": doc.get("docType"),
                "first_name": format_string_field(fields.get("FirstName", {})),
                "last_name": format_string_field(fields.get("LastName", {})),
                "document_number": format_string_field(fields.get("DocumentNumber", {})),
                "date_of_birth": format_date_field(fields.get("DateOfBirth", {})),
                "date_of_expiration": format_date_field(fields.get("DateOfExpiration", {})),
                "sex": format_string_field(fields.get("Sex", {})),
                "address": format_address_field(fields.get("Address", {})),
                "country_region": format_string_field(fields.get("CountryRegion", {})),
                "state_province_region": format_string_field(fields.get("Region", {})),
                "nationality": format_string_field(fields.get("Nationality", {})),
                "place_of_birth": format_string_field(fields.get("PlaceOfBirth", {})),
                "issuing_authority": format_string_field(fields.get("IssuingAuthority", {})),
                "personal_number": format_string_field(fields.get("PersonalNumber", {})),
                "mrz": format_string_field(fields.get("MachineReadableZone", {})),
                "confidence": format_confidence(doc.get("confidence")),
            })

        return {
            "model": self.model_type,
            "pages": format_pages_summary(raw_result),
            "id_documents": id_docs,
        }


registry.register(IDDocumentExtractor())
