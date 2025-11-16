import { createRouter, createWebHistory } from 'vue-router'
import Home from './Home.vue'
import ProfileEdit from './ProfileEdit.vue'
import Login from './Login.vue'

const routes = [
  { path: '/', redirect: '/auth' },
  { path: '/auth', component: Login },
  { path: '/home', component: Home },
  { path: '/profile/edit', component: ProfileEdit }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
