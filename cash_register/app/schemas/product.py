"""
Product schemas for the cash_register application.

These schemas define the data structures for product-related responses.
"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductResponse(BaseModel):
    """
    Response schema for product information.

    This schema represents a product in the supermarket system.

    Attributes:
        id: Unique identifier for the product
        product_name: Name of the product
        unit_price: Price per unit of the product
    """
    id: UUID
    product_name: str
    unit_price: float

    model_config = ConfigDict(from_attributes=True)
