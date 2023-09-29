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
    system_info["os"]["name"] = platform.system()
    system_info["os"]["version"] = platform.mac_ver()[0]

    # Collect domain/host information
    system_info["domain"]["hostname"] = platform.node()
    system_info["domain"]["fqdn"] = platform.node()

    # Collect CPU information
    cpu_info = dict(psutil.cpu_info()._asdict())
    system_info["cpu"]["cpu_count"] = psutil.cpu_count(logical=False)
    system_info["cpu"]["cpu_threads"] = psutil.cpu_count(logical=True)
    system_info["cpu"]["cpu_model"] = cpu_info["brand"]
    system_info["cpu"]["cpu_architecture"] = platform.machine()

    # Collect memory information
    memory_info = dict(psutil.virtual_memory()._asdict())
    system_info["memory"]["total_memory"] = memory_info["total"]
    system_info["memory"]["available_memory"] = memory_info["available"]

    # Collect disk information
    disk_info = []
    for partition in psutil.disk_partitions():
        disk = {
            "device": partition.device,
            "mountpoint": partition.mountpoint,
            "fstype": partition.fstype,
        }
        disk_usage = psutil.disk_usage(partition.mountpoint)
        disk["total_size"] = disk_usage.total
        disk["used_size"] = disk_usage.used
        disk["free_size"] = disk_usage.free
        disk_info.append(disk)
    system_info["disks"] = disk_info

    # Collect network interface information including MAC addresses
    network_info = []
    for interface, addrs in psutil.net_if_addrs().items():
        network = {
            "interface_name": interface,
            "addresses": []
        }
        for addr in addrs:
            address = {
                "family": addr.family.name,
                "address": addr.address,
                "netmask": addr.netmask,
            }
            network["addresses"].append(address)
        
        # Add MAC address to the network interface information
        network_info.append(network)
        network_info[-1]["mac_address"] = psutil.net_if_addrs()[interface][0].address

    system_info["network_interfaces"] = network_info

    # Print the JSON result
    return system_info
