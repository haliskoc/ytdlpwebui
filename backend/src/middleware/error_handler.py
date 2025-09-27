"""
Error handling middleware for yt-dlp Web UI.
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from typing import Callable


class ErrorHandlerMiddleware:
    """Middleware for handling errors."""
    
    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger(__name__)
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            try:
                await self.app(scope, receive, send)
            except Exception as e:
                await self._handle_error(request, e, send)
        else:
            await self.app(scope, receive, send)
    
    async def _handle_error(self, request: Request, error: Exception, send):
        """Handle different types of errors."""
        try:
            if isinstance(error, HTTPException):
                await self._handle_http_exception(request, error, send)
            elif isinstance(error, RequestValidationError):
                await self._handle_validation_error(request, error, send)
            elif isinstance(error, StarletteHTTPException):
                await self._handle_starlette_exception(request, error, send)
            else:
                await self._handle_generic_error(request, error, send)
        except Exception as e:
            self.logger.error(f"Error in error handler: {e}")
            # Fallback error response
            response = JSONResponse(
                status_code=500,
                content={"error": "Internal server error"}
            )
            await response(scope, receive, send)
    
    async def _handle_http_exception(self, request: Request, error: HTTPException, send):
        """Handle FastAPI HTTP exceptions."""
        self.logger.warning(f"HTTP error: {error.status_code} - {error.detail}")
        
        response = JSONResponse(
            status_code=error.status_code,
            content={"error": error.detail}
        )
        await response(request.scope, request.receive, send)
    
    async def _handle_validation_error(self, request: Request, error: RequestValidationError, send):
        """Handle request validation errors."""
        self.logger.warning(f"Validation error: {error.errors()}")
        
        response = JSONResponse(
            status_code=422,
            content={
                "error": "Validation error",
                "details": error.errors()
            }
        )
        await response(request.scope, request.receive, send)
    
    async def _handle_starlette_exception(self, request: Request, error: StarletteHTTPException, send):
        """Handle Starlette HTTP exceptions."""
        self.logger.warning(f"Starlette HTTP error: {error.status_code} - {error.detail}")
        
        response = JSONResponse(
            status_code=error.status_code,
            content={"error": error.detail}
        )
        await response(request.scope, request.receive, send)
    
    async def _handle_generic_error(self, request: Request, error: Exception, send):
        """Handle generic exceptions."""
        self.logger.error(f"Unhandled error: {type(error).__name__}: {error}")
        
        response = JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )
        await response(request.scope, request.receive, send)

