"""
Progress API endpoints for yt-dlp Web UI.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import Dict, Any
import asyncio
import json

from ..models.download_job import DownloadJob, JobStatus
from ..storage.job_storage import get_job

router = APIRouter()


@router.get("/progress/{job_id}")
async def stream_progress(job_id: str):
    """Stream download progress via Server-Sent Events."""
    try:
        # Get job
        job = get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Create SSE stream
        async def event_generator():
            last_progress = -1
            
            while True:
                # Get current job status
                current_job = get_job(job_id)
                if not current_job:
                    break
                
                # Send progress update if changed
                if current_job.progress != last_progress:
                    event_data = {
                        "job_id": current_job.id,
                        "status": current_job.status,
                        "progress": current_job.progress
                    }
                    
                    yield f"data: {json.dumps(event_data)}\n\n"
                    last_progress = current_job.progress
                
                # Stop if job is completed or failed
                if current_job.status in [JobStatus.COMPLETED, JobStatus.FAILED]:
                    break
                
                # Wait before next update
                await asyncio.sleep(1)
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
