"""
Dependency injection for the cash_register application.

This module provides dependency injection functions for FastAPI services.
"""

from fastapi import Depends

from cash_register.app.services.branch_service import BranchService
from cash_register.app.services.product_service import ProductService
from cash_register.app.services.register_service import RegisterService
from shared.database.dependencies import get_db


def get_branch_service(db=Depends(get_db)) -> BranchService:
    return BranchService(db)


def get_product_service(db=Depends(get_db)) -> ProductService:
    return ProductService(db)


def get_purchase_service(db=Depends(get_db)) -> RegisterService:
    return RegisterService(db)
