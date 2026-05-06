from mcp.server.fastmcp import FastMCP

from server.config import settings

# Import all extractors to trigger self-registration into the registry
import server.extractors.read          # noqa: F401
import server.extractors.document      # noqa: F401
import server.extractors.layout        # noqa: F401
import server.extractors.invoice       # noqa: F401
import server.extractors.receipt       # noqa: F401
import server.extractors.id_document   # noqa: F401
import server.extractors.custom        # noqa: F401

from server.tools import analyze as analyze_tools
from server.tools import models as model_tools
from server.tools import results as result_tools
from server.resources import document as document_resources

mcp = FastMCP(
    name="azure-document-intelligence",
    instructions=(
        "MCP server for Azure Document Intelligence. "
        "Use analyze_document to extract structured data from PDF chunks. "
        "Use list_models to see supported model types. "
        "Use get_result to retrieve cached results."
    ),
)

analyze_tools.register(mcp)
model_tools.register(mcp)
result_tools.register(mcp)
document_resources.register(mcp)
