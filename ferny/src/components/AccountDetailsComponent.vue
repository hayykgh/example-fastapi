<template>
  <div class="account-details">
    <h1>Account Details</h1>
    <span v-if="!isEditable" @click="openReauthModal" class="edit-icon"></span>
    <span v-if="isEditable" @click="refreshPage" class="refresh-icon"></span>
    <div class="user-info" :class="{ 'disabled': !isEditable }">
      <div class="info-item">
        <label class="label">Email:</label>
        <div class="info-content">
          <div v-if="!isEditable" class="info-text">{{ userEmail }}</div>
          <input v-else type="text" v-model="newEmail" class="input email-input" />
          <button v-if="isEditable" @click="saveEmailChanges" class="btn-check">
            <img src="@/assets/checkmark.png" alt="Save Email">
          </button>
        </div>
      </div>
      <div class="info-item">
        <label class="label">First Name:</label>
        <div class="info-content">
          <div v-if="!isEditable" class="info-text">{{ firstName }}</div>
          <input v-else type="text" v-model="newFirstName" class="input name-input" />
          <button v-if="isEditable" @click="saveFirstNameChanges" class="btn-check">
            <img src="@/assets/checkmark.png" alt="Save First Name">
          </button>
        </div>
      </div>
      <div class="info-item">
        <label class="label">Last Name:</label>
        <div class="info-content">
          <div v-if="!isEditable" class="info-text">{{ lastName }}</div>
          <input v-else type="text" v-model="newLastName" class="input name-input" />
          <button v-if="isEditable" @click="saveLastNameChanges" class="btn-check">
            <img src="@/assets/checkmark.png" alt="Save Last Name">
          </button>
        </div>
      </div>
      <div class="info-item" v-if="showNewPassword">
        <label class="label">New Password:</label>
        <input type="password" v-model="newPassword" class="input" :class="{ 'long-input': showNewPassword }" :disabled="!isEditable" />
        <button v-if="isEditable" @click="savePasswordChange" class="btn-check">
          <img src="@/assets/checkmark.png" alt="Save Password">
        </button>
      </div>
      <div class="info-item">
        <button v-if="isEditable" @click="confirmDeleteAccount" class="btn-delete">Delete Account</button>
      </div>
    </div>

    <!-- Success Notification -->
    <div v-if="successMessage" class="notification success">
      <p>{{ successMessage }}</p>
    </div>

    <!-- Error Notification -->
    <div v-if="errorMessage" class="notification error">
      <p>{{ errorMessage }}</p>
    </div>

    <!-- Reauth Modal -->
    <div v-if="showReauthModal" class="modal">
      <div class="modal-content smaller">
        <span class="close" @click="closeReauthModal">&times;</span>
        <h2>Re-authenticate</h2>
        <p class="modal-text">Please enter your password to continue.</p>
        <input type="password"
              v-model="reauthPassword"
              placeholder="Enter your password"
              class="input"
              @keyup.enter="reauthenticate" />
        <p v-if="reauthError" class="error-msg">{{ reauthError }}</p>
        <button @click="reauthenticate" class="btn-save">Submit</button>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirmation" class="modal">
      <div class="modal-content smaller">
        <span class="close" @click="cancelDelete">&times;</span>
        <h2>Confirm Account Deletion</h2>
        <p class="modal-text">Are you sure you want to delete your account?</p>
        <div class="modal-buttons">
          <button @click="deleteAccount" class="btn-delete-confirm">Confirm Delete</button>
          <button @click="cancelDelete" class="btn-cancel">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from '../axios'; // Adjust the path as needed
import router from '../router'; // Assuming you have a router instance
import messages from '@/assets/en-US.json'; // Import messages from JSON file

