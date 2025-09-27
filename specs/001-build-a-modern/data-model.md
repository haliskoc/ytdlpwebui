# Data Model: yt-dlp Web UI

**Date**: 2024-12-19  
**Feature**: 001-build-a-modern  

## Entities

### DownloadRequest
Represents a user's request to download a video with specific format and options.

**Fields**:
- `id`: string (UUID) - Unique identifier
- `url`: string - YouTube video URL (validated)
- `format`: enum - "video", "audio_mp3", "audio_wav", "metadata"
- `include_subtitles`: boolean - Whether to download subtitles
- `advanced_options`: object - Optional cookies, proxy, output template
- `user_id`: string - User identifier (session-based)
- `created_at`: datetime - Request creation timestamp

**Validation Rules**:
- URL must be valid YouTube URL format
- Format must be one of the allowed values
- Advanced options must be valid if provided

**State Transitions**:
- `pending` → `processing` → `completed` | `failed`

### DownloadJob
Represents an active or completed download operation with status and progress information.

**Fields**:
- `id`: string (UUID) - Unique identifier
- `request_id`: string - Reference to DownloadRequest
- `status`: enum - "pending", "processing", "completed", "failed"
- `progress`: number (0-100) - Download progress percentage
- `file_path`: string - Path to downloaded file (if completed)
- `file_size`: number - Size of downloaded file in bytes
- `error_message`: string - Error details (if failed)
- `started_at`: datetime - When download started
- `completed_at`: datetime - When download finished
- `expires_at`: datetime - When file will be deleted (24 hours)

**Validation Rules**:
- Progress must be between 0 and 100
- File path must exist if status is completed
- Error message required if status is failed

**State Transitions**:
- `pending` → `processing` → `completed` | `failed`
- `completed` → `expired` (after 24 hours)

### VideoMetadata
Contains video information extracted from YouTube before download.

**Fields**:
- `url`: string - YouTube video URL
- `title`: string - Video title
- `duration`: number - Video duration in seconds
- `thumbnail_url`: string - URL to video thumbnail
- `description`: string - Video description (truncated)
- `uploader`: string - Channel/uploader name
- `view_count`: number - Number of views
- `upload_date`: string - Upload date (YYYYMMDD)
- `available_formats`: array - List of available download formats
- `available_subtitles`: array - List of available subtitle languages
- `extracted_at`: datetime - When metadata was extracted

**Validation Rules**:
- URL must be valid YouTube URL
- Duration must be positive number
- Thumbnail URL must be valid HTTP/HTTPS URL

**Relationships**:
- One-to-many with DownloadRequest (multiple requests can use same metadata)

## Data Flow

1. **Metadata Extraction**: User provides URL → System extracts VideoMetadata
2. **Request Creation**: User selects format/options → System creates DownloadRequest
3. **Job Processing**: DownloadRequest → System creates DownloadJob → Processes download
4. **File Management**: Completed DownloadJob → File available for download → Auto-cleanup after 24h

## Storage Strategy

- **In-Memory**: Active DownloadJobs and recent VideoMetadata (Redis or similar)
- **File System**: Downloaded files in temporary directories
- **Database**: Optional persistence for analytics (not required for MVP)

## Cleanup Strategy

- **Files**: Automatic deletion after 24 hours based on `expires_at`
- **Metadata**: Cache for 1 hour, then refresh on new requests
- **Jobs**: Keep completed jobs for 24 hours, failed jobs for 1 hour

