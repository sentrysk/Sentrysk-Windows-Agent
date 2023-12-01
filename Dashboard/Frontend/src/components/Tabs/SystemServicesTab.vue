<template>
    <ul class="nav nav-tabs" id="systemSubTab" role="tablist">
        <li class="nav-item" role="presentation">
            <button class="nav-link active" id="systemServicesTab" data-bs-toggle="tab" data-bs-target="#systemServices" type="button" role="tab" aria-controls="systemServices" aria-selected="true">
              <i class="bi bi-code-square"></i>Services
              <span class="badge rounded-pill bg-primary">
              {{ systemServicesCount }}
              </span>
            </button>
        </li>
    </ul>

    <!-- Last Update -->
    <div class="row">
      <span :title=localUpdateTime>Last Update : {{ timeDiff }}</span>
    </div>

    <div class="tab-content" id="sysServicesTabContent">
        <div class="tab-pane fade show active" id="systemServices" role="tabpanel" aria-labelledby="systemServices">
            <table class="table table-striped table-bordered table-sm table-hover nowrap"  id="systemServicesTable">
                <thead>
                    <tr>
                        <th>Status</th>
                        <th>Display Name</th>
                        <th>Service Name</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(service, index) in systemServices.services" :key="index">
                        <td>{{ service.status }}</td>
                        <td>{{ service.display_name }}</td>
                        <td>{{ service.service_name }}</td>
                        <td>{{ service.description }}</td>
                    </tr>
                </tbody>
            </table>
        </div>

    </div>
</template>

<script>
    import { formatToLocalTime,calculateDatetimeDifference } from '../../utils/timeUtils';
    import { getServices } from '../../utils/requestUtils'

    
    export default {
      name: 'SystemServicesTab',
      data() {
        return {
          systemServices: {},
          systemServicesCount: 0,
          localUpdateTime: "",
          timeDiff: "",
        };
      },
      mounted() {
        this.fillServices();
      },
      methods: {
        async fillServices() {
          try {
            // Get the ID from the URL
            const agentId = this.$route.params.id;

            // Retrieve System Apps
            this.systemServices =  await getServices(agentId);

            // Set Local Update Time and Time Diff
            this.localUpdateTime = formatToLocalTime(this.systemServices.updated);
            this.timeDiff =  calculateDatetimeDifference(this.systemServices.updated);

            // Set system Installed Apps Count
            this.systemServicesCount = this.systemServices.services.length;

          } catch (error) {
            console.error(error);
          }
        },
      },
    };
</script>

<style>
.sysAppsActionIcons{
  font-size: 2em;
  max-width: 4rem;
}
</style>