# Quickstart Guide: yt-dlp Web UI

**Date**: 2024-12-19  
**Feature**: 001-build-a-modern  

## Overview
This guide demonstrates the complete user journey for downloading YouTube videos using the yt-dlp Web UI.

## Prerequisites
- Modern web browser
- YouTube video URL
- Backend server running on localhost:8000
- Frontend application running on localhost:3000

## User Journey: Download YouTube Video

### Step 1: Access the Application
1. Open web browser
2. Navigate to `http://localhost:3000`
3. Verify the modern, responsive UI loads correctly

### Step 2: Get Video Metadata (Optional)
1. Paste YouTube URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
2. Click "Get Info" button
3. Verify metadata displays:
   - Video title
   - Duration
   - Thumbnail
   - Available formats
   - Subtitle languages

### Step 3: Configure Download Options
1. Select download format:
   - **Video**: Full video file (MP4)
   - **Audio (MP3)**: Audio only, MP3 format
   - **Audio (WAV)**: Audio only, WAV format
   - **Metadata**: JSON metadata only
2. Check "Include Subtitles" if desired
3. Optionally expand "Advanced Options":
   - Cookies file path
   - Proxy settings
   - Output filename template

### Step 4: Start Download
1. Click "Download" button
2. Verify progress indicator appears
3. Monitor real-time progress updates
4. Wait for completion

### Step 5: Download File
1. When status shows "Completed"
2. Click "Download File" button
3. Verify file downloads to browser's download folder
4. Confirm file plays correctly

## User Journey: Handle Errors

### Invalid URL
1. Enter invalid URL: `not-a-youtube-url`
2. Click "Download"
3. Verify error message: "Invalid YouTube URL"
4. Correct URL and retry

### Network Error
1. Start download with valid URL
2. Disconnect internet connection
3. Verify error message: "Network error occurred"
4. Reconnect and retry

### File Expired
1. Complete a download
2. Wait 24 hours (or modify system time)
3. Try to download file again
4. Verify message: "File has expired and been deleted"

## User Journey: Advanced Features

### Multiple Concurrent Downloads
1. Start first download
2. Start second download (different URL)
3. Verify both progress indicators show
4. Confirm both complete successfully
5. Try to start 6th download
6. Verify error: "Maximum concurrent downloads reached (5)"

### Subtitle Download
1. Select video with available subtitles
2. Check "Include Subtitles" option
3. Start download
4. Verify subtitle file downloads alongside video
5. Confirm subtitles display correctly

### Progress Monitoring
1. Start long download (large video file)
2. Open browser developer tools
3. Monitor Server-Sent Events in Network tab
4. Verify real-time progress updates
5. Confirm progress bar updates smoothly

## Integration Test Scenarios

### Scenario 1: Complete Download Flow
```bash
# Test metadata extraction
curl -X POST http://localhost:8000/api/metadata \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'

# Test download initiation
curl -X POST http://localhost:8000/api/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "format": "video"}'

# Test status checking
curl http://localhost:8000/api/status/{job_id}

# Test file download
curl http://localhost:8000/api/download/{job_id} -o downloaded_file.mp4
```

### Scenario 2: Error Handling
```bash
# Test invalid URL
curl -X POST http://localhost:8000/api/download \
  -H "Content-Type: application/json" \
  -d '{"url": "invalid-url", "format": "video"}'

# Test missing format
curl -X POST http://localhost:8000/api/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

### Scenario 3: Progress Streaming
```bash
# Test Server-Sent Events
curl -N http://localhost:8000/api/progress/{job_id}
```

## Validation Checklist

### Functional Validation
- [ ] URL validation works correctly
- [ ] All download formats work
- [ ] Progress updates in real-time
- [ ] Files download successfully
- [ ] Subtitles download when requested
- [ ] Metadata extraction works
- [ ] Error messages are clear

### Performance Validation
- [ ] Response time < 2 seconds for metadata
- [ ] Progress updates every 1-2 seconds
- [ ] Concurrent downloads work (up to 5)
- [ ] File cleanup after 24 hours
- [ ] Memory usage remains stable

### Security Validation
- [ ] Invalid URLs rejected
- [ ] Command injection prevented
- [ ] Files isolated in temp directories
- [ ] No sensitive data in logs
- [ ] CORS configured correctly

### UI/UX Validation
- [ ] Responsive design works on mobile
- [ ] Progress indicators are clear
- [ ] Error messages are user-friendly
- [ ] Drag-and-drop URL input works
- [ ] Modern, clean interface
- [ ] Smooth transitions and animations

