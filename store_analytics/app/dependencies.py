from fastapi import Depends
from sqlalchemy.orm import Session

from shared.database.dependencies import get_db
from store_analytics.app.services.analitics_service import AnalyticsService


def get_analytics_service(db: Session = Depends(get_db)) -> AnalyticsService:
    return AnalyticsService(db)
