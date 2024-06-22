<template>
  <div class="create-post">
    <!-- Keep this comment: This is the create post section -->
    <h2>Create Post</h2>
    <form @submit.prevent="createPost">
      <!-- Keep this comment: Form for creating a new post -->
      <div class="form-group">
        <label for="title" class="label">Title:</label>
        <input v-model="form.title" type="text" id="title" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="content" class="label">Content:</label>
        <textarea v-model="form.content" id="content" class="form-control" rows="5" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Create</button>
    </form>
    <Notification v-if="notificationMessage" :message="notificationMessage" :type="notificationType" />
  </div>
</template>

<script>
import axios from 'axios';
import Notification from './NotificationComponent.vue';

export default {
  data() {
    return {
      form: {
        title: '',
        content: ''
      },
      notificationMessage: '', // Notification message for success or error
      notificationType: 'success' // Default notification type is success
    };
  },
  methods: {
    async createPost() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('No token available');
        }

        await axios.post('http://127.0.0.1:8000/posts', this.form, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        this.form.title = '';
        this.form.content = '';

        // Set success notification message
        this.notificationMessage = 'Post created successfully!';
        this.notificationType = 'success';

        // Emit an event to notify the parent component (if needed)
        this.$emit('postCreated');

      } catch (error) {
        console.error('Error creating post:', error);

        // Set error notification message
        this.notificationMessage = 'Error creating post!';
        this.notificationType = 'error';
      }
    }
  },
  components: {
    Notification
  }
};
</script>

<style scoped>
/* Integrate Google Font */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

.create-post {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #ebeced; /* Background color */
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font */
}

h2 {
  text-align: center;
  color: #1a202c; /* Dark text color */
  margin-bottom: 20px;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font */
}

.form-group {
  margin-bottom: 20px;
}

.label {
  font-weight: bold;
  color: #2d3748; /* Darker text color */
  display: block;
  margin-bottom: 5px;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font */
}

.form-control {
  width: calc(100% - 22px); /* Adjust based on your padding and border */
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #cbd5e0; /* Light border color */
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font */
  color: #2d3748; /* Darker text color */
}

textarea.form-control {
  resize: vertical; /* Allow vertical resizing only */
  min-height: 50px;
  max-height: 300px;
  overflow-y: auto;
}

/* Custom scrollbar styles */
textarea.form-control::-webkit-scrollbar {
  width: 6px; /* Width of the scrollbar */
}

textarea.form-control::-webkit-scrollbar-track {
  background: #f1f1f1; /* Background of the scrollbar track */
  border-radius: 10px;
}

textarea.form-control::-webkit-scrollbar-thumb {
  background: rgb(14, 100, 75); /* Scrollbar thumb color */
  border-radius: 10px;
}

textarea.form-control::-webkit-scrollbar-thumb:hover {
  background: rgb(91, 159, 143); /* Scrollbar thumb hover color */
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  text-decoration: none;
  border: none;
  background-color: rgb(14, 100, 75); /* Button background color */
  color: #fff; /* Button text color */
  cursor: pointer;
  border-radius: 20px;
  transition: background-color 0.3s ease;
  font-family: 'Montserrat', sans-serif;
}

input:focus {
  outline: none;
  border-color: rgb(14, 100, 75);
}

.btn:hover {
  background-color: rgb(91, 159, 143); /* Button background color on hover */
  color: rgb(20, 33, 39);
}
</style>
