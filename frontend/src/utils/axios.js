import axios from 'axios'
import { useAuthStore } from '../stores/auth.js'

// Configure axios defaults
// Note: baseURL is not set because Vite proxy handles routing to backend

// Request interceptor to add auth header
axios.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.accessToken) {
      config.headers.Authorization = `Bearer ${authStore.accessToken}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle token refresh
axios.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    const authStore = useAuthStore()

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshResult = await authStore.refreshAccessToken()
        if (refreshResult.success) {
          // Retry the original request with new token
          originalRequest.headers.Authorization = `Bearer ${authStore.accessToken}`
          return axios(originalRequest)
        }
      } catch (refreshError) {
        // Refresh failed, logout user
        authStore.logout()
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default axios