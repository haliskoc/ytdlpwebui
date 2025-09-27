"""
DownloadJob model for yt-dlp Web UI.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, Field, validator


class JobStatus(str, Enum):
    """Download job status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"


class DownloadJob(BaseModel):
    """Represents an active or completed download operation."""
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    request_id: str = Field(..., description="Reference to DownloadRequest")
    status: JobStatus = Field(default=JobStatus.PENDING, description="Current job status")
    progress: int = Field(default=0, ge=0, le=100, description="Download progress percentage")
    file_path: Optional[str] = Field(default=None, description="Path to downloaded file")
    file_size: Optional[int] = Field(default=None, ge=0, description="File size in bytes")
    error_message: Optional[str] = Field(default=None, description="Error details if failed")
    started_at: Optional[datetime] = Field(default=None, description="When download started")
    completed_at: Optional[datetime] = Field(default=None, description="When download finished")
    expires_at: datetime = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(hours=24),
        description="When file will be deleted"
    )
    
    @validator('progress')
    def validate_progress(cls, v):
        """Validate progress is between 0 and 100."""
        if not 0 <= v <= 100:
            raise ValueError('Progress must be between 0 and 100')
        return v
    
    @validator('file_path')
    def validate_file_path(cls, v, values):
        """Validate file path exists if status is completed."""
        status = values.get('status')
        if status == JobStatus.COMPLETED and not v:
            raise ValueError('File path is required for completed jobs')
        return v
    
    @validator('error_message')
    def validate_error_message(cls, v, values):
        """Validate error message is provided if status is failed."""
        status = values.get('status')
        if status == JobStatus.FAILED and not v:
            raise ValueError('Error message is required for failed jobs')
        return v
    
    def is_expired(self) -> bool:
        """Check if the job has expired."""
        return datetime.utcnow() > self.expires_at
    
    def update_progress(self, progress: int, status: Optional[JobStatus] = None) -> None:
        """Update job progress and optionally status."""
        if not 0 <= progress <= 100:
            raise ValueError('Progress must be between 0 and 100')
        
        self.progress = progress
        
        if status:
            self.status = status
            
            if status == JobStatus.PROCESSING and not self.started_at:
                self.started_at = datetime.utcnow()
            elif status in [JobStatus.COMPLETED, JobStatus.FAILED]:
                self.completed_at = datetime.utcnow()
    
    def mark_failed(self, error_message: str) -> None:
        """Mark job as failed with error message."""
        self.status = JobStatus.FAILED
        self.error_message = error_message
        self.completed_at = datetime.utcnow()
    
    def mark_completed(self, file_path: str, file_size: int) -> None:
        """Mark job as completed with file information."""
        self.status = JobStatus.COMPLETED
        self.progress = 100
        self.file_path = file_path
        self.file_size = file_size
        self.completed_at = datetime.utcnow()
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

