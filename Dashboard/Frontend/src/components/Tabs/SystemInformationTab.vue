<template>
    <ul class="nav nav-tabs" id="systemSubTab" role="tablist">
        <li class="nav-item" role="presentation">
            <button class="nav-link active" id="systemOsTab" data-bs-toggle="tab" data-bs-target="#systemOs" type="button" role="tab" aria-controls="systemOs" aria-selected="true"><i class="bi bi-code-square"></i> OS</button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="systemDomainTab" data-bs-toggle="tab" data-bs-target="#systemDomain" type="button" role="tab" aria-controls="systemDomain" aria-selected="false"><i class="fa-solid fa-network-wired"></i> Domain</button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="systemCpuTab" data-bs-toggle="tab" data-bs-target="#systemCpu" type="button" role="tab" aria-controls="systemCpu" aria-selected="false"><i class="bi bi-cpu"></i> CPU</button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="systemMemoryTab" data-bs-toggle="tab" data-bs-target="#systemMemory" type="button" role="tab" aria-controls="systemMemory" aria-selected="false"><i class="bi bi-memory"></i> Memory</button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="systemDisksTab" data-bs-toggle="tab" data-bs-target="#systemDisks" type="button" role="tab" aria-controls="systemDisks" aria-selected="false"><i class="bi bi-hdd-stack"></i> Disks</button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="systemNetworkInterfacesTab" data-bs-toggle="tab" data-bs-target="#systemNetworkInterfaces" type="button" role="tab" aria-controls="systemNetworkInterfaces" aria-selected="false"><i class="bi bi-wifi"></i> Network Interfaces</button>
        </li>
    </ul>

    <!-- Last Update -->
    <div class="row">
        <span :title=formatToLocalTime(systemInfo.updated)>Last Update : {{ calculateDatetimeDifference(systemInfo.updated) }}</span>
    </div>

    <div class="tab-content" id="myTabContent">
        <!-- OS Tab -->
        <div class="tab-pane fade show active" id="systemOs" role="tabpanel" aria-labelledby="systemOs">
            <!-- Use Bootstrap Cards to display the data -->
            <div class="row">
                <div class="col-md-6" v-for="(item, index) in systemInfo.os" :key="index">
                    <div class="card">
                        <div class="card-body">
                            <h3 class="card-title">{{ index }}</h3>
                            <p class="card-text">{{ item }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Domain Tab -->
        <div class="tab-pane fade" id="systemDomain" role="tabpanel" aria-labelledby="systemDomain">
            <!-- Use Bootstrap Cards to display the data -->
            <div class="row">
                <div class="col-md-6" v-for="(item, index) in systemInfo.domain" :key="index">
                    <div class="card">
                        <div class="card-body">
                            <h3 class="card-title">{{ index }}</h3>
                            <p class="card-text">{{ item }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- CPU Tab -->
        <div class="tab-pane fade" id="systemCpu" role="tabpanel" aria-labelledby="systemCpu">
            <!-- Use Bootstrap Cards to display the data -->
            <div class="row">
                <div class="col-md-6" v-for="(item, index) in systemInfo.cpu" :key="index">
                    <div class="card">
                        <div class="card-body">
                            <h3 class="card-title">{{ index }}</h3>
                            <p class="card-text">{{ item }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Memory Tab -->
        <div class="tab-pane fade" id="systemMemory" role="tabpanel" aria-labelledby="systemMemory">
            <!-- Use Bootstrap Cards to display the data -->
            <div class="row">
                <div class="col-md-6" v-for="(item, index) in systemInfo.memory" :key="index">
                    <div class="card">
                        <div class="card-body">
                            <h3 class="card-title">{{ index }}</h3>
                            <p class="card-text">{{ item }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Disks Tab -->
        <div class="tab-pane fade" id="systemDisks" role="tabpanel" aria-labelledby="systemDisks">
            <!-- Use Bootstrap Cards to display the data -->
            <div class="row">
                <div class="col-md-6" v-for="(item, index) in systemInfo.disks" :key="index">
                    <div class="card">
                        <div class="card-body">
                            <h3 class="card-title">{{ index }}</h3>
                            <table class="table table-striped table-bordered table-sm">
                                <tbody>
                                    <tr v-for="(diskVal, diskKey) in item" :key="diskKey">
                                        <td>
                                            {{ diskKey }}
                                        </td>
                                        <td>
                                            {{ diskVal }}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
       
        <!-- Network Interfaces Tab -->
        <div class="tab-pane fade" id="systemNetworkInterfaces" role="tabpanel" aria-labelledby="systemNetworkInterfaces">
            <!-- Use Bootstrap Cards to display the data -->
            <div class="row">
                <div class="col-md-6" v-for="(item, index) in systemInfo.network_interfaces" :key="index">
                    <div class="card">
                        <div class="card-body">
                            <h3 class="card-title">{{ index }}</h3>
                            <h4>MAC Addr : {{ item.mac_address }}</h4>
                            <table class="table table-striped table-bordered table-sm">
                                <thead>
                                    <th>
                                        family
                                    </th>
                                    <th>
                                        Address
                                    </th>
                                    <th>
                                        Netmask
                                    </th>
                                    <th>
                                        Broadcast
                                    </th>
                                </thead>
                                <tbody v-if="item.IPv4 && item.IPv6">
                                    <tr>
                                        <td>
                                            IPv4
                                        </td>
                                        <td>
                                            {{ item.IPv4.address }}
                                        </td>
                                        <td>
                                            {{ item.IPv4.netmask }}
                                        </td>
                                        <td>
                                            {{ item.IPv4.broadcast }}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            IPv6
                                        </td>
                                        <td>
                                            {{ item.IPv6.address }}
                                        </td>
                                        <td>
                                            {{ item.IPv6.netmask }}
                                        </td>
                                        <td>
                                            {{ item.IPv6.broadcast }}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
    import axios from 'axios';
    
    export default {
      name: 'SystemInformationTab',
      data() {
        return {
          systemInfo: {},
        };
      },
      mounted() {
        this.getSystemInformation();
      },
      methods: {
        async getSystemInformation() {
          try {
            // Get the ID from the URL
            const id = this.$route.params.id;

            // Retrieve JWT token from session storage
            const jwtToken = sessionStorage.getItem('jwtToken');
            const API_URL  =  "http://localhost:5000/sysinfo/"+id
            const response = await axios.get(API_URL, {
              headers: {
                Authorization: jwtToken,
              },
            });
    
            this.systemInfo = response.data;
          } catch (error) {
            console.error('Error fetching agents:', error);
          }
        },
        formatToLocalTime(utcTime) {
            // Create a Date object from the UTC time
            const utcDate = new Date(utcTime);

            // Format the date and time to the user's locale and timezone
            const formattedTime = utcDate.toLocaleString(undefined, {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            timeZoneName: 'short',
            hour12: false,
            });

            return formattedTime;
        },
        // Function to calculate the difference between two datetime values
        calculateDatetimeDifference(datetime1) {
            // Parse the datetime strings into Date objects
            const date1 = new Date(datetime1);
            const date2 = new Date();

            // Calculate the time difference in milliseconds
            const timeDifference = Math.abs(date1 - date2);

            // Calculate the difference in days, hours, minutes, and seconds
            const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
            const hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);
            
            if (seconds > 0){
                if(minutes > 0){
                    if(hours > 0){
                        if(days > 0){
                            return days.toString()+" days "+hours.toString()+" hours "+minutes.toString()+" minutes "+seconds.toString()+" seconds ago"
                        }
                        return hours.toString()+" hours "+minutes.toString()+" minutes "+seconds.toString()+" seconds ago"
                    }
                    return minutes.toString()+" minutes "+seconds.toString()+" seconds ago"
                }
                return seconds.toString()+" seconds ago"
            }
        }
      },
    };
</script>

<style>

</style>