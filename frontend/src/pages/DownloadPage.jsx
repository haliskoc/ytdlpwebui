import React, { useState, useEffect, useCallback } from 'react'
import UrlInput from '../components/UrlInput'
import FormatSelector from '../components/FormatSelector'
import ProgressIndicator from '../components/ProgressIndicator'
import DownloadButton from '../components/DownloadButton'
import LogPanel from '../components/LogPanel'
import AdvancedOptions from '../components/AdvancedOptions'
import apiService from '../services/api'
import sseService from '../services/sse'

const DownloadPage = () => {
  // State management
  const [url, setUrl] = useState('')
  const [selectedFormat, setSelectedFormat] = useState('video')
  const [includeSubtitles, setIncludeSubtitles] = useState(false)
  const [advancedOptions, setAdvancedOptions] = useState({})
  const [showAdvanced, setShowAdvanced] = useState(false)
  
  // Download state
  const [isLoading, setIsLoading] = useState(false)
  const [currentJob, setCurrentJob] = useState(null)
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState('idle')
  const [message, setMessage] = useState('')
  
  // UI state
  const [showLogs, setShowLogs] = useState(false)
  const [logs, setLogs] = useState([])
  const [error, setError] = useState('')
  const [metadata, setMetadata] = useState(null)

  // Add log entry
  const addLog = useCallback((level, message) => {
    const timestamp = new Date().toISOString()
    setLogs(prev => [...prev, { level, message, timestamp }])
  }, [])

  // Clear logs
  const clearLogs = useCallback(() => {
    setLogs([])
  }, [])

  // Validate URL
  const validateUrl = useCallback((url) => {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)[\w-]+/
    return youtubeRegex.test(url)
  }, [])

  // Handle URL change
  const handleUrlChange = useCallback((newUrl) => {
    setUrl(newUrl)
    setError('')
    
    if (newUrl && !validateUrl(newUrl)) {
      setError('Please enter a valid YouTube URL')
    }
  }, [validateUrl])

  // Handle format change
  const handleFormatChange = useCallback((format) => {
    setSelectedFormat(format)
  }, [])

  // Handle advanced options change
  const handleAdvancedOptionsChange = useCallback((options) => {
    setAdvancedOptions(options)
  }, [])

  // Get metadata
  const getMetadata = useCallback(async () => {
    if (!url || !validateUrl(url)) {
      setError('Please enter a valid YouTube URL')
      return
    }

    try {
      setIsLoading(true)
      setError('')
      addLog('info', 'Fetching video metadata...')
      
      const data = await apiService.getMetadata(url)
      setMetadata(data)
      addLog('info', `Metadata loaded: ${data.title}`)
      
    } catch (error) {
      setError(error.message)
      addLog('error', `Failed to get metadata: ${error.message}`)
    } finally {
      setIsLoading(false)
    }
  }, [url, validateUrl, addLog])

  // Start download
  const startDownload = useCallback(async () => {
    if (!url || !validateUrl(url)) {
      setError('Please enter a valid YouTube URL')
      return
    }

    try {
      setIsLoading(true)
      setError('')
      setStatus('pending')
      setProgress(0)
      addLog('info', 'Starting download...')
      
      const downloadRequest = {
        url,
        format: selectedFormat,
        include_subtitles: includeSubtitles,
        advanced_options: Object.keys(advancedOptions).length > 0 ? advancedOptions : undefined
      }
      
      const response = await apiService.startDownload(downloadRequest)
      setCurrentJob(response.job_id)
      setStatus('processing')
      addLog('info', `Download started with job ID: ${response.job_id}`)
      
      // Start progress monitoring
      monitorProgress(response.job_id)
      
    } catch (error) {
      setError(error.message)
      setStatus('failed')
      addLog('error', `Download failed: ${error.message}`)
    } finally {
      setIsLoading(false)
    }
  }, [url, selectedFormat, includeSubtitles, advancedOptions, validateUrl, addLog])

  // Monitor download progress
  const monitorProgress = useCallback((jobId) => {
    const progressUrl = apiService.getProgressStreamUrl(jobId)
    
    sseService.connect(
      progressUrl,
      (data) => {
        setProgress(data.progress)
        setStatus(data.status)
        
        if (data.status === 'completed') {
          addLog('info', 'Download completed successfully!')
          setMessage('Download completed! Click "Download File" to save.')
          sseService.disconnect() // Disconnect when completed
        } else if (data.status === 'failed') {
          addLog('error', 'Download failed')
          setMessage('Download failed. Check logs for details.')
          sseService.disconnect() // Disconnect when failed
        } else {
          setMessage(`Downloading... ${data.progress}%`)
        }
      },
      (error) => {
        addLog('error', `Progress monitoring error: ${error.message || error}`)
        // Try to get status via polling as fallback
        pollStatus(jobId)
      },
      () => {
        addLog('info', 'Progress monitoring started')
      }
    )
  }, [addLog])

  // Fallback polling for status
  const pollStatus = useCallback(async (jobId) => {
    try {
      const statusData = await apiService.getStatus(jobId)
      setProgress(statusData.progress)
      setStatus(statusData.status)
      
      if (statusData.status === 'completed') {
        addLog('info', 'Download completed successfully!')
        setMessage('Download completed! Click "Download File" to save.')
      } else if (statusData.status === 'failed') {
        addLog('error', 'Download failed')
        setMessage('Download failed. Check logs for details.')
      } else {
        setMessage(`Downloading... ${statusData.progress}%`)
        // Continue polling if not completed
        setTimeout(() => pollStatus(jobId), 2000)
      }
    } catch (error) {
      addLog('error', `Status polling error: ${error.message}`)
    }
  }, [addLog])

  // Handle download file
  const handleDownloadFile = useCallback(async () => {
    if (!currentJob) return

    try {
      addLog('info', 'Preparing file download...')
      await apiService.downloadFile(currentJob)
      addLog('info', 'File download completed')
    } catch (error) {
      addLog('error', `File download failed: ${error.message}`)
    }
  }, [currentJob, addLog])

  // Handle retry
  const handleRetry = useCallback(() => {
    setStatus('idle')
    setProgress(0)
    setMessage('')
    setCurrentJob(null)
    addLog('info', 'Retrying download...')
    startDownload()
  }, [startDownload, addLog])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      sseService.disconnect()
    }
  }, [])

  // Get button action based on status
  const getButtonAction = () => {
    switch (status) {
      case 'completed':
        return handleDownloadFile
      case 'failed':
        return handleRetry
      default:
        return startDownload
    }
  }

  return (
    <div className="download-page">
      <div className="container">
        <header className="page-header">
          <h1>yt-dlp Web UI</h1>
          <p>Download YouTube videos with ease</p>
        </header>

        <main className="download-form">
          <div className="form-section">
            <h2>Video URL</h2>
            <UrlInput
              onUrlChange={handleUrlChange}
              onUrlSubmit={getMetadata}
              placeholder="Paste YouTube URL here..."
              disabled={isLoading}
              hasError={!!error}
              errorMessage={error}
            />
          </div>

          {metadata && (
            <div className="metadata-section">
              <h2>Video Information</h2>
              <div className="metadata-card">
                <div className="metadata-thumbnail">
                  <img src={metadata.thumbnail_url} alt="Video thumbnail" />
                </div>
                <div className="metadata-info">
                  <h3>{metadata.title}</h3>
                  <p><strong>Uploader:</strong> {metadata.uploader}</p>
                  <p><strong>Duration:</strong> {Math.floor(metadata.duration / 60)}:{(metadata.duration % 60).toFixed(0).padStart(2, '0')}</p>
                  <p><strong>Views:</strong> {metadata.view_count.toLocaleString()}</p>
                  {metadata.available_subtitles.length > 0 && (
                    <p><strong>Subtitles:</strong> {metadata.available_subtitles.join(', ')}</p>
                  )}
                </div>
              </div>
            </div>
          )}

          <div className="form-section">
            <h2>Download Options</h2>
            <FormatSelector
              selectedFormat={selectedFormat}
              onFormatChange={handleFormatChange}
              disabled={isLoading}
            />
            
            <div className="subtitle-option">
              <label>
                <input
                  type="checkbox"
                  checked={includeSubtitles}
                  onChange={(e) => setIncludeSubtitles(e.target.checked)}
                  disabled={isLoading}
                />
                Include subtitles (if available)
              </label>
            </div>
          </div>

          <div className="form-section">
            <AdvancedOptions
              isVisible={showAdvanced}
              onToggle={() => setShowAdvanced(!showAdvanced)}
              options={advancedOptions}
              onOptionsChange={handleAdvancedOptionsChange}
            />
          </div>

          <div className="form-section">
            <DownloadButton
              onClick={getButtonAction()}
              disabled={!url || !!error || isLoading}
              isLoading={isLoading}
              status={status}
              downloadUrl={status === 'completed' ? `/api/download/${currentJob}` : null}
            />
          </div>

          {(status !== 'idle' || logs.length > 0) && (
            <div className="form-section">
              <ProgressIndicator
                progress={progress}
                status={status}
                message={message}
                isVisible={status !== 'idle'}
              />
            </div>
          )}

          <div className="form-section">
            <button
              onClick={() => setShowLogs(!showLogs)}
              className="toggle-logs-button"
            >
              {showLogs ? 'Hide' : 'Show'} Logs
            </button>
            
            {showLogs && (
              <LogPanel
                logs={logs}
                isVisible={showLogs}
                onClear={clearLogs}
              />
            )}
          </div>
        </main>
      </div>
    </div>
  )
}

export default DownloadPage