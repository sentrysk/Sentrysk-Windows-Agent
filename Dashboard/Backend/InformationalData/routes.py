#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, jsonify

from Shared.validators import auth_token_required
from .functions import (
    get_agent_count,
    get_sys_user_count_by_agent_id,
    get_sys_user_changelog_entry_count_by_agent_id,
    get_last_logons_by_agent_id,
    get_sys_installed_apps_count_by_agent_id
)
##############################################################################

# Blueprint
##############################################################################
inf_data_bp = Blueprint('informational_data', __name__)
##############################################################################


# Routes 
##############################################################################

# About Agents
##############################################################################
# Get Agent Count
@inf_data_bp.route('/agent_count', methods=['GET'])
@auth_token_required
def agent_count():  
    return jsonify({
        "agent_count": str(get_agent_count())
    })
##############################################################################

# About Users
##############################################################################
# Get Sys User Count by Agent ID
@inf_data_bp.route('/user_count/<agent_id>', methods=['GET'])
@auth_token_required
def sys_user_count_by_agent_id(agent_id):
    sys_user_count = get_sys_user_count_by_agent_id(agent_id)
    
    return jsonify({
        "user_count": str(sys_user_count)
    })

# Get Sys User ChangeLog Count by Agent ID
@inf_data_bp.route('/user_changelog_count/<agent_id>', methods=['GET'])
@auth_token_required
def sys_user_changelog_count_by_agent_id(agent_id):
    user_changelog_count = get_sys_user_changelog_entry_count_by_agent_id(agent_id)
    
    return jsonify({
        "user_changelog_count": str(user_changelog_count)
    })

# Get Sys Users Last Logons Count by Agent ID
@inf_data_bp.route('/user_last_logons_count/<agent_id>', methods=['GET'])
@auth_token_required
def sys_user_last_logons_count_by_agent_id(agent_id):
    user_last_logons_count = get_last_logons_by_agent_id(agent_id)
    
    return jsonify({
        "user_last_logons_count": str(user_last_logons_count)
    })
##############################################################################


# About Installed Apps
##############################################################################

# Get Installed Apps Count by Agent ID
@inf_data_bp.route('/installed_apps_count/<agent_id>', methods=['GET'])
@auth_token_required
def installed_apps_count_by_agent_id(agent_id):  
    return jsonify({
        "installed_apps_count": str(get_sys_installed_apps_count_by_agent_id(agent_id))
    })

##############################################################################

##############################################################################