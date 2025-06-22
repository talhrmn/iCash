from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from cash_register.app.logger import logger
from cash_register.app.repositories.product_repo import ProductRepository
from cash_register.app.schemas.product import ProductResponse
from shared.database.exceptions import DatabaseError


class ProductService:
    """
    Service for managing supermarket products.

    Provides business logic for product operations in the supermarket system.

    Attributes:
        db: SQLAlchemy session for database operations
        repo: Repository for product operations
    """

    def __init__(self, db: Session):
        self.db = db
        self.repo = ProductRepository(db)

    def list_products(self) -> List[ProductResponse]:
        """
        Retrieve all products in the system.

        Returns:
            List of products with their details

        Raises:
            DatabaseError: If there's an error retrieving products
        """
        try:
            products = self.repo.get_products()
            logger.info(f"Retrieved {len(products)} products")

            return [
                ProductResponse(
                    id=product.id,
                    product_name=product.product_name,
                    unit_price=float(product.unit_price)
                )
                for product in products
            ]
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving products: {e}")
            raise DatabaseError(f"Failed to retrieve products: {e}")
