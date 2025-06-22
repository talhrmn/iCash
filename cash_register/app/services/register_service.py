from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from cash_register.app.exceptions import (
    BranchNotFoundError, ProductNotFoundError, InvalidPurchaseDataError, PurchaseCreationError
)
from cash_register.app.repositories.purchase_repo import PurchaseRepository
from cash_register.app.schemas.purchase import PurchaseCreate, PurchaseResponse
from cash_register.app.schemas.purchase_item import PurchaseItemResponse
from shared.database.exceptions import DatabaseError
from shared.database.logger import logger
from ..repositories.branch_repo import BranchRepository
from ..repositories.product_repo import ProductRepository
from ..repositories.users_repo import UsersRepository


class RegisterService:
    """
    Service for managing purchase transactions.

    Provides business logic for creating and managing purchases in the supermarket system.

    Attributes:
        db: SQLAlchemy session for database operations
        branch_repo: Repository for branch operations
        user_repo: Repository for user operations
        product_repo: Repository for product operations
        purchase_repo: Repository for purchase operations
    """

    def __init__(self, db: Session):
        self.db = db
        self.branch_repo = BranchRepository(db)
        self.user_repo = UsersRepository(db)
        self.product_repo = ProductRepository(db)
        self.purchase_repo = PurchaseRepository(db)

    def create_purchase(self, purchase_data: PurchaseCreate) -> PurchaseResponse:
        """
        Create a new purchase transaction.

        Args:
            purchase_data: Purchase data containing branch ID, user ID, and items

        Returns:
            PurchaseResponse: Response containing the created purchase details

        Raises:
            BranchNotFoundError: If the specified branch doesn't exist
            UserNotFoundError: If the specified user doesn't exist
            ProductNotFoundError: If any of the specified products don't exist
            InvalidPurchaseDataError: If purchase data is invalid
            PurchaseCreationError: If there's an error creating the purchase
            DatabaseError: If there's a database error
        """
        supermarket_id = purchase_data.supermarket_id
        user_id = purchase_data.user_id
        items = purchase_data.items

        if not items:
            raise InvalidPurchaseDataError("No items provided in purchase")

        logger.info(f"Starting purchase creation for branch {supermarket_id}")

        branch = self.branch_repo.get_branch_by_id(supermarket_id)
        if not branch:
            raise BranchNotFoundError(f"Branch '{supermarket_id}' not found")

        try:
            user = self.user_repo.get_or_create_user(user_id)
        except (SQLAlchemyError, DatabaseError) as e:
            raise PurchaseCreationError(f"Failed to get or create user: {e}")

        product_names = [item.product_name for item in items]
        try:
            products = self.product_repo.get_products_by_names(product_names)
        except (DatabaseError, ProductNotFoundError) as e:
            raise InvalidPurchaseDataError(f"Invalid products: {e}")

        if len(products) != len(items):
            missing = set(product_names) - {p.product_name for p in products}
            raise ProductNotFoundError(f"Products not found: {', '.join(missing)}")

        total_calc = sum(float(p.unit_price) for p in products)
        try:
            purchase = self.purchase_repo.create_purchase(
                supermarket_id=branch.id,
                user_id=user.id,
                products=products,
                total_amount=total_calc,
                timestamp=purchase_data.timestamp or datetime.utcnow()
            )
        except SQLAlchemyError as e:
            logger.error(f"Database error during purchase creation: {e}")
            raise PurchaseCreationError(f"Failed to create purchase: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during purchase creation: {e}")
            raise PurchaseCreationError(f"Failed to create purchase: {e}")

        created = self.purchase_repo.get_purchase_by_id(purchase.id)
        if not created:
            raise PurchaseCreationError("Purchase created but cannot retrieve it")

        logger.info(f"Purchase created successfully: {purchase.id}")

        return PurchaseResponse(
            id=created.id,
            supermarket_id=created.supermarket_id,
            user_id=created.user_id,
            timestamp=created.timestamp,
            total_amount=float(created.total_amount),
            items=[
                PurchaseItemResponse(
                    product_id=pi.product.id,
                    product_name=pi.product.product_name,
                    unit_price=float(pi.unit_price),
                    quantity=pi.quantity
                ) for pi in created.purchase_items
            ]
        )
