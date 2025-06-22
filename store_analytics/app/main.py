"""
Main application file for the iCash store analytics service.

This module contains the FastAPI application setup and configuration.
"""

from contextlib import asynccontextmanager
from datetime import datetime, UTC
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from shared.database import SessionLocal
from store_analytics.app.logger import logger
from store_analytics.app.routers.api import api_router
from store_analytics.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.

    Handles startup and shutdown events for the FastAPI application.

    Args:
        app: FastAPI application instance

    Yields:
        None: Application context
    """
    logger.info("🚀 Starting iCash store_analytics...")

    try:
        db = SessionLocal()
        try:
            db.execute(text("SELECT 1"))
            logger.info("✅ Database connection established")
        except Exception as e:
            logger.error(f"❌ Database connection failed: {str(e)}")
            raise
        finally:
            db.close()

        logger.info("🎮 iCash store_analytics started successfully!")

    except Exception as e:
        logger.error(f"❌ Failed to start application: {str(e)}")
        raise

    yield

    logger.info("🛑 Shutting down iCash Analytics...")
    logger.info("👋 Application shutdown complete")


app = FastAPI(
    title="iCash - Analytics",
    description="Analytics service for iCash supermarkets",
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    """
    Handle SQLAlchemy database errors.

    Args:
        request: FastAPI request object
        exc: SQLAlchemy error instance

    Returns:
        JSONResponse: Error response
    """
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Database error occurred"}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Handle HTTP exceptions.

    Args:
        request: FastAPI request object
        exc: HTTPException instance

    Returns:
        JSONResponse: Error response
    """
    logger.error(f"HTTP error: {str(exc)}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Handle general exceptions.

    Args:
        request: FastAPI request object
        exc: Exception instance

    Returns:
        JSONResponse: Error response
    """
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error"}
    )


app.include_router(api_router, prefix="/api")


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the application is running properly.

    Returns:
        dict: Health check status
    """
    try:
        db = SessionLocal()
        try:
            db.execute(text("SELECT 1"))
            db_status = "healthy"
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            db_status = "unhealthy"
        finally:
            db.close()

        return {
            "status": "healthy" if db_status == "healthy" else "degraded",
            "timestamp": datetime.now(UTC).isoformat(),
            "version": "1.0.0",
            "components": {
                "database": db_status,
                "api": "healthy"
            }
        }

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.now(UTC).isoformat(),
                "error": "Service unavailable"
            }
        )


@app.get("/")
async def root():
    """
    Root endpoint with basic information about the API.

    Returns:
        dict: API information
    """
    return {
        "name": "iCash Analytics API",
        "version": "1.0.0",
        "description": "Analytics service for iCash supermarkets",
        "documentation": "/docs",
        "endpoints": {
            "health": "/health",
            "docs": "/docs" if settings.DEBUG else "disabled",
            "api": "/api/analytics"
        },
        "features": [
            "Count unique buyers across chain",
            "Identify loyal customers (3+ purchases)",
            "Top 3 best-selling products analysis",
            "Real-time analytics dashboard"
        ]
    }


@app.middleware("http")
async def log_requests(request, call_next):
    """
    Log all incoming requests for debugging and monitoring.
    """
    start_time = __import__('time').time()

    logger.info(
        f"📨 {request.method} {request.url.path} - Client: {request.client.host if request.client else 'unknown'}")

    try:
        response = await call_next(request)
        process_time = __import__('time').time() - start_time
        logger.info(
            f"📤 {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.3f}s")

        response.headers["X-Process-Time"] = str(process_time)

        return response

    except Exception as e:
        process_time = __import__('time').time() - start_time
        logger.error(f"💥 {request.method} {request.url.path} - Error: {str(e)} - Time: {process_time:.3f}s")
        raise


if __name__ == "__main__":
    import uvicorn

    logger.info("🚀 Starting store-analytics application...")

    uvicorn.run(
        settings.STORE_ANALYTICS_PATH,
        host=settings.STORE_ANALYTICS_HOST,
        port=settings.STORE_ANALYTICS_PORT,
        reload=settings.DEBUG,
        log_level="info",
        access_log=True,
    )
