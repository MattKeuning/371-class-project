import { createRouter, createWebHistory } from 'vue-router'
import Home from './Home.vue'
import ProfileEdit from './ProfileEdit.vue'
import Auth from './Auth.vue'

const routes = [
  { path: '/', redirect: '/auth' },
  { path: '/auth', component: Auth },
  { path: '/profile/edit', component: ProfileEdit }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router