"""
Purchase routes for the cash_register application.

This module contains FastAPI routes for managing purchase transactions.
"""

from fastapi import APIRouter, Depends, status, HTTPException

from cash_register.app.dependencies import get_purchase_service
from cash_register.app.exceptions import InvalidPurchaseDataError, ProductNotFoundError, PurchaseCreationError, \
    BranchNotFoundError
from cash_register.app.logger import logger
from cash_register.app.schemas.purchase import PurchaseResponse, PurchaseCreate
from cash_register.app.services.register_service import RegisterService
from shared.database.exceptions import DatabaseError

router = APIRouter()


@router.post(
    "/",
    response_model=PurchaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new purchase"
)
async def create_purchase(
        purchase_data: PurchaseCreate,
        register_service: RegisterService = Depends(get_purchase_service)
) -> PurchaseResponse:
    """
    Create a new purchase transaction.

    Args:
        purchase_data: Purchase data containing supermarket ID, user ID, and items
        register_service: RegisterService instance

    Returns:
        PurchaseResponse: Created purchase information

    Raises:
        HTTPException: If there's an error creating the purchase
    """
    try:
        purchase = register_service.create_purchase(purchase_data)
        logger.info(f"Created purchase {purchase.id} for supermarket {purchase.supermarket_id}")
        return purchase
    except (BranchNotFoundError, PurchaseCreationError, InvalidPurchaseDataError) as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message
        )
    except ProductNotFoundError as e:
        logger.warning(f"Product not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    except DatabaseError as e:
        logger.error(f"Database error creating purchase: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create purchase"
        )
    except Exception as e:
        logger.error(f"Unexpected error creating purchase: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
