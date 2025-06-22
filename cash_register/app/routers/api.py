from fastapi import APIRouter

from cash_register.app.routers import purchase_route, product_route, branch_route

api_router = APIRouter(prefix="/cash-register")

api_router.include_router(purchase_route.router, prefix="/purchase", tags=["purchases"])
api_router.include_router(product_route.router, prefix="/product", tags=["products"])
api_router.include_router(branch_route.router, prefix="/branch", tags=["branches"])
