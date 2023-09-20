<template>
    <!-- Modal -->
    <div class="modal fade" id="updateAgentModal" data-bs-keyboard="false" tabindex="-1" aria-labelledby="updateAgentModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="updateAgentModalLabel">Update</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <section class="modal-card-body">
                        <label class="label">Agent Id</label>
                        <input type="text" id="updateAgentId" ref="agentId" class="form-control" disabled="true">
                        <label class="label">Token</label>
                        <input type="text" id="updateAgentToken" ref="agentToken" class="form-control" disabled="true">
                        <!-- Agent Type dropdown -->
                        <div class="field">
                            <label class="label">Agent Type</label>
                            <div class="control">
                                <label class="radio">
                                    <input type="radio" v-model="selectedAgentType" value="windows" name="updateAgentTypeGroup">
                                    <span title="Windows">
                                        <i class="bi bi-windows"></i>
                                    </span>
                                </label>&nbsp;
                                <label class="radio">
                                    <input type="radio" v-model="selectedAgentType" value="linux" name="updateAgentTypeGroup">
                                    <span title="Linux">
                                        <i class="fab fa-linux"></i>
                                    </span>
                                </label>&nbsp;
                                <label class="radio">
                                    <input type="radio" v-model="selectedAgentType" value="macos" name="updateAgentTypeGroup">
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
                    <button class="btn btn-primary is-success" @click="updateAgent">Update</button>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
  import Swal from 'sweetalert2';
  import axios from 'axios';
  
  export default {
    methods: {
      async updateAgent() {
        //alert(document.getElementById('updateAgentId').value)
        try {
          // Retrieve JWT token from session storage
          const jwtToken = sessionStorage.getItem('jwtToken');
          const agentId =  this.$refs.agentId.value

          // Send PUT request to update the agent type by ID
          await axios.put(`http://localhost:5000/agent/${agentId}`, {
            type: this.selectedAgentType,
          }, {
            headers: {
              Authorization: jwtToken,
            },
          });
  
          // Show success message
          Swal.fire({
            icon: 'success',
            title: 'Agent Updated',
            text: 'The agent has been successfully updated.',
          }).then(() => {
            location.reload()
          });
  
        } catch (error) {
          // Show error message
          Swal.fire({
            icon: 'error',
            title: 'Agent Update Failed',
            text: 'Failed to update the agent. Please try again later.',
          });
  
          console.error('Agent update failed:', error);
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
  