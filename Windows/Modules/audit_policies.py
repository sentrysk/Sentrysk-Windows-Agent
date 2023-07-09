#!/usr/bin/env python3

# Libraries
##############################################################################
import subprocess
##############################################################################

# Functions
##############################################################################
def get_audit_policies():
    """
    Retrieve the audit policies configured on the system.
    """
    audit_policies = []

    try:
        output = subprocess.check_output('auditpol /get /category:*',
            shell=True, 
            universal_newlines=True
        )
        lines = output.strip().split('\n')
        for line in lines[2:]:
            values = line.strip().split()
            if len(values) >= 4:
                category = ' '.join(values[:-3])
                subcategory = values[-3]
                setting = values[-2]
                success = values[-1] == 'Success'
                audit_policies.append({
                    'category': category,
                    'subcategory': subcategory,
                    'setting': setting,
                    'success': success
                })
    except subprocess.CalledProcessError:
        pass

    return audit_policies
##############################################################################


