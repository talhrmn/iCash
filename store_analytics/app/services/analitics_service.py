"""
Analytics service for store analytics.

This module provides business logic for analytics operations.
"""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from shared.database.exceptions import DatabaseError
from shared.database.logger import logger
from store_analytics.app.repositories.analytics_repo import AnalyticsRepository


class AnalyticsService:
    """
    Service for store analytics.

    Provides business logic for analytics operations.

    Attributes:
        db: SQLAlchemy session for database operations
        repo: Repository for analytics data
    """

    def __init__(self, db: Session):
        self.db = db
        self.repo = AnalyticsRepository(db)

    def get_unique_buyers_count(self) -> int:
        """
        Get count of unique buyers across all branches.

        Returns:
            int: Number of unique buyers

        Raises:
            DatabaseError: If there's an error retrieving the count
        """
        try:
            count = self.repo.count_unique_buyers()
            logger.info(f"Retrieved unique buyers count: {count}")
            return count
        except SQLAlchemyError as e:
            logger.error(f"Error getting unique buyers count: {e}")
            raise DatabaseError(f"Failed to get unique buyers count: {e}")

    def get_loyal_customers(self, min_purchases: int = 3):
        """
        Get list of loyal customers.

        Args:
            min_purchases: Minimum number of purchases to be considered loyal

        Returns:
            List of loyal customers with their purchase counts

        Raises:
            DatabaseError: If there's an error retrieving loyal customers
        """
        try:
            customers = self.repo.get_loyal_customers(min_purchases)
            logger.info(f"Retrieved {len(customers)} loyal customers")
            return customers
        except SQLAlchemyError as e:
            logger.error(f"Error getting loyal customers: {e}")
            raise DatabaseError(f"Failed to get loyal customers: {e}")

    def get_top_selling_products(self, limit: int = 3):
        """
        Get top selling products by quantity.

        Args:
            limit: Maximum number of products to return

        Returns:
            List of top-selling products with their quantities

        Raises:
            DatabaseError: If there's an error retrieving top products
        """
        try:
            products = self.repo.get_top_selling_products(limit)
            logger.info(f"Retrieved top {len(products)} selling products")
            return products
        except SQLAlchemyError as e:
            logger.error(f"Error getting top selling products: {e}")
            raise DatabaseError(f"Failed to get top selling products: {e}")
