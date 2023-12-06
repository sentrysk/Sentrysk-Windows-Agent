#!/usr/bin/env python3

# Libraries
##############################################################################
import win32net
import win32netcon
import logging
import datetime
##############################################################################


# Functions
##############################################################################    
def get_last_logons():
    last_logons = []
    try:
        resume = 0
        while True:
            user_data, total, resume = win32net.NetUserEnum(None, 2, win32netcon.FILTER_NORMAL_ACCOUNT, resume)
            for user_info in user_data:
                last_logon_timestamp = user_info['last_logon']
                last_logon_datetime = datetime.datetime.fromtimestamp(last_logon_timestamp)
                last_logons.append({
                    "username": user_info['name'],
                    "last_logon": last_logon_datetime.strftime("%Y-%m-%d %H:%M:%S")
                })
            if resume == 0:
                break
        return last_logons
    except Exception as e:
        # Log the error
        logging.error(e)

    return last_logons
##############################################################################