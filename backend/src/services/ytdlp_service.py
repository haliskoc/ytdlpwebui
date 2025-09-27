"""
YtDlpService for handling yt-dlp operations.
"""

import asyncio
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from datetime import datetime

from ..models.download_request import DownloadRequest, DownloadFormat
from ..models.download_job import DownloadJob, JobStatus
from ..models.video_metadata import VideoMetadata
from ..storage.job_storage import get_job, save_job


class YtDlpService:
    """Service for handling yt-dlp operations."""
    
    def __init__(self, temp_dir: Optional[str] = None):
        """Initialize YtDlpService."""
        self.temp_dir = temp_dir or "downloads"
        self.download_dir = Path(self.temp_dir)
        self.download_dir.mkdir(exist_ok=True)
    
    async def extract_metadata(self, url: str) -> VideoMetadata:
        """Extract video metadata using yt-dlp."""
        try:
            # Run yt-dlp to get metadata
            cmd = [
                "yt-dlp",
                "--dump-json",
                "--no-download",
                url
            ]
            
            result = await self._run_command(cmd)
            
            if result.returncode != 0:
                raise Exception(f"yt-dlp failed: {result.stderr.decode()}")
            
            # Parse JSON output
            metadata_json = json.loads(result.stdout.decode())
            
            # Extract relevant information
            return VideoMetadata(
                url=url,
                title=metadata_json.get("title", "Unknown Title"),
                duration=metadata_json.get("duration", 0),
                thumbnail_url=metadata_json.get("thumbnail", ""),
                description=metadata_json.get("description", ""),
                uploader=metadata_json.get("uploader", "Unknown Uploader"),
                view_count=metadata_json.get("view_count", 0),
                upload_date=metadata_json.get("upload_date", ""),
                available_formats=self._extract_available_formats(metadata_json),
                available_subtitles=self._extract_available_subtitles(metadata_json)
            )
            
        except Exception as e:
            raise Exception(f"Failed to extract metadata: {str(e)}")
    
    async def download_video(
        self, 
        request: DownloadRequest, 
        job: DownloadJob,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> str:
        """Download video using yt-dlp."""
        try:
            # Update job status
            job.update_progress(0, JobStatus.PROCESSING)
            
            # Build yt-dlp command
            cmd = self._build_download_command(request, job)
            
            # Create output directory for this job
            job_dir = self.download_dir / job.id
            job_dir.mkdir(exist_ok=True)
            
            # Run download with progress tracking
            file_path = await self._run_download_with_progress(
                cmd, job_dir, job, progress_callback
            )
            
            # Mark job as completed
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            job.mark_completed(str(file_path), file_size)
            save_job(job)  # Save completed job to storage
            
            return file_path
            
        except Exception as e:
            job.mark_failed(str(e))
            save_job(job)  # Save failed job to storage
            raise
    
    def _build_download_command(self, request: DownloadRequest, job: DownloadJob) -> list:
        """Build yt-dlp command for download."""
        cmd = ["yt-dlp"]
        
        # Set output template
        output_template = f"{job.id}/%(title)s.%(ext)s"
        if request.advanced_options and "output_template" in request.advanced_options:
            output_template = request.advanced_options["output_template"]
        
        cmd.extend(["-o", output_template])
        
        # Set format based on request
        if request.format == DownloadFormat.VIDEO:
            cmd.extend(["-f", "best[height<=720]"])
        elif request.format == DownloadFormat.AUDIO_MP3:
            cmd.extend(["-f", "bestaudio", "--extract-audio", "--audio-format", "mp3"])
        elif request.format == DownloadFormat.AUDIO_WAV:
            cmd.extend(["-f", "bestaudio", "--extract-audio", "--audio-format", "wav"])
        elif request.format == DownloadFormat.METADATA:
            cmd.extend(["--write-info-json", "--skip-download"])
        
        # Add subtitle options
        if request.include_subtitles:
            cmd.extend(["--write-subs", "--sub-langs", "all"])
        
        # Add advanced options
        if request.advanced_options:
            if "cookies" in request.advanced_options:
                cmd.extend(["--cookies", request.advanced_options["cookies"]])
            if "proxy" in request.advanced_options:
                cmd.extend(["--proxy", request.advanced_options["proxy"]])
        
        # Add URL
        cmd.append(request.url)
        
        return cmd
    
    async def _run_download_with_progress(
        self, 
        cmd: list, 
        output_dir: Path, 
        job: DownloadJob,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> str:
        """Run download command with progress tracking."""
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=self.download_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Monitor progress
        while True:
            # Check if process is still running
            if process.returncode is not None:
                break
            
            # Read stderr for progress information
            try:
                stderr_data = await asyncio.wait_for(process.stderr.read(1024), timeout=1.0)
                if stderr_data:
                    progress = self._parse_progress(stderr_data.decode())
                    if progress is not None:
                        job.update_progress(progress)
                        save_job(job)  # Save progress to storage
                        if progress_callback:
                            progress_callback(progress)
            except asyncio.TimeoutError:
                pass
            
            await asyncio.sleep(0.5)
        
        # Wait for process to complete
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise Exception(f"Download failed: {stderr.decode()}")
        
        # Find the downloaded file
        downloaded_files = list(output_dir.glob("*"))
        if not downloaded_files:
            raise Exception("No files were downloaded")
        
        # Return the first file (main download)
        return str(downloaded_files[0])
    
    def _parse_progress(self, stderr_output: str) -> Optional[int]:
        """Parse progress from yt-dlp stderr output."""
        try:
            # Look for progress percentage in stderr
            lines = stderr_output.split('\n')
            for line in lines:
                if '%' in line and 'ETA' in line:
                    # Extract percentage
                    parts = line.split()
                    for part in parts:
                        if part.endswith('%'):
                            return int(part[:-1])
        except (ValueError, IndexError):
            pass
        
        return None
    
    def _extract_available_formats(self, metadata_json: Dict[str, Any]) -> list:
        """Extract available formats from metadata."""
        formats = []
        if "formats" in metadata_json:
            for fmt in metadata_json["formats"]:
                if "format_note" in fmt:
                    formats.append(fmt["format_note"])
                elif "ext" in fmt:
                    formats.append(fmt["ext"])
        
        return list(set(formats))  # Remove duplicates
    
    def _extract_available_subtitles(self, metadata_json: Dict[str, Any]) -> list:
        """Extract available subtitle languages from metadata."""
        subtitles = []
        if "subtitles" in metadata_json:
            for lang in metadata_json["subtitles"].keys():
                subtitles.append(lang)
        
        return subtitles
    
    async def _run_command(self, cmd: list) -> subprocess.CompletedProcess:
        """Run a command and return the result."""
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=process.returncode,
            stdout=stdout,
            stderr=stderr
        )
