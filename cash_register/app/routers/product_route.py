"""
Product routes for the cash_register application.

This module contains FastAPI routes for managing supermarket products.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from cash_register.app.dependencies import get_product_service
from cash_register.app.logger import logger
from cash_register.app.schemas.product import ProductResponse
from cash_register.app.services.product_service import ProductService
from shared.database.exceptions import DatabaseError

router = APIRouter()


@router.get("/", response_model=List[ProductResponse], summary="List all products")
async def get_products(
        product_service: ProductService = Depends(get_product_service)
) -> List[ProductResponse]:
    """
    Retrieve a list of all products in the supermarket.

    Returns:
        List[ProductResponse]: List of product information

    Raises:
        HTTPException: If there's an error retrieving products
    """
    try:
        products = product_service.list_products()
        logger.info(f"Retrieved {len(products)} products")
        return products
    except DatabaseError as e:
        logger.error(f"Database error retrieving products: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve products"
        )
    except Exception as e:
        logger.error(f"Unexpected error retrieving products: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
