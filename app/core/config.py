from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    MAX_BOT_TOKEN: str
    MAX_API_URL: str = Field(default="https://platform-api.max.ru")
    DATABASE_URL: str = Field(description="PostgreSQL async connection string")
    REDIS_URL: str = Field(description="Redis connection string")


settings = Settings()
