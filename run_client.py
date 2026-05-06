"""Start the Azure Document Intelligence MCP client (FastAPI REST API)."""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import uvicorn
from client.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "client.main:app",
        host=settings.client_host,
        port=settings.client_port,
        reload=False,
    )
