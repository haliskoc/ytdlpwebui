"""
Status API endpoints for yt-dlp Web UI.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import os
import time

from ..models.download_job import DownloadJob, JobStatus
from ..storage.job_storage import get_job

router = APIRouter()


@router.get("/status/{job_id}")
async def get_job_status(job_id: str):
    """Get the status of a download job."""
    try:
        # Get job
        job = get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Return job status
        return {
            "job_id": job.id,
            "status": job.status,
            "progress": job.progress,
            "file_path": job.file_path,
            "file_size": job.file_size,
            "error_message": job.error_message,
            "started_at": job.started_at,
            "completed_at": job.completed_at,
            "expires_at": job.expires_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/activity")
async def update_activity():
    """Update the last activity timestamp for idle monitoring."""
    try:
        # Get the project root directory (go up from backend/src/api)
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
        activity_file = os.path.join(project_root, ".last_activity")
        
        # Update activity timestamp
        with open(activity_file, 'w') as f:
            f.write(str(int(time.time())))
        
        return {"status": "activity_updated", "timestamp": int(time.time())}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
