from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    data_path: Path = Path("data/large.jsonl")
    log_level: str = "INFO"
    batch_size: int = Field(default=500, gt=0)


settings = Settings()
