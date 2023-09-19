<template>
    <div class="registration-container">
      <div class="registration-box">
        <h1 class="text-center mb-4">Register</h1>
        <form @submit.prevent="register">
          <div class="input-group mb-3">
            <span class="input-group-text"><i class="bi bi-person"></i></span>
            <input type="text" v-model="name" class="form-control" placeholder="First Name" required />
          </div>
          <div class="input-group mb-3">
            <span class="input-group-text"><i class="bi bi-person"></i></span>
            <input type="text" v-model="lastname" class="form-control" placeholder="Last Name" required />
          </div>
          <div class="input-group mb-3">
            <span class="input-group-text"><i class="bi bi-envelope"></i></span>
            <input type="email" v-model="email" class="form-control" placeholder="Email" required />
          </div>
          <div class="input-group mb-4">
            <span class="input-group-text"><i class="bi bi-lock"></i></span>
            <input type="password" v-model="password" class="form-control" placeholder="Password" required />
          </div>
          <button type="submit" class="btn btn-primary btn-block">Register</button>
        </form>
      </div>
    </div>
</template>
  
<script>
  import axios from 'axios';
  import Swal from 'sweetalert2';
  
  export default {
    data() {
      return {
        name: '',
        lastname: '',
        email: '',
        password: '',
      };
    },
    methods: {
      async register() {
        const registrationData = {
          name: this.name,
          lastname: this.lastname,
          email: this.email,
          password: this.password,
        };
  
        try {
          // Send a POST request to the registration endpoint
          const response = await axios.post('http://localhost:5000/user/register', registrationData);
  
          // Check if registration was successful
          if (response.status === 201) {
            // Show a success message with SweetAlert2
            Swal.fire({
              icon: 'success',
              title: 'Registration Successful',
              text: 'You have been registered successfully.',
            });
  
            // Redirect to the login page
            this.$router.push('/login'); // Make sure to define the login route
          }
        } catch (error) {
          // Handle registration error (e.g., show an error message)
          Swal.fire({
            icon: 'error',
            title: 'Registration Failed',
            text: 'An error occurred during registration. Please try again later.',
          });
  
          console.error('Registration failed:', error);
        }
      },
    },
  };
</script>
  
<style scoped>
.registration-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.registration-box {
  max-width: 400px;
  width: 100%;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.2);
}

.input-group {
  margin-bottom: 15px;
}

.input-group-text {
  background-color: #f8f9fa;
}

.bi {
  font-size: 1.2rem;
}

.btn-primary {
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  padding: 10px;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.text-center {
  text-align: center;
}

.mb-4 {
  margin-bottom: 1.5rem;
}
</style>