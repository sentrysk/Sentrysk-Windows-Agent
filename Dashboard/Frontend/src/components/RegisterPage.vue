<template>
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card mt-5">
            <div class="card-header bg-dark text-white">
              <h1 class="text-center">
                <i class="bi bi-speedometer2"></i> Register
              </h1>
            </div>
            <div class="card-body">
              <form @submit.prevent="register">
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="bi bi-person"></i></span>
                  <input type="text" v-model="name" class="form-control" placeholder="First Name" required />
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="bi bi-person"></i></span>
                  <input type="text" v-model="lastname" class="form-control" placeholder="Last Name" required />
                </div>
                <div class="mb-3 input-group">
                  <span class="input-group-text"><i class="bi bi-envelope"></i></span>
                  <input type="email" v-model="email" class="form-control" placeholder="Email" required />
                </div>
                <div class="mb-4 input-group">
                  <span class="input-group-text"><i class="bi bi-lock"></i></span>
                  <input
                    :type="showPassword ? 'text' : 'password'"
                    v-model="password"
                    class="form-control"
                    placeholder="Password"
                    required
                  />
                  <button type="button" class="btn btn-outline-secondary" @click="togglePasswordVisibility">
                    <i :class="['bi', showPassword ? 'bi-eye-slash' : 'bi-eye']"></i>
                  </button>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Register</button>
              </form>
            </div>
          </div>
        </div>
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
        showPassword: false,
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
          const API_URL = "http://localhost:5000/user/register"
          const response = await axios.post(API_URL, registrationData);
  
          if (response.status === 201) {
            Swal.fire({
              icon: 'success',
              title: 'Registration Successful',
              text: 'You have been registered successfully.',
            });
  
            this.$router.push('/login');
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
      togglePasswordVisibility() {
        this.showPassword = !this.showPassword;
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
  background-color: #343a40; /* Darker background color */
  border: none;
  color: white; /* White text color */
}

.bi {
  font-size: 1.2rem;
  color: #007bff; /* Blue icon color */
}

.btn-outline-secondary {
  background-color: #343a40; /* Darker background color */
  border: none;
  color: white; /* White text color */
}

.btn-outline-secondary:hover {
  background-color: #292e33; /* Slightly darker on hover */
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