from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(..., alias="DATABASE_URL")
    api_key: str = Field(..., alias="API_KEY")

    openai_base_url: str = Field(
        "https://api.openai.com/v1", alias="OPENAI_BASE_URL"
    )
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    openai_embeddings_model: str = Field(
        "text-embedding-3-small", alias="OPENAI_EMBEDDINGS_MODEL"
    )
    openai_chat_model: str = Field(
        "gpt-4.1-mini", alias="OPENAI_CHAT_MODEL"
    )

    log_level: str = Field("INFO", alias="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore[arg-type]

