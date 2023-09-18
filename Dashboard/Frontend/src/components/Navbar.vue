<template>
    <nav class="navbar">
    <div class="navbar-brand">
      <router-link to="/">Home</router-link>
    </div>
    <div class="navbar-menu">
      <div class="navbar-end">
        <div class="navbar-item">
          <button @click="logout">Logout</button>
        </div>
      </div>
    </div>
  </nav>
  </template>
  
<script>
  import axios from "axios";
  import Swal from "sweetalert2";
  
  export default {
    // ... Your other component options
  
    methods: {
      async logout() {
        // Get the JWT token from sessionStorage
        const jwtToken = sessionStorage.getItem("jwtToken");
  
        if (jwtToken) {
          try {
            const API_URL = "http://localhost:5000/user/logout"
            // Send a POST request to the logout endpoint with Authorization header
            await axios.post(API_URL, null, {
              headers: {
                Authorization: jwtToken,
              },
            });
  
            // Clear the JWT token and session expiration from sessionStorage
            sessionStorage.removeItem("jwtToken");
            sessionStorage.removeItem("tokenExpiration");
  
            // Show a logout success message with SweetAlert
            Swal.fire({
              icon: "success",
              title: "Logged out",
              text: "You have been successfully logged out.",
            });
  
            // Redirect to the login page
            this.$router.push("/login"); // You can change "/login" to the actual login route
          } catch (error) {
            console.error("Logout failed:", error);
  
            // Handle logout error and show an error message with SweetAlert
            Swal.fire({
              icon: "error",
              title: "Logout error",
              text: "An error occurred during the logout process.",
            });
          }
        } else {
          // User is not authenticated (no JWT token), redirect to the login page
          this.$router.push("/login"); // You can change "/login" to the actual login route
        }
      },
    },
  };
</script>