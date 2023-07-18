#!/usr/bin/env python3

# Libraries
##############################################################################

##############################################################################

# Functions
##############################################################################
def get_user_info():
    try:
        with open('/etc/passwd', 'r') as passwd_file:
            users = []
            for line in passwd_file:
                user_info = line.strip().split(':')
                user = {
                    'username': user_info[0],
                    'uid': user_info[2],
                    'gid': user_info[3],
                    'home_directory': user_info[5],
                    'shell': user_info[6]
                }
                users.append(user)
            
            return users
    except FileNotFoundError:
        print("The /etc/passwd file does not exist.")
        return []
##############################################################################