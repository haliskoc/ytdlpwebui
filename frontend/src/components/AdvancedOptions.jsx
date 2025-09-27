import React, { useState } from 'react'

const AdvancedOptions = ({ 
  isVisible, 
  onToggle, 
  options, 
  onOptionsChange 
}) => {
  const [localOptions, setLocalOptions] = useState(options || {})

  const handleOptionChange = (key, value) => {
    const newOptions = { ...localOptions, [key]: value }
    setLocalOptions(newOptions)
    onOptionsChange?.(newOptions)
  }

  const handleClearOption = (key) => {
    const newOptions = { ...localOptions }
    delete newOptions[key]
    setLocalOptions(newOptions)
    onOptionsChange?.(newOptions)
  }

  if (!isVisible) {
    return (
      <button 
        onClick={onToggle}
        className="toggle-advanced-button"
        aria-expanded="false"
      >
        Advanced Options
      </button>
    )
  }

  return (
    <div className="advanced-options">
      <div className="advanced-header">
        <h3>Advanced Options</h3>
        <button 
          onClick={onToggle}
          className="toggle-advanced-button"
          aria-expanded="true"
        >
          Hide Advanced Options
        </button>
      </div>
      
      <div className="advanced-content">
        <div className="option-group">
          <label htmlFor="cookies-input" className="option-label">
            Cookies File Path
          </label>
          <div className="input-group">
            <input
              id="cookies-input"
              type="text"
              value={localOptions.cookies || ''}
              onChange={(e) => handleOptionChange('cookies', e.target.value)}
              placeholder="/path/to/cookies.txt"
              className="option-input"
            />
            {localOptions.cookies && (
              <button
                onClick={() => handleClearOption('cookies')}
                className="clear-option-button"
                aria-label="Clear cookies path"
              >
                ×
              </button>
            )}
          </div>
          <div className="option-description">
            Path to cookies file for authentication
          </div>
        </div>

        <div className="option-group">
          <label htmlFor="proxy-input" className="option-label">
            Proxy URL
          </label>
          <div className="input-group">
            <input
              id="proxy-input"
              type="text"
              value={localOptions.proxy || ''}
              onChange={(e) => handleOptionChange('proxy', e.target.value)}
              placeholder="http://proxy:8080"
              className="option-input"
            />
            {localOptions.proxy && (
              <button
                onClick={() => handleClearOption('proxy')}
                className="clear-option-button"
                aria-label="Clear proxy URL"
              >
                ×
              </button>
            )}
          </div>
          <div className="option-description">
            Proxy server URL for downloads
          </div>
        </div>

        <div className="option-group">
          <label htmlFor="output-template-input" className="option-label">
            Output Template
          </label>
          <div className="input-group">
            <input
              id="output-template-input"
              type="text"
              value={localOptions.output_template || ''}
              onChange={(e) => handleOptionChange('output_template', e.target.value)}
              placeholder="%(title)s.%(ext)s"
              className="option-input"
            />
            {localOptions.output_template && (
              <button
                onClick={() => handleClearOption('output_template')}
                className="clear-option-button"
                aria-label="Clear output template"
              >
                ×
              </button>
            )}
          </div>
          <div className="option-description">
            Custom filename template (e.g., %(title)s.%(ext)s)
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdvancedOptions