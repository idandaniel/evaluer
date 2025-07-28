from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class HiveSettings(BaseModel):
    base_url: str
    username: str
    password: str


class DatabaseSettings(BaseModel):
    url: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")

    hive: HiveSettings
    database: DatabaseSettings

@lru_cache
def get_settings() -> Settings:
    return Settings()
