from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Load the .env file
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )

    MODEL: str = "groq/llama-3.3-70b-versatile"
