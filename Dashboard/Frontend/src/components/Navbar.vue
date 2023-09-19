<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">Dasboard</router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/system-data">System Data</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/users">Users</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/agents">Agents</router-link>
            </li>
          </ul>
          <div class="dropdown d-flex">
            <button
              class="btn btn-secondary dropdown-toggle"
              type="button"
              id="userDropdown"
              data-bs-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              Username <!-- Replace with the user's name or username -->
            </button>
            <div class="dropdown-menu dropdown-menu-right" aria-labelledby="userDropdown">
              <button class="dropdown-item" @click="logout">Logout</button>
            </div>
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