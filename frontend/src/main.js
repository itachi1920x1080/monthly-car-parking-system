import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router' // ថែមការទាញយក router នេះ

// ភ្ជាប់ router ទៅនឹងកម្មវិធី
createApp(App).use(router).mount('#app')
