import { createRouter, createWebHistory } from 'vue-router'
import Home from './Home.vue'
import ProfileEdit from './ProfileEdit.vue'
import Login from './Login.vue'
import { useAuthStore } from './stores/auth.js'

const routes = [
  { path: '/', redirect: '/auth' },
  { path: '/auth', component: Login, meta: { requiresAuth: false } },
  { path: '/home', component: Home, meta: { requiresAuth: true } },
  { path: '/profile/edit', component: ProfileEdit, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    // Redirect to login if trying to access protected route without authentication
    next('/auth')
  } else if (to.path === '/auth' && authStore.isLoggedIn) {
    // Redirect to home if trying to access login while already authenticated
    next('/home')
  } else {
    next()
  }
})

export default router
