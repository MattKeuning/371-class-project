import { createApp } from 'vue';
import { createPinia } from 'pinia';
import './index.css';
import axios from './utils/axios.js';
import App from './App.vue';
import router from './router.js';

// Set axios baseURL at runtime for production
axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.mount('#root');
