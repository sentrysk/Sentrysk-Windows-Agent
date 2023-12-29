#!/usr/bin/env python3

# Libraries
##############################################################################

from SystemUsers.models import SystemUsers

##############################################################################


# Functions

# Get User Count By Agent ID
##############################################################################
def get_sys_user_count_by_agent_id(agent_id):
    try:
        # Get System Users
        sys_users = SystemUsers.objects(agent=agent_id).first()
        # If exist
        if sys_users:
            return len(sys_users.users)
        return 0
    except Exception as e:
        return 0
##############################################################################