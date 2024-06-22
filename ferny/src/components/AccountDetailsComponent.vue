<template>
  <div class="account-details">
    <h1>Account Details</h1>
    <span @click="openReauthModal" class="edit-icon"></span>
    <div class="user-info" :class="{ 'disabled': !isEditable }">
      <div class="info-item">
        <label class="label" style="color: rgb(14, 100, 75);">Email:</label>
        <div class="info-content">
          <div v-if="!isEditable" class="info-text" style="color: rgb(14, 100, 75);">{{ userEmail }}</div>
          <input v-else type="text" v-model="newEmail" class="input" />
          <button v-if="isEditable" @click="saveEmailChanges" class="btn-check">
            <img :src="require('@/assets/checkmark.png')" alt="Save Email">
          </button>
        </div>
      </div>
      <div class="info-item">
        <label class="label" style="color: rgb(14, 100, 75);">First Name:</label>
        <div class="info-content">
          <div v-if="!isEditable" class="info-text" style="color: rgb(14, 100, 75);">{{ firstName }}</div>
          <input v-else type="text" v-model="newFirstName" class="input" />
          <button v-if="isEditable" @click="saveFirstNameChanges" class="btn-check">
            <img :src="require('@/assets/checkmark.png')" alt="Save First Name">
          </button>
        </div>
      </div>
      <div class="info-item">
        <label class="label" style="color: rgb(14, 100, 75);">Last Name:</label>
        <div class="info-content">
          <div v-if="!isEditable" class="info-text" style="color: rgb(14, 100, 75);">{{ lastName }}</div>
          <input v-else type="text" v-model="newLastName" class="input" />
          <button v-if="isEditable" @click="saveLastNameChanges" class="btn-check">
            <img :src="require('@/assets/checkmark.png')" alt="Save Last Name">
          </button>
        </div>
      </div>
      <div class="info-item" v-if="showNewPassword">
        <label class="label" style="color: rgb(14, 100, 75);">New Password:</label>
        <input type="password" v-model="newPassword" class="input" :disabled="!isEditable" />
        <button v-if="isEditable" @click="savePasswordChange" class="btn-check">
          <img :src="require('@/assets/checkmark.png')" alt="Save Password">
        </button>
      </div>
    </div>

    <div v-if="successMessage" class="notification success">
      <p>Data was changed successfully!</p>
    </div>

    <div v-if="showReauthModal" class="modal">
      <div class="modal-content smaller">
        <span class="close" @click="closeReauthModal">&times;</span> <!-- Close button moved here -->
        <h2>Re-authenticate</h2>
        <input type="password"
               v-model="reauthPassword"
               placeholder="Enter your password"
               class="input"
               @keyup.enter="reauthenticate" />
        <button @click="reauthenticate" class="btn-save">Submit</button>
        <p v-if="reauthError" class="error-msg">{{ reauthError }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from '../axios'; // Adjust the path as needed

export default {
  name: "AccountDetails",
  data() {
    return {
      userEmail: "hayykgh@gmail.com",
      firstName: "Hayk",
      lastName: "Ghazaryan",
      newPassword: "",
      newEmail: "",
      newFirstName: "",
      newLastName: "",
      successMessage: false,
      isEditable: false,
      showReauthModal: false,
      showNewPassword: false,
      reauthPassword: "",
      reauthError: "" // Initialize reauthError for error handling
    };
  },
  mounted() {
    this.getUserDetails();
  },
  methods: {
    getUserDetails() {
      const token = localStorage.getItem("token");
      if (token) {
        const decodedToken = JSON.parse(atob(token.split(".")[1]));
        this.userEmail = decodedToken.user_email;
        this.firstName = decodedToken.first_name;
        this.lastName = decodedToken.last_name;
      }
    },
    openReauthModal() {
      this.showReauthModal = true;
    },
    closeReauthModal() {
      this.showReauthModal = false;
      this.reauthPassword = "";
      this.reauthError = ""; // Reset reauthError when closing modal
    },
    async reauthenticate() {
      const token = localStorage.getItem("token");
      if (!token) {
        alert("Token not found. Please login again.");
        return;
      }

      const decodedToken = JSON.parse(atob(token.split(".")[1]));
      const username = decodedToken.user_email; // Assuming user_email is the username
      const password = this.reauthPassword;

      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      try {
        const response = await axiosInstance.post('/login', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        if (response.status === 200){
          this.isEditable = true;
          this.showNewPassword = true;
          this.closeReauthModal();
        }
      } catch (error) {
        console.error("Re-authentication failed:", error);
        this.reauthError = "Incorrect password. Please try again."; // Set error message
      }
    },
    async saveEmailChanges() {
      await this.saveFieldChanges('email', this.newEmail);
    },
    async saveFirstNameChanges() {
      await this.saveFieldChanges('first_name', this.newFirstName);
    },
    async saveLastNameChanges() {
      await this.saveFieldChanges('last_name', this.newLastName);
    },
    async savePasswordChange() {
      await this.saveFieldChanges('password', this.newPassword);
    },
    async saveFieldChanges(field, value) {
      const token = localStorage.getItem("token");
      if (token && this.isEditable) {
        const updatedData = {
          [field]: value
        };

        try {
          const response = await axiosInstance.patch('/users', updatedData);
          
          if (response.status === 200) {
            localStorage.setItem("token", response.data.access_token);
            this.successMessage = true;
            setTimeout(() => {
              this.successMessage = false;
            }, 5000);
          }
        } catch (error) {
          console.error(`Error updating ${field}:`, error);
          alert(`An error occurred while updating ${field}.`);
        }
      }
    }
  }
};
</script>

<style scoped>
.account-details {
  max-width: 500px;
  margin: 50px auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  position: relative;
}

.account-details h1 {
  font-size: 2.5em;
  color: #333;
  margin-bottom: 20px;
}

.edit-icon {
  width: 24px;
  height: 24px;
  cursor: pointer;
  display: inline-block;
  background-image: url('@/assets/edit-icon.png');
  background-size: cover;
  position: absolute;
  top: 20px;
  right: 20px;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* Align items to the left */
}

.user-info.disabled .input {
  background-color: #f0f0f0;
  cursor: not-allowed;
}

.info-item {
  width: 100%;
  padding: 10px 0;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #ddd;
  margin-bottom: 10px;
}

.label {
  font-weight: bold;
  color: #555;
  margin-right: 10px;
  flex: 1;
  text-align: right;
}

.info-content {
  display: flex;
  align-items: center;
  justify-content: flex-start; /* Align content to the left */
  flex: 2; /* Adjust flex basis */
}

.info-text {
  font-size: 1.2em;
  color: rgb(14, 100, 75); /* Changed to green */
  margin-left: 10px;
}

.input {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: rgb(14, 100, 75); /* Changed to green */
}

.btn-check {
  border: none;
  background-color: transparent;
  cursor: pointer;
  margin-left: 10px;
}

.btn-check img {
  width: 24px;
  height: 24px;
}

.notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #4caf50;
  color: white;
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  transition: transform 0.3s ease-out;
}

.notification p {
  margin: 0;
}

.notification.success {
  background-color: #4caf50;
}

.modal {
  display: block; /* Hidden by default */
  position: fixed;
  z-index: 1000; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgba(0, 0, 0, 0.6); /* Black w/ opacity */
  padding-top: 60px;
}

.modal-content {
  background-color: #fefefe;
  margin: 10% auto; /* Centered vertically and closer to top */
  padding: 30px;
  border-radius: 10px;
  width: 40%; /* Adjusted width */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.modal-content h2 {
  font-size: 1.8em;
  color: #333;
  margin-bottom: 20px;
}

.modal-content .close {
  color: #aaa;
  font-size: 28px;
  font-weight: bold;
  position: absolute;
  top: 20px;
  right: 30px;
  cursor: pointer;
}

.modal-content .close:hover,
.modal-content .close:focus {
  color: black;
  text-decoration: none;
}

.btn-save {
  background-color: rgb(14, 100, 75);
  color: white;
  padding: 14px 20px;
  border: none;
  cursor: pointer;
  border-radius: 20px;
  font-weight: bold;
  transition: background-color 0.3s;
}

.btn-save:hover {
  background-color: rgb(91, 159, 143);
}

.error-msg {
  color: #f44336;
  margin-top: 10px;
}
</style>
