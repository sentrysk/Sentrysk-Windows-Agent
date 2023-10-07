#!/usr/bin/env python3

# Libraries
##############################################################################
import pwd
import logging
##############################################################################

# Functions
##############################################################################
def get_user_info():
    try:
        # Initialize an empty list to store user information
        users = []

        # Iterate through the user entries in the /etc/passwd file
        for entry in pwd.getpwall():
            user_info = {
                "Username": entry.pw_name,
                "UserID": entry.pw_uid,
                "GroupID": entry.pw_gid,
                "HomeDirectory": entry.pw_dir,
                "Shell": entry.pw_shell,
            }
            users.append(user_info)
            
        return users
    except Exception as e:
        # Log the error
        logging.error(e)
        return []
##############################################################################
