import React from 'react'
import DownloadPage from './pages/DownloadPage'
import { useActivityTracker } from './hooks/useActivityTracker'
import './App.css'

function App() {
  // Track user activity to prevent idle shutdown
  useActivityTracker()

  return (
    <div className="App">
      <DownloadPage />
    </div>
  )
}

export default App