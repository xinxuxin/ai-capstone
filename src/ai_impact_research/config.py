from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


def _find_project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in [current, *current.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    return Path.cwd()


@dataclass(frozen=True)
class Settings:
    project_root: Path
    environment: str
    database_url: str | None
    larridin_api_base_url: str | None
    larridin_api_key: str | None
    sec_user_agent: str | None

    @property
    def samples_dir(self) -> Path:
        return self.project_root / "data" / "samples"

    @property
    def processed_dir(self) -> Path:
        return self.project_root / "data" / "processed"

    @property
    def reports_dir(self) -> Path:
        return self.project_root / "reports"


def load_settings() -> Settings:
    return Settings(
        project_root=_find_project_root(),
        environment=os.getenv("PROJECT_ENV", "dev"),
        database_url=os.getenv("DATABASE_URL"),
        larridin_api_base_url=os.getenv("LARRIDIN_API_BASE_URL"),
        larridin_api_key=os.getenv("LARRIDIN_API_KEY"),
        sec_user_agent=os.getenv("SEC_USER_AGENT"),
    )
