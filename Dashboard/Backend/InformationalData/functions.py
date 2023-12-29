#!/usr/bin/env python3

# Libraries
##############################################################################

from SystemUsers.models import SystemUsers, ChangeLogSystemUsers

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
    
# Get User ChangeLog Count By Agent ID
##############################################################################
def get_sys_user_changelog_entry_count_by_agent_id(agent_id):
    chlg_count = 0
    try:
        # Get System Users
        sys_users = SystemUsers.objects(agent=agent_id).first()
        # If exist
        if sys_users:
            # Get ChangeLogs
            sys_users_chlg = ChangeLogSystemUsers.objects(sys_users=sys_users)
            # If any ChangeLog exists
            if sys_users_chlg:
                # Iterate over ChangeLogs
                for chlg in sys_users_chlg:
                    if chlg.changes.get('new_users'):
                        chlg_count = chlg_count + len(chlg.changes.get('new_users'))
                    
                    if chlg.changes.get('deleted_users'):
                        chlg_count = chlg_count + len(chlg.changes.get('deleted_users'))
                    
                    if chlg.changes.get('updated_users'):
                        chlg_count = chlg_count + len(chlg.changes.get('updated_users'))

        return chlg_count
    except Exception as e:
        print(e)
        return chlg_count
##############################################################################