<template>
    <Navbar /> <!-- Include the Navbar component here -->
    <div class="container">
        <table class="table table-striped table-bordered table-hover nowrap" id="dashboardLastLoginsTable">
          <thead>
            <tr>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lastLogin in lastLoginsData" :key="lastLogin.email">
                <td>{{ lastLogin.created }}</td>
            </tr>
          </tbody>
        </table>
    </div>
    
</template>
  
<script>
  // @ is an alias to /src
  import $ from "jquery";
  import Navbar from '@/components/Navbar.vue';
  import { getMyLastDashboardLogins } from '@/utils/requestUtils';
  
  export default {
    name: 'DashboardLastLoginsView',
    components: {
      Navbar,
    },
    data(){
        return{
            lastLoginsData: {}
        }
    },
    mounted(){
        this.fillLastDasboardLogins();
    },
    methods:{
        async fillLastDasboardLogins(){
            this.lastLoginsData = await getMyLastDashboardLogins();

            // Make Users Last Logons Table as DataTable
            $(document).ready(() => {
                $('#dashboardLastLoginsTable').DataTable({
                searching: true,
                lengthChange: true,
                pageLength: 25,
                lengthMenu: [
                    [25, 50, 100, 250, -1],
                    [25, 50, 100, 250, 'All']
                ],
                order: [ 0, 'desc' ]
                });
                // Style length Menu
                const pageEntrySize = document.getElementById('dashboardLastLoginsTable_length')
                pageEntrySize.style = "float:left"
                const pageInfoText = document.getElementById('dashboardLastLoginsTable_info')
                pageInfoText.style = "float:left"

            });
        }
    }
  }
</script>

<style>
  #dashboardLastLoginsTable{
    margin-top: 5rem;
  }
</style>
  