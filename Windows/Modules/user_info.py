#!/usr/bin/env python3

# Libraries
##############################################################################
import subprocess
import logging
##############################################################################

# Functions
##############################################################################
def get_user_info():
    """
    Retrieve information about the user accounts on the system.
    """
    user_info = []

    try:
        output = subprocess.check_output(
            'wmic useraccount get name,sid', 
            shell=True, 
            universal_newlines=True
        )
        lines = output.strip().split('\n')
        for line in lines[1:]:
            values = line.strip().split()
            if len(values) == 2:
                name, sid = values
                user_info.append({
                    'name': name,
                    'sid': sid
                })
    except Exception as e:
        # Log the error
        logging.error(e)

    return user_info
##############################################################################