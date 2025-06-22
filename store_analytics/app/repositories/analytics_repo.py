"""
Analytics repository for store analytics.

This module provides database operations for analytics data.
"""
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from shared.database.models import User, Purchase, Product, PurchaseItem


class AnalyticsRepository:
    """
    Repository obj to access analytics data.

    Provides database operations for analytics queries.

    Attributes:
        db: SQLAlchemy session for database operations
    """

    def __init__(self, db: Session):
        self.db = db

    def count_unique_buyers(self) -> int:
        """
        Count the number of unique buyers across all branches.

        Returns:
            int: Number of unique buyers
        """
        stmt = select(func.count(User.id))
        result = self.db.execute(stmt)
        return result.scalar_one()

    def get_loyal_customers(self, min_purchases: int = 3) -> list[tuple[UUID, int]]:
        """
        Get list of loyal customers based on purchase count.

        This method performs a database query to find users who have made at least
        the specified number of purchases. It uses database-level aggregation to
        efficiently calculate purchase counts and filter loyal customers.

        Args:
            min_purchases: Minimum number of purchases to be considered loyal

        Returns:
            List of tuples containing (user_id, purchase_count) for each loyal customer
        """
        stmt = (
            select(Purchase.user_id, func.count().label('purchase_count'))
            .group_by(Purchase.user_id)
            .having(func.count() >= min_purchases)
            .order_by(func.count().desc())
        )
        result = self.db.execute(stmt)
        return result.all()

    def get_top_selling_products(self, limit: int = 3):
        """
        Get top selling products by quantity, including all products with tied popularity levels.

        Returns products from the top N distinct popularity levels.
        For example, if limit=3 and we have products with quantities [20, 20, 5, 1],
        all products will be returned because there are exactly 3 distinct popularity levels.

        Args:
            limit: Number of distinct popularity levels to include

        Returns:
            List of tuples containing (product_name, total_sold, rank)
        """
        subquery = (
            select(
                Product.product_name,
                func.sum(PurchaseItem.quantity).label('total_sold'),
                func.dense_rank().over(
                    order_by=func.sum(PurchaseItem.quantity).desc()
                ).label('popularity_rank')
            )
            .join(PurchaseItem, Product.id == PurchaseItem.product_id)
            .group_by(Product.id, Product.product_name)
        ).subquery()

        stmt = (
            select(
                subquery.c.product_name,
                subquery.c.total_sold,
                subquery.c.popularity_rank
            )
            .where(subquery.c.popularity_rank <= limit)
            .order_by(subquery.c.total_sold.desc(), subquery.c.product_name)
        )

        result = self.db.execute(stmt)
        return result.all()
