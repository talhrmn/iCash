from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    ENVIRONMENT: str
    DEBUG: bool = True

    STORE_ANALYTICS_PATH: str
    STORE_ANALYTICS_HOST: str
    STORE_ANALYTICS_PORT: int

    ALLOWED_ORIGINS: List[str]


settings = Settings()
