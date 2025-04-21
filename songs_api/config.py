from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017/songs"
    PAGE_SIZE_DEFAULT: int = 10
    PAGE_SIZE_MAX: int = 100

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }
