#!/usr/bin/env python3

# Libraries
##############################################################################
import subprocess
import json
##############################################################################


# Functions
############################################################################## 
last_logons = []

for line in subprocess.check_output(["last", "-w"]).decode("utf-8").splitlines():
    fields = line.split()
    if len(fields) >= 7:
        user = fields[0]
        last_logon = f"{fields[3]} {fields[4]} {fields[5]}"
        last_logons.append({
            "username": user, 
            "last_logon": last_logon
        })

return last_logons
##############################################################################