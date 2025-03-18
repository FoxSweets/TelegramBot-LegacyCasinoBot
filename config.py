from os.path import join, dirname
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__)

LOG_LEVEL = "INFO"  # "INFO", "DEBUG", "ERROR"


class Config(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_URL: SecretStr
    ROOT_ADMIN_ID: SecretStr

    model_config = SettingsConfigDict(
        env_file=join(dirname(__file__), ".env"),
        env_file_encoding="UTF-8"
    )


config = Config()