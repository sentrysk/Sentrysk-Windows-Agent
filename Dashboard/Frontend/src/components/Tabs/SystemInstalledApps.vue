<template>
    <ul class="nav nav-tabs" id="systemSubTab" role="tablist">
        <li class="nav-item" role="presentation">
            <button class="nav-link active" id="systemInstalledAppsTab" data-bs-toggle="tab" data-bs-target="#systemInstalledApps" type="button" role="tab" aria-controls="systemInstalledApps" aria-selected="true">
              <i class="bi bi-code-square"></i>Installed Apps
              <span class="badge rounded-pill bg-primary">
              {{ systemInstalledAppsCount }}
              </span>
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="systemInstalledAppsChangelogTab" data-bs-toggle="tab" data-bs-target="#systemInstalledAppsChangelog" type="button" role="tab" aria-controls="systemInstalledAppsChangelog" aria-selected="false">
              <i class="bi bi-file-diff"></i>Changelogs 
              <span class="badge rounded-pill bg-primary">
              </span>
            </button>
        </li>
    </ul>

    <!-- Last Update -->
    <div class="row">
      <span :title=localUpdateTime>Last Update : {{ timeDiff }}</span>
    </div>

    <div class="tab-content" id="sysInstalledAppsTabContent">
        <div class="tab-pane fade show active" id="systemInstalledApps" role="tabpanel" aria-labelledby="systemInstalledApps">
            <table class="table table-striped table-bordered table-sm nowrap">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Version</th>
                        <th>Installed By</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(app, index) in systemInstalledApps.apps" :key="index">
                        <td>{{ app.name }}</td>
                        <td>{{ app.version }}</td>
                        <td>{{ app.installed_by }}</td>

                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>


<script>
    import axios from 'axios';
    import $ from "jquery";
    import { formatToLocalTime,calculateDatetimeDifference } from '../../utils/timeUtils';

    
    export default {
      name: 'SystemInstalledAppsTab',
      data() {
        return {
          systemInstalledApps: {},
          systemInstalledAppsCount: 0,
          changeLogData: [],
          changeLogCount: 0,
          localUpdateTime: "",
          timeDiff: "",
        };
      },
      mounted() {
        this.getInstalledApps();
      },
      methods: {
        async getInstalledApps() {
          try {
            // Get the ID from the URL
            const id = this.$route.params.id;

            // Retrieve JWT token from session storage
            const jwtToken = sessionStorage.getItem('jwtToken');
            const API_URL  =  "http://localhost:5000/sysapps/"+id
            const response = await axios.get(API_URL, {
              headers: {
                Authorization: jwtToken,
              },
            });
    
            this.systemInstalledApps = response.data;
            this.localUpdateTime = formatToLocalTime(this.systemInstalledApps.updated);
            this.timeDiff =  calculateDatetimeDifference(this.systemInstalledApps.updated);

            // Set system Installed Apps Count
            this.systemInstalledAppsCount = this.systemInstalledApps.apps.length;
          } catch (error) {
            console.error('Error fetching agents:', error);
          }
        },
      },
    };
</script>

<style>
</style>