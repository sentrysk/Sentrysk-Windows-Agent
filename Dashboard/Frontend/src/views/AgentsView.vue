<template>
  <Navbar /> <!-- Include the Navbar component here -->
  <div class="container">
    <h1 class="my-4">Agents</h1>
    <div class="card">
      <div class="card-body">
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#createAgentModal" style="margin-left: 88%;margin-right: 0%;">
          <i class="bi bi-plus-circle"></i> Create Agent
        </button>
        <table class="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Type</th>
              <th>Token</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="agent in agents" :key="agent.id">
              <td>{{ agent.id }}</td>
              <td>
                <span v-if="agent.type === 'windows'" title="Windows">
                  <i class="bi bi-windows"></i>
                </span>
                <span v-else-if="agent.type === 'linux'" title="Linux">
                  <i class="fab fa-linux"></i>
                </span>
                <span v-else-if="agent.type === 'macos'" title="macOS">
                  <i class="bi bi-apple"></i>
                </span>
              </td>
              <td>
                <span v-if="!agent.showToken">**********</span> <!-- Masked token -->
                <span v-else>{{ agent.token }}</span> <!-- Revealed token -->
                <button class="btn btn-link btn-sm" @click="toggleTokenVisibility(agent)">
                  <i :class="['bi', agent.showToken ? 'bi-eye-slash' : 'bi-eye']"></i>
                </button>
              </td>
              <td>{{ agent.created }}</td>
              <td>
                <button class="btn btn-danger btn-sm" @click="deleteAgent(agent.id)">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <AgentCreateModal></AgentCreateModal>

  </div>
</template>
  
<script>
  import axios from 'axios';
  import Swal from 'sweetalert2';
  import Navbar from '../components/Navbar.vue'
  import AgentCreateModal from '@/components/AgentCreateModal.vue';
  
  export default {
    components: {
      Navbar, // Declare Navbar as a component
      AgentCreateModal,
    },
    data() {
      return {
        agents: [],
      };
    },
    mounted() {
      this.getAgents();
    },
    methods: {
      async getAgents() {
        try {
          // Retrieve JWT token from session storage
          const jwtToken = sessionStorage.getItem('jwtToken');
          const API_URL  =  "http://localhost:5000/agent/"
          const response = await axios.get(API_URL, {
            headers: {
              Authorization: jwtToken,
            },
          });
  
          this.agents = response.data;
        } catch (error) {
          console.error('Error fetching agents:', error);
        }
      },
      toggleTokenVisibility(agent) {
        agent.showToken = !agent.showToken;
      },
      async deleteAgent(agentId) {
        try {
          const confirmResult = await Swal.fire({
            title: 'Are you sure?',
            text: 'You are about to delete this agent.',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, delete it',
            cancelButtonText: 'No, cancel',
            reverseButtons: true,
          });

          if (confirmResult.isConfirmed) {
            // Retrieve JWT token from session storage
            const jwtToken = sessionStorage.getItem('jwtToken');

            // Send DELETE request to delete the agent by ID
            await axios.delete(`http://localhost:5000/agent/${agentId}`, {
              headers: {
                Authorization: jwtToken,
              },
            });

            // Show success message
            Swal.fire({
              icon: 'success',
              title: 'Agent Deleted',
              text: 'The agent has been successfully deleted.',
            }).then(() => {
              // Remove the deleted agent from the list
              this.agents = this.agents.filter(agent => agent.id !== agentId);
              // Reload Page
              location.reload()
            });;
          }
          
        } catch (error) {
          // Show error message
          Swal.fire({
            icon: 'error',
            title: 'Agent Deletion Failed',
            text: 'Failed to delete the agent. Please try again later.',
          });

          console.error('Agent deletion failed:', error);
        }
      },
    },
  };
</script>
  
<style scoped>
  /* Add your custom styles here */
  .table {
    margin-top: 20px;
  }
  
  .table thead th {
    background-color: #007bff; /* Blue header background color */
    color: white;
  }
  
  .table tbody tr:nth-child(odd) {
    background-color: #f2f2f2; /* Alternate row background color */
  }
  
  .table tbody tr:hover {
    background-color: #dcdcdc; /* Hover row background color */
  }
  
  .table td,
  .table th {
    vertical-align: middle;
  }
</style>
  