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
