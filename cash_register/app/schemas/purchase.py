"""
Purchase schemas for the cash_register application.

These schemas define the data structures for purchase-related requests and responses.
"""

from datetime import datetime, UTC
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, field_validator, ConfigDict, Field

from cash_register.app.schemas.purchase_item import PurchaseItemCreate, PurchaseItemResponse


class PurchaseCreate(BaseModel):
    """
    Schema for creating a new purchase.

    Attributes:
        supermarket_id: ID of the supermarket branch
        user_id: ID of the user making the purchase (optional for walk-in customers)
        items: List of items being purchased
    """
    supermarket_id: str
    user_id: Optional[UUID] = None
    items: List[PurchaseItemCreate]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator('supermarket_id')
    def validate_supermarket_id(cls, v):
        """
        Validate supermarket ID.

        Args:
            v: The supermarket ID to validate

        Raises:
            ValueError: If supermarket ID is empty or invalid
        """
        if not v or not v.strip():
            raise ValueError('Supermarket ID cannot be empty')
        return v.strip()

    @field_validator('items')
    def validate_items(cls, v):
        """
        Validate purchase items.

        Args:
            v: List of purchase items to validate

        Raises:
            ValueError: If items list is empty, over 10 items or contains duplicates
        """
        if not v:
            raise ValueError('Items list cannot be empty')
        if len(v) > 10:
            raise ValueError('Cannot purchase more than 10 different products')

        product_names = [item.product_name for item in v]
        if len(product_names) != len(set(product_names)):
            raise ValueError('Cannot purchase multiple units of the same product')

        return v


class PurchaseResponse(BaseModel):
    """
    Response schema for a purchase.

    This schema represents a completed purchase transaction.

    Attributes:
        id: Unique identifier for the purchase
        supermarket_id: ID of the supermarket branch
        user_id: ID of the user who made the purchase
        timestamp: Timestamp of the purchase
        total_amount: Total amount of the purchase
        items: List of purchased items
    """
    id: UUID
    supermarket_id: str
    user_id: UUID
    timestamp: datetime
    total_amount: float
    items: List[PurchaseItemResponse]

    model_config = ConfigDict(from_attributes=True)


class PurchaseListResponse(BaseModel):
    """
    Response schema for a list of purchases with pagination.

    This schema represents a paginated list of purchases.

    Attributes:
        purchases: List of purchase responses
        total: Total number of purchases
        page: Current page number
        page_size: Number of items per page
        total_pages: Total number of pages
    """
    purchases: List[PurchaseResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
