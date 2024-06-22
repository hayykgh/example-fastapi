<template>
  <!-- Create Post Component -->
  <div class="create-post-container">
    <CreatePostComponent @postCreated="handlePostCreated" />
  </div>

  <div class="post-feed">
    <NotificationComponent v-if="notificationMessage" :message="notificationMessage" :type="notificationType" />

    <h2>Post Feed</h2>

    <!-- Post List -->
    <div v-for="(post, index) in posts" :key="post.Post.id" class="post-item">
      <!-- Show post owner's name if available -->
      <div v-if="post.Post.owner" class="post-owner-info">
        <span class="owner-name">{{ post.Post.owner.first_name }} {{ post.Post.owner.last_name }}</span>
      </div>

      <!-- Show dropdown menu only if user is owner -->
      <div v-if="isOwner(post.Post.owner.id)" class="dropdown">
        <button class="dropbtn" @click="toggleDropdown(index)">...</button>
        <div class="dropdown-content" v-if="post.showDropdown">
          <a @click="updatePost(post.Post.id)">Update</a>
          <a @click="deletePost(post.Post.id)">Delete</a>
        </div>
      </div>

      <div class="post-header">
        <h3>{{ post.Post.title }}</h3>
      </div>
      <div class="post-content">
        <p>{{ post.Post.content }}</p>
      </div>
      <div class="post-actions">
        <VoteComponent
          :postId="post.Post.id"
          :initialLikes="post.votes"
          :initialLiked="post.liked"
          @update:likes="updateLikes(index, $event)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import CreatePostComponent from './CreatePostComponent.vue';
import VoteComponent from './VoteComponent.vue';
import NotificationComponent from './NotificationComponent.vue';

export default {
  components: {
    CreatePostComponent,
    VoteComponent,
    NotificationComponent
  },
  data() {
    return {
      posts: [],
      notificationMessage: '',
      notificationType: '',
      userId: null // Add userId data property to store current user's id
    };
  },
  methods: {
    async fetchPosts() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/posts');
        this.posts = response.data.map(post => ({
          ...post,
          showDropdown: false,
          liked: localStorage.getItem(`liked_${post.Post.id}`) === 'true'
        }));
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    },
    async updatePost(id) {
      this.$router.push({ name: 'UpdatePost', params: { id } });
    },
    async deletePost(id) {
      const token = localStorage.getItem('token');
      try {
        await axios.delete(`http://127.0.0.1:8000/posts/${id}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.fetchPosts();
        this.showNotification('Post deleted successfully!', 'success');
      } catch (error) {
        console.error('Error deleting post:', error);
        this.showNotification('Error deleting post!', 'error');
      }
    },
    toggleDropdown(index) {
      this.posts = this.posts.map((post, i) => ({
        ...post,
        showDropdown: i === index ? !post.showDropdown : false
      }));
    },
    startAutoRefresh() {
      this.intervalId = setInterval(() => {
        this.fetchPosts();
      }, 600000); // Refresh every 60 seconds (adjust as needed)
    },
    stopAutoRefresh() {
      clearInterval(this.intervalId);
    },
    showNotification(message, type) {
      this.notificationMessage = message;
      this.notificationType = type;
    },
    updateLikes(index, newLikes) {
      // Update the likes count for the post at the specified index
      this.posts[index].votes = newLikes;
    },
    handlePostCreated() {
      this.fetchPosts();
    },
    isOwner(ownerId) {
      return this.userId === ownerId;
    }
  },
  mounted() {
    this.fetchPosts();
    this.startAutoRefresh();
    const token = localStorage.getItem('token');
    // Retrieve and store current user's id from token
    if (token) {
      const payload = JSON.parse(atob(token.split('.')[1]));
      this.userId = payload.user_id;
    }
  },
  beforeUnmount() {
    this.stopAutoRefresh();
  }
};
</script>

<style scoped>
/* Add this style block to change the background color of the page */
:root {
  --page-background-color: #e0f7fa; /* Light cyan background color */
}

body {
  background-color: #7dddc7; /* Use the defined background color */
  margin: 0;
  color: #7dddc7;
  font-family: 'Montserrat', sans-serif;

}

/* Your existing styles */
.post-feed {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #ffffff; /* White background */
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: rgb(20, 33, 39); /* Text color */
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to logout button */
  margin-bottom: 20px;
}

.create-post-container {
  margin-bottom: 20px;
}

.post-item {
  position: relative;
  background-color: #f9f9f9; /* Light gray background */
  border: 1px solid #ccc;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.dropdown {
  position: absolute;
  top: 10px; /* Adjust as needed */
  right: 10px; /* Adjust as needed */
}

button.dropbtn {
  background-color: transparent;
  color: #333;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.dropdown-content {
  position: absolute;
  right: 0;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  background-color: rgb(14, 100, 75); /* Button background color */
  color: #fff; /* Button text color */
  cursor: pointer;
  border-radius: 20px;
  transition: background-color 0.3s ease;
  z-index: 1;
  border-radius: 5px;
  display: none;
}

.dropdown:hover .dropdown-content {
  display: block;
}

.dropdown-content a {
  color: #333;
  padding: 12px 16px;
  text-decoration: none;
  color: #fff;
  display: block;
  border-bottom: 1px solid #f1f1f1;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to logout button */
}

.dropdown-content a:hover {
  background-color: rgb(91, 159, 143); /* Button background color on hover */
  color: rgb(20, 33, 39);
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to logout button */
}

.dropdown-content a:last-child {
  border-bottom: none;
}

.post-content {
  color: #666; /* Text color */
}

.post-owner-info .owner-name {
  color: rgb(14, 100, 75); /* Owner name color */
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to owner name */
  font-weight: bold;
}

.post-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.votes {
  margin-top: 10px;
  color: #666; /* Text color */
}

.vote-component {
  margin-left: 10px;
}
</style>
