// src/main.js
import { createApp } from 'vue';
import AppComponent from './AppComponent.vue';
import router from './router';

// Import FontAwesome
import '@fortawesome/fontawesome-free/css/all.css';

// Import Global CSS
import '../global.css'; // Add this line

// Create a Vue application instance
const app = createApp(AppComponent);

// Use the router with the app instance
app.use(router);

// Mount the app to the DOM
app.mount('#app');
