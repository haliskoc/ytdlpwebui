"""
Main FastAPI application for yt-dlp Web UI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging

from .api import download, status, metadata, progress
from .services.cleanup_service import CleanupService
from .services.file_service import FileService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="yt-dlp Web UI API",
    description="API for downloading YouTube videos using yt-dlp",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"]
)

# Include routers
app.include_router(download.router, prefix="/api", tags=["download"])
app.include_router(status.router, prefix="/api", tags=["status"])
app.include_router(metadata.router, prefix="/api", tags=["metadata"])
app.include_router(progress.router, prefix="/api", tags=["progress"])

# Initialize services
file_service = FileService()
cleanup_service = CleanupService(file_service)


@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info("Starting yt-dlp Web UI API")
    
    # Start cleanup scheduler
    await cleanup_service.start_cleanup_scheduler()
    logger.info("Cleanup scheduler started")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info("Shutting down yt-dlp Web UI API")
    
    # Stop cleanup scheduler
    await cleanup_service.stop_cleanup_scheduler()
    logger.info("Cleanup scheduler stopped")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "yt-dlp Web UI API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": "2024-12-19T00:00:00Z"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
