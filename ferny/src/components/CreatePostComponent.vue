<template>
  <div class="create-post">
    <h2>Create Post</h2>
    <form @submit.prevent="createPost">
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
import axiosInstance from '../axios'; // Import axiosInstance from src/axios.js
import Notification from './NotificationComponent.vue';

export default {
  data() {
    return {
      form: {
        title: '',
        content: ''
      },
      notificationMessage: '',
      notificationType: 'success'
    };
  },
  methods: {
    async createPost() {
      try {
        await axiosInstance.post('/posts/', this.form);

        this.form.title = '';
        this.form.content = '';

        this.notificationMessage = 'Post created successfully!';
        this.notificationType = 'success';

        this.$emit('postCreated');
      } catch (error) {
        console.error('Error creating post:', error);

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
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

.create-post {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #ebeced;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  font-family: 'Montserrat', sans-serif;
}

h2 {
  text-align: center;
  color: #1a202c;
  margin-bottom: 20px;
  font-family: 'Montserrat', sans-serif;
}

.form-group {
  margin-bottom: 20px;
}

.label {
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 5px;
  font-family: 'Montserrat', sans-serif;
}

.form-control {
  width: calc(100% - 22px);
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #cbd5e0;
  font-family: 'Montserrat', sans-serif;
  color: #2d3748;
}

textarea.form-control {
  resize: vertical;
  min-height: 50px;
  max-height: 300px;
  overflow-y: auto;
}

/* Custom scrollbar styles */
textarea.form-control::-webkit-scrollbar {
  width: 6px;
}

textarea.form-control::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

textarea.form-control::-webkit-scrollbar-thumb {
  background: rgb(14, 100, 75);
  border-radius: 10px;
}

textarea.form-control::-webkit-scrollbar-thumb:hover {
  background: rgb(91, 159, 143);
}

input:focus,
textarea:focus {
  outline: none;
  border-color: rgb(14, 100, 75);
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  text-decoration: none;
  border: none;
  background-color: rgb(14, 100, 75);
  color: #fff;
  cursor: pointer;
  border-radius: 20px;
  transition: background-color 0.3s ease;
  font-family: 'Montserrat', sans-serif;
}

.btn:hover {
  background-color: rgb(91, 159, 143);
  color: rgb(20, 33, 39);
}
</style>
