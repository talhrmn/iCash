from fastapi import APIRouter

from store_analytics.app.routers import analytics_route

api_router = APIRouter(prefix="/analytics", tags=["analytics"])

api_router.include_router(analytics_route.router)
