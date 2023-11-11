#!/usr/bin/env python3

# Libraries
##############################################################################
import subprocess
import logging
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
            'wmic service get DisplayName,Name,State,Description /format:csv',
            shell=True, 
            universal_newlines=True
        )
        lines = output.strip().split('\n')
        header = [h.strip() for h in lines[0].strip().split(',')]

        for line in lines[1:]:
            values = line.strip().split(',')
            if len(values) == len(header):
                service = {
                    header[i]: value.strip() for i, value in enumerate(values)
                }
                service_info.append(service)

        # Remove the Node section & change Name to ServiceName
        for service in service_info:
            service["ServiceName"] = service["Name"]
            del service["Name"]
            del service["Node"]
    except Exception as e:
        # Log the error
        logging.error(e)

    return service_info
##############################################################################