export default {
  name: "AccountDetails",
  data() {
    return {
      userEmail: '',
      firstName: '',
      lastName: '',
      newPassword: "",
      newEmail: "",
      newFirstName: "",
      newLastName: "",
      successMessage: "",
      errorMessage: "",
      isEditable: false,
      showReauthModal: false,
      showNewPassword: false,
      reauthPassword: "",
      reauthError: "",
      showDeleteConfirmation: false // Track whether to show delete confirmation
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
        this.newEmail = this.userEmail;
        this.newFirstName = this.firstName;
        this.newLastName = this.lastName;
      }
    },
    openReauthModal() {
      this.showReauthModal = true;
    },
    closeReauthModal() {
      this.showReauthModal = false;
      this.reauthPassword = "";
      this.reauthError = "";
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
        if (response.status === 200) {
          this.isEditable = true;
          this.showNewPassword = true;
          this.closeReauthModal();
        }
      } catch (error) {
        console.error("Re-authentication failed:", error);
        this.reauthError = "Incorrect password. Please try again.";
      }
    },
    async saveEmailChanges() {
      await this.saveFieldChanges('user_email', this.newEmail, 'userUpdatedEmail');
    },
    async saveFirstNameChanges() {
      await this.saveFieldChanges('first_name', this.newFirstName, 'userUpdatedFirstName');
    },
    async saveLastNameChanges() {
      await this.saveFieldChanges('last_name', this.newLastName, 'userUpdatedLastName');
    },
    async savePasswordChange() {
      await this.saveFieldChanges('password', this.newPassword, 'userUpdatedPassword');
    },
    async saveFieldChanges(field, value, successMessageKey) {
      const token = localStorage.getItem("token");
      if (token && this.isEditable) {
        const updatedData = {
          [field]: value
        };

        try {
          const response = await axiosInstance.patch('/users', updatedData);

          if (response.status === 200) {
            localStorage.setItem("token", response.data.access_token);
            this.successMessage = messages.success[successMessageKey];
            this.addNotification({
              type: 'success',
              message: this.successMessage
            });
            setTimeout(() => {
              this.successMessage = "";
            }, 5000);
          }
        } catch (error) {
          console.error(`Error updating ${field}:`, error);
          this.errorMessage = messages.error.userUpdateFailed;
          this.addNotification({
            type: 'error',
            message: this.errorMessage
          });
        }
      }
    },
    refreshPage() {
      window.location.reload();
    },
    confirmDeleteAccount() {
      // Show delete confirmation modal
      this.showDeleteConfirmation = true;
    },
    cancelDelete() {
      // Cancel delete action
      this.showDeleteConfirmation = false;
    },
    async deleteAccount() {
      const token = localStorage.getItem("token");
      if (token && this.isEditable) {
        const decodedToken = JSON.parse(atob(token.split(".")[1]));
        const userId = decodedToken.user_id; // Assuming user_id is part of the token

        try {
          const response = await axiosInstance.delete(`/users/${userId}`);

          if (response.status === 204) {
            // Account deleted successfully
            localStorage.removeItem("token");
            router.push('/signup'); // Redirect to signup page
          }
        } catch (error) {
          console.error("Error deleting account:", error);
          this.errorMessage = messages.error.userDeleteFailed;
          this.addNotification({
            type: 'error',
            message: this.errorMessage
          });
        }
      }
    },
    addNotification(notification) {
      this.$emit('add-notification', notification);
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

.edit-icon,
.refresh-icon {
  width: 24px;
  height: 24px;
  cursor: pointer;
  display: inline-block;
  background-size: cover;
  position: absolute;
  top: 20px;
  right: 20px;
}

.edit-icon {
  background-image: url('@/assets/edit-icon.png');
}

.refresh-icon {
  background-image: url('@/assets/refresh-icon.png');
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
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
  justify-content: flex-start;
  flex: 3;
}

.info-text {
  font-size: 1.2em;
  color: rgb(14, 100, 75);
  margin-left: 10px;
}

.input {
  width: 100%;
  min-width: 200px;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.input:focus {
  outline: none;
  border-color: rgb(14, 100, 75);
}

.long-input {
  width: 100%;
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

.btn-delete {
  background-color: #f44336;
  color: white;
  padding: 12px 20px;
  margin: 10px 0;
  border: none;
  cursor: pointer;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  transition: background-color 0.3s;
}

.btn-delete:hover {
  background-color: #d32f2f;
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

.notification.error {
  background-color: #f44336;
}

.modal {
  display: block;
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.6);
  padding-top: 60px;
}

.modal-content {
  background-color: #fefefe;
  margin: 10% auto;
  padding: 30px;
  border-radius: 10px;
  width: 40%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  position: relative;
}

.modal-content h2 {
  font-size: 1.8em;
  color: #333;
}

.modal-content .modal-text {
  font-size: 1em;
  color: #333;
  margin-bottom: 10px;
}

.modal-content .close {
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
  margin-top: 20px;
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
  margin-top: 5px;
  font-size: 0.9em;
}

.modal-buttons {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.btn-delete-confirm,
.btn-cancel {
  padding: 10px 20px;
  margin-right: 10px;
  border: none;
  cursor: pointer;
  border-radius: 4px;
  font-weight: bold;
  transition: background-color 0.3s;
}

.btn-delete-confirm {
  background-color: #f44336;
  color: white;
}

.btn-delete-confirm:hover {
  background-color: #d32f2f;
}

.btn-cancel {
  background-color: #ddd;
  color: #333;
}

.btn-cancel:hover {
  background-color: #bbb;
}
</style>
