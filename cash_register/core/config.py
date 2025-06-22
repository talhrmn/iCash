from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    ENVIRONMENT: str
    DEBUG: bool

    CASH_REGISTER_PATH: str
    CASH_REGISTER_HOST: str
    CASH_REGISTER_PORT: int

    ALLOWED_ORIGINS: List[str]


settings = Settings()
