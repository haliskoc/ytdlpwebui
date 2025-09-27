"""
Metadata API endpoints for yt-dlp Web UI.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from ..models.video_metadata import VideoMetadata
from ..services.ytdlp_service import YtDlpService

router = APIRouter()

# Initialize service
ytdlp_service = YtDlpService()


@router.post("/metadata")
async def get_video_metadata(request: Dict[str, str]):
    """Extract video metadata."""
    try:
        # Validate request
        if "url" not in request:
            raise HTTPException(status_code=422, detail="URL is required")
        
        url = request["url"]
        
        # Extract metadata
        metadata = await ytdlp_service.extract_metadata(url)
        
        # Return metadata
        return {
            "url": metadata.url,
            "title": metadata.title,
            "duration": metadata.duration,
            "thumbnail_url": metadata.thumbnail_url,
            "description": metadata.description,
            "uploader": metadata.uploader,
            "view_count": metadata.view_count,
            "upload_date": metadata.upload_date,
            "available_formats": metadata.available_formats,
            "available_subtitles": metadata.available_subtitles,
            "extracted_at": metadata.extracted_at
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

