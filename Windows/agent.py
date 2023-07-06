import platform
import psutil
import math
import winreg
import subprocess
import win32com.client
import json
from datetime import datetime
import docker

def get_system_info():
    """
    Retrieve system information including operating system, CPU, memory, disks, installed programs,
    user information, service details, audit policies, BitLocker status, Windows update history, and missing updates.
    """
    system_info = {}

    # Operating System
    system_info['system'] = platform.system()
    system_info['release'] = platform.release()
    system_info['version'] = platform.version()

    # CPU Information
    system_info['cpu'] = platform.processor()
    system_info['cpu_cores'] = psutil.cpu_count(logical=False)
    system_info['cpu_threads'] = psutil.cpu_count(logical=True)

    # Memory Information
    memory = psutil.virtual_memory()
    system_info['total_memory'] = convert_size(memory.total)
    system_info['available_memory'] = convert_size(memory.available)
    system_info['memory_percent'] = memory.percent

    # Disk Information
    partitions = psutil.disk_partitions()
    disk_info = []
    for partition in partitions:
        if platform.system() == 'Windows':
            if 'cdrom' in partition.opts or partition.fstype == '':
                continue

        disk_usage = psutil.disk_usage(partition.mountpoint)
        disk = {
            'device': partition.device,
            'mountpoint': partition.mountpoint,
            'filesystem': partition.fstype,
            'total_size': convert_size(disk_usage.total),
            'used_size': convert_size(disk_usage.used),
            'free_size': convert_size(disk_usage.free),
            'usage_percent': disk_usage.percent
        }

        # BitLocker Status
        bitlocker_status = check_bitlocker_status(partition.device)
        disk['bitlocker_status'] = bitlocker_status

        disk_info.append(disk)

    system_info['disks'] = disk_info

    # Installed Programs
    installed_programs = get_installed_programs()
    system_info['installed_programs'] = installed_programs

    # User Information
    user_info = get_user_info()
    system_info['users'] = user_info

    # Service Information
    service_info = get_service_info()
    system_info['services'] = service_info

    # Audit Policies
    audit_policies = get_audit_policies()
    system_info['audit_policies'] = audit_policies

    # Windows Update History
    update_history = get_update_history()
    system_info['update_history'] = update_history

    # Missing Updates
    missing_updates = check_missing_updates()
    categorized_updates = categorize_updates(missing_updates)
    system_info['missing_updates'] = categorized_updates

    # Docker Information
    if check_docker_installed():
        docker_info = get_docker_info()
        system_info['docker_info'] = docker_info
    else:
        system_info['docker_info'] = {"running": False}

    return system_info


def convert_size(size_bytes):
    """
    Convert the size in bytes to a more human-readable format.
    """
    if size_bytes == 0:
        return "0B"
    size_names = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    i = int(math.log(size_bytes, 1024))
    size = round(size_bytes / (1024 ** i), 2)
    return f"{size} {size_names[i]}"


def get_installed_programs():
    """
    Retrieve a list of installed programs and their versions from the Windows Registry.
    """
    installed_programs = []

    # Registry paths to search for installed programs
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    try:
        # Machine-wide installed programs
        for reg_path in reg_paths:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            num_subkeys = winreg.QueryInfoKey(reg_key)[0]

            for i in range(num_subkeys):
                subkey_name = winreg.EnumKey(reg_key, i)
                subkey_path = rf"{reg_path}\{subkey_name}"
                subkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)

                try:
                    program_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    program_version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                    installed_programs.append({
                        'name': program_name,
                        'version': program_version
                    })
                except WindowsError:
                    continue

                winreg.CloseKey(subkey)

            winreg.CloseKey(reg_key)

        # User-specific installed programs
        users = get_user_info()
        for user in users:
            user_reg_path = rf"HKEY_USERS\{user['sid']}\Software\Microsoft\Windows\CurrentVersion\Uninstall"
            reg_key = winreg.OpenKey(winreg.HKEY_USERS, user_reg_path, 0, winreg.KEY_READ)
            num_subkeys = winreg.QueryInfoKey(reg_key)[0]

            for i in range(num_subkeys):
                subkey_name = winreg.EnumKey(reg_key, i)
                subkey_path = rf"{user_reg_path}\{subkey_name}"
                subkey = winreg.OpenKey(winreg.HKEY_USERS, subkey_path, 0, winreg.KEY_READ)

                try:
                    program_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    program_version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                    installed_programs.append({
                        'name': program_name,
                        'version': program_version
                    })
                except WindowsError:
                    continue

                winreg.CloseKey(subkey)

            winreg.CloseKey(reg_key)
    except WindowsError:
        pass

    return installed_programs


def get_user_info():
    """
    Retrieve information about the user accounts on the system.
    """
    user_info = []

    try:
        output = subprocess.check_output('wmic useraccount get name,sid', shell=True, universal_newlines=True)
        lines = output.strip().split('\n')
        for line in lines[1:]:
            values = line.strip().split()
            if len(values) == 2:
                name, sid = values
                user_info.append({
                    'name': name,
                    'sid': sid
                })
    except subprocess.CalledProcessError:
        pass

    return user_info


def get_service_info():
    """
    Retrieve information about the services running on the system.
    """
    service_info = []

    try:
        output = subprocess.check_output('wmic service get name,state,startmode,pathname,displayname /format:csv',
                                         shell=True, universal_newlines=True)
        lines = output.strip().split('\n')
        header = [h.strip().lower() for h in lines[0].strip().split(',')]

        for line in lines[1:]:
            values = line.strip().split(',')
            if len(values) == len(header):
                service = {header[i]: value.strip() for i, value in enumerate(values)}
                service_info.append(service)
    except subprocess.CalledProcessError:
        pass

    return service_info


def get_audit_policies():
    """
    Retrieve the audit policies configured on the system.
    """
    audit_policies = []

    try:
        output = subprocess.check_output('auditpol /get /category:*', shell=True, universal_newlines=True)
        lines = output.strip().split('\n')
        for line in lines[2:]:
            values = line.strip().split()
            if len(values) >= 4:
                category = ' '.join(values[:-3])
                subcategory = values[-3]
                setting = values[-2]
                success = values[-1] == 'Success'
                audit_policies.append({
                    'category': category,
                    'subcategory': subcategory,
                    'setting': setting,
                    'success': success
                })
    except subprocess.CalledProcessError:
        pass

    return audit_policies


def check_bitlocker_status(device):
    """
    Check the BitLocker protection status of a disk.
    """
    device = device.replace("\\", "")

    try:
        output = subprocess.check_output(f'manage-bde -status {device}', shell=True, universal_newlines=True)
        lines = output.strip().split('\n')
        for line in lines:
            if line.strip().startswith('Protection Status:'):
                status = line.split(':', 1)[1].strip()
                return status
    except subprocess.CalledProcessError:
        pass

    return 'Unknown'


def get_update_history():
    update_history = []

    try:
        update_session = win32com.client.Dispatch("Microsoft.Update.Session")
        update_searcher = update_session.CreateUpdateSearcher()

        search_result = update_searcher.QueryHistory(0, update_searcher.GetTotalHistoryCount())

        for update in search_result:
            update_info = {
                'title': update.Title,
                'description': update.Description,
                'operation': update.Operation,
                'result_code': update.ResultCode,
                'date': update.Date.strftime('%Y-%m-%d %H:%M:%S'),
            }
            update_history.append(update_info)
    except Exception:
        pass

    return update_history


def check_missing_updates():
    """
    Check for missing Windows updates.
    """
    missing_updates = []

    try:
        update_session = win32com.client.Dispatch("Microsoft.Update.Session")
        update_searcher = update_session.CreateUpdateSearcher()

        # Search for updates
        search_result = update_searcher.Search("IsInstalled=0")

        for update in search_result.Updates:
            missing_update = {
                'title': update.Title,
                'description': update.Description,
                'category': update.Categories[0].Name if update.Categories else 'Uncategorized'
            }
            missing_updates.append(missing_update)
    except Exception:
        pass

    return missing_updates


def categorize_updates(updates):
    """
    Categorize the list of updates based on their classification.
    """
    categorized_updates = {}

    for update in updates:
        if update['category'] not in categorized_updates:
            categorized_updates[update['category']] = []
        categorized_updates[update['category']].append(update)

    return categorized_updates


def check_docker_installed() -> bool:
    try:
        client = docker.from_env()
        client.ping()
        return True
    except:
        return False
    finally:
        client.close()


def get_docker_info():
    # Connect to the Docker daemon
    client = docker.from_env()

    # Get Docker images
    images = client.images.list()

    # Get Docker containers
    containers = client.containers.list(all=True)

    # Get Docker volumes
    volumes = client.volumes.list()

    # Get Docker networks
    networks = client.networks.list()

    # Get Docker disk usage
    disk_usage = client.df()

    # Prepare Docker information
    docker_info = {
        "running": True,
        "images": [],
        "containers": [],
        "volumes": [],
        "networks": [],
        "disk_usage": {
            "total_space": convert_size(disk_usage["LayersSize"])
        }
    }

    # Collect Docker image information
    for image in images:
        docker_info["images"].append({
            "image_id": image.id,
            "tags": image.tags,
            "size": convert_size(image.attrs["Size"]),
            "created": image.attrs["Created"],
            "labels": image.attrs["ContainerConfig"]["Labels"]
        })

    # Collect Docker container information
    for container in containers:
        docker_info["containers"].append({
            "container_id": container.id,
            "image": container.attrs["Config"]["Image"],
            "status": container.attrs["State"]["Status"],
            "ports": container.attrs["NetworkSettings"]["Ports"],
            "networks": container.attrs["NetworkSettings"]["Networks"],
            "created": container.attrs["Created"],
            "labels": container.attrs["Config"]["Labels"]
        })

    # Collect Docker volume information
    for volume in volumes:
        docker_info["volumes"].append({
            "volume_name": volume.name,
            "mountpoint": volume.attrs["Mountpoint"],
            "created": volume.attrs["CreatedAt"],
            "labels": volume.attrs["Labels"]
        })

    # Collect Docker network information
    for network in networks:
        docker_info["networks"].append({
            "network_id": network.id,
            "name": network.name,
            "driver": network.attrs["Driver"],
            "created": network.attrs["Created"],
            "labels": network.attrs["Labels"]
        })

    return docker_info

# Usage
system_info = get_system_info()
json_data = json.dumps(system_info, indent=4)
print(json_data)
