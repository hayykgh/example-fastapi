<!-- src/components/VoteComponent.vue -->

<template>
  <div class="vote-component">
    <button @click="toggleLike" :class="{ 'liked': liked }" class="like-button">
      <i :class="['heart-icon', liked ? 'fas fa-heart' : 'far fa-heart']"></i>
      <span>{{ likes }}</span>
    </button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    postId: Number,
    initialLikes: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      likes: this.initialLikes,
      liked: false // Initialize liked state
    };
  },
  mounted() {
    this.likes = this.initialLikes;
    this.loadLikedState(); // Load liked state from localStorage
  },
  methods: {
    loadLikedState() {
      // Load liked state from localStorage
      const likedState = localStorage.getItem(`liked_${this.postId}`);
      this.liked = likedState === 'true';
    },
    async toggleLike() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.post(
          `http://127.0.0.1:8000/vote/${this.postId}`,
          { liked: !this.liked },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        // Update local state based on response from server
        this.likes = response.data.likes;
        this.liked = !this.liked;

        // Save liked state to localStorage
        localStorage.setItem(`liked_${this.postId}`, this.liked.toString());

        // Emit event to notify parent component of updated likes count
        this.$emit('update:likes', this.likes);
      } catch (error) {
        console.error('Error toggling like:', error);
        // Handle error (optional): show message to user, etc.
      }
    }
  }
};
</script>


<style scoped>
.like-button {
  display: flex;
  align-items: center;
  background-color: transparent;
  border: none;
  cursor: pointer;
  outline: none;
}

.heart-icon {
  font-size: 24px;
  margin-right: 5px;
}

.fas.fa-heart {
  color: #f44336; /* Filled heart color */
}

.far.fa-heart {
  color: #aaa; /* Outline heart color */
}

.like-button span {
  font-size: 14px;
  color: #333;
  margin-left: 5px;
}

.like-button:hover .fas.fa-heart {
  color: #d32f2f; /* Filled heart color on hover */
}

.like-button:hover .far.fa-heart {
  color: #666; /* Outline heart color on hover */
}
</style>
