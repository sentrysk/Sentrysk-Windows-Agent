<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card mt-5 shadow">
          <div class="card-header bg-dark text-white">
            <h1 class="text-center">
              Login
            </h1>
          </div>
          <div class="card-body">
            <form @submit.prevent="login">
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
              <button type="submit" class="btn btn-primary btn-block">Login</button>
            </form>
            <!-- Add registration link here -->
            <div class="text-center mt-3">
              <router-link to="/register">Don't have an account? Register here.</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
  import axios from "axios";
  import Swal from "sweetalert2"; // Import SweetAlert2

  
  export default {
    data() {
      return {
        email: "",
        password: "",
      };
    },
    methods: {
      async login() {
        try {
          const API_URL = "http://localhost:5000/user/login"
          const response = await axios.post(API_URL, {
            email: this.email,
            password: this.password,
          });

          // Assuming the API responds with a JWT token
          const token = response.data.token;
  
          // Store the token in a session variable
          sessionStorage.setItem("jwtToken", token);
  
          // Set the session expiration time based on the JWT token's expiration
          const jwtPayload = JSON.parse(atob(token.split(".")[1]));
          const expirationTime = new Date(jwtPayload.exp * 1000);
          sessionStorage.setItem("tokenExpiration", expirationTime);
          
          // Show a success message with SweetAlert
          Swal.fire({
            icon: "success",
            title: "Success!",
            text: "Login successful.",
          });

          // Redirect to another page or perform other actions as needed
          // For example, you can use Vue Router to navigate to a different page
          this.$router.push("/");
        } catch (error) {
          console.error("Login failed:", error);
          // Handle login error, show an error message, etc.
          // Show an error message with SweetAlert
          Swal.fire({
            icon: "error",
            title: "Error!",
            text: "Login failed. Please check your credentials.",
          });
        }
      },
    },
  };
</script>
  
<style scoped>
.shadow {
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
  font-size: 1.5rem;
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