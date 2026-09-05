from __future__ import annotations

from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def find_env_file() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / '.env').exists() or (parent / '.env.example').exists():
            return parent / '.env'
    return Path(__file__).resolve().parents[1] / '.env'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_env_file(),
        env_file_encoding='utf-8',
        extra='ignore',
    )

    environment: str = 'development'
    api_port: int = 8000
    database_url: str
    allowed_origins: str = 'http://localhost:3000,http://localhost:3001'
    allowed_origin_regex: str | None = None
    paypal_client_id: str | None = None
    paypal_secret: str | None = None
    email_from: str | None = None

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(',') if origin.strip()]

    @field_validator('database_url')
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith('postgres://'):
            return value.replace('postgres://', 'postgresql://', 1)
        return value


settings = Settings()
