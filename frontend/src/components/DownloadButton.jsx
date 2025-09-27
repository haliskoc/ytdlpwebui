import React from 'react'

const DownloadButton = ({ 
  onClick, 
  disabled, 
  isLoading, 
  status,
  downloadUrl 
}) => {
  const getButtonText = () => {
    if (isLoading) {
      return 'Processing...'
    }
    
    switch (status) {
      case 'completed':
        return 'Download File'
      case 'failed':
        return 'Retry Download'
      default:
        return 'Start Download'
    }
  }

  const getButtonClass = () => {
    let baseClass = 'download-button'
    
    if (disabled || isLoading) {
      baseClass += ' disabled'
    }
    
    if (status === 'completed') {
      baseClass += ' success'
    } else if (status === 'failed') {
      baseClass += ' error'
    }
    
    return baseClass
  }

  const handleClick = () => {
    if (status === 'completed' && downloadUrl) {
      // Direct download for completed files
      window.open(downloadUrl, '_blank')
    } else {
      onClick?.()
    }
  }

  return (
    <button
      onClick={handleClick}
      disabled={disabled || isLoading}
      className={getButtonClass()}
      aria-label={getButtonText()}
    >
      {isLoading && (
        <span className="loading-spinner" aria-hidden="true">
          ⟳
        </span>
      )}
      <span className="button-text">{getButtonText()}</span>
    </button>
  )
}

export default DownloadButton