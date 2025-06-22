"""
Purchase item schemas for the cash_register application.

These schemas define the data structures for purchase item-related requests and responses.
"""

from uuid import UUID

from pydantic import BaseModel, field_validator, Field, ConfigDict


class PurchaseItemCreate(BaseModel):
    """
    Schema for creating a purchase item.

    Attributes:
        product_name: Name of the product being purchased
        quantity: Number of units (always 1)
    """
    product_name: str
    quantity: int = Field(default=1, ge=1, le=1)  # Max 1 of each product

    @field_validator('product_name')
    def validate_product_name(cls, v):
        """
        Validate product name.

        Args:
            v: The product name to validate

        Raises:
            ValueError: If product name is empty or invalid
        """
        if not v or not v.strip():
            raise ValueError('Product name cannot be empty')
        return v.strip()


class PurchaseItemResponse(BaseModel):
    """
    Response schema for a purchase item.

    This schema represents an item in a purchase transaction.

    Attributes:
        product_id: Unique identifier for the product
        product_name: Name of the product
        unit_price: Price per unit of the product
        quantity: Number of units purchased
    """
    product_id: UUID
    product_name: str
    unit_price: float
    quantity: int

    model_config = ConfigDict(from_attributes=True)
