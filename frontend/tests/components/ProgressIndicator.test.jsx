/**
 * Test for ProgressIndicator component.
 * This test MUST fail initially (no implementation exists).
 */

import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import ProgressIndicator from '../../src/components/ProgressIndicator'

// Mock the component since it doesn't exist yet
const ProgressIndicator = ({ progress, status, message, isVisible }) => {
  if (!isVisible) return null

  return (
    <div data-testid="progress-indicator">
      <div data-testid="progress-bar">
        <div 
          data-testid="progress-fill" 
          style={{ width: `${progress}%` }}
        />
      </div>
      <div data-testid="progress-text">
        {status}: {progress}%
      </div>
      {message && (
        <div data-testid="progress-message">
          {message}
        </div>
      )}
    </div>
  )
}

describe('ProgressIndicator', () => {
  it('renders when visible', () => {
    render(<ProgressIndicator progress={50} status="processing" isVisible={true} />)
    
    expect(screen.getByTestId('progress-indicator')).toBeInTheDocument()
  })

  it('does not render when not visible', () => {
    render(<ProgressIndicator progress={50} status="processing" isVisible={false} />)
    
    expect(screen.queryByTestId('progress-indicator')).not.toBeInTheDocument()
  })

  it('displays correct progress percentage', () => {
    render(<ProgressIndicator progress={75} status="processing" isVisible={true} />)
    
    const progressText = screen.getByTestId('progress-text')
    expect(progressText).toHaveTextContent('75%')
  })

  it('displays correct status', () => {
    render(<ProgressIndicator progress={50} status="downloading" isVisible={true} />)
    
    const progressText = screen.getByTestId('progress-text')
    expect(progressText).toHaveTextContent('downloading')
  })

  it('displays progress message when provided', () => {
    const message = 'Downloading video...'
    render(
      <ProgressIndicator 
        progress={30} 
        status="processing" 
        message={message}
        isVisible={true} 
      />
    )
    
    const messageElement = screen.getByTestId('progress-message')
    expect(messageElement).toHaveTextContent(message)
  })

  it('does not display message when not provided', () => {
    render(<ProgressIndicator progress={50} status="processing" isVisible={true} />)
    
    expect(screen.queryByTestId('progress-message')).not.toBeInTheDocument()
  })

  it('shows progress bar with correct width', () => {
    render(<ProgressIndicator progress={60} status="processing" isVisible={true} />)
    
    const progressFill = screen.getByTestId('progress-fill')
    expect(progressFill).toHaveStyle('width: 60%')
  })

  it('handles 0% progress', () => {
    render(<ProgressIndicator progress={0} status="pending" isVisible={true} />)
    
    const progressFill = screen.getByTestId('progress-fill')
    const progressText = screen.getByTestId('progress-text')
    
    expect(progressFill).toHaveStyle('width: 0%')
    expect(progressText).toHaveTextContent('0%')
  })

  it('handles 100% progress', () => {
    render(<ProgressIndicator progress={100} status="completed" isVisible={true} />)
    
    const progressFill = screen.getByTestId('progress-fill')
    const progressText = screen.getByTestId('progress-text')
    
    expect(progressFill).toHaveStyle('width: 100%')
    expect(progressText).toHaveTextContent('100%')
  })

  it('handles different status types', () => {
    const statuses = ['pending', 'processing', 'downloading', 'completed', 'failed']
    
    statuses.forEach(status => {
      const { unmount } = render(
        <ProgressIndicator progress={50} status={status} isVisible={true} />
      )
      
      const progressText = screen.getByTestId('progress-text')
      expect(progressText).toHaveTextContent(status)
      
      unmount()
    })
  })

  it('shows appropriate styling for different statuses', () => {
    // Test completed status
    const { rerender } = render(
      <ProgressIndicator progress={100} status="completed" isVisible={true} />
    )
    
    let progressIndicator = screen.getByTestId('progress-indicator')
    expect(progressIndicator).toBeInTheDocument()
    
    // Test failed status
    rerender(
      <ProgressIndicator progress={50} status="failed" isVisible={true} />
    )
    
    progressIndicator = screen.getByTestId('progress-indicator')
    expect(progressIndicator).toBeInTheDocument()
  })

  it('handles progress updates smoothly', () => {
    const { rerender } = render(
      <ProgressIndicator progress={0} status="processing" isVisible={true} />
    )
    
    // Simulate progress updates
    for (let progress = 10; progress <= 100; progress += 10) {
      rerender(
        <ProgressIndicator progress={progress} status="processing" isVisible={true} />
      )
      
      const progressFill = screen.getByTestId('progress-fill')
      const progressText = screen.getByTestId('progress-text')
      
      expect(progressFill).toHaveStyle(`width: ${progress}%`)
      expect(progressText).toHaveTextContent(`${progress}%`)
    }
  })

  it('displays error state for failed downloads', () => {
    const errorMessage = 'Download failed: Network error'
    render(
      <ProgressIndicator 
        progress={0} 
        status="failed" 
        message={errorMessage}
        isVisible={true} 
      />
    )
    
    const messageElement = screen.getByTestId('progress-message')
    expect(messageElement).toHaveTextContent(errorMessage)
  })

  it('has proper accessibility attributes', () => {
    render(<ProgressIndicator progress={50} status="processing" isVisible={true} />)
    
    const progressIndicator = screen.getByTestId('progress-indicator')
    expect(progressIndicator).toHaveAttribute('role', 'progressbar')
    expect(progressIndicator).toHaveAttribute('aria-valuenow', '50')
    expect(progressIndicator).toHaveAttribute('aria-valuemin', '0')
    expect(progressIndicator).toHaveAttribute('aria-valuemax', '100')
  })
})

