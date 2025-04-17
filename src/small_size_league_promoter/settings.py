from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Load the .env file
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )

    FULL_SSL_MCP_PATH: str = "mcp.py"
    OPENAI_API_KEY: str
    MODEL: str = "gpt-4o-mini"

settings = Settings()