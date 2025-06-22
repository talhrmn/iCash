from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from shared.database import Base


class Branch(Base):
    """
    Represents a supermarket branch.

    Each branch is a physical location where purchases can be made.
    Branches have a unique identifier and can have multiple purchases.

    Attributes:
        id: Unique identifier for the branch
        purchases: List of purchases made at this branch
    """
    __tablename__ = "branches"

    id = Column(
        String,
        primary_key=True,
        index=True,
        doc="Unique identifier for the branch"
    )

    purchases = relationship(
        "Purchase",
        back_populates="branch",
        cascade="all, delete-orphan",
        doc="List of purchases made at this branch"
    )

    def __repr__(self) -> str:
        """Return a string representation of the branch."""
        return f"<Branch id={self.id} purchases={len(self.purchases)}>"

    def get_total_sales(self) -> float:
        """
        Calculate and return the total sales amount for this branch.

        Returns:
            float: Total sales amount
        """
        return sum(float(purchase.total_amount) for purchase in self.purchases)

    def get_customer_count(self) -> int:
        """
        Return the number of unique customers who have made purchases at this branch.

        Returns:
            int: Number of unique customers
        """
        return len({purchase.user_id for purchase in self.purchases})
