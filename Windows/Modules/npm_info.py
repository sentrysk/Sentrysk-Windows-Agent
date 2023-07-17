#!/usr/bin/env python3

# Libraries
##############################################################################
import json
import subprocess
import sys
import logging
from datetime import datetime
import os
##############################################################################

# Configs
##############################################################################

# Configure logging to write errors to a log file
logfile = os.path.dirname(os.path.realpath(__file__)) + "\\error.log"
logging.basicConfig(filename=logfile, level=logging.ERROR)

##############################################################################


# Global Values
##############################################################################
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
##############################################################################


# Functions
##############################################################################
def get_npm_packages():
    try:
        # Check if npm is installed
        subprocess.run('npm -v', capture_output=True, check=True, shell=True)

        # NPM is installed, collect packages and versions
        completed_process = subprocess.run(
            'npm list --depth=0 --json', 
            capture_output=True, 
            check=True, 
            shell=True
        )
        package_list = json.loads(completed_process.stdout)['dependencies']
        
        npm_data = json.loads('{"installed":true, "packages":""}')
        package_data = []
        for package_name, package_info in package_list.items():
            package = {"name": package_name, "version": package_info['version']}
            package_data.append(package)

        npm_data["packages"] = package_data

        return npm_data
    except Exception as e:
        # Log the error with date and time
        timestamp = datetime.now().strftime(TIME_FORMAT)
        logging.error(f'[{timestamp}] Error: {e}')
        data = {
            "running":False
        }
        return data

##############################################################################