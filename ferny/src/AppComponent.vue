<template>
  <div id="app">
    <HeaderComponent />
    <router-view></router-view>
    <SessionExpiredModal />
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import HeaderComponent from './components/HeaderComponent.vue'; // Adjust the path if necessary
import SessionExpiredModal from './components/SessionExpiredModal.vue'; // Adjust the path if necessary

export default defineComponent({
  components: {
    HeaderComponent,
    SessionExpiredModal
  }
});
</script>

<style>
/* Your global styles for App.vue */
</style>
