from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    azure_document_intelligence_endpoint: str = ""
    azure_document_intelligence_key: str = ""
    result_ttl: int = 3600
    server_host: str = "0.0.0.0"
    server_port: int = 8000


settings = ServerSettings()
