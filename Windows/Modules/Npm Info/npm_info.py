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
def check_npm_and_collect_packages():
    try:
        # Check if npm is installed
        subprocess.run('npm -v', capture_output=True, check=True, shell=True)

        # NPM is installed, collect packages and versions
        completed_process = subprocess.run(
            'npm list --depth=0 --json safas', 
            capture_output=True, 
            check=True, 
            shell=True
        )
        package_list = json.loads(completed_process.stdout)['dependencies']
        
        npm_data = json.loads('{"npm":{"installed":true, "packages":""} }')
        package_data = []
        for package_name, package_info in package_list.items():
            package = {"name": package_name, "version": package_info['version']}
            package_data.append(package)

        npm_data["npm"]["packages"] = package_data

        return json.dumps(npm_data, indent=4)
    except subprocess.CalledProcessError as e:
        # Log the error with date and time
        timestamp = datetime.now().strftime(TIME_FORMAT)
        logging.error(f'[{timestamp}] Error executing command: {e.cmd}')
        logging.error(f'[{timestamp}] Return code: {e.returncode}')
        logging.error(f'[{timestamp}] Stdout: {e.stdout.decode().strip()}')
        logging.error(f'[{timestamp}] Stderr: {e.stderr.decode().strip()}')
        sys.exit(1)
    except FileNotFoundError:
        # Log the error with date and time
        timestamp = datetime.now().strftime(TIME_FORMAT)
        return json.dumps(
            {
                "npm":{
                    "installed":False
                }
        })
##############################################################################