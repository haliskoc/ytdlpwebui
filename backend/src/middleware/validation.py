"""
Validation middleware for yt-dlp Web UI.
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Callable
import re


class ValidationMiddleware:
    """Middleware for request validation."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            # Validate request based on path
            if request.url.path.startswith("/api/download"):
                await self._validate_download_request(request)
            elif request.url.path.startswith("/api/metadata"):
                await self._validate_metadata_request(request)
        
        await self.app(scope, receive, send)
    
    async def _validate_download_request(self, request: Request):
        """Validate download request."""
        if request.method == "POST":
            try:
                body = await request.json()
                
                # Validate URL
                if "url" not in body:
                    raise HTTPException(status_code=422, detail="URL is required")
                
                url = body["url"]
                if not self._is_valid_youtube_url(url):
                    raise HTTPException(status_code=400, detail="Invalid YouTube URL")
                
                # Validate format
                if "format" not in body:
                    raise HTTPException(status_code=422, detail="Format is required")
                
                valid_formats = ["video", "audio_mp3", "audio_wav", "metadata"]
                if body["format"] not in valid_formats:
                    raise HTTPException(status_code=422, detail="Invalid format")
                
            except Exception as e:
                if isinstance(e, HTTPException):
                    raise
                raise HTTPException(status_code=400, detail="Invalid request body")
    
    async def _validate_metadata_request(self, request: Request):
        """Validate metadata request."""
        if request.method == "POST":
            try:
                body = await request.json()
                
                # Validate URL
                if "url" not in body:
                    raise HTTPException(status_code=422, detail="URL is required")
                
                url = body["url"]
                if not self._is_valid_youtube_url(url):
                    raise HTTPException(status_code=400, detail="Invalid YouTube URL")
                
            except Exception as e:
                if isinstance(e, HTTPException):
                    raise
                raise HTTPException(status_code=400, detail="Invalid request body")
    
    def _is_valid_youtube_url(self, url: str) -> bool:
        """Check if URL is a valid YouTube URL."""
        if not url:
            return False
        
        # YouTube URL patterns
        patterns = [
            r'^https?://(www\.)?youtube\.com/watch\?v=[\w-]+',
            r'^https?://youtu\.be/[\w-]+',
            r'^https?://(www\.)?youtube\.com/embed/[\w-]+',
            r'^https?://(www\.)?youtube\.com/v/[\w-]+',
            r'^https?://m\.youtube\.com/watch\?v=[\w-]+'
        ]
        
        return any(re.match(pattern, url) for pattern in patterns)

