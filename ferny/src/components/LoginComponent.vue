<!-- src/components/LoginComponent.vue -->
<template>
  <div class="login-container">
    <h2>Sign In</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required @input="validateEmail" />
        <span v-if="!isValidEmail && isEmailTouched" class="error-message">Please enter a valid email address.</span>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <div class="password-input-container">
          <input
            :type="passwordFieldType"
            id="password"
            v-model="password"
            required
            @input="validatePassword"
            :class="{ 'error': !isValidPassword && isPasswordTouched }"
          />
          <span class="toggle-password" @click="togglePasswordVisibility">
            <i :class="passwordFieldType === 'password' ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
          </span>
        </div>
        <span v-if="!isValidPassword && isPasswordTouched" class="error-message">Your password must have at least 8 characters.</span>
      </div>
      <button type="submit" :disabled="!isValidForm" class="signin-button">Sign In</button>
      <p v-if="error" class="error-message">{{ error }}</p>
    </form>
    <div class="signup-link">
      <router-link to="/signup" class="signup-link-text">Don't have an account yet? Create one</router-link>
    </div>
  </div>
</template>

<script>
import axios from '../axios'; // Assuming you have a custom axios instance

export default {
  name: 'LoginComponent',
  data() {
    return {
      email: '',
      password: '',
      error: null,
      isEmailTouched: false,
      isPasswordTouched: false,
      passwordFieldType: 'password' // Initial type of password input
    };
  },
  computed: {
    isValidEmail() {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return this.isEmailTouched ? emailPattern.test(this.email) : true;
    },
    isValidPassword() {
      const passwordPattern = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
      return this.isPasswordTouched ? passwordPattern.test(this.password) : true;
    },
    isValidForm() {
      return this.isEmailTouched && this.isPasswordTouched && this.isValidEmail && this.isValidPassword;
    }
  },
  methods: {
    validateEmail() {
      this.isEmailTouched = true;
    },
    validatePassword() {
      this.isPasswordTouched = true;
    },
    togglePasswordVisibility() {
      this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password';
    },
    async login() {
      try {
        const formData = new FormData();
        formData.append('username', this.email);
        formData.append('password', this.password);

        const response = await axios.post('/login', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        localStorage.setItem('token', response.data.access_token);
        this.$router.push('/');
      } catch (err) {
        this.error = 'Invalid email or password';
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 500px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #ebeced;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  font-family: 'Montserrat', sans-serif;
}

h2 {
  text-align: center;
  color: #333;
}

form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #555;
}

input {
  width: 100%;
  padding: 12px;
  box-sizing: border-box;
  border: 1px solid #ddd;
  border-radius: 5px;
  transition: border-color 0.3s ease;
}

input:focus {
  outline: none;
  border-color: rgb(14, 100, 75);
}

.password-input-container {
  position: relative;
}

.password-input-container input {
  padding-right: 30px;
}

.toggle-password {
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  cursor: pointer;
  color: #666;
}

.signin-button {
  padding: 14px;
  background-color: rgb(14, 100, 75);
  color: #fff;
  border: none;
  font-weight: bold;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-family: 'Montserrat', sans-serif;
  margin-top: 15px;
  margin-bottom: 20px;
}

.signin-button:disabled {
  background-color: #ccc;
}

.signin-button:hover:enabled {
  background-color: rgb(91, 159, 143);
  color: rgb(20, 33, 39);

}

.error-message {
  color: #dc3545;
  font-size: 0.9rem;
  margin-top: 4px;
  text-align: center;
}

.signup-link {
  text-align: center; /* Center-align the contents */
}

.signup-link-text {
  color: rgb(14, 100, 75);
  text-decoration: none;
  cursor: pointer;
}
</style>

