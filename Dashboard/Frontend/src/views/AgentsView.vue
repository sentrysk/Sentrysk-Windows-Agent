<template>
  <Navbar /> <!-- Include the Navbar component here -->
  <div class="container">
    <h1 class="my-4">Agents</h1>
    <div class="card">
      <div class="card-body">
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#createAgentModal" style="margin-left: 88%;margin-right: 0%;margin-bottom: 1rem;">
          <i class="bi bi-plus-circle"></i> Create Agent
        </button>
        <table class="table table-striped table-bordered dt-responsive nowrap" id="agentsTable">
          <thead>
            <tr>
              <th>#</th>
              <th>Type</th>
              <th>Token</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(agent, index) in agents" :key="agent.id">
              <td>
                {{index}}
              </td>
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
                <span v-if="!agent.showToken">************************************</span> <!-- Masked token -->
                <span v-else>{{ agent.token }}</span> <!-- Revealed token -->
                <button class="btn btn-link btn-sm" @click="toggleTokenVisibility(agent)">
                  <i :class="['bi', agent.showToken ? 'bi-eye-slash' : 'bi-eye']"></i>
                </button>
              </td>
              <td>{{ formatToLocalTime(agent.created) }}</td>
              <td>
                <button type="button" class="btn btn-warning btn-sm" data-bs-toggle="modal" data-bs-target="#updateAgentModal" @click="setUpdateAttributes(agent.id,agent.token,agent.type)">
                  <i class="bi bi-plus-circle"></i> Update
                </button>&nbsp;
                <button class="btn btn-danger btn-sm" @click="deleteAgent(agent.id)">
                  <i class="bi bi-trash"></i> Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <AgentCreateModal></AgentCreateModal>
    <AgentUpdateModal></AgentUpdateModal>

  </div>
</template>
  
<script>
  import axios from 'axios';
  import Swal from 'sweetalert2';
  import Navbar from '../components/Navbar.vue'
  import AgentCreateModal from '@/components/AgentCreateModal.vue';
  import AgentUpdateModal from '@/components/AgentUpdateModal.vue';
  import $ from "jquery";
  
  export default {
    components: {
      Navbar, // Declare Navbar as a component
      AgentCreateModal,
      AgentUpdateModal,
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
      formatToLocalTime(utcTime) {
        // Create a Date object from the UTC time
        const utcDate = new Date(utcTime);

        // Format the date and time to the user's locale and timezone
        const formattedTime = utcDate.toLocaleString(undefined, {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          timeZoneName: 'short',
          hour12: false,
        });

        return formattedTime;
      },
      setUpdateAttributes(agentId,agentToken,selectedAgentType){
        document.getElementById('updateAgentId').value = agentId;
        document.getElementById('updateAgentToken').value = agentToken;
        document.querySelector(`#updateAgentModal input[type=radio][value=${selectedAgentType}]`).click()
      },
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
          $(document).ready(() => {
            $('#agentsTable').DataTable({
              responsive: true,
              searching: true,
              lengthChange: true,
              pageLength: 10,
              order: [[3, 'desc']],
              lengthMenu: [
                  [10, 25, 50, 100, -1],
                  [10, 25, 50, 100, 'All']
              ],
            });
            // Style length Menu
            const pageEntrySize = document.getElementById('agentsTable_length')
            pageEntrySize.style = "margin-right:100%"
          });
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
  