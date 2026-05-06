import json
from contextlib import asynccontextmanager
from typing import Any

from mcp import ClientSession
from mcp.client.sse import sse_client

from client.config import settings
from shared.exceptions import MCPCallError


@asynccontextmanager
async def _session():
    """Open a short-lived MCP session to the configured server."""
    async with sse_client(settings.mcp_sse_url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session


async def call_tool(tool_name: str, arguments: dict[str, Any]) -> Any:
    """Call an MCP tool and return the parsed result content."""
    try:
        async with _session() as session:
            result = await session.call_tool(tool_name, arguments)
    except Exception as exc:
        raise MCPCallError(tool_name, str(exc)) from exc

    if result.isError:
        error_text = result.content[0].text if result.content else "unknown error"
        raise MCPCallError(tool_name, error_text)

    raw = result.content[0].text if result.content else "{}"
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


async def list_models() -> list[dict]:
    return await call_tool("list_models", {})


async def analyze_document(pdf_b64: str, model_type: str, model_id: str = "") -> dict:
    return await call_tool("analyze_document", {
        "pdf_b64": pdf_b64,
        "model_type": model_type,
        "model_id": model_id,
    })


async def get_result(result_id: str, include_raw: bool = False) -> dict:
    return await call_tool("get_result", {
        "result_id": result_id,
        "include_raw": include_raw,
    })
