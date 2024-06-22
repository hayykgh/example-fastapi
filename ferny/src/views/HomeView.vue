<!-- src/views/Home.vue -->
<template>
  <div class="home">
    <PostFeed />
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import PostFeed from '../components/PostFeed.vue'; // Adjust path if necessary

export default defineComponent({
  components: {
    PostFeed,
  },
});
</script>

<style scoped>
/* Your component styles */
</style>