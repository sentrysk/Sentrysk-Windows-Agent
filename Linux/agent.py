#!/usr/bin/env python3

# Libraries
##############################################################################
import json
import os
import logging

from Modules.system_info import get_system_info
from Modules.user_info import get_user_info
from Modules.installed_apps import get_installed_programs
from Modules.npm_info import get_npm_packages
from Modules.service_info import get_service_info
from Modules.pip_info import get_pip_packages
from Modules.docker_info import get_docker_info
from Modules.last_logon import get_last_logons
##############################################################################

# Configs
##############################################################################
def load_config(file_path):
    with open(file_path, 'r') as file:
        config_data = json.load(file)
    return config_data

# Specify the path to your JSON configuration file
config_file_path = 'config.json'

# Load configuration from the JSON file
config = load_config(config_file_path)

# Extract information from the configuration
base_url = config['api']['base_url']
endpoints = config['api']['endpoints']
agent_token = config['api']['agent_token']

home_dir = config['dirs']['home_dir']
logs_dir = os.path.join(home_dir,'logs')
logfile_relative_path = config['dirs']['logfile']
logfile_path = os.path.join(home_dir, logfile_relative_path)

# Check if path not exist, create new one
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

FORMAT = '%(asctime)s :: %(levelname)-6s :: %(name)s :: [%(filename)s:%(lineno)s - %(funcName)s()] :: %(message)s'
# Configure logging to write logs to a log file
logging.basicConfig(
    filename=logfile_path,
    level=logging.INFO,
    format=FORMAT,
    encoding='utf-8'
)
##############################################################################

# Functions
##############################################################################
"""
    Retrieve system information.
"""

system_info = {}

system_info['system']               = get_system_info()
system_info['users']                = get_user_info()
system_info['installed_programs']   = get_installed_programs()
system_info['npm_info']             = get_npm_packages()
system_info['services']             = get_service_info()
system_info['pip_info']             = get_pip_packages()
system_info['docker_info']          = get_docker_info()
system_info['last_logons']          = get_last_logons()
##############################################################################


# Usage
json_data = json.dumps(system_info, indent=4)
with open('result.json','w') as f:
    f.write(json_data)
print(json_data)
