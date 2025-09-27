"""
Integration test for complete download flow.
This test MUST fail initially (no implementation exists).
"""

import pytest
import time
from fastapi.testclient import TestClient


class TestDownloadFlow:
    """Test complete download flow from request to file download."""

    def test_complete_download_flow(self):
        """Test complete flow: metadata -> download request -> status -> file download."""
        # This test will fail until implementation is complete
        client = TestClient(app=None)  # Will be replaced with actual app
        
        # Step 1: Get metadata
        metadata_response = client.post(
            "/api/metadata",
            json={
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            }
        )
        
        assert metadata_response.status_code == 200
        metadata = metadata_response.json()
        assert "title" in metadata
        
        # Step 2: Start download
        download_response = client.post(
            "/api/download",
            json={
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "format": "video"
            }
        )
        
        assert download_response.status_code == 202
        download_data = download_response.json()
        job_id = download_data["job_id"]
        
        # Step 3: Monitor status until completion
        max_attempts = 30  # 30 seconds timeout
        for attempt in range(max_attempts):
            status_response = client.get(f"/api/status/{job_id}")
            assert status_response.status_code == 200
            
            status_data = status_response.json()
            if status_data["status"] == "completed":
                break
            elif status_data["status"] == "failed":
                pytest.fail(f"Download failed: {status_data.get('error_message', 'Unknown error')}")
            
            time.sleep(1)
        else:
            pytest.fail("Download did not complete within timeout")
        
        # Step 4: Download file
        file_response = client.get(f"/api/download/{job_id}")
        assert file_response.status_code == 200
        assert file_response.headers["content-type"] == "application/octet-stream"
        assert len(file_response.content) > 0

    def test_audio_download_flow(self):
        """Test complete flow for audio download."""
        client = TestClient(app=None)  # Will be replaced with actual app
        
        # Start audio download
        download_response = client.post(
            "/api/download",
            json={
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "format": "audio_mp3"
            }
        )
        
        assert download_response.status_code == 202
        download_data = download_response.json()
        job_id = download_data["job_id"]
        
        # Monitor until completion
        max_attempts = 30
        for attempt in range(max_attempts):
            status_response = client.get(f"/api/status/{job_id}")
            assert status_response.status_code == 200
            
            status_data = status_response.json()
            if status_data["status"] == "completed":
                break
            elif status_data["status"] == "failed":
                pytest.fail(f"Audio download failed: {status_data.get('error_message', 'Unknown error')}")
            
            time.sleep(1)
        else:
            pytest.fail("Audio download did not complete within timeout")
        
        # Download audio file
        file_response = client.get(f"/api/download/{job_id}")
        assert file_response.status_code == 200
        assert len(file_response.content) > 0

    def test_metadata_only_flow(self):
        """Test metadata-only download (no actual file)."""
        client = TestClient(app=None)  # Will be replaced with actual app
        
        # Start metadata download
        download_response = client.post(
            "/api/download",
            json={
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "format": "metadata"
            }
        )
        
        assert download_response.status_code == 202
        download_data = download_response.json()
        job_id = download_data["job_id"]
        
        # Check status (should complete quickly)
        status_response = client.get(f"/api/status/{job_id}")
        assert status_response.status_code == 200
        
        status_data = status_response.json()
        assert status_data["status"] == "completed"
        
        # Download metadata file
        file_response = client.get(f"/api/download/{job_id}")
        assert file_response.status_code == 200
        
        # Should be JSON content
        import json
        metadata = json.loads(file_response.content)
        assert "title" in metadata
        assert "duration" in metadata

    def test_subtitle_download_flow(self):
        """Test download with subtitles."""
        client = TestClient(app=None)  # Will be replaced with actual app
        
        # Start download with subtitles
        download_response = client.post(
            "/api/download",
            json={
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "format": "video",
                "include_subtitles": True
            }
        )
        
        assert download_response.status_code == 202
        download_data = download_response.json()
        job_id = download_data["job_id"]
        
        # Monitor until completion
        max_attempts = 30
        for attempt in range(max_attempts):
            status_response = client.get(f"/api/status/{job_id}")
            assert status_response.status_code == 200
            
            status_data = status_response.json()
            if status_data["status"] == "completed":
                break
            elif status_data["status"] == "failed":
                pytest.fail(f"Download with subtitles failed: {status_data.get('error_message', 'Unknown error')}")
            
            time.sleep(1)
        else:
            pytest.fail("Download with subtitles did not complete within timeout")
        
        # Download file (should include subtitles)
        file_response = client.get(f"/api/download/{job_id}")
        assert file_response.status_code == 200
        assert len(file_response.content) > 0

