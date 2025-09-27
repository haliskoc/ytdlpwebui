"""
FileService for handling file operations.
"""

import os
import shutil
from pathlib import Path
from typing import Optional, List
from datetime import datetime, timedelta

from ..models.download_job import DownloadJob


class FileService:
    """Service for handling file operations."""
    
    def __init__(self, base_dir: Optional[str] = None):
        """Initialize FileService."""
        self.base_dir = Path(base_dir) if base_dir else Path("downloads")
        self.base_dir.mkdir(exist_ok=True)
    
    def get_file_path(self, job: DownloadJob) -> Optional[str]:
        """Get the file path for a download job."""
        if not job.file_path:
            return None
        
        file_path = Path(job.file_path)
        if file_path.exists():
            return str(file_path)
        
        return None
    
    def get_file_size(self, file_path: str) -> int:
        """Get file size in bytes."""
        try:
            return os.path.getsize(file_path)
        except OSError:
            return 0
    
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists."""
        return os.path.exists(file_path)
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except OSError:
            return False
    
    def delete_directory(self, dir_path: str) -> bool:
        """Delete a directory and all its contents."""
        try:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                return True
            return False
        except OSError:
            return False
    
    def cleanup_expired_files(self, max_age_hours: int = 24) -> List[str]:
        """Clean up files older than specified hours."""
        cleaned_files = []
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        try:
            for item in self.base_dir.iterdir():
                if item.is_file():
                    # Check file modification time
                    file_mtime = datetime.fromtimestamp(item.stat().st_mtime)
                    if file_mtime < cutoff_time:
                        if self.delete_file(str(item)):
                            cleaned_files.append(str(item))
                elif item.is_dir():
                    # Check directory modification time
                    dir_mtime = datetime.fromtimestamp(item.stat().st_mtime)
                    if dir_mtime < cutoff_time:
                        if self.delete_directory(str(item)):
                            cleaned_files.append(str(item))
        
        except OSError as e:
            print(f"Error during cleanup: {e}")
        
        return cleaned_files
    
    def get_available_space(self) -> int:
        """Get available disk space in bytes."""
        try:
            stat = shutil.disk_usage(self.base_dir)
            return stat.free
        except OSError:
            return 0
    
    def get_total_space(self) -> int:
        """Get total disk space in bytes."""
        try:
            stat = shutil.disk_usage(self.base_dir)
            return stat.total
        except OSError:
            return 0
    
    def get_used_space(self) -> int:
        """Get used disk space in bytes."""
        try:
            stat = shutil.disk_usage(self.base_dir)
            return stat.used
        except OSError:
            return 0
    
    def create_job_directory(self, job_id: str) -> str:
        """Create a directory for a specific job."""
        job_dir = self.base_dir / job_id
        job_dir.mkdir(exist_ok=True)
        return str(job_dir)
    
    def list_job_files(self, job_id: str) -> List[str]:
        """List all files in a job directory."""
        job_dir = self.base_dir / job_id
        if not job_dir.exists():
            return []
        
        files = []
        try:
            for item in job_dir.iterdir():
                if item.is_file():
                    files.append(str(item))
        except OSError:
            pass
        
        return files
    
    def get_file_info(self, file_path: str) -> Optional[dict]:
        """Get file information."""
        try:
            if not os.path.exists(file_path):
                return None
            
            stat = os.stat(file_path)
            return {
                "path": file_path,
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime),
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "is_file": os.path.isfile(file_path),
                "is_directory": os.path.isdir(file_path)
            }
        except OSError:
            return None
    
    def move_file(self, src_path: str, dst_path: str) -> bool:
        """Move a file from source to destination."""
        try:
            shutil.move(src_path, dst_path)
            return True
        except OSError:
            return False
    
    def copy_file(self, src_path: str, dst_path: str) -> bool:
        """Copy a file from source to destination."""
        try:
            shutil.copy2(src_path, dst_path)
            return True
        except OSError:
            return False
    
    def ensure_directory_exists(self, dir_path: str) -> bool:
        """Ensure directory exists, create if it doesn't."""
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            return True
        except OSError:
            return False
