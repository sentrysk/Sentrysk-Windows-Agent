#!/usr/bin/env python3

# Libraries
##############################################################################
import platform
import psutil
import subprocess
import psutil
import socket
import wmi
import logging

from .helper_funcs import convert_size
##############################################################################

# Functions
##############################################################################
def get_system_info():
    """
    Retrieve system information including operating system, domain, CPU, 
    memory, disks, and network interfaces.
    """
    system_info = {
        "os": {},
        "domain": {},
        "cpu": {},
        "memory": {},
        "disks": {},
        "network_interfaces": {}
    }

    # Operating System
    system_info['os']['system'] = platform.system()
    system_info['os']['release'] = platform.release()
    system_info['os']['version'] = platform.version()

    # Domain Information
    try:
        # Connect to the WMI service
        c = wmi.WMI()
        system_info['domain']['domain'] = c.Win32_ComputerSystem()[0].Domain
        system_info['domain']['dns_hostname'] = c.Win32_ComputerSystem()[0].DNSHostName
    except Exception as e:
        # Log the error
        logging.error(e)

    # CPU Information
    system_info['cpu']['cpu'] = platform.processor()
    system_info['cpu']['cpu_cores'] = psutil.cpu_count(logical=False)
    system_info['cpu']['cpu_threads'] = psutil.cpu_count(logical=True)

    # Memory Information
    memory = psutil.virtual_memory()
    system_info['memory']['total_memory'] = convert_size(memory.total)
    system_info['memory']['available_memory'] = convert_size(memory.available)
    system_info['memory']['memory_percent'] = memory.percent

    # Disk Information
    partitions = psutil.disk_partitions()
    disk_info = {}
    for partition in partitions:
        if platform.system() == 'Windows':
            if 'cdrom' in partition.opts or partition.fstype == '':
                continue

        disk_usage = psutil.disk_usage(partition.mountpoint)
        disk_info[partition.device] = {
            'device': partition.device,
            'mountpoint': partition.mountpoint,
            'filesystem': partition.fstype,
            'total_size': convert_size(disk_usage.total),
            'used_size': convert_size(disk_usage.used),
            'free_size': convert_size(disk_usage.free),
            'usage_percent': disk_usage.percent,
            'bitlocker_status': check_bitlocker_status(partition.device)
        }

    system_info['disks'] = disk_info

    # Network Information
    system_info['network_interfaces'] = get_network_info()

    return system_info


def check_bitlocker_status(device):
    """
    Check the BitLocker protection status of a disk.
    """
    device = device.replace("\\", "")

    try:
        output = subprocess.check_output(f'manage-bde -status {device}',
            shell=True,
            universal_newlines=True
        )
        lines = output.strip().split('\n')
        for line in lines:
            if line.strip().startswith('Protection Status:'):
                status = line.split(':', 1)[1].strip()
                return status
    except Exception as e:
        # Log the error
        logging.error(e)

    return 'Unknown'


def get_network_info():
    """
    Get network interfaces and their addresses using psutil
    """
    interfaces = psutil.net_if_addrs()

    network_info = {}
    for name, addresses in interfaces.items():
        network_info[name] = { 
            'mac_address': ''
        }

        for address in addresses:
            if address.family == socket.AF_INET:
                # IPv4 address
                network_info[name]['IPv4'] = {
                    'ip_address': address.address,
                    'netmask': address.netmask,
                    'broadcast': address.broadcast
                }

            if address.family == socket.AF_INET6:
                # IPv6 address
                network_info[name]['IPv6'] = {
                    'ip_address': address.address,
                    'netmask': address.netmask,
                    'broadcast': None
                }

            if address.family == psutil.AF_LINK:
                # MAC address
                network_info[name]['mac_address'] = address.address

    return network_info
##############################################################################