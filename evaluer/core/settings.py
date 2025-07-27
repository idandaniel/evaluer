from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    hive_base_url: str = Field(
        default="https://localhost", description="Base URL for Hive API"
    )
    hive_username: str = Field(
        default="root", description="Username for Hive authentication"
    )
    hive_password: str = Field(
        default="Password1", description="Password for Hive authentication"
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="forbid"
    )


settings = Settings()
