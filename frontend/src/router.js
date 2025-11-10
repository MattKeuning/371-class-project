import { createRouter, createWebHistory } from 'vue-router'
import Home from './Home.vue'
import ProfileEdit from './ProfileEdit.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/profile/edit', component: ProfileEdit }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router