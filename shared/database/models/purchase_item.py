from typing import Optional

from sqlalchemy import Column, UUID, ForeignKey, Integer, NUMERIC, CheckConstraint
from sqlalchemy.orm import relationship, validates

from shared.database import Base
from shared.database.core.config import settings


class PurchaseItem(Base):
    """
    Represents an item in a purchase transaction.

    Each purchase item links a specific product to a purchase with its quantity
    and unit price at the time of purchase. This model implements the many-to-many
    relationship between purchases and products.

    Attributes:
        purchase_id: ID of the purchase this item belongs to
        product_id: ID of the product being purchased
        quantity: Number of units purchased (must be 1 or less)
        unit_price: Price per unit at the time of purchase.
        purchase: Relationship to the Purchase model
        product: Relationship to the Product model
    """
    __tablename__ = "purchase_items"

    purchase_id = Column(
        UUID(as_uuid=True),
        ForeignKey("purchases.id", ondelete="CASCADE"),
        primary_key=True,
        doc="ID of the purchase this item belongs to"
    )

    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="RESTRICT"),
        primary_key=True,
        doc="ID of the product being purchased"
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1,
        doc="Number of units purchased (must be 1 or less)"
    )

    unit_price = Column(
        NUMERIC,
        nullable=False,
        doc="Price per unit at the time of purchase"
    )

    purchase = relationship(
        "Purchase",
        back_populates="purchase_items",
        doc="Relationship to the Purchase model"
    )

    product = relationship(
        "Product",
        back_populates="purchase_items",
        doc="Relationship to the Product model"
    )

    def __repr__(self) -> str:
        """Return a string representation of the purchase item."""
        return f"<PurchaseItem purchase={self.purchase_id} product={self.product_id} quantity={self.quantity}>"

    def get_total_price(self) -> float:
        """Calculate and return the total price for this item."""
        return float(self.unit_price) * self.quantity

    @property
    def product_name(self) -> Optional[str]:
        """Return the product name if the product relationship is loaded."""
        return self.product.product_name if self.product else None

    # Add constraints based on assignment requirements
    __table_args__ = (
        CheckConstraint('quantity > 0', name='positive_quantity'),
        CheckConstraint(f'quantity <= {settings.MAX_QUANTITY_PER_PRODUCT}', name='max_quantity_per_product'),
        CheckConstraint('unit_price >= 0', name='non_negative_unit_price'),
    )

    @validates('quantity')
    def validate_quantity(self, key, quantity):
        """Validate quantity is within allowed limits"""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if quantity > settings.MAX_QUANTITY_PER_PRODUCT:
            raise ValueError(f"Quantity cannot exceed {settings.MAX_QUANTITY_PER_PRODUCT} per product")
        return quantity

    @validates('unit_price')
    def validate_unit_price(self, key, price):
        """Validate unit price is positive"""
        if price < 0:
            raise ValueError("Unit price must be positive")
        return price
