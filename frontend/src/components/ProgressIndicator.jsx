import React from 'react'

const ProgressIndicator = ({ progress, status, message, isVisible }) => {
  if (!isVisible) return null

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return '#4CAF50'
      case 'failed':
        return '#F44336'
      case 'processing':
      case 'downloading':
        return '#2196F3'
      default:
        return '#9E9E9E'
    }
  }

  const getStatusText = (status) => {
    switch (status) {
      case 'pending':
        return 'Pending'
      case 'processing':
        return 'Processing'
      case 'downloading':
        return 'Downloading'
      case 'completed':
        return 'Completed'
      case 'failed':
        return 'Failed'
      default:
        return status
    }
  }

  return (
    <div 
      className="progress-indicator"
      role="progressbar"
      aria-valuenow={progress}
      aria-valuemin="0"
      aria-valuemax="100"
      aria-label={`${getStatusText(status)}: ${progress}%`}
    >
      <div className="progress-header">
        <span className="progress-status" style={{ color: getStatusColor(status) }}>
          {getStatusText(status)}
        </span>
        <span className="progress-percentage">{progress}%</span>
      </div>
      
      <div className="progress-bar">
        <div 
          className="progress-fill"
          style={{ 
            width: `${progress}%`,
            backgroundColor: getStatusColor(status)
          }}
        />
      </div>
      
      {message && (
        <div className="progress-message">
          {message}
        </div>
      )}
    </div>
  )
}

export default ProgressIndicator