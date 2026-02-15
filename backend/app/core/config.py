from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ZUNO"
    env: str = "development"
    secret_key: str = "change-me"
    access_token_exp_minutes: int = 30
    refresh_token_exp_minutes: int = 60 * 24 * 7
    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/zuno"
    redis_url: str = "redis://redis:6379/0"
    media_bucket: str = "zuno-media"
    media_cdn_base: str = "https://cdn.example.com"
    rate_limit_per_minute: int = 120

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
