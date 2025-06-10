from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    data_path: Path = Path("/data")
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    chunk_size: int = 1 * 1024 * 1024 # 1 MB
    allowed_file_types: list[str] = ["pdf", "jpg", "png"]


def get_settings():
    return Settings()
