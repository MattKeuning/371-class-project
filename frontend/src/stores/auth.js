import { defineStore } from 'pinia'
import axios from '../utils/axios.js'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: null,
    refreshToken: null,
    isAuthenticated: false
  }),

  getters: {
    isLoggedIn: (state) => state.isAuthenticated && !!state.accessToken
  },

  actions: {
    async login(credentials) {
      try {
        const response = await axios.post('/api/auth/login/', credentials)
        const { access, refresh, user } = response.data

        this.accessToken = access
        this.refreshToken = refresh
        this.user = user
        this.isAuthenticated = true

        // Store tokens in localStorage
        localStorage.setItem('accessToken', access)
        localStorage.setItem('refreshToken', refresh)
        localStorage.setItem('user', JSON.stringify(user))

        // Set axios default header
        axios.defaults.headers.common['Authorization'] = `Bearer ${access}`

        return { success: true }
      } catch (error) {
        console.error('Login failed:', error)
        return {
          success: false,
          error: error.response?.data?.detail || 'Login failed'
        }
      }
    },

    async register(userData) {
      try {
        const response = await axios.post('/api/auth/register/', userData)
        return { success: true, data: response.data }
      } catch (error) {
        console.error('Registration failed:', error)
        return {
          success: false,
          error: error.response?.data?.error || 'Registration failed'
        }
      }
    },

    async refreshAccessToken() {
      try {
        const refreshToken = this.refreshToken || localStorage.getItem('refreshToken')
        if (!refreshToken) {
          throw new Error('No refresh token available')
        }

        const response = await axios.post('/api/auth/refresh/', {
          refresh: refreshToken
        })

        const { access } = response.data
        this.accessToken = access
        localStorage.setItem('accessToken', access)
        axios.defaults.headers.common['Authorization'] = `Bearer ${access}`

        return { success: true }
      } catch (error) {
        console.error('Token refresh failed:', error)
        this.logout()
        return { success: false, error: 'Session expired' }
      }
    },

    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      this.isAuthenticated = false

      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('user')

      delete axios.defaults.headers.common['Authorization']
    },

    initializeAuth() {
      const accessToken = localStorage.getItem('accessToken')
      const refreshToken = localStorage.getItem('refreshToken')
      const user = localStorage.getItem('user')

      if (accessToken && refreshToken && user) {
        this.accessToken = accessToken
        this.refreshToken = refreshToken
        this.user = JSON.parse(user)
        this.isAuthenticated = true
        axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
      }
    }
  }
})