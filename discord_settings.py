from pydantic_settings import BaseSettings, SettingsConfigDict


class DiscordSettings(BaseSettings):
    # Load the .env file
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )

    DISCORD_BOT_TOKEN: str
    DISCORD_GUILD_ID: str | None = None


discord_settings = DiscordSettings()
