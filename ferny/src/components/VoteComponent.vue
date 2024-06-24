<template>
  <div class="vote-component">
    <button @click="toggleLike" :class="{ 'liked': liked }" class="like-button">
      <i :class="['heart-icon', liked ? 'fas fa-heart' : 'far fa-heart']"></i>
      <span>{{ likes }}</span>
    </button>
  </div>
</template>

<script>
import axiosInstance from '../axios';

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
      liked: false
    };
  },
  mounted() {
    this.fetchLikedState();
    this.likes = this.initialLikes;
  },
  methods: {
    async fetchLikedState() {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await axiosInstance.get('/vote/', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          const likedPosts = response.data.map(item => item.postid);
          this.liked = likedPosts.includes(this.postId);
        } catch (error) {
          console.error('Error fetching liked posts:', error);
        }
      }
    },
    async toggleLike() {
      try {
        const token = localStorage.getItem('token');
        const response = await axiosInstance.post(
          `vote/${this.postId}`,
          { liked: !this.liked },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );
        this.likes = response.data.likes;
        this.liked = !this.liked;
        this.$emit('update:likes', this.likes);
        this.fetchLikedState(); // Fetch the liked state again to ensure accuracy
      } catch (error) {
        console.error('Error toggling like:', error);
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
