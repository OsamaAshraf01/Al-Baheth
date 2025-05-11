import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    LANGUAGE_PROCESSOR: str
    PARSING_SERVICE: str
    INDEXING_SERVICE: str
    DB_URL: str
    ES_URL: str
    ES_INDEXING: str
    EMBEDDING_MODEL: str

    model_config = {
        "env_file": os.path.join(os.path.dirname(__file__), "../.env"),
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }


def get_settings():
    return Settings()
