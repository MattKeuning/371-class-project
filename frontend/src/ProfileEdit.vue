<template>
  <div class="profile-container">
    <h2>Edit Profile</h2>

    <div v-if="error" class="error-message">{{ error }}</div>

    <form @submit.prevent="saveProfile" class="profile-form">
       <div class="form-group">
         <label for="name">Name:</label>
         <input id="name" v-model="profile.name" type="text" />
       </div>

       <div class="form-group">
         <label for="email">Email:</label>
         <input id="email" v-model="profile.email" type="email" readonly />
       </div>

       <div class="form-group">
         <label for="age">Age:</label>
         <input id="age" v-model.number="profile.age" type="number" />
       </div>

      <button type="submit" :disabled="loading" class="save-btn">
        {{ loading ? 'Saving...' : 'Save' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from './stores/auth.js'
import axios from './utils/axios.js'

const authStore = useAuthStore()

const profile = reactive({
  name: '',
  email: '',
  age: null
})

const loading = ref(false)
const error = ref('')

const loadProfile = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await axios.get('/api/auth/profiles/me/')
    profile.name = response.data.name || ''
    profile.email = response.data.email || ''
    profile.age = response.data.age || null
  } catch (error) {
    console.error('Error loading profile:', error)
    if (error.response?.status === 401) {
      // Token might be expired, try to refresh
      const refreshResult = await authStore.refreshAccessToken()
      if (refreshResult.success) {
        // Retry the request
        try {
          const response = await axios.get('/api/auth/profiles/me/')
          profile.name = response.data.name || ''
          profile.email = response.data.email || ''
          profile.age = response.data.age || null
        } catch (retryError) {
          error.value = 'Failed to load profile'
        }
      } else {
        error.value = 'Session expired. Please log in again.'
      }
    } else {
      error.value = 'Failed to load profile'
    }
  } finally {
    loading.value = false
  }
}

const saveProfile = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await axios.put('/api/auth/profiles/me/', profile)
    alert('Profile updated successfully')
    await loadProfile() // Refresh the profile data
  } catch (error) {
    console.error('Error saving profile:', error)
    if (error.response?.status === 401) {
      const refreshResult = await authStore.refreshAccessToken()
      if (refreshResult.success) {
        // Retry the request
        try {
          await axios.put('/api/auth/profiles/me/', profile)
          alert('Profile updated successfully')
          await loadProfile() // Refresh the profile data
        } catch (retryError) {
          error.value = 'Failed to update profile'
        }
      } else {
        error.value = 'Session expired. Please log in again.'
      }
    } else {
      error.value = error.response?.data?.error || 'Failed to update profile'
    }
  } finally {
    loading.value = false
  }
}

onMounted(loadProfile)
</script>

<style scoped>
.profile-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.profile-form {
  margin-top: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.save-btn {
  width: 100%;
  padding: 10px;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.save-btn:hover {
  background-color: #369870;
}

.save-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  background-color: #faddd7;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
}
</style>