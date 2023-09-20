<template>
    <!-- Modal -->
    <div class="modal fade" id="createAgentModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="createAgentModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="createAgentModalLabel">Create Agent</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <section class="modal-card-body">
                        <!-- Agent Type dropdown -->
                        <div class="field">
                            <label class="label">Agent Type</label>
                            <div class="control">
                                <label class="radio">
                                    <input type="radio" v-model="selectedAgentType" value="windows">
                                    <span title="Windows">
                                        <i class="bi bi-windows"></i>
                                    </span>
                                </label>&nbsp;
                                <label class="radio">
                                    <input type="radio" v-model="selectedAgentType" value="linux">
                                    <span title="Linux">
                                        <i class="fab fa-linux"></i>
                                    </span>
                                </label>&nbsp;
                                <label class="radio">
                                    <input type="radio" v-model="selectedAgentType" value="macos">
                                    <span title="macOS">
                                        <i class="bi bi-apple"></i>
                                    </span>
                                </label>
                            </div>
                        </div>
                    </section>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button class="btn btn-primary is-success" @click="registerAgent">Create</button>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import Swal from 'sweetalert2';
import axios from 'axios';

export default {
  data() {
    return {
      selectedAgentType: 'windows', // Default value
    };
  },
  methods: {
    async registerAgent() {
      // Send a POST request to register the agent
      try {
        const jwtToken = sessionStorage.getItem("jwtToken");
        const API_URL = "http://localhost:5000/agent/register"
        await axios.post(API_URL, {
          // Request Body
          type: this.selectedAgentType,
        },{
          // Request Headers
          headers: { Authorization: jwtToken }
        });

        // Show success message
        Swal.fire({
          icon: 'success',
          title: 'Agent Created',
          text: 'The agent has been successfully created.',
        }).then(() => {
            location.reload()
        });

        
      } catch (error) {
        // Show error message
        Swal.fire({
          icon: 'error',
          title: 'Agent Creation Failed',
          text: 'Failed to create the agent. Please try again later.',
        });

        console.error('Agent creation failed:', error);
      }
    },
  },
};
</script>

<style scoped>
.bi{
  font-size: 3rem;
  margin: 2rem;
}
.fab{
  font-size: 3rem;
  margin: 2rem;
}
</style>