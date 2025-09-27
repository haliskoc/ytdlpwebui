class SSEService {
  constructor() {
    this.eventSource = null
    this.listeners = new Map()
  }

  // Connect to Server-Sent Events stream
  connect(url, onMessage, onError, onOpen) {
    if (this.eventSource) {
      this.disconnect()
    }

    this.eventSource = new EventSource(url)

    this.eventSource.onopen = (event) => {
      console.log('SSE connection opened:', event)
      onOpen?.(event)
    }

    this.eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        console.log('SSE message received:', data)
        onMessage?.(data)
      } catch (error) {
        console.error('Error parsing SSE message:', error)
        onError?.(error)
      }
    }

    this.eventSource.onerror = (event) => {
      console.error('SSE connection error:', event)
      // Check if it's a connection error or server error
      if (event.target.readyState === EventSource.CLOSED) {
        console.log('SSE connection closed')
        onError?.(new Error('Connection closed'))
      } else {
        onError?.(new Error('Connection error'))
      }
    }

    return this.eventSource
  }

  // Disconnect from SSE stream
  disconnect() {
    if (this.eventSource) {
      this.eventSource.close()
      this.eventSource = null
    }
  }

  // Check if connected
  isConnected() {
    return this.eventSource && this.eventSource.readyState === EventSource.OPEN
  }

  // Get connection state
  getReadyState() {
    if (!this.eventSource) return EventSource.CLOSED
    return this.eventSource.readyState
  }

  // Add event listener
  addEventListener(type, listener) {
    if (this.eventSource) {
      this.eventSource.addEventListener(type, listener)
    }
  }

  // Remove event listener
  removeEventListener(type, listener) {
    if (this.eventSource) {
      this.eventSource.removeEventListener(type, listener)
    }
  }
}

// Create singleton instance
const sseService = new SSEService()

export default sseService