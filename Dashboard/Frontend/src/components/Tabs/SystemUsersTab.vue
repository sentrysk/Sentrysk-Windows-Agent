<template>
    <ul class="nav nav-tabs" id="systemSubTab" role="tablist">
        <li class="nav-item" role="presentation">
            <button class="nav-link active" id="systemUsersUsersTab" data-bs-toggle="tab" data-bs-target="#systemUsers" type="button" role="tab" aria-controls="systemUsers" aria-selected="true"><i class="bi bi-code-square"></i>Users</button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="systemUsersChangelogTab" data-bs-toggle="tab" data-bs-target="#systemUsersChangelog" type="button" role="tab" aria-controls="systemUsersChangelog" aria-selected="false"><i class="bi bi-file-diff"></i> Changelogs</button>
        </li>
    </ul>

    <!-- Last Update -->
    <div class="row">
      <span :title=localUpdateTime>Last Update : {{ timeDiff }}</span>
    </div>

    <div class="tab-content" id="sysUsersTabContent">
        <div class="tab-pane fade show active" id="systemUsers" role="tabpanel" aria-labelledby="systemUsers">
            <table class="table table-striped table-bordered table-sm nowrap" id="systemUsersTable">
                <thead>
                    <tr>
                        <th>User ID</th>
                        <th>SID</th>
                        <th>Username</th>
                        <th>Group ID</th>
                        <th>Home Directory</th>
                        <th>Shell</th>
                        <th>Full Name</th>
                        <th>Comment</th>
                        <th>Last Logon</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(user, index) in systemUsers.users" :key="index">
                        <td>{{ user.user_id }}</td>
                        <td>{{ user.sid }}</td>
                        <td>{{ user.username }}</td>
                        <td>{{ user.group_id }}</td>
                        <td>{{ user.home_directory }}</td>
                        <td>{{ user.shell }}</td>
                        <td>{{ user.full_name }}</td>
                        <td>{{ user.comment }}</td>
                        <td>{{ user.last_logon }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="tab-pane fade" id="systemUsersChangelog" role="tabpanel" aria-labelledby="systemUsersChangelog">
          <table class="table table-striped table-bordered table-sm" id="sysUsersChangelogsTable">
            <thead>
              <tr>
                <th>Time</th>
                <th>Action</th>
                <th>Username</th>
                <th>Field</th>
                <th>Previous Value</th>
                <th>New Value</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="data in parsedData" :key="data">
                <td>
                  {{ data.date }}
                </td>

                <td v-if="data.action == 'New'" class="sysUserActionIcons" style="color: green;">
                  <span title="New User"><i class="bi bi-person-fill-add"></i></span>
                </td>
                <td v-if="data.action == 'Delete'"  class="sysUserActionIcons" style="color:crimson">
                  <span title="Deleted User"><i class="fa-solid fa-user-slash fa-xs"></i></span>
                </td>
                <td v-if="data.action == 'Update'" class="sysUserActionIcons" style="color: coral;">
                  <span title="Updated User"><i class="bi bi-person-fill-up"></i></span>
                </td>


                <td>
                  {{ data.username }}
                </td>
                <td>
                  {{ data.field }}
                </td>
                <td style="color:crimson">
                  {{ data.previous_value }}
                </td>
                <td style="color: green;">
                  {{ data.new_value }}
                </td>
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
      name: 'SystemUsersTab',
      data() {
        return {
          systemUsers: {},
          changeLog: {},
          localUpdateTime: "",
          timeDiff: "",
          parsedData: [],
        };
      },
      mounted() {
        this.getSystemUsers();
      },
      methods: {
        async getSystemUsers() {
          try {
            // Get the ID from the URL
            const id = this.$route.params.id;

            // Retrieve JWT token from session storage
            const jwtToken = sessionStorage.getItem('jwtToken');
            const API_URL  =  "http://localhost:5000/sysusers/"+id
            const response = await axios.get(API_URL, {
              headers: {
                Authorization: jwtToken,
              },
            });
    
            this.systemUsers = response.data;
            this.localUpdateTime = formatToLocalTime(this.systemUsers.updated);
            this.timeDiff =  calculateDatetimeDifference(this.systemUsers.updated);

            //Get Changelog Request
            const CHANGELOG_URL = "http://localhost:5000/sysusers/changelog/"+response.data.id
            const changelog = await axios.get(CHANGELOG_URL, {
              headers: {
                Authorization: jwtToken,
              },
            });
            this.changeLog = changelog.data;

            this.parsedData = changelog.data.map((item) => {
            const date = formatToLocalTime(item.timestamp);
            const changes = item.changes;

            const actionList = [];
            
            if (changes.deleted_users) {
              for (const user of changes.deleted_users) {
                actionList.push({
                  date,
                  action: "Delete",
                  username:  user.username,
                  field: "-",
                  previous_value: user,
                  new_value: "-",
                });
              }
            }

            if (changes.new_users) {
              for (const user of changes.new_users) {
                actionList.push({
                  date,
                  action: "New",
                  username:  user.username,
                  field: "-",
                  previous_value: "-",
                  new_value: user,
                });
              }
            }

            if (changes.updated_users) {
              for (const username in changes.updated_users) {
                const userChanges = changes.updated_users[username];
                for (const changeKey in userChanges) {
                  actionList.push({
                    date,
                    action: "Update",
                    username: username,
                    field: changeKey,
                    previous_value: userChanges[changeKey]["previous_value"],
                    new_value: userChanges[changeKey]["new_value"],
                  });
                }
              }
            }

            return actionList;
          }).flat();

          $(document).ready(() => {
              $('#systemUsersTable').DataTable({
              searching: true,
              lengthChange: true,
              pageLength: 10,
              lengthMenu: [
                  [10, 25, 50, 100, -1],
                  [10, 25, 50, 100, 'All']
              ],
              });
              // Style length Menu
              const pageEntrySize = document.getElementById('systemUsersTable_length')
              pageEntrySize.style = "margin-right:100%"
              const pageInfoText = document.getElementById('systemUsersTable_info')
              pageInfoText.style = "float:left"

              $('#sysUsersChangelogsTable').DataTable({
              searching: true,
              lengthChange: true,
              pageLength: 10,
              lengthMenu: [
                  [10, 25, 50, 100, -1],
                  [10, 25, 50, 100, 'All']
              ],
              order: [ 0, 'desc' ],
              select: true,
              });
              // Style length Menu
              const chlgPageEntrySize = document.getElementById('sysUsersChangelogsTable_length')
              chlgPageEntrySize.style = "margin-right:100%"
              const chlgPageInfoText = document.getElementById('sysUsersChangelogsTable_info')
              chlgPageInfoText.style = "float:left"
          });


          } catch (error) {
            console.error('Error fetching agents:', error);
          }
        },
        async getUserKeys(data){
            const keys = Object.keys(data || {});
            return keys;
        }
      },
    };
</script>

<style>
.sysUserActionIcons{
  font-size: 2em;
  max-width: 4rem;
}
</style>