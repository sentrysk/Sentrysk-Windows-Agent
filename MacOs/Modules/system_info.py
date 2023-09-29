#!/usr/bin/env python3

# Libraries
##############################################################################
import psutil
import platform
import json

from .helper_funcs import convert_size
##############################################################################


# Functions
##############################################################################
def get_system_info():
    # Initialize the system_info dictionary
    system_info = {
        "os": {},
        "domain": {},
        "cpu": {},
        "memory": {},
        "disks": {},
        "network_interfaces": {}
    }

    # Collect OS information
    system_info["os"]["system"] = platform.system()
    system_info["os"]["version"] = platform.mac_ver()[0] # Os Release Version
    system_info["os"]["kernel"] = platform.release() # Kernel

    # Collect domain/host information
    system_info["domain"]["hostname"] = platform.node()
    system_info["domain"]["fqdn"] = platform.node()

    # Collect CPU information
    system_info["cpu"]["cpu_count"] = psutil.cpu_count(logical=False)
    system_info["cpu"]["cpu_threads"] = psutil.cpu_count(logical=True)
    system_info["cpu"]["cpu_model"] = platform.processor()
    system_info["cpu"]["cpu_architecture"] = platform.machine()

    # Collect memory information
    memory_info = dict(psutil.virtual_memory()._asdict())
    system_info["memory"]["total_memory"] = memory_info["total"]
    system_info["memory"]["available_memory"] = memory_info["available"]

    # Collect disk information
    for partition in psutil.disk_partitions():
        system_info["disks"][partition.device] = {
            "mountpoint": partition.mountpoint,
            "fstype": partition.fstype,
        }
        disk_usage = psutil.disk_usage(partition.mountpoint)
        system_info["disks"][partition.device]["total_size"] = disk_usage.total
        system_info["disks"][partition.device]["used_size"] = disk_usage.used
        system_info["disks"][partition.device]["free_size"] = disk_usage.free

    # Collect network interface information including MAC addresses
    for interface, addrs in psutil.net_if_addrs().items():
        system_info["network_interfaces"][interface] = {
            "mac_address": ""
        }
        for addr in addrs:
            system_info["network_interfaces"][interface][addr.family.name] = {
                "family": addr.family.name,
                "address": addr.address,
                "netmask": addr.netmask,
            }
        
        # Add MAC address to the network interface information
        system_info["network_interfaces"][interface]["mac_address"] = psutil.net_if_addrs()[interface][0].address

    # Print the JSON result
    return system_info
