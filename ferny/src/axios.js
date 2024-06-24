// src/axios.js

import axios from 'axios';
import eventBus from './eventBus'; // Import the event bus
const apiHost = process.env.VUE_APP_API_HOST;

const axiosInstance = axios.create({
  baseURL: apiHost,
  headers: {
    'Content-Type': 'application/json'
  }
});

axiosInstance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error.response && error.response.status === 401) {
      console.error('Session expired. Emitting event...');
      eventBus.emit('session-expired'); // Emit session-expired event
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;