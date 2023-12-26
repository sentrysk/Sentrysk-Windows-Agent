<template>
    <div class="tab-pane fade" id="systemUsersLastLogons" role="tabpanel" aria-labelledby="SystemUsersLastLogons">
        <b>Last Update : {{ lastUpdate }}</b>
        <table class="table table-striped table-bordered table-sm" id="sysUsersLastLogonsTable">
            <thead>
                <tr>
                <th>Username</th>
                <th>Last Logon</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="data in systemUsersLastLogons.last_logons" :key="data">
                    <td>
                        {{ data.username }}
                    </td>
                    <td>
                        {{ data.last_logon }}
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    import { getSystemUsersLastLogons } from '../../../utils/requestUtils';

    export default {
        name: 'LastLogonsTab',
        data(){
            return{
                systemUsersLastLogons: {},
                lastUpdate: ""
            }
        },
        mounted() {
            this.fillSystemUsersLastLogons();
        },
        methods:{
            async fillSystemUsersLastLogons(){
                try {
                    // Get the Agent ID from the URL
                    const agentId = this.$route.params.id;
                    
                    // Retrive System Users
                    this.systemUsersLastLogons = await getSystemUsersLastLogons(agentId);

                    // Set Last Update
                    this.lastUpdate = this.systemUsersLastLogons.updated;

                } catch (error) {
                    console.error('Error fetching system users last logons:', error);
                }
            }
        }
    }
</script>

<style>

</style>