from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = Field(default="dev", alias="APP_ENV")
    database_url: str = Field(default="sqlite+pysqlite:///./local.db", alias="DATABASE_URL")
    bot_token: str = Field(default="", alias="BOT_TOKEN")
    admin_api_token: str = Field(default="", alias="ADMIN_API_TOKEN")
    admin_ids: str = Field(default="", alias="ADMIN_IDS")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    llm_provider: str = Field(default="mock", alias="LLM_PROVIDER")
    llm_api_key: str = Field(default="", alias="LLM_API_KEY")
    llm_model: str = Field(default="gpt-4o-mini", alias="LLM_MODEL")
    llm_disabled: bool = Field(default=True, alias="LLM_DISABLED")

    default_language: str = Field(default="ru", alias="DEFAULT_LANGUAGE")
    default_questions_per_session: int = Field(default=5, alias="DEFAULT_QUESTIONS_PER_SESSION")
    rate_limit_per_minute: int = Field(default=20, alias="RATE_LIMIT_PER_MINUTE")
    rate_limit_window_seconds: int = Field(default=60, alias="RATE_LIMIT_WINDOW_SECONDS")
    max_join_seconds: int = Field(default=30, alias="MAX_JOIN_SECONDS")
    season_id: str = Field(default="2026S1", alias="SEASON_ID")

    @property
    def admin_id_set(self) -> set[int]:
        if not self.admin_ids.strip():
            return set()
        return {int(x.strip()) for x in self.admin_ids.split(",") if x.strip()}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
