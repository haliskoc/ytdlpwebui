import axios from 'axios'

const API_BASE_URL = '/api'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// API functions
export const apiService = {
  // Get video metadata
  async getMetadata(url) {
    try {
      const response = await api.post('/metadata', { url })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get metadata')
    }
  },

  // Start download
  async startDownload(downloadRequest) {
    try {
      const response = await api.post('/download', downloadRequest)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to start download')
    }
  },

  // Get download status
  async getStatus(jobId) {
    try {
      const response = await api.get(`/status/${jobId}`)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get status')
    }
  },

  // Download file
  async downloadFile(jobId) {
    try {
      const response = await api.get(`/download/${jobId}`, {
        responseType: 'blob',
      })
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      
      // Get filename from Content-Disposition header
      const contentDisposition = response.headers['content-disposition']
      let filename = `download_${jobId}`
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="(.+)"/)
        if (filenameMatch) {
          filename = filenameMatch[1]
        }
      }
      
      link.setAttribute('download', filename)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      
      return { success: true, filename }
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to download file')
    }
  },

  // Get progress stream URL
  getProgressStreamUrl(jobId) {
    return `${API_BASE_URL}/progress/${jobId}`
  },

  // Health check
  async healthCheck() {
    try {
      const response = await api.get('/health')
      return response.data
    } catch (error) {
      throw new Error('Health check failed')
    }
  },

  // Update activity for idle monitoring
  async updateActivity() {
    try {
      const response = await api.post('/activity')
      return response.data
    } catch (error) {
      // Don't throw error for activity updates to avoid disrupting user experience
      console.warn('Activity update failed:', error.message)
      return null
    }
  },
}

export default apiService