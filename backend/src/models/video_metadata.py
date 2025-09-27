"""
VideoMetadata model for yt-dlp Web UI.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator


class VideoMetadata(BaseModel):
    """Contains video information extracted from YouTube."""
    
    url: str = Field(..., description="YouTube video URL")
    title: str = Field(..., description="Video title")
    duration: float = Field(..., ge=0, description="Video duration in seconds")
    thumbnail_url: str = Field(..., description="URL to video thumbnail")
    description: Optional[str] = Field(default=None, description="Video description")
    uploader: str = Field(..., description="Channel/uploader name")
    view_count: int = Field(..., ge=0, description="Number of views")
    upload_date: str = Field(..., description="Upload date (YYYYMMDD)")
    available_formats: List[str] = Field(default_factory=list, description="Available download formats")
    available_subtitles: List[str] = Field(default_factory=list, description="Available subtitle languages")
    extracted_at: datetime = Field(default_factory=datetime.utcnow, description="When metadata was extracted")
    
    @validator('url')
    def validate_youtube_url(cls, v):
        """Validate that URL is a YouTube URL."""
        if not v:
            raise ValueError('URL cannot be empty')
        
        youtube_domains = [
            'youtube.com',
            'www.youtube.com',
            'youtu.be',
            'm.youtube.com'
        ]
        
        if not any(domain in v for domain in youtube_domains):
            raise ValueError('URL must be a valid YouTube URL')
        
        return v
    
    @validator('duration')
    def validate_duration(cls, v):
        """Validate duration is positive."""
        if v <= 0:
            raise ValueError('Duration must be positive')
        return v
    
    @validator('view_count')
    def validate_view_count(cls, v):
        """Validate view count is non-negative."""
        if v < 0:
            raise ValueError('View count must be non-negative')
        return v
    
    @validator('upload_date')
    def validate_upload_date(cls, v):
        """Validate upload date format."""
        if not v:
            raise ValueError('Upload date cannot be empty')
        
        # Should be in YYYYMMDD format
        if len(v) != 8 or not v.isdigit():
            raise ValueError('Upload date must be in YYYYMMDD format')
        
        return v
    
    @validator('thumbnail_url')
    def validate_thumbnail_url(cls, v):
        """Validate thumbnail URL format."""
        if not v:
            raise ValueError('Thumbnail URL cannot be empty')
        
        if not v.startswith(('http://', 'https://')):
            raise ValueError('Thumbnail URL must be a valid HTTP/HTTPS URL')
        
        return v
    
    def get_duration_formatted(self) -> str:
        """Get formatted duration string (HH:MM:SS)."""
        hours = int(self.duration // 3600)
        minutes = int((self.duration % 3600) // 60)
        seconds = int(self.duration % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def get_view_count_formatted(self) -> str:
        """Get formatted view count string."""
        if self.view_count >= 1_000_000:
            return f"{self.view_count / 1_000_000:.1f}M"
        elif self.view_count >= 1_000:
            return f"{self.view_count / 1_000:.1f}K"
        else:
            return str(self.view_count)
    
    def get_upload_date_formatted(self) -> str:
        """Get formatted upload date string."""
        try:
            date_obj = datetime.strptime(self.upload_date, "%Y%m%d")
            return date_obj.strftime("%B %d, %Y")
        except ValueError:
            return self.upload_date
    
    def has_subtitles(self) -> bool:
        """Check if video has available subtitles."""
        return len(self.available_subtitles) > 0
    
    def get_available_formats_summary(self) -> str:
        """Get summary of available formats."""
        if not self.available_formats:
            return "No formats available"
        
        return f"{len(self.available_formats)} formats available"
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

