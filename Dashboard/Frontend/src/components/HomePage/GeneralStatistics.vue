<template>
    <div class="row">
        <div class="col-sm-2">
            <div class="card">
                <div class="card-header"><i class="bi bi-cpu"></i> Total Agents</div>
                <div class="card-body">
                    <router-link class="nav-link" to="/agents"><p class="card-text">{{ agentCount }}</p></router-link>
                </div>
            </div>
        </div>
        <div class="col-sm-2">
            <div class="card">
                <div class="card-header"><i class="bi bi-people"></i> Total Users</div>
                <div class="card-body">
                    <p class="card-text">{{ userCount }}</p>
                </div>
            </div>
        </div>
        <div class="col-sm-2">
            <div class="card">
                <div class="card-header"><i class="bi bi-window"></i> Total Installed Apps</div>
                <div class="card-body">
                    <p class="card-text">{{ installedAppsCount }}</p>
                </div>
            </div>
        </div>
        <div class="col-sm-2">
            <div class="card">
                <div class="card-header">Data Here</div>
                <div class="card-body">
                    <p class="card-text">Data Here</p>
                </div>
            </div>
        </div>
        <div class="col-sm-2">
            <div class="card">
                <div class="card-header">Data Here</div>
                <div class="card-body">
                    <p class="card-text">Data Here</p>
                </div>
            </div>
        </div>
        <div class="col-sm-2">
            <div class="card">
                <div class="card-header">Data Here</div>
                <div class="card-body">
                    <p class="card-text">Data Here</p>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
    // @ is an alias to /src
    import { getHomePageStatistics } from '@/utils/requestUtils.js';
    
    export default {
        name: 'GeneralStatistics',
        data(){
            return{
                agentCount: 0,
                userCount: 0,
                installedAppsCount: 0,
                homePageData: {}
            }
        },
        mounted(){
            this.fillHomePageStatistics();
        },
        methods:{
            async fillHomePageStatistics(){
                this.homePageData = await getHomePageStatistics();

                this.agentCount = this.homePageData.agent_count;
                this.userCount  = this.homePageData.sys_user_count;
                this.installedAppsCount = this.homePageData.installed_apps_count;

            }
        }
    }
</script>
  