"""
Application settings, loaded from environment variables (see .env.example
at the repo root). Uses pydantic-settings so values are validated once at
startup instead of read ad-hoc with os.environ throughout the codebase.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- Core ---
    APP_NAME: str = "KSP Crime AI"
    ENV: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    # --- Database ---
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5433/ksp_crime"

    # --- Auth ---
    JWT_SECRET: str = "changeme"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # --- AI / RAG (optional, used by services/nlp_service.py) ---
    OPENAI_OR_LLM_API_KEY: str = ""
    VECTOR_DB_URL: str = ""

    # --- CORS ---
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
