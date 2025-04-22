from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class Settings(BaseSettings):
    MONGO_URI: str = ""
    PAGE_SIZE_DEFAULT: int = 10
    PAGE_SIZE_MAX: int = 100
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    TESTING: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @classmethod
    def get_test_settings(cls) -> "Settings":
        """Return settings configured for testing."""
        return cls(
            MONGO_URI="mongodb://localhost:27017/test_songs_db",
            DEBUG=True,
            ENVIRONMENT=Environment.TESTING,
            TESTING=True,
        )


settings = Settings()
