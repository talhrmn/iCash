from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from cash_register.app.exceptions import BranchNotFoundError, UserNotFoundError, PurchaseCreationError
from shared.database.exceptions import DatabaseError
from shared.database.logger import logger
from shared.database.models import Product, Purchase, PurchaseItem


class PurchaseRepository:
    """
    Repository for managing purchase transactions.

    Provides methods for creating and retrieving purchase transactions.
    Each purchase represents a customer's transaction at a specific branch.

    Attributes:
        db: SQLAlchemy session for database operations
    """

    def __init__(self, db: Session):
        self.db = db

    def create_purchase(
            self,
            supermarket_id: str,
            user_id: UUID,
            products: List[Product],
            total_amount: float,
            timestamp: datetime = None,
    ) -> Purchase:
        """
        Create a new purchase transaction.

        Args:
            supermarket_id: ID of the branch where the purchase occurred
            user_id: ID of the customer making the purchase
            products: List of products being purchased
            total_amount: Total amount of the purchase
            timestamp: Optional timestamp for the purchase (defaults to current time)

        Returns:
            Purchase: The created purchase transaction

        Raises:
            BranchNotFoundError: If the specified branch doesn't exist
            UserNotFoundError: If the specified user doesn't exist
            PurchaseCreationError: If there's an error creating the purchase
            DatabaseError: If there's a database error
        """
        try:
            # Create the purchase record
            purchase = Purchase(
                supermarket_id=supermarket_id,
                user_id=user_id,
                timestamp=timestamp or datetime.utcnow(),
                items_list=", ".join(p.product_name for p in products),
                total_amount=total_amount
            )
            self.db.add(purchase)
            self.db.flush()  # Flush to get the purchase ID

            # Create purchase items for each product
            for product in products:
                purchase_item = PurchaseItem(
                    purchase_id=purchase.id,
                    product_id=product.id,
                    unit_price=product.unit_price,
                    quantity=1
                )
                self.db.add(purchase_item)

            # Commit the transaction
            self.db.commit()
            logger.info(f"Created purchase {purchase.id} with {len(products)} items")
            return purchase

        except (BranchNotFoundError, UserNotFoundError):
            # Rollback on domain errors
            self.db.rollback()
            raise
        except SQLAlchemyError as e:
            # Rollback on database errors
            self.db.rollback()
            logger.error(f"Error creating purchase: {e}")
            raise PurchaseCreationError(f"Failed to create purchase: {e}")

    def get_purchase_by_id(self, purchase_id: UUID) -> Optional[Purchase]:
        """
        Retrieve a purchase transaction by its ID.

        Args:
            purchase_id: ID of the purchase to retrieve

        Returns:
            Optional[Purchase]: The purchase if found, None otherwise

        Raises:
            DatabaseError: If there's an error retrieving the purchase
        """
        try:
            stmt = (
                select(Purchase)
                .options(
                    selectinload(Purchase.purchase_items).selectinload(PurchaseItem.product)
                )
                .where(Purchase.id == purchase_id)
            )
            result = self.db.execute(stmt)
            purchase = result.scalars().first()

            if not purchase:
                logger.warning(f"Purchase not found: {purchase_id}")
                return None

            return purchase
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving purchase {purchase_id}: {e}")
            raise DatabaseError(f"Failed to retrieve purchase: {e}")
