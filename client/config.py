from pydantic_settings import BaseSettings, SettingsConfigDict


class ClientSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mcp_server_url: str = "http://localhost:8000"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-6"
    chunk_size: int = 5
    chunk_overlap: int = 1
    client_host: str = "0.0.0.0"
    client_port: int = 8001

    @property
    def mcp_sse_url(self) -> str:
        return f"{self.mcp_server_url}/sse"


settings = ClientSettings()
