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

        # Remove the Node section & change naming
        for service in service_info:
            # Change Name to service_name
            service["service_name"] = service["Name"]
            del service["Name"]
            # Change DisplayName to display_name
            service["display_name"] = service["DisplayName"]
            del service["DisplayName"]
            # Change State to status
            service["status"] = service["State"]
            del service["State"]
            # Change Description to description
            service["description"] = service["Description"]
            del service["Description"]
            # Delete Node
            del service["Node"]
    except Exception as e:
        # Log the error
        logging.error(e)

    return service_info
##############################################################################