import React from 'react'

const FormatSelector = ({ selectedFormat, onFormatChange, disabled }) => {
  const formats = [
    { value: 'video', label: 'Video', description: 'Download full video (MP4)' },
    { value: 'audio_mp3', label: 'Audio (MP3)', description: 'Extract audio as MP3' },
    { value: 'audio_wav', label: 'Audio (WAV)', description: 'Extract audio as WAV' },
    { value: 'metadata', label: 'Metadata', description: 'Download video information only' }
  ]

  const handleFormatChange = (formatValue) => {
    onFormatChange?.(formatValue)
  }

  const handleKeyDown = (e, formatValue) => {
    if (e.key === ' ' || e.key === 'Enter') {
      e.preventDefault()
      handleFormatChange(formatValue)
    }
  }

  return (
    <div className="format-selector" role="radiogroup" aria-label="Download format">
      <fieldset>
        <legend>Download Format</legend>
        {formats.map(format => (
          <div key={format.value} className="format-option">
            <label className="format-label">
              <input
                type="radio"
                name="format"
                value={format.value}
                checked={selectedFormat === format.value}
                onChange={() => handleFormatChange(format.value)}
                onKeyDown={(e) => handleKeyDown(e, format.value)}
                disabled={disabled}
                className="format-radio"
                aria-describedby={`${format.value}-description`}
              />
              <span className="format-text">{format.label}</span>
            </label>
            <div 
              id={`${format.value}-description`}
              className="format-description"
            >
              {format.description}
            </div>
          </div>
        ))}
      </fieldset>
    </div>
  )
}

export default FormatSelector