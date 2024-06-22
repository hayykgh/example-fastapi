<!-- src/components/Test401Component.vue -->

<template>
    <div>
      <h1>Test 401 Error</h1>
      <button @click="test401Error">Trigger 401 Error</button>
    </div>
  </template>
  
  <script>
  import axiosInstance from '../axios';
  import eventBus from '../eventBus';
  
  export default {
    methods: {
      test401Error() {
        axiosInstance.get('/some-protected-endpoint')
          .catch(error => {
            if (error.response && error.response.status === 401) {
              console.log('Manually triggered 401 error');
              eventBus.emit('session-expired');
            }
          });
      }
    },
    mounted() {
      // Optionally, trigger the error when the component mounts
      // this.test401Error();
    }
  };
  </script>
  
  <style scoped>
  /* Your component styles */
  </style>
  