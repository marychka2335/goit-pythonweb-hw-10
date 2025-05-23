from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Config(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:567234@localhost:5432/todo_app"

    model_config = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )


config = Config()
