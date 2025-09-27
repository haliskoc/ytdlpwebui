import React from 'react'

const LogPanel = ({ logs, isVisible, onClear }) => {
  if (!isVisible) return null

  const getLogLevelClass = (level) => {
    switch (level) {
      case 'error':
        return 'log-error'
      case 'warning':
        return 'log-warning'
      case 'info':
        return 'log-info'
      default:
        return 'log-default'
    }
  }

  const formatTimestamp = (timestamp) => {
    try {
      return new Date(timestamp).toLocaleTimeString()
    } catch {
      return timestamp
    }
  }

  return (
    <div className="log-panel">
      <div className="log-header">
        <h3>Download Logs</h3>
        {logs.length > 0 && (
          <button 
            onClick={onClear}
            className="clear-logs-button"
            aria-label="Clear logs"
          >
            Clear
          </button>
        )}
      </div>
      
      <div className="log-content" role="log" aria-live="polite">
        {logs.length === 0 ? (
          <div className="no-logs">
            No logs available
          </div>
        ) : (
          logs.map((log, index) => (
            <div 
              key={index} 
              className={`log-entry ${getLogLevelClass(log.level)}`}
            >
              <span className="log-timestamp">
                {formatTimestamp(log.timestamp)}
              </span>
              <span className="log-level">
                [{log.level.toUpperCase()}]
              </span>
              <span className="log-message">
                {log.message}
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default LogPanel