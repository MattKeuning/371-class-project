import { createApp } from 'vue';
import { createPinia } from 'pinia';
import './index.css';
import axios from './utils/axios.js';
import App from './App.vue';
import router from './router.js';

// Set axios baseURL for production
axios.defaults.baseURL = 'https://backend-production-8306.up.railway.app';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.mount('#root');
