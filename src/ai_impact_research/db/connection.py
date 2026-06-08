from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseConfig:
    url: str


def require_database_url(database_url: str | None) -> str:
    if not database_url:
        raise ValueError("DATABASE_URL is not set. Copy .env.example to .env and configure it.")
    return database_url
