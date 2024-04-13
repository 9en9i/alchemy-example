from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    SQLALCHEMY_URI: PostgresDsn

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent / ".env",
        env_prefix="CORE__",
        case_sensitive=True,
    )


settings = Settings()  # pyright: ignore[reportCallIssue]
