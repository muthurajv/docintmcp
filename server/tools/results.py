import json

from mcp.server.fastmcp import FastMCP

from server.storage.result_store import result_store
from shared.exceptions import ResultNotFoundError


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def get_result(result_id: str, include_raw: bool = False) -> str:
        """Retrieve a previously stored analysis result by ID.

        Args:
            result_id: The result ID returned by analyze_document.
            include_raw: Whether to include the raw Azure DI JSON (default False).

        Returns:
            JSON string with the stored result.
        """
        data = result_store.get(result_id)
        if data is None:
            raise ResultNotFoundError(result_id)

        if not include_raw:
            data = {k: v for k, v in data.items() if k != "raw_json"}

        return json.dumps(data)

    @mcp.tool()
    def list_results() -> str:
        """List all currently cached result IDs.

        Returns:
            JSON array of result IDs.
        """
        return json.dumps(result_store.list_ids())
