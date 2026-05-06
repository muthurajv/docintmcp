"""Shared formatting helpers used by extractors."""
from typing import Any


def safe_get(d: dict, *keys: str, default: Any = None) -> Any:
    for key in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(key, default)
    return d


def format_bounding_box(box: list | None) -> dict | None:
    if not box:
        return None
    points = [{"x": box[i], "y": box[i + 1]} for i in range(0, len(box), 2)]
    return {"points": points}


def format_confidence(value: float | None) -> float | None:
    if value is None:
        return None
    return round(value, 4)


def format_currency_field(field: dict) -> dict | None:
    if not field:
        return None
    return {
        "amount": field.get("valueCurrency", {}).get("amount"),
        "currency_code": field.get("valueCurrency", {}).get("currencyCode"),
        "content": field.get("content"),
        "confidence": format_confidence(field.get("confidence")),
    }


def format_string_field(field: dict) -> dict | None:
    if not field:
        return None
    return {
        "value": field.get("valueString") or field.get("content"),
        "confidence": format_confidence(field.get("confidence")),
    }


def format_date_field(field: dict) -> dict | None:
    if not field:
        return None
    return {
        "value": field.get("valueDate"),
        "content": field.get("content"),
        "confidence": format_confidence(field.get("confidence")),
    }


def format_address_field(field: dict) -> dict | None:
    if not field:
        return None
    addr = field.get("valueAddress", {})
    return {
        "house_number": addr.get("houseNumber"),
        "po_box": addr.get("poBox"),
        "road": addr.get("road"),
        "city": addr.get("city"),
        "state": addr.get("state"),
        "postal_code": addr.get("postalCode"),
        "country_region": addr.get("countryRegion"),
        "content": field.get("content"),
        "confidence": format_confidence(field.get("confidence")),
    }


def format_pages_summary(raw_result: dict) -> list[dict]:
    pages = []
    for page in raw_result.get("pages", []):
        pages.append({
            "page_number": page.get("pageNumber"),
            "width": page.get("width"),
            "height": page.get("height"),
            "unit": page.get("unit"),
            "line_count": len(page.get("lines", [])),
            "word_count": len(page.get("words", [])),
        })
    return pages


def format_tables(raw_result: dict) -> list[dict]:
    tables = []
    for table in raw_result.get("tables", []):
        cells = []
        for cell in table.get("cells", []):
            cells.append({
                "row": cell.get("rowIndex"),
                "col": cell.get("columnIndex"),
                "row_span": cell.get("rowSpan", 1),
                "col_span": cell.get("columnSpan", 1),
                "kind": cell.get("kind", "content"),
                "content": cell.get("content"),
            })
        tables.append({
            "row_count": table.get("rowCount"),
            "column_count": table.get("columnCount"),
            "cells": cells,
        })
    return tables
