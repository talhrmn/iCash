"""
Branch routes for the cash_register application.

This module contains FastAPI routes for managing supermarket branches.
"""

from typing import List

from fastapi import APIRouter, HTTPException, status, Depends

from cash_register.app.dependencies import get_branch_service
from cash_register.app.logger import logger
from cash_register.app.schemas.branch import BranchResponse
from cash_register.app.services.branch_service import BranchService
from shared.database.exceptions import DatabaseError

router = APIRouter()


@router.get("/", response_model=List[BranchResponse], summary="List all branches")
async def get_branches(
        branch_service: BranchService = Depends(get_branch_service)
) -> List[BranchResponse]:
    """
    Retrieve a list of all supermarket branches.

    Returns:
        List[BranchResponse]: List of branch information

    Raises:
        HTTPException: If there's an error retrieving branches
    """
    try:
        branches = branch_service.list_branches()
        logger.info(f"Retrieved {len(branches)} branches")
        return branches
    except DatabaseError as e:
        logger.error(f"Database error retrieving branches: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve branches"
        )
    except Exception as e:
        logger.error(f"Unexpected error retrieving branches: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
