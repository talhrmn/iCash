"""
Analytics schemas for the store analytics service.

These schemas define the data structures for analytics-related requests and responses.
"""

from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UniqueBuyersResponse(BaseModel):
    """
    Response schema for unique buyers count.

    Attributes:
        unique_buyers_count: Total number of unique buyers across all branches
    """
    unique_buyers_count: int

    model_config = ConfigDict(from_attributes=True)


class LoyalCustomer(BaseModel):
    """
    Schema for a single loyal customer.

    Attributes:
        user_id: Unique identifier for the customer
        purchase_count: Total number of purchases made by this customer
    """
    user_id: UUID
    purchase_count: int

    model_config = ConfigDict(from_attributes=True)


class LoyalCustomersResponse(BaseModel):
    """
    Response schema for loyal customers list.

    Attributes:
        loyal_customers: List of loyal customers
        criteria: Criteria used to define loyal customers
        total_loyal_customers: Total number of loyal customers found
    """
    loyal_customers: List[LoyalCustomer]
    criteria: str
    total_loyal_customers: int

    model_config = ConfigDict(from_attributes=True)


class TopSellingProduct(BaseModel):
    """
    Schema for a single top-selling product.

    Attributes:
        product_name: Name of the product
        total_sold: Total quantity sold across all branches
        rank: Rank in the top-selling list (1-based)
    """
    product_name: str
    total_sold: int
    rank: int

    model_config = ConfigDict(from_attributes=True)


class TopSellingProductsResponse(BaseModel):
    """
    Response schema for top-selling products.

    Attributes:
        top_selling_products: List of top-selling products
        limit: Maximum number of products requested
        total_products_found: Actual number of products returned
    """
    top_selling_products: List[TopSellingProduct]
    limit: int
    total_products_found: int

    model_config = ConfigDict(from_attributes=True)
