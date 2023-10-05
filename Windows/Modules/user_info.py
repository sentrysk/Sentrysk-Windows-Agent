#!/usr/bin/env python3

# Libraries
##############################################################################
import win32net
import win32netcon
import pywintypes
import datetime
import logging
##############################################################################

# Global Values
##############################################################################
# Define constants for user account flags
USER_FLAGS = {
    win32netcon.UF_SCRIPT: "Logon script is executed",
    win32netcon.UF_ACCOUNTDISABLE: "Account is disabled",
    win32netcon.UF_HOMEDIR_REQUIRED: "User requires a home directory",
    win32netcon.UF_PASSWD_NOTREQD: "No password is required",
    win32netcon.UF_PASSWD_CANT_CHANGE: "User cannot change the password",
    win32netcon.UF_LOCKOUT: "Account is locked out",
    win32netcon.UF_DONT_EXPIRE_PASSWD: "Password does not expire",
    win32netcon.UF_NORMAL_ACCOUNT: "Normal user account",
    win32netcon.UF_TEMP_DUPLICATE_ACCOUNT: "Temporary duplicate account",
    win32netcon.UF_INTERDOMAIN_TRUST_ACCOUNT: "Interdomain trust account",
    win32netcon.UF_WORKSTATION_TRUST_ACCOUNT: "Workstation trust account",
    win32netcon.UF_SERVER_TRUST_ACCOUNT: "Server trust account",
}
##############################################################################

# Functions
##############################################################################
def get_user_sid(username):
    try:
        user_info = win32net.NetUserGetInfo(None, username, 4)  # Level 4 returns the user's SID
        sid_str = str(user_info['user_sid'])  # Convert the SID to a string
        # Remove the "PySID:" section from the SID
        if sid_str.startswith("PySID:"):
            sid_str = sid_str[6:]
        return sid_str
    except pywintypes.error:
        return "N/A"
    
def get_user_info():
    """
    Retrieve information about the user accounts on the system.
    """
    users = []

    """
    Explanation of the line 71

    2: 
    This is the level of information we want to retrieve. 
    Level 2 provides detailed information about user accounts, including their names, full names, comments, and other attributes.

    win32netcon.FILTER_NORMAL_ACCOUNT: T
    his parameter specifies that we want to filter the results to include only normal user accounts. 
    It excludes system accounts and other types of accounts.

    resume: 
    This variable is used to keep track of the position in the user account enumeration. 
    The win32net.NetUserEnum function may return a large number of user accounts, 
    so it can be called multiple times with an updated resume value to retrieve the next batch of results. 
    It starts at 0 and is updated by the function with each call to enumerate more users.
    """

    try:
        resume = 0
        while True:
            user_data, total, resume = win32net.NetUserEnum(None, 2, win32netcon.FILTER_NORMAL_ACCOUNT, resume)
            for user_info in user_data:
                last_logon_timestamp = user_info['last_logon']
                last_logon_datetime = datetime.datetime.fromtimestamp(last_logon_timestamp)
                user_flags = [flag_name for flag, flag_name in USER_FLAGS.items() if user_info['flags'] & flag]
                user_sid = get_user_sid(user_info['name'])
                users.append({
                    "username": user_info['name'],
                    "full_name": user_info['full_name'],
                    "comment": user_info['comment'],
                    "last_logon": last_logon_datetime.strftime("%Y-%m-%d %H:%M:%S"),  # Convert to a formatted string
                    "flags": user_flags,
                    "sid": user_sid,  # Include the SID as a string
                })
            if resume == 0:
                break
        return users
    except Exception as e:
        # Log the error
        logging.error(e)

    return users
##############################################################################