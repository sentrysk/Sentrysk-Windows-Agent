#!/usr/bin/env python3

# Libraries
##############################################################################
import subprocess
##############################################################################

# Functions
##############################################################################
def get_service_info():
    """
    Retrieve information about the services running on the system.
    """
    service_info = []

    try:
        output = subprocess.check_output(
            'wmic service get name,state,startmode,pathname,displayname /format:csv',
            shell=True, 
            universal_newlines=True
        )
        lines = output.strip().split('\n')
        header = [h.strip().lower() for h in lines[0].strip().split(',')]

        for line in lines[1:]:
            values = line.strip().split(',')
            if len(values) == len(header):
                service = {
                    header[i]: value.strip() for i, value in enumerate(values)
                }
                service_info.append(service)
    except subprocess.CalledProcessError:
        pass

    return service_info
##############################################################################