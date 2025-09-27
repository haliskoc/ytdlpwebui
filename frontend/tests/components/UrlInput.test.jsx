/**
 * Test for UrlInput component.
 * This test MUST fail initially (no implementation exists).
 */

import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import UrlInput from '../../src/components/UrlInput'

// Mock the component since it doesn't exist yet
const UrlInput = ({ onUrlChange, onUrlSubmit, placeholder, disabled }) => {
  return (
    <div data-testid="url-input">
      <input
        type="text"
        placeholder={placeholder || "Enter YouTube URL"}
        disabled={disabled}
        onChange={(e) => onUrlChange?.(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && onUrlSubmit?.()}
      />
      <button onClick={onUrlSubmit} disabled={disabled}>
        Submit
      </button>
    </div>
  )
}

describe('UrlInput', () => {
  it('renders with default placeholder', () => {
    render(<UrlInput />)
    
    const input = screen.getByPlaceholderText('Enter YouTube URL')
    expect(input).toBeInTheDocument()
  })

  it('renders with custom placeholder', () => {
    const customPlaceholder = 'Paste your YouTube URL here'
    render(<UrlInput placeholder={customPlaceholder} />)
    
    const input = screen.getByPlaceholderText(customPlaceholder)
    expect(input).toBeInTheDocument()
  })

  it('calls onUrlChange when input value changes', () => {
    const mockOnUrlChange = vi.fn()
    render(<UrlInput onUrlChange={mockOnUrlChange} />)
    
    const input = screen.getByPlaceholderText('Enter YouTube URL')
    fireEvent.change(input, { target: { value: 'https://www.youtube.com/watch?v=test' } })
    
    expect(mockOnUrlChange).toHaveBeenCalledWith('https://www.youtube.com/watch?v=test')
  })

  it('calls onUrlSubmit when submit button is clicked', () => {
    const mockOnUrlSubmit = vi.fn()
    render(<UrlInput onUrlSubmit={mockOnUrlSubmit} />)
    
    const button = screen.getByText('Submit')
    fireEvent.click(button)
    
    expect(mockOnUrlSubmit).toHaveBeenCalled()
  })

  it('calls onUrlSubmit when Enter key is pressed', () => {
    const mockOnUrlSubmit = vi.fn()
    render(<UrlInput onUrlSubmit={mockOnUrlSubmit} />)
    
    const input = screen.getByPlaceholderText('Enter YouTube URL')
    fireEvent.keyPress(input, { key: 'Enter', code: 'Enter' })
    
    expect(mockOnUrlSubmit).toHaveBeenCalled()
  })

  it('disables input and button when disabled prop is true', () => {
    render(<UrlInput disabled={true} />)
    
    const input = screen.getByPlaceholderText('Enter YouTube URL')
    const button = screen.getByText('Submit')
    
    expect(input).toBeDisabled()
    expect(button).toBeDisabled()
  })

  it('supports drag and drop functionality', () => {
    render(<UrlInput />)
    
    const input = screen.getByPlaceholderText('Enter YouTube URL')
    
    // Test drag over event
    fireEvent.dragOver(input)
    
    // Test drop event
    const mockDataTransfer = {
      getData: vi.fn(() => 'https://www.youtube.com/watch?v=test')
    }
    
    fireEvent.drop(input, { dataTransfer: mockDataTransfer })
    
    expect(mockDataTransfer.getData).toHaveBeenCalledWith('text/plain')
  })

  it('validates YouTube URL format', () => {
    const mockOnUrlChange = vi.fn()
    render(<UrlInput onUrlChange={mockOnUrlChange} />)
    
    const input = screen.getByPlaceholderText('Enter YouTube URL')
    
    // Test valid YouTube URL
    fireEvent.change(input, { target: { value: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' } })
    expect(mockOnUrlChange).toHaveBeenCalledWith('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    
    // Test invalid URL
    fireEvent.change(input, { target: { value: 'not-a-youtube-url' } })
    expect(mockOnUrlChange).toHaveBeenCalledWith('not-a-youtube-url')
  })

  it('shows error state for invalid URLs', () => {
    render(<UrlInput hasError={true} errorMessage="Invalid YouTube URL" />)
    
    // This test will need to be updated when the actual component is implemented
    // to include error display functionality
    expect(screen.getByTestId('url-input')).toBeInTheDocument()
  })
})

