from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from cash_register.app.exceptions import ProductNotFoundError
from shared.database.exceptions import DatabaseError
from shared.database.logger import logger
from shared.database.models import Product


class ProductRepository:
    """
    Repository for managing product data.

    Provides methods for creating, retrieving, and managing products in the supermarket.
    Each product has a unique name and price, and can be purchased by customers.

    Attributes:
        db: SQLAlchemy session for database operations
    """

    def __init__(self, db: Session):
        self.db = db

    def get_products(self) -> List[Product]:
        """
        Retrieve all products in the supermarket.

        Returns:
            List[Product]: List of all products in the system

        Raises:
            DatabaseError: If there's an error retrieving products
        """
        try:
            stmt = select(Product)
            result = self.db.execute(stmt)
            products = result.scalars().all()
            logger.info(f"Retrieved {len(products)} products")
            return products
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving products: {e}")
            raise DatabaseError(f"Failed to retrieve products: {e}")

    def get_product_by_name(self, product_name: str) -> Optional[Product]:
        """
        Retrieve a product by its name.

        Args:
            product_name: Name of the product to retrieve

        Returns:
            Optional[Product]: The product if found, None otherwise

        Raises:
            DatabaseError: If there's an error retrieving the product
        """
        try:
            stmt = select(Product).where(Product.product_name == product_name)
            result = self.db.execute(stmt)
            product = result.scalars().first()
            if not product:
                logger.warning(f"Product not found: {product_name}")
                return None
            return product
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving product {product_name}: {e}")
            raise DatabaseError(f"Failed to retrieve product: {e}")

    def get_products_by_names(self, product_names: List[str]) -> List[Product]:
        """
        Retrieve multiple products by their names.

        Args:
            product_names: List of product names to retrieve

        Returns:
            List[Product]: List of found products

        Raises:
            ProductNotFoundError: If any requested products are not found
            DatabaseError: If there's an error retrieving products
        """
        try:
            if not product_names:
                return []
            stmt = select(Product).where(Product.product_name.in_(product_names))
            result = self.db.execute(stmt)
            products = result.scalars().all()

            found_names = {p.product_name for p in products}
            missing_names = set(product_names) - found_names
            if missing_names:
                logger.error(f"Products not found: {missing_names}")
                raise ProductNotFoundError(f"Products not found: {', '.join(missing_names)}")

            logger.info(f"Retrieved {len(products)} products by names")
            return products
        except ProductNotFoundError:
            # re-raise domain exception
            raise
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving products by names: {e}")
            raise DatabaseError(f"Failed to retrieve products: {e}")

    def get_or_create_product(self, product_name: str, unit_price: float) -> Product:
        """
        Get an existing product or create a new one if it doesn't exist.

        Args:
            product_name: Name of the product
            unit_price: Price per unit of the product

        Returns:
            Product: The existing or newly created product

        Raises:
            DatabaseError: If there's an error creating the product
        """
        try:
            existing = self.get_product_by_name(product_name)
            if existing:
                return existing

            product = Product(product_name=product_name, unit_price=unit_price)
            self.db.add(product)
            self.db.commit()
            logger.info(f"Created new product: {product_name}")
            return product
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error creating product {product_name}: {e}")
            raise DatabaseError(f"Failed to create product: {e}")
