<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin" class="login-form">
      <div v-if="error" class="error-message">{{ error }}</div>

      <div class="form-group">
        <label for="username">Username:</label>
        <input id="username" v-model="username" required />
      </div>

      <div class="form-group">
        <label for="password">Password:</label>
        <input id="password" v-model="password" type="password" required />
      </div>

      <button type="submit" :disabled="loading" class="login-btn">
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>
    </form>

    <div class="register-link">
      <p>Don't have an account? <button @click="showRegister = !showRegister" class="link-btn">
        {{ showRegister ? 'Back to Login' : 'Register' }}
      </button></p>
    </div>

    <form v-if="showRegister" @submit.prevent="handleRegister" class="register-form">
      <h3>Register</h3>
      <div v-if="registerError" class="error-message">{{ registerError }}</div>
      <div v-if="registerSuccess" class="success-message">{{ registerSuccess }}</div>

      <div class="form-group">
        <label for="regUsername">Username:</label>
        <input id="regUsername" v-model="regUsername" required />
      </div>

      <div class="form-group">
        <label for="regEmail">Email:</label>
        <input id="regEmail" v-model="regEmail" type="email" />
      </div>

      <div class="form-group">
        <label for="regPassword">Password:</label>
        <input id="regPassword" v-model="regPassword" type="password" required />
      </div>

      <button type="submit" :disabled="registerLoading" class="register-btn">
        {{ registerLoading ? 'Registering...' : 'Register' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from './stores/auth.js'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const showRegister = ref(false)
const regUsername = ref('')
const regEmail = ref('')
const regPassword = ref('')
const registerLoading = ref(false)
const registerError = ref('')
const registerSuccess = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  const result = await authStore.login({
    username: username.value,
    password: password.value
  })

  loading.value = false

  if (result.success) {
    router.push('/home')
  } else {
    error.value = result.error
  }
}

const handleRegister = async () => {
  registerLoading.value = true
  registerError.value = ''
  registerSuccess.value = ''

  const result = await authStore.register({
    username: regUsername.value,
    email: regEmail.value,
    password: regPassword.value
  })

  registerLoading.value = false

  if (result.success) {
    registerSuccess.value = 'Registration successful! You can now log in.'
    regUsername.value = ''
    regEmail.value = ''
    regPassword.value = ''
    showRegister.value = false
  } else {
    registerError.value = result.error
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.login-form, .register-form {
  margin-bottom: 20px;
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

.login-btn, .register-btn {
  width: 100%;
  padding: 10px;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.login-btn:hover, .register-btn:hover {
  background-color: #369870;
}

.login-btn:disabled, .register-btn:disabled {
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

.success-message {
  color: #27ae60;
  background-color: #d5f4e6;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
}

.register-link {
  text-align: center;
  margin: 20px 0;
}

.link-btn {
  background: none;
  border: none;
  color: #42b883;
  cursor: pointer;
  text-decoration: underline;
}

.link-btn:hover {
  color: #369870;
}
</style>