from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str
    app_env: str
    debug: bool

    api_host: str = '0.0.0.0'
    api_port: int = 8080

    bot_token: str
    admin_user: str

    db_url: str

    redis_url: str

    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    openai_api_key: str | None = None
    google_places_api_key: str | None = None
    yandex_maps_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()