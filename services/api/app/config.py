from __future__ import annotations

from pathlib import Path
from typing import Literal
from urllib.parse import urlsplit

from pydantic import Field, field_validator, model_validator
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
        hide_input_in_errors=True,
    )

    environment: Literal['development', 'preview', 'production'] = 'development'
    api_port: int = 8000
    database_url: str = Field(repr=False)
    allowed_origins: str = 'http://localhost:3000,http://localhost:3001'
    allowed_origin_regex: str | None = None
    public_web_url: str | None = None
    paypal_client_id: str | None = None
    paypal_client_secret: str | None = Field(default=None, repr=False)
    paypal_environment: str = 'sandbox'
    paypal_currency: str = 'USD'
    paypal_webhook_id: str | None = None
    email_from: str | None = None
    ops_enabled: bool = False
    ops_web_url: str | None = None
    ops_session_hours: int = Field(default=8, ge=1, le=24)

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip().rstrip('/') for origin in self.allowed_origins.split(',') if origin.strip()]

    @field_validator('database_url')
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith('postgres://'):
            return value.replace('postgres://', 'postgresql://', 1)
        return value

    @field_validator('public_web_url', 'ops_web_url')
    @classmethod
    def validate_public_web_url(cls, value: str | None) -> str | None:
        if not value:
            return None
        value = value.strip().rstrip('/')
        parsed = urlsplit(value)
        if (parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username
                or parsed.password or parsed.path or parsed.query or parsed.fragment):
            raise ValueError('PUBLIC_WEB_URL must be a web origin without a path or credentials.')
        return value

    @model_validator(mode='after')
    def validate_hosted_configuration(self):
        if self.environment == 'development':
            return self
        if self.ops_enabled and not self.ops_web_url:
            raise ValueError('Enabled hosted Operations requires OPS_WEB_URL.')
        if not self.database_url.startswith(('postgresql://', 'postgresql+psycopg2://')):
            raise ValueError('Hosted deployments require PostgreSQL DATABASE_URL.')
        if self.paypal_environment != 'sandbox':
            raise ValueError('Hosted preview supports PAYPAL_ENVIRONMENT=sandbox only.')
        if self.allowed_origin_regex:
            raise ValueError('Hosted deployments require exact ALLOWED_ORIGINS, not a regex.')
        for origin in self.allowed_origins_list + ([self.public_web_url] if self.public_web_url else []) + ([self.ops_web_url] if self.ops_web_url else []):
            parsed = urlsplit(origin)
            if (parsed.scheme != 'https' or not parsed.hostname or '*' in origin
                    or parsed.username or parsed.password or parsed.path not in ('', '/')
                    or parsed.query or parsed.fragment or parsed.hostname in ('localhost', '127.0.0.1', '::1')
                    or parsed.hostname.endswith('.app.github.dev')):
                raise ValueError('Hosted web URLs must be exact HTTPS origins independent of Codespaces.')
        return self


settings = Settings()
