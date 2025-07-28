from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class HiveSettings(BaseModel):
    base_url: str
    username: str
    password: str


class RedisSettings(BaseModel):
    url: str
    cache_ttl: int = 3600


class DatabaseSettings(BaseModel):
    url: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")

    hive: HiveSettings
    redis: RedisSettings
    database: DatabaseSettings

@lru_cache
def get_settings() -> Settings:
    return Settings()
