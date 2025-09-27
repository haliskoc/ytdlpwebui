"""
Global job storage for yt-dlp Web UI.
"""

from typing import Dict
from ..models.download_job import DownloadJob

# Global job storage
jobs_storage: Dict[str, DownloadJob] = {}

def get_job(job_id: str) -> DownloadJob:
    """Get a job by ID."""
    return jobs_storage.get(job_id)

def save_job(job: DownloadJob) -> None:
    """Save a job to storage."""
    jobs_storage[job.id] = job

def delete_job(job_id: str) -> bool:
    """Delete a job from storage."""
    if job_id in jobs_storage:
        del jobs_storage[job_id]
        return True
    return False

def get_all_jobs() -> Dict[str, DownloadJob]:
    """Get all jobs."""
    return jobs_storage.copy()

