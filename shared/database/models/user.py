from uuid import uuid4

from sqlalchemy import Column, UUID
from sqlalchemy.orm import relationship

from shared.database import Base


class User(Base):
    """
    Represents a customer/user in the supermarket system.

    Each user has a unique identifier and can make multiple purchases.
    Users are identified by UUID and can be created automatically when
    they make their first purchase.

    Attributes:
        id: Unique identifier for the user
        purchases: List of purchases made by this user
    """
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid4,
        doc="Unique identifier for the user"
    )

    purchases = relationship(
        "Purchase",
        back_populates="user",
        cascade="all, delete-orphan",
        doc="List of purchases made by this user"
    )

    def __repr__(self) -> str:
        """Return a string representation of the user."""
        return f"<User id={self.id} purchases={len(self.purchases)}>"

    def get_total_spent(self) -> float:
        """
        Calculate and return the total amount spent by this user.

        Returns:
            float: Total amount spent
        """
        return sum(float(purchase.total_amount) for purchase in self.purchases)

    def get_purchase_count(self) -> int:
        """
        Return the number of purchases made by this user.

        Returns:
            int: Number of purchases
        """
        return len(self.purchases)

    def is_loyal_customer(self, min_purchases: int = 3) -> bool:
        """
        Check if this user is a loyal customer.

        A loyal customer is defined as someone who has made at least
        the specified number of purchases (default: 3).

        Args:
            min_purchases: Minimum number of purchases to be considered loyal

        Returns:
            bool: True if the user is a loyal customer, False otherwise
        """
        return self.get_purchase_count() >= min_purchases

    def get_favorite_product(self) -> str:
        """
        Return the product that this user has purchased the most.

        Returns:
            str: Name of the favorite product
        """
        if not self.purchases:
            return ""

        product_counts = {}
        for purchase in self.purchases:
            for item in purchase.items:
                product_counts[item.product.product_name] = product_counts.get(item.product.product_name,
                                                                               0) + item.quantity

        if not product_counts:
            return ""

        return max(product_counts.items(), key=lambda x: x[1])[0]
