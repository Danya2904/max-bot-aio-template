from pydantic import Field, SecretStr, PostgresDsn, RedisDsn, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # --- MAX API Config ---
    MAX_BOT_TOKEN: SecretStr = Field(description="Strictly secret bot token")
    MAX_API_URL: HttpUrl = Field(default="https://platform-api.max.ru")

    # --- Infrastructure Config ---
    DATABASE_URL: PostgresDsn = Field(description="PostgreSQL async connection string")
    REDIS_URL: RedisDsn = Field(description="Redis connection string")


settings = Settings()