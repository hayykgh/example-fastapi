<template>
  <transition name="fade">
    <div v-if="visible" :class="['notification', type, divClass]">
      <i :class="icon"></i>
      <p>{{ message }}</p>
      <span class="close-btn" @click="dismissNotification">&times;</span>
    </div>
  </transition>
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
  data() {
    return {
      icon: '',
      divClass: '',
      textColor: '',
      visible: false // Initially hidden
    };
  },
  methods: {
    dismissNotification() {
      this.visible = false; // Hide the notification
      this.$emit('dismiss'); // Emit dismiss event to parent
    },
    setNotificationStyles() {
      if (this.type === 'success') {
        this.icon = 'fas fa-check';
        this.divClass = 'success';
        this.textColor = '#64963b';
      } else if (this.type === 'error') {
        this.icon = 'fas fa-times';
        this.divClass = 'error';
        this.textColor = '#963b3b';
      }
    },
    showNotification() {
      this.visible = true; // Show the notification
      setTimeout(() => {
        this.dismissNotification();
      }, 5000); // 5 seconds
    }
  },
  watch: {
    message() {
      this.showNotification();
    },
    type() {
      this.setNotificationStyles();
    }
  },
  mounted() {
    this.setNotificationStyles();
    if (this.message) {
      this.showNotification();
    }
  }
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css');

.notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #f0f4f5; /* Default background color */
  color: white;
  padding: 15px 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  z-index: 1000; /* Ensure it's on top of other content */
  cursor: pointer;
  display: flex;
  align-items: center;
  max-width: 300px; /* Fixed maximum width */
  width: auto; /* Auto width to adjust based on content */
  min-width: 150px; /* Minimum width */
}

.notification.success {
  background-color: #e0f2e9; /* Light green background for success */
}

.notification.error {
  background-color: #f2e0e0; /* Light red background for error */
}

.notification i {
  margin-right: 10px;
  font-size: 20px;
  color: var(--icon-color, #fff); /* Default icon color */
}

.notification.success i {
  --icon-color: #64963b; /* Green icon for success */
}

.notification.error i {
  --icon-color: #963b3b; /* Red icon for error */
}

.notification p {
  margin: 0;
  color: var(--text-color, #fff); /* Default text color */
  flex: 1; /* Take remaining space */
}

.notification.success p {
  --text-color: #64963b; /* Green text for success */
}

.notification.error p {
  --text-color: #963b3b; /* Red text for error */
}

.close-btn {
  position: absolute; /* Position the close button absolutely */
  top: 10px; /* Adjust the top position */
  right: 10px; /* Adjust the right position */
  font-size: 20px;
  cursor: pointer;
  color: var(--icon-color, #fff); /* Default close button color */
}

.close-btn:hover {
  color: #000; /* Change color on hover */
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease-out, transform 0.5s ease-out; /* Animation properties */
}

.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
  transform: translateY(20px); /* Slide down */
}
</style>
