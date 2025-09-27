"""
Download API endpoints for yt-dlp Web UI.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from typing import Dict, Any
import os

from ..models.download_request import DownloadRequest
from ..models.download_job import DownloadJob, JobStatus
from ..services.ytdlp_service import YtDlpService
from ..services.file_service import FileService
from ..storage.job_storage import get_job, save_job

router = APIRouter()

# Initialize services
ytdlp_service = YtDlpService()
file_service = FileService()


@router.post("/download")
async def start_download(request: DownloadRequest, background_tasks: BackgroundTasks):
    """Start a download job."""
    try:
        # Create download job
        job = DownloadJob(request_id=request.id)
        save_job(job)
        
        # Start download in background
        background_tasks.add_task(
            _process_download,
            request,
            job
        )
        
        return {
            "job_id": job.id,
            "status": job.status,
            "message": "Download started"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/download/{job_id}")
async def download_file(job_id: str):
    """Download the completed file."""
    try:
        # Get job
        job = get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Check if job is completed
        if job.status != JobStatus.COMPLETED:
            raise HTTPException(status_code=404, detail="File not ready for download")
        
        # Check if file exists
        if not job.file_path or not file_service.file_exists(job.file_path):
            raise HTTPException(status_code=410, detail="File has expired and been deleted")
        
        # Return file
        return FileResponse(
            path=job.file_path,
            filename=os.path.basename(job.file_path),
            media_type='application/octet-stream'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _process_download(request: DownloadRequest, job: DownloadJob):
    """Process download in background."""
    try:
        # Update job status
        job.update_progress(0, JobStatus.PROCESSING)
        
        # Download video
        file_path = await ytdlp_service.download_video(request, job)
        
        # Update job with file information
        file_size = file_service.get_file_size(file_path)
        job.mark_completed(file_path, file_size)
        
    except Exception as e:
        job.mark_failed(str(e))
