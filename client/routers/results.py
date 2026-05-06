from fastapi import APIRouter, HTTPException

from client.mcp.client import get_result, call_tool
from shared.exceptions import DocIntMCPError

router = APIRouter(prefix="/results", tags=["results"])


@router.get("/{result_id}")
async def fetch_result(result_id: str, include_raw: bool = False) -> dict:
    """Retrieve a cached analysis result from the MCP server by result ID."""
    try:
        return await get_result(result_id, include_raw=include_raw)
    except DocIntMCPError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("")
async def list_cached_results() -> list[str]:
    """List all result IDs currently cached on the MCP server."""
    try:
        return await call_tool("list_results", {})
    except DocIntMCPError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
