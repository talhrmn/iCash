from uuid import uuid4

from sqlalchemy import Column, ForeignKey, UUID, DateTime, String, func
from sqlalchemy.dialects.mysql import NUMERIC
from sqlalchemy.orm import relationship

from shared.database import Base


class Purchase(Base):
    """
    Represents a purchase transaction in the supermarket system.

    A purchase is a record of a customer's shopping transaction at a specific
    supermarket branch. Each purchase contains multiple purchase items and
    has a total amount associated with it.

    Attributes:
        id: Unique identifier for the purchase
        supermarket_id: ID of the branch where the purchase was made
        user_id: ID of the customer who made the purchase
        timestamp: When the purchase was made
        total_amount: Total amount of the purchase
        branch: Relationship to the Branch model
        user: Relationship to the User model
        purchase_items: List of PurchaseItem objects for this purchase
    """
    __tablename__ = "purchases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    supermarket_id = Column(
        String,
        ForeignKey("branches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="ID of the branch where the purchase was made"
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="ID of the customer who made the purchase"
    )

    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="When the purchase was made"
    )

    total_amount = Column(
        NUMERIC,
        nullable=False,
        default=0,
        doc="Total amount of the purchase"
    )

    branch = relationship(
        "Branch",
        back_populates="purchases",
        doc="Relationship to the Branch model"
    )

    user = relationship(
        "User",
        back_populates="purchases",
        doc="Relationship to the User model"
    )

    purchase_items = relationship(
        "PurchaseItem",
        back_populates="purchase",
        cascade="all, delete-orphan",
        doc="List of PurchaseItem objects for this purchase"
    )

    def __repr__(self) -> str:
        """Return a string representation of the purchase."""
        return f"<Purchase id={self.id} branch={self.supermarket_id} user={self.user_id} total={self.total_amount}>"

    def get_item_count(self) -> int:
        """Return the number of items in this purchase."""
        return len(self.purchase_items)
