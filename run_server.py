"""Start the Azure Document Intelligence MCP server (HTTP + SSE transport)."""
import sys
import os

# Allow imports from project root
sys.path.insert(0, os.path.dirname(__file__))

from server.main import mcp
from server.config import settings

if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host=settings.server_host,
        port=settings.server_port,
    )
