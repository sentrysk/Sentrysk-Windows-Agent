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
                {{ changeLogCount }}
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
            <table class="table table-striped table-bordered table-sm table-hover nowrap"  id="systemInstalledAppsTable">
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
    import $ from "jquery";
    import { formatToLocalTime,calculateDatetimeDifference } from '../../utils/timeUtils';
    import { getInstalledApps,getInstalledAppsChangeLog } from '../../utils/requestUtils'

    
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
        this.fillInstalledApps();
      },
      methods: {
        async fillInstalledApps() {
          try {
            // Get the ID from the URL
            const agentId = this.$route.params.id;

            // Retrieve System Apps
            this.systemInstalledApps =  await getInstalledApps(agentId);
            // Retrieve System Apps Changelogs
            this.changeLogData = await getInstalledAppsChangeLog(this.systemInstalledApps.id)

            // Set Local Update Time and Time Diff
            this.localUpdateTime = formatToLocalTime(this.systemInstalledApps.updated);
            this.timeDiff =  calculateDatetimeDifference(this.systemInstalledApps.updated);

            // Set system Installed Apps Count
            this.systemInstalledAppsCount = this.systemInstalledApps.apps.length;
            

            this.changeLogData = this.changeLogData.map((item) => {
            const date = formatToLocalTime(item.timestamp);
            const changes = item.changes;

            // Define the Action List
            const actionList = [];
            
            // Find Deleted Apps
            if (changes.deleted_apps) {
              for (const app of changes.deleted_apps) {
                actionList.push({
                  date,
                  action: "Delete",
                  appname:  app.name,
                  field: "-",
                  previous_value: app,
                  new_value: "-",
                });
              }
            }

            // Find Newly Added Apps
            if (changes.new_apps) {
              for (const app of changes.new_apps) {
                actionList.push({
                  date,
                  action: "New",
                  appname:  app.name,
                  field: "-",
                  previous_value: "-",
                  new_value: app,
                });
              }
            }

            // Find Updated Apps
            if (changes.updated_apps) {
              for (const appname in changes.updated_apps) {
                const appChanges = changes.updated_apps[appname];
                for (const changeKey in userChanges) {
                  actionList.push({
                    date,
                    action: "Update",
                    appname: appname,
                    field: changeKey,
                    previous_value: appChanges[changeKey]["previous_value"],
                    new_value: appChanges[changeKey]["new_value"],
                  });
                }
              }
            }

            return actionList;
          }).flat();

            $(document).ready(() => {
              $('#systemInstalledAppsTable').DataTable({
              searching: true,
              lengthChange: true,
              pageLength: 25,
              lengthMenu: [
                  [25, 50, 100, 200, -1],
                  [25, 50, 100, 200, 'All']
              ],
              });
              // Style length Menu
              const pageEntrySize = document.getElementById('systemInstalledAppsTable_length')
              pageEntrySize.style = "margin-right:100%"
              const pageInfoText = document.getElementById('systemInstalledAppsTable_info')
              pageInfoText.style = "float:left"
            });
          } catch (error) {
            console.error('Error fetching agents:', error);
          }
        },
      },
    };
</script>

<style>
</style>