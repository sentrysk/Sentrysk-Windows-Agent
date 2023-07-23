#!/usr/bin/env python3

# Libraries
##############################################################################
import pkg_resources
##############################################################################

# Functions
##############################################################################
def get_installed_packages():
    try:
        # Get a list of all installed packages using pkg_resources
        installed_packages = [
            {
                'name': package.project_name,
                'version': package.version
            }
            for package in pkg_resources.working_set
        ]
        pip_info = {
            "installed":True,
            "packages":installed_packages
        }
        return pip_info
    except Exception as e:
        pip_info = {
            "installed":False
        }
        print(f"Error: {e}")
        return pip_info
##############################################################################