<template>
  <Navbar /> <!-- Include the Navbar component here -->
  <GeneralStatistics></GeneralStatistics>
  <div class="container mt-5">
    <div class="jumbotron">
      <h1 class="display-4">Welcome to Our App</h1>
      <p class="lead">This is a beautiful home view created with Vue.js and Bootstrap.</p>
      <hr class="my-4">
      <p>Enjoy exploring our app's features and functionality.</p>
      <a class="btn btn-primary btn-lg" href="#" role="button">Learn more</a>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Navbar from '@/components/Navbar.vue';
import GeneralStatistics from '@/components/HomePage/GeneralStatistics.vue'

export default {
  name: 'HomeView',
  components: {
    Navbar,
    GeneralStatistics,
  }
}
</script>
