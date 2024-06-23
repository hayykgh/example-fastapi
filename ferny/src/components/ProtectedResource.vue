
<!-- src/components/ProtectResource.vue -->

<template>
    <div>
      <h1>Protected Resource</h1>
      <p>{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axiosInstance from '../axios'; // Use the custom axios instance
  
  export default {
    name: 'ProtectedResource',
    data() {
      return {
        message: ''
      };
    },
    async created() {
      try {
        const response = await axiosInstance.get('/protected-resource');
        this.message = response.data.message;
      } catch (err) {
        this.message = 'Error fetching protected resource';
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add your styles here */
  </style>
  