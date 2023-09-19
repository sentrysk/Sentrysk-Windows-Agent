import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginPage from '../components/LoginPage.vue'
import RegisterPage from '../components/RegisterPage.vue'
import axios from "axios";

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Add a navigation guard to check session validity
router.beforeEach(async (to, from, next) => {
  // Check if the route requires authentication
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // Check if the user is logged in
    const jwtToken = sessionStorage.getItem("jwtToken");

    if (jwtToken) {
      // User is authenticated, proceed to check the session
      try {
        // Send a GET request to the session check endpoint
        const response = await axios.get("http://localhost:5000/session/check", {
          headers: {
            Authorization: jwtToken,
          },
        });

        // Check if the session check is successful (e.g., HTTP status 200)
        if (response.status === 200) {
          // Session is valid, allow access to the route
          next();
        } else {
          // Session check failed, redirect to the login page
          next("/login");
        }
      } catch (error) {
        console.error("Session check failed:", error);
        // Handle session check error, redirect to login or display an error message
        next("/login");
      }
    } else {
      // User is not authenticated, redirect to the login page
      next("/login");
    }
  } else {
    // Route doesn't require authentication, allow access
    next();
  }
});

export default router;
