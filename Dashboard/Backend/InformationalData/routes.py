#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify

from SystemUsers.models import SystemUsers

##############################################################################

# Blueprint
##############################################################################
inf_data_bp = Blueprint('informational_data', __name__)
##############################################################################


# Routes 
##############################################################################
@inf_data_bp.route('/user_counts/<agent_id>', methods=['GET'])
def get_sys_user_counts_by_agent_id(agent_id):
    try:
        # Get System Users
        sys_users = SystemUsers.objects(agent=agent_id).first()
        
        # If exist
        if sys_users:
            return jsonify({
                "user_counts":str(len(sys_users.users))
            })
        return jsonify({
                "user_counts":0
        })
    except Exception as e:
        return jsonify({
                "user_counts":0
        })
##############################################################################