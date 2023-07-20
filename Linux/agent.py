#!/usr/bin/env python3

# Libraries
##############################################################################
import json

from Modules.user_info import get_user_info
from Modules.installed_apps import get_installed_programs
from Modules.npm_info import get_npm_packages
##############################################################################

# Functions
##############################################################################
"""
    Retrieve system information.
"""

system_info = {}

system_info['users']                = get_user_info()
system_info['installed_programs']   = get_installed_programs()
system_info['npm_info']             = get_npm_packages()
##############################################################################


# Usage
json_data = json.dumps(system_info, indent=4)
with open('result.json','w') as f:
    f.write(json_data)
print(json_data)
