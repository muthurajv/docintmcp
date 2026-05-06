from fastapi import FastAPI

from client.routers.analyze import router as analyze_router
from client.routers.results import router as results_router

app = FastAPI(
    title="Azure Document Intelligence MCP Client",
    description=(
        "REST API that chunks PDFs, calls the Azure Document Intelligence MCP server, "
        "merges results, and interprets them with Claude."
    ),
    version="1.0.0",
)

app.include_router(analyze_router)
app.include_router(results_router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
