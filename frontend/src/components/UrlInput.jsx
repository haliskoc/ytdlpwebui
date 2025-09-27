import React, { useState } from 'react'

const UrlInput = ({ onUrlChange, onUrlSubmit, placeholder, disabled, hasError, errorMessage }) => {
  const [url, setUrl] = useState('')

  const handleInputChange = (e) => {
    const value = e.target.value
    setUrl(value)
    onUrlChange?.(value)
  }

  const handleSubmit = () => {
    if (url.trim()) {
      onUrlSubmit?.(url.trim())
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSubmit()
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const text = e.dataTransfer.getData('text/plain')
    if (text) {
      setUrl(text)
      onUrlChange?.(text)
    }
  }

  return (
    <div className="url-input-container">
      <div className="input-group">
        <input
          type="text"
          value={url}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          placeholder={placeholder || "Enter YouTube URL"}
          disabled={disabled}
          className={`url-input ${hasError ? 'error' : ''}`}
          aria-label="YouTube URL"
        />
        <button
          onClick={handleSubmit}
          disabled={disabled || !url.trim()}
          className="submit-button"
        >
          Submit
        </button>
      </div>
      {hasError && errorMessage && (
        <div className="error-message" role="alert">
          {errorMessage}
        </div>
      )}
    </div>
  )
}

export default UrlInput