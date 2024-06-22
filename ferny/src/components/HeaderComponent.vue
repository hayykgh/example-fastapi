  <!-- src/components/HeaderComponent.vue -->

<template>
  <header class="header" :style="{ backgroundColor: headerColor, border: 'none' }">
    <nav class="navbar">
      <div class="navbar-brand">
        <router-link to="/">
          <img src="../assets/logo.png" alt="Ferny" class="logo" />
        </router-link>
      </div>
      <div class="navbar-menu">
        <router-link v-if="isLoggedIn" to="/account" class="navbar-item">{{ userName }}</router-link>
        <router-link v-if="!isLoggedIn" to="/signin" class="navbar-item">Sign In</router-link>
        <router-link v-if="!isLoggedIn" to="/signup" class="navbar-item">Sign Up</router-link>
        <button v-if="isLoggedIn" @click="logout" class="navbar-item btn-logout">Sign Out</button>
      </div>
    </nav>
  </header> 
</template>

<script>
export default {
  name: "HeaderComponent",
  data() {
    return {
      isLoggedIn: false,
      userEmail: '',
      userName: '', // To store user's full name
      headerColor: '#ebeced' // Set initial header background color
    };
  },
  mounted() {
    this.checkAuthentication();
  },
  watch: {
    '$route': 'checkAuthentication'
  },
  methods: {
    checkAuthentication() {
      const token = localStorage.getItem('token');
      if (token) {
        const decodedToken = JSON.parse(atob(token.split('.')[1]));
        this.isLoggedIn = true;
        this.userEmail = decodedToken.email; // Assuming email is stored in the token
        this.userName = `${decodedToken.first_name} ${decodedToken.last_name}`;
      } else {
        this.isLoggedIn = false;
        this.userEmail = '';
        this.userName = '';
      }
    },
    logout() {
      localStorage.removeItem('token');
      this.isLoggedIn = false;
      this.userEmail = '';
      this.userName = '';
      this.$router.push('/signin'); // Redirect to login page after logout
    }
  }
};
</script>

<style scoped>
/* Integrate Google Font */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

.header {
  padding: 10px 0;
  background-color: #ebeced; /* Light gray background color */
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to header */
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.navbar-brand .logo {
  height: 70px;
}

.navbar-menu {
  display: flex;
  align-items: center;
}

.navbar-item {
  margin: 0 10px;
  color: rgb(20, 33, 39); /* Text color for navbar items */
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to navbar items */
}

.navbar-item:hover {
  color: rgb(91, 159, 143); /* Highlight color on hover */
}

.btn-logout {
  padding: 8px 16px;
  border: none;
  background-color: rgb(14, 100, 75); /* Button background color */
  color: #fff; /* Button text color */
  cursor: pointer;
  border-radius: 20px;
  transition: background-color 0.3s ease;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to logout button */
}

.btn-logout:hover {
  background-color: rgb(91, 159, 143); /* Button background color on hover */
  color: rgb(20, 33, 39);
}
</style>
