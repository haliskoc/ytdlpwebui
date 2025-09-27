import { useEffect, useRef } from 'react'
import { apiService } from '../services/api'

/**
 * Hook to track user activity and update server-side activity timestamp
 * This helps with idle monitoring to prevent automatic shutdown
 */
export const useActivityTracker = (intervalMs = 30000) => { // 30 seconds
  const intervalRef = useRef(null)

  useEffect(() => {
    // Function to update activity
    const updateActivity = async () => {
      try {
        await apiService.updateActivity()
      } catch (error) {
        // Silently fail to avoid disrupting user experience
        console.debug('Activity update failed:', error.message)
      }
    }

    // Update activity immediately when component mounts
    updateActivity()

    // Set up interval to update activity periodically
    intervalRef.current = setInterval(updateActivity, intervalMs)

    // Update activity on user interactions
    const handleUserActivity = () => {
      updateActivity()
    }

    // Listen for various user activities
    const events = [
      'mousedown',
      'mousemove',
      'keypress',
      'scroll',
      'touchstart',
      'click'
    ]

    // Add event listeners
    events.forEach(event => {
      document.addEventListener(event, handleUserActivity, true)
    })

    // Cleanup function
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
      
      // Remove event listeners
      events.forEach(event => {
        document.removeEventListener(event, handleUserActivity, true)
      })
    }
  }, [intervalMs])

  return null // This hook doesn't return anything
}
