<template>
  <div class="post-details" v-if="post">
    <h2>{{ post.Post.title }}</h2>
    <p>{{ post.Post.content }}</p>
    <p><strong>Votes: </strong>{{ post.votes }}</p>
    <button @click="vote(post.Post.id)">Vote</button>
    <button @click="editPost(post.Post.id)">Edit</button>
  </div>
  <div v-else>
    <p>Loading...</p>
  </div>
</template>

<script>
import axiosInstance from '../axios'; // Assuming you have an axios instance configured with baseURL

export default {
  data() {
    return {
      post: null,
    };
  },
  methods: {
    async fetchPost(id) {
      try {
        const response = await axiosInstance.get(`/posts/${id}`);
        this.post = response.data;
      } catch (error) {
        console.error('Error fetching post:', error);
        // Optionally handle error display or retry logic
      }
    },
    async vote(id) {
      try {
        await axiosInstance.post(`/vote/${id}`);
        await this.fetchPost(id); // Fetch updated post after voting
      } catch (error) {
        console.error('Error voting:', error);
        // Optionally handle error display or retry logic
      }
    },
    editPost(id) {
      this.$router.push({ name: 'UpdatePost', params: { id } });
    },
  },
  mounted() {
    const postId = this.$route.params.id;
    this.fetchPost(postId);
  },
};
</script>

<style scoped>
.post-details {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}
</style>
