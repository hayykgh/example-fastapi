<!--
  src/components/RegisterComponent.vue
  
  Component for user registration form.
-->

<template>
  <div class="register-container">
    <h2>Sign Up</h2>
    <form @submit.prevent="registerUser">
      <div class="input-group">
        <div class="form-group">
          <label for="first_name">First Name:</label>
          <input v-model.trim="form.first_name" type="text" id="first_name" required @blur="validateName('first_name')" />
          <span v-if="!isInitialFirstNameValid && !form.first_name" class="initial-error-message">First Name is required.</span>
          <span v-if="!isInitialFirstNameValid && form.first_name && !isValidName('first_name')" class="error-message">Please enter only letters.</span>
        </div>
        <div class="form-group">
          <label for="last_name">Last Name:</label>
          <input v-model.trim="form.last_name" type="text" id="last_name" required @blur="validateName('last_name')" />
          <span v-if="!isInitialLastNameValid && !form.last_name" class="initial-error-message">Last Name is required.</span>
          <span v-if="!isInitialLastNameValid && form.last_name && !isValidName('last_name')" class="error-message">Please enter only letters.</span>
        </div>
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input v-model.trim="form.email" type="email" id="email" required @blur="validateEmail" />
        <span v-if="!isInitialEmailValid && !form.email" class="initial-error-message">Email is required.</span>
        <span v-if="!isInitialEmailValid && form.email && !isValidEmail" class="error-message">Please enter a valid email address.</span>
        <span v-if="registrationError" class="error-message">{{ registrationError }}</span>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <div class="password-input-container">
          <input v-model="form.password" :type="passwordFieldType" id="password" required @blur="validatePassword" />
          <div class="password-toggle" @mousedown.prevent>
            <i class="fas" :class="passwordFieldType === 'password' ? 'fa-eye-slash' : 'fa-eye'" @click="togglePasswordVisibility"></i>
          </div>
        </div>
        <span v-if="!isInitialPasswordValid && !form.password" class="initial-error-message">Password is required.</span>
        <span v-if="!isInitialPasswordValid && form.password && !isValidPassword" class="error-message">
          Password must be at least 8 characters long, contain at least one uppercase letter, one number, and one special character.
        </span>
      </div>
      <button type="submit" :disabled="!isValidForm" class="signup-button">Sign Up</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        email: '',
        password: '',
        first_name: '',
        last_name: ''
      },
      isInitialEmailValid: true,
      isInitialPasswordValid: true,
      isInitialFirstNameValid: true,
      isInitialLastNameValid: true,
      passwordFieldType: 'password', // Initial type of password input
      registrationError: null // To store registration error message
    };
  },
  computed: {
    isValidEmail() {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailPattern.test(this.form.email);
    },
    isValidPassword() {
      const passwordPattern = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
      return passwordPattern.test(this.form.password);
    },
    isValidForm() {
      return (
        this.isValidEmail &&
        this.isValidPassword &&
        this.isValidName('first_name') &&
        this.isValidName('last_name')
      );
    }
  },
  methods: {
    validateEmail() {
      this.isInitialEmailValid = false;
    },
    validatePassword() {
      this.isInitialPasswordValid = false;
    },
    validateName(field) {
      if (field === 'first_name') {
        this.isInitialFirstNameValid = false;
      } else if (field === 'last_name') {
        this.isInitialLastNameValid = false;
      }
    },
    isValidName(field) {
      const namePattern = /^[A-Za-z]+$/;
      if (field === 'first_name') {
        return namePattern.test(this.form.first_name);
      } else if (field === 'last_name') {
        return namePattern.test(this.form.last_name);
      }
      return false;
    },
    togglePasswordVisibility() {
      this.passwordFieldType =
        this.passwordFieldType === 'password' ? 'text' : 'password';
    },
    async registerUser() {
      if (this.isValidForm) {
        try {
          const response = await axios.post('http://127.0.0.1:8000/users', {
            email: this.form.email,
            password: this.form.password,
            first_name: this.form.first_name,
            last_name: this.form.last_name
          });
          console.log(response.data);
          // Navigate to login page upon successful registration
          this.$router.push('/login');
        } catch (error) {
          if (
            error.response &&
            error.response.status === 400 &&
            error.response.data.detail === 'Email already registered'
          ) {
            this.registrationError =
              'This email is already registered. Please use a different email.';
          } else {
            console.error(error);
            this.registrationError =
              'An error occurred during registration. Please try again later.';
          }
        }
      }
    }
  }
};
</script>

<style scoped>

@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

.register-container {
  max-width: 500px; /* Adjusted max-width for better spacing */
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px; /* Increased border radius for a softer look */
  background-color: #ebeced; /* Light background color */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  font-family: 'Montserrat', sans-serif;  /* Subtle box shadow for depth */
}

h2 {
  text-align: center;
  color: #333; /* Darker text color */
}

form {
  display: flex;
  flex-direction: column;
}

.input-group {
  display: flex;
  gap: 20px; /* Increased gap between first_name and last_name inputs */
}

.form-group {
  flex: 1; /* Allow inputs to grow equally within the form-group */
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #555; /* Slightly darker label color */
}

input {
  width: 100%;
  padding: 12px; /* Increased padding for larger fields */
  box-sizing: border-box;
  border: 1px solid #ddd; /* Light border */
  border-radius: 5px; /* Rounded corners */
  transition: border-color 0.3s ease; /* Smooth border color transition */
}

input:focus {
  outline: none;
  border-color: rgb(14, 100, 75); /* Focus border color */
}

.password-input-container {
  position: relative;
}

.password-toggle {
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  cursor: pointer;
}

.password-toggle i {
  font-size: 1rem;
  
}

.signup-button {
  padding: 14px; /* Increased padding for larger button */
  background-color: rgb(14, 100, 75); /* Button background color */
  color: #fff; /* Button text color */
  cursor: pointer;
  border-radius: 20px;
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease; /* Smooth background color transition */
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to logout button */
  margin-top: 15px; /* Add margin top */
  margin-bottom: 20px; /* Add margin bottom */
}

.signup-button:disabled {
  background-color: #ccc;
  font-family: 'Montserrat', sans-serif; /* Apply Montserrat font to logout button */

}

.signup-button:hover:enabled {
  background-color: rgb(91, 159, 143); /* Button background color on hover */
  color: rgb(20, 33, 39);
  font-family: 'Montserrat', sans-serif;  /* Apply Montserrat font to logout button */

}

.initial-error-message,
.error-message {
  color: #dc3545; /* Error message color */
  font-size: 0.9rem; /* Font size adjustment */
  margin-top: 4px;
}

.error-message {
  display: none; /* Hide error messages by default */
}

.error-message.active {
  display: block; /* Display error message when active */
}
</style>
