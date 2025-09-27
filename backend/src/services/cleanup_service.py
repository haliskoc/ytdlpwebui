"""
CleanupService for handling automatic file cleanup.
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

from ..models.download_job import DownloadJob, JobStatus
from .file_service import FileService


class CleanupService:
    """Service for handling automatic cleanup of expired files and jobs."""
    
    def __init__(self, file_service: FileService, cleanup_interval_hours: int = 1):
        """Initialize CleanupService."""
        self.file_service = file_service
        self.cleanup_interval_hours = cleanup_interval_hours
        self.logger = logging.getLogger(__name__)
        self._cleanup_task = None
        self._running = False
    
    async def start_cleanup_scheduler(self):
        """Start the automatic cleanup scheduler."""
        if self._running:
            return
        
        self._running = True
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
        self.logger.info("Cleanup scheduler started")
    
    async def stop_cleanup_scheduler(self):
        """Stop the automatic cleanup scheduler."""
        if not self._running:
            return
        
        self._running = False
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        
        self.logger.info("Cleanup scheduler stopped")
    
    async def _cleanup_loop(self):
        """Main cleanup loop."""
        while self._running:
            try:
                await self.cleanup_expired_files()
                await self.cleanup_expired_jobs()
                
                # Wait for next cleanup cycle
                await asyncio.sleep(self.cleanup_interval_hours * 3600)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in cleanup loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
    
    async def cleanup_expired_files(self) -> List[str]:
        """Clean up expired files from disk."""
        try:
            cleaned_files = self.file_service.cleanup_expired_files(max_age_hours=24)
            
            if cleaned_files:
                self.logger.info(f"Cleaned up {len(cleaned_files)} expired files")
                for file_path in cleaned_files:
                    self.logger.debug(f"Cleaned up file: {file_path}")
            
            return cleaned_files
            
        except Exception as e:
            self.logger.error(f"Error cleaning up expired files: {e}")
            return []
    
    async def cleanup_expired_jobs(self, jobs: List[DownloadJob] = None) -> List[str]:
        """Clean up expired jobs and their associated files."""
        if jobs is None:
            # In a real implementation, this would get jobs from a database
            # For now, we'll just clean up files
            return []
        
        cleaned_jobs = []
        
        try:
            for job in jobs:
                if self._is_job_expired(job):
                    # Clean up job files
                    if job.file_path and self.file_service.file_exists(job.file_path):
                        if self.file_service.delete_file(job.file_path):
                            self.logger.info(f"Cleaned up file for expired job: {job.id}")
                    
                    # Mark job as expired
                    job.status = JobStatus.EXPIRED
                    cleaned_jobs.append(job.id)
            
            if cleaned_jobs:
                self.logger.info(f"Cleaned up {len(cleaned_jobs)} expired jobs")
            
            return cleaned_jobs
            
        except Exception as e:
            self.logger.error(f"Error cleaning up expired jobs: {e}")
            return []
    
    def _is_job_expired(self, job: DownloadJob) -> bool:
        """Check if a job has expired."""
        return datetime.utcnow() > job.expires_at
    
    async def cleanup_job_files(self, job: DownloadJob) -> bool:
        """Clean up files for a specific job."""
        try:
            if not job.file_path:
                return True
            
            # Delete the main file
            if self.file_service.file_exists(job.file_path):
                if not self.file_service.delete_file(job.file_path):
                    self.logger.warning(f"Failed to delete file: {job.file_path}")
                    return False
            
            # Delete the job directory
            job_dir = self.file_service.base_dir / job.id
            if job_dir.exists():
                if not self.file_service.delete_directory(str(job_dir)):
                    self.logger.warning(f"Failed to delete job directory: {job_dir}")
                    return False
            
            self.logger.info(f"Cleaned up files for job: {job.id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error cleaning up job files for {job.id}: {e}")
            return False
    
    async def force_cleanup_all(self) -> Dict[str, Any]:
        """Force cleanup of all files and return statistics."""
        try:
            # Clean up all files older than 1 hour
            cleaned_files = self.file_service.cleanup_expired_files(max_age_hours=1)
            
            # Get disk usage statistics
            total_space = self.file_service.get_total_space()
            used_space = self.file_service.get_used_space()
            available_space = self.file_service.get_available_space()
            
            return {
                "cleaned_files": len(cleaned_files),
                "total_space": total_space,
                "used_space": used_space,
                "available_space": available_space,
                "cleanup_timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in force cleanup: {e}")
            return {
                "error": str(e),
                "cleanup_timestamp": datetime.utcnow().isoformat()
            }
    
    def get_cleanup_stats(self) -> Dict[str, Any]:
        """Get cleanup service statistics."""
        return {
            "running": self._running,
            "cleanup_interval_hours": self.cleanup_interval_hours,
            "total_space": self.file_service.get_total_space(),
            "used_space": self.file_service.get_used_space(),
            "available_space": self.file_service.get_available_space(),
            "last_check": datetime.utcnow().isoformat()
        }

