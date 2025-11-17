<template>
  <div id="app">
    <!-- Only show nav if not on auth page -->
    <nav v-if="!isAuthPage">
      <router-link to="/" class="nav-btn">Home</router-link>
      <router-link to="/profile/edit" class="nav-btn">Edit Profile</router-link>
      <button v-if="authStore.isLoggedIn" @click="logout" class="logout-btn">Logout</button>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth.js'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const isAuthPage = computed(() => route.path === '/auth')

onMounted(() => {
  authStore.initializeAuth()
})

const logout = () => {
  authStore.logout()
  router.push('/auth')
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  background: #ffffff;
  padding: 1rem 2rem;
  border-bottom: 1px solid #e1e5e9;
  display: flex;
  justify-content: flex-end;
  gap: 1.5rem;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  position: relative;
}

.nav-btn {
  color: #495057;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  background-color: #ffffff;
  transition: all 0.2s ease;
  font-weight: 500;
  display: inline-block;
}

.nav-btn:hover {
  background-color: #f8f9fa;
  border-color: #adb5bd;
  color: #212529;
}

.nav-btn.router-link-exact-active {
  background-color: #007bff;
  border-color: #007bff;
  color: white;
}

.logout-btn {
  background: #dc3545;
  color: white;
  border: 1px solid #dc3545;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: #c82333;
  border-color: #bd2130;
}
</style>