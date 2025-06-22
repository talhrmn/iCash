"""
Analytics routes for the store analytics service.

This module contains FastAPI routes for accessing store analytics data.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from shared.database.exceptions import DatabaseError
from store_analytics.app.dependencies import get_analytics_service
from store_analytics.app.schemas.analytics import UniqueBuyersResponse, LoyalCustomersResponse, \
    TopSellingProductsResponse, \
    LoyalCustomer, TopSellingProduct
from store_analytics.app.services.analitics_service import AnalyticsService

router = APIRouter()


@router.get(
    "/unique-buyers",
    response_model=UniqueBuyersResponse,
    summary="Get unique buyers count"
)
async def get_unique_buyers_count(
        analytics_service: AnalyticsService = Depends(get_analytics_service)
) -> UniqueBuyersResponse:
    """
    Get the total number of unique buyers across all branches.

    Returns:
        UniqueBuyersResponse: Response containing the unique buyers count

    Raises:
        HTTPException: If there's an error retrieving the count
    """
    try:
        count = analytics_service.get_unique_buyers_count()
        return UniqueBuyersResponse(unique_buyers_count=count)
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve unique buyers count: {str(e)}"
        )


@router.get(
    "/loyal-customers",
    response_model=LoyalCustomersResponse,
    summary="Get loyal customers"
)
async def get_loyal_customers(
        min_purchases: int = Query(
            default=3,
            ge=1,
            le=100,
            description="Minimum number of purchases to be considered a loyal customer"
        ),
        analytics_service: AnalyticsService = Depends(get_analytics_service)
) -> LoyalCustomersResponse:
    """
    Get list of loyal customers.

    Args:
        min_purchases: Minimum number of purchases to be considered loyal
        analytics_service: AnalyticsService instance

    Returns:
        LoyalCustomersResponse: Response containing loyal customers list

    Raises:
        HTTPException: If there's an error retrieving loyal customers
    """
    try:
        customers_data = analytics_service.get_loyal_customers(min_purchases)

        # Convert to proper schema objects
        loyal_customers = [
            LoyalCustomer(user_id=user_id, purchase_count=count)
            for user_id, count in customers_data
        ]

        return LoyalCustomersResponse(
            loyal_customers=loyal_customers,
            criteria=f"At least {min_purchases} purchases",
            total_loyal_customers=len(loyal_customers)
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve loyal customers: {str(e)}"
        )


@router.get(
    "/top-selling-products",
    response_model=TopSellingProductsResponse,
    summary="Get top-selling products of all time"
)
async def get_top_selling_products(
        limit: int = Query(
            default=3,
            ge=1,
            le=50,
            description="Maximum number of top products to return"
        ),
        analytics_service: AnalyticsService = Depends(get_analytics_service)
) -> TopSellingProductsResponse:
    """
    Get top-selling products.

    Args:
        limit: Maximum number of products to return
        analytics_service: AnalyticsService instance

    Returns:
        TopSellingProductsResponse: Response containing top selling products

    Raises:
        HTTPException: If there's an error retrieving top products
    """
    try:
        products_data = analytics_service.get_top_selling_products(limit)

        top_products = [
            TopSellingProduct(
                product_name=name,
                total_sold=sold,
                rank=rank
            )
            for name, sold, rank in products_data
        ]

        return TopSellingProductsResponse(
            top_selling_products=top_products,
            limit=limit,
            total_products_found=len(top_products)
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve top selling products: {str(e)}"
        )
