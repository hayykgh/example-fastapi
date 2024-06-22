<!-- src/components/PostDetailsComponent.vue -->

<template>
    <div class="post-details" v-if="post">
      <h2>{{ post.Post.title }}</h2>
      <p>{{ post.Post.content }}</p>
      <p><strong>Votes: </strong>{{ post.votes }}</p>
      <button @click="vote(post.Post.id)">Vote</button>
      <button @click="editPost(post.Post.id)">Edit</button>
    </div>
  </template>

  <script>
  import axios from 'axios';

  export default {
    data() {
      return {
        post: null,
      };
    },
    methods: {
      async fetchPost(id) {
        const response = await axios.get(`http://127.0.0.1:8000/posts/${id}`);
        this.post = response.data;
      },
      async vote(id) {
        await axios.post(`http://127.0.0.1:8000/vote/${id}`);
        this.fetchPost(id);
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