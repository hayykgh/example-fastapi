<template>
  <div class="login-view">
    <LoginComponent />
  </div>
</template>

<script>
import LoginComponent from '../components/LoginComponent.vue';

export default {
  name: 'LoginView',
  components: {
    LoginComponent,
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>