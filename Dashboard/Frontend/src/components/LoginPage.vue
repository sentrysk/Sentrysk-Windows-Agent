<template>
    <div class="login-container">
      <h1>Login</h1>
      <form @submit.prevent="login">
        <input type="text" v-model="email" placeholder="Email" />
        <input type="password" v-model="password" placeholder="Password" />
        <button type="submit">Login</button>
      </form>
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
  .login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    text-align: center;
  }
  
  input {
    width: 100%;
    padding: 10px;
    margin: 10px 0;
  }
  
  button {
    background-color: #007bff;
    color: #fff;
    padding: 10px 20px;
    border: none;
    cursor: pointer;
  }
  </style>
  