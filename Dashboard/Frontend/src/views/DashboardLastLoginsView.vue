<template>
    <Navbar /> <!-- Include the Navbar component here -->
    <div class="container">
        <table class="table table-striped table-bordered dt-responsive nowrap" id="agentsTable">
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
        }
    }
  }
  </script>
  