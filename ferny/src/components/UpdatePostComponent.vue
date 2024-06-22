<template>
  <div class="update-post" v-if="post">
    <h2>Update Post</h2>
    <form @submit.prevent="updatePost">
      <div class="form-group">
        <label for="title">Title:</label>
        <input v-model="post.title" type="text" id="title" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="content">Content:</label>
        <textarea v-model="post.content" id="content" class="form-control" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Update</button>
    </form>
    <Notification v-if="notificationMessage" :message="notificationMessage" :type="notificationType" />
  </div>
</template>

<script>
import axios from 'axios';
import Notification from './NotificationComponent.vue';

export default {
  components: {
    Notification,
  },
  data() {
    return {
      post: null,
      notificationMessage: '',
      notificationType: 'success',
    };
  },
  methods: {
    async fetchPost(id) {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/posts/${id}`);
        this.post = response.data.Post;
      } catch (error) {
        console.error('Error fetching post:', error);
      }
    },
    async updatePost() {
      try {
        await axios.put(`http://127.0.0.1:8000/posts/${this.$route.params.id}`, this.post, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.notificationMessage = 'Post updated successfully!';
        this.notificationType = 'success';
        setTimeout(() => {
          this.notificationMessage = '';
          this.$router.push({ name: 'PostFeed' });
        }, 2000);
      } catch (error) {
        console.error('Error updating post:', error);
        this.notificationMessage = 'Error updating post! You are not the owner of this post';
        this.notificationType = 'error';
      }
    },
  },
  async mounted() {
    const postId = this.$route.params.id;
    await this.fetchPost(postId);
  },
};
</script>

<style scoped>
.update-post {
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
  font-family: 'Montserrat', sans-serif;
}

.form-group {
  margin-bottom: 20px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-family: 'Montserrat', sans-serif;
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
