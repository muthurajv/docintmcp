class DocIntMCPError(Exception):
    pass


class ExtractorNotFoundError(DocIntMCPError):
    def __init__(self, model_type: str):
        super().__init__(f"No extractor registered for model type: {model_type}")


class ResultNotFoundError(DocIntMCPError):
    def __init__(self, result_id: str):
        super().__init__(f"Result not found or expired: {result_id}")


class AzureAnalysisError(DocIntMCPError):
    def __init__(self, model_id: str, detail: str):
        super().__init__(f"Azure Document Intelligence analysis failed for model '{model_id}': {detail}")


class PDFChunkError(DocIntMCPError):
    pass


class MCPCallError(DocIntMCPError):
    def __init__(self, tool: str, detail: str):
        super().__init__(f"MCP tool call '{tool}' failed: {detail}")
