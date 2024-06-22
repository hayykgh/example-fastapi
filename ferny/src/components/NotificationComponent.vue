<!-- src/components/NotificationComponent.vue -->

<template>
  <div v-if="message" class="notification" :class="type" @click="dismissNotification">
    <p>{{ message }}</p>
  </div>
</template>

<script>
export default {
  props: {
    message: String,
    type: {
      type: String,
      default: 'success' // Default type is success
    }
  },
  methods: {
    dismissNotification() {
      this.$emit('dismiss');
    }
  },
  mounted() {
    // Automatically dismiss the notification after 5 seconds
    setTimeout(() => {
      this.dismissNotification();
    }, 5000); // Adjust the time as needed
  }
};
</script>

<style scoped>
.notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #4CAF50;
  color: white;
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  z-index: 1000; /* Ensure it's on top of other content */
  transition: transform 0.3s ease-out;
  cursor: pointer;
}

.notification.error {
  background-color: #f44336;
}
</style>