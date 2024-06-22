<!-- src/components/SessionExpiredModal.vue -->


<template>
    <div v-if="isVisible" class="modal">
      <h2>Session Expired</h2>
      <p>Your session has expired. Please log in again.</p>
      <button @click="redirectToLogin">Log In</button>
    </div>
  </template>
  
  <script>
  import { defineComponent, ref, onMounted } from 'vue';
  import eventBus from '../eventBus'; // Ensure this path is correct
  
  export default defineComponent({
    setup() {
      const isVisible = ref(false);
  
      // Listen for the session-expired event
      const handleSessionExpired = () => {
        console.log('Session expired event received');
        isVisible.value = true;
      };
  
      onMounted(() => {
        eventBus.on('session-expired', handleSessionExpired);
      });
  
      const redirectToLogin = () => {
        window.location.href = '/login';
      };
  
      return {
        isVisible,
        redirectToLogin,
      };
    },
  });
  </script>
  
  <style scoped>
  .modal {
    color: blue;
    /* Additional styles to ensure visibility */
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    z-index: 1000;
  }
  </style>
  