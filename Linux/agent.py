#!/usr/bin/env python3

# Libraries
##############################################################################
import json
from configparser import ConfigParser

from Modules.system_info import get_system_info
from Modules.user_info import get_user_info
from Modules.installed_apps import get_installed_programs
from Modules.npm_info import get_npm_packages
from Modules.service_info import get_service_info
from Modules.pip_info import get_pip_packages
from Modules.docker_info import get_docker_info
##############################################################################

# Configs
##############################################################################
CONFIG_FILE = 'config.ini'

config = ConfigParser()
config.read(CONFIG_FILE)

DASHBOARD_URL = config.get('dashboard','url')
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
##############################################################################


# Usage
json_data = json.dumps(system_info, indent=4)
with open('result.json','w') as f:
    f.write(json_data)
print(json_data)
