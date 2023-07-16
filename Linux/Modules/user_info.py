#!/usr/bin/env python3

# Libraries
##############################################################################
import subprocess
##############################################################################

# Functions
##############################################################################
def get_users():
    try:
        # Execute the 'getent' command to retrieve the list of users
        result = subprocess.run(
            ['getent', 'passwd'], 
            capture_output=True, 
            text=True
        )

        # Check the command's exit status
        if result.returncode == 0:
            # Parse the output and extract user information
            user_list = result.stdout.strip().split('\n')
            users = []
            for user_info in user_list:
                user_data = user_info.split(':')
                user = {
                    'username': user_data[0],
                    'uid': user_data[2],
                    'gid': user_data[3],
                    'home_directory': user_data[5],
                    'shell': user_data[6]
                }
                users.append(user)
            
            return users
        else:
            print(f"Error: {result.stderr}")
            return []
    except FileNotFoundError:
        print("The 'getent' command is not available on your system.")
        return []
##############################################################################
