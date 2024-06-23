<template>
  <div id="app">
    <HeaderComponent />
    <router-view @add-notification="handleNotification"></router-view>
    <SessionExpiredModal />
    <NotificationComponent
      v-if="notification.type && notification.message"
      :type="notification.type"
      :message="notification.message"
      @close="clearNotification"
    />
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue';
import HeaderComponent from './components/HeaderComponent.vue';
import SessionExpiredModal from './components/SessionExpiredModal.vue';
import NotificationComponent from './components/NotificationComponent.vue';

export default defineComponent({
  components: {
    HeaderComponent,
    SessionExpiredModal,
    NotificationComponent
  },
  setup() {
    const notification = ref({
      type: '',
      message: ''
    });

    const handleNotification = (notificationData) => {
      notification.value.type = notificationData.type;
      notification.value.message = notificationData.message;
    };

    const clearNotification = () => {
      notification.value.type = '';
      notification.value.message = '';
    };

    return {
      notification,
      handleNotification,
      clearNotification
    };
  }
});
</script>

<style>
/* Global styles for AppComponent.vue */
</style>
