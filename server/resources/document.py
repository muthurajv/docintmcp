import json

from mcp.server.fastmcp import FastMCP

from server.storage.result_store import result_store


def register(mcp: FastMCP) -> None:
    @mcp.resource("document://{result_id}/raw")
    def raw_document(result_id: str) -> str:
        """Raw Azure Document Intelligence JSON for a given result ID."""
        data = result_store.get(result_id)
        if data is None:
            return json.dumps({"error": f"Result '{result_id}' not found or expired."})
        return json.dumps(data.get("raw_json", {}), indent=2)

    @mcp.resource("document://{result_id}/formatted")
    def formatted_document(result_id: str) -> str:
        """Formatted/extracted JSON for a given result ID."""
        data = result_store.get(result_id)
        if data is None:
            return json.dumps({"error": f"Result '{result_id}' not found or expired."})
        return json.dumps(data.get("formatted_json", {}), indent=2)
