import axios from 'axios';

// Global Variables
const API_URL  =  "http://localhost:5000"
const SYS_INFO_EP = "/sysinfo/"
const SYS_USR_EP = "/sysusers/"
const SYS_APPS_EP = "/sysapps/"
const SYS_SRVCS_EP = "/sysservices/"
const CHLG_EP = "/changelog"

// Retrive System Information
export async function getSystemInformation(agentId){
    try {
        // Retrieve JWT token from session storage
        const jwtToken = sessionStorage.getItem('jwtToken');
        const URL = API_URL + SYS_INFO_EP + agentId;
        const response =  await axios.get(URL, {
            headers: {
                Authorization: jwtToken,
            },
        });
        return response.data;
    } catch(error) {
        console.error('Error fetching System Information:', error);
    }
}

// Retrive System Information Changelog
export async function getSysInfoChangeLog(sysInfoId){
    try {
        // Retrieve JWT token from session storage
        const jwtToken = sessionStorage.getItem('jwtToken');
        const URL = API_URL + SYS_INFO_EP + sysInfoId + CHLG_EP;
        const changelog = await axios.get(URL, {
            headers: {
            Authorization: jwtToken,
            },
        });
        return changelog.data
    } catch (error) {
        console.error('Error fetching System Information Changelog:', error);
    }
}

// Retrive System Users
export async function getSystemUsers(agentId){
    try {
        // Retrieve JWT token from session storage
        const jwtToken = sessionStorage.getItem('jwtToken');
        const URL = API_URL + SYS_USR_EP + agentId;
        const response = await axios.get(URL, {
            headers: {
                Authorization: jwtToken,
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching System Users:', error);
    }
}

// Retrive System Users Changelog
export async function getSysUsersChangeLog(sysUsersId){
    try {
        // Retrieve JWT token from session storage
        const jwtToken = sessionStorage.getItem('jwtToken');
        const URL = API_URL + SYS_USR_EP + sysUsersId + CHLG_EP;
        const changelog = await axios.get(URL, {
            headers: {
            Authorization: jwtToken,
            },
        });
        return changelog.data
    } catch (error) {
        console.error('Error fetching System Users Changelog:', error);
    }
}

// Retrive System Apps
export async function getInstalledApps(agentId){
    try {
        // Retrieve JWT token from session storage
        const jwtToken = sessionStorage.getItem('jwtToken');
        const URL = API_URL + SYS_APPS_EP + agentId;
        const response = await axios.get(URL, {
            headers: {
                Authorization: jwtToken,
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching System Apps:', error);
    }
}

// Retrive System Users Changelog
export async function getInstalledAppsChangeLog(sysInstalledAppsId){
    try {
        // Retrieve JWT token from session storage
        const jwtToken = sessionStorage.getItem('jwtToken');
        const URL = API_URL + SYS_APPS_EP + sysInstalledAppsId + CHLG_EP;
        const changelog = await axios.get(URL, {
            headers: {
            Authorization: jwtToken,
            },
        });
        return changelog.data
    } catch (error) {
        console.error('Error fetching System Apps Changelog:', error);
    }
}

// Retrive System Services
export async function getServices(agentId){
    try {
        // Retrieve JWT token from session storage
        const jwtToken = sessionStorage.getItem('jwtToken');
        const URL = API_URL + SYS_SRVCS_EP + agentId;
        const response = await axios.get(URL, {
            headers: {
                Authorization: jwtToken,
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching System Services:', error);
    }
}

// Retrive System Services Changelog
export async function getServicesChangeLog(sysServicesId){
    try {
        // Retrieve JWT token from session storage
        const jwtToken = sessionStorage.getItem('jwtToken');
        const URL = API_URL + SYS_SRVCS_EP + sysServicesId + CHLG_EP;
        const changelog = await axios.get(URL, {
            headers: {
            Authorization: jwtToken,
            },
        });
        return changelog.data
    } catch (error) {
        console.error('Error fetching System Services Changelog:', error);
    }
}