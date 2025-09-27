"""
DownloadRequest model for yt-dlp Web UI.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from uuid import uuid4
from pydantic import BaseModel, Field, validator


class DownloadFormat(str, Enum):
    """Supported download formats."""
    VIDEO = "video"
    AUDIO_MP3 = "audio_mp3"
    AUDIO_WAV = "audio_wav"
    METADATA = "metadata"


class DownloadRequest(BaseModel):
    """Represents a user's request to download a video."""
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    url: str = Field(..., description="YouTube video URL")
    format: DownloadFormat = Field(..., description="Download format")
    include_subtitles: bool = Field(default=False, description="Whether to download subtitles")
    advanced_options: Optional[Dict[str, Any]] = Field(default=None, description="Advanced options")
    user_id: str = Field(default="anonymous", description="User identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('url')
    def validate_youtube_url(cls, v):
        """Validate that URL is a YouTube URL."""
        if not v:
            raise ValueError('URL cannot be empty')
        
        # Basic YouTube URL validation
        youtube_domains = [
            'youtube.com',
            'www.youtube.com',
            'youtu.be',
            'm.youtube.com'
        ]
        
        if not any(domain in v for domain in youtube_domains):
            raise ValueError('URL must be a valid YouTube URL')
        
        return v
    
    @validator('advanced_options')
    def validate_advanced_options(cls, v):
        """Validate advanced options if provided."""
        if v is None:
            return v
        
        allowed_options = ['cookies', 'proxy', 'output_template']
        for key in v.keys():
            if key not in allowed_options:
                raise ValueError(f'Invalid advanced option: {key}')
        
        return v
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

