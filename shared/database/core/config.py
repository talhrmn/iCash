from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 30
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600

    PRODUCTS_CSV_PATH: str
    PURCHASES_CSV_PATH: str

    REQUIRED_BRANCH_COUNT: int = 3
    REQUIRED_PRODUCT_COUNT: int = 10
    MAX_QUANTITY_PER_PRODUCT: int = 1

settings = Settings()