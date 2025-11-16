import { createApp } from 'vue';
import { createPinia } from 'pinia';
import './index.css';
import './utils/axios.js';
import App from './App.vue';
import router from './router.js';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.mount('#root');
