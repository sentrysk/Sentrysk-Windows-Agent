#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
import json
from datetime import datetime
import pickle

from .models import SystemUsers, ChangeLogSystemUsers
from Shared.validators import agent_token_required

from Agents.helper_funcs import get_id_by_token
from Agents.models import Agent
##############################################################################

# Blueprint
##############################################################################
sys_users_bp = Blueprint('sys_users_blueprint', __name__)
##############################################################################


# Routes
##############################################################################

# Register
@sys_users_bp.route('/', methods=['POST'])
@agent_token_required
def register():
    # Get Agent Token by Authorization Header
    agent_token = request.headers.get('Authorization')
    # Get Agent ID by Token
    agent_id = get_id_by_token(agent_token)
    # Get Agent by Agent ID
    agent = Agent.objects(id=agent_id).first()

    # Get Data from Request
    data = request.get_json()

    # Validate the Request
    if 'users' not in data:
        return jsonify({'error': 'Invalid JSON data'}), 400
        
    # Get if record already exist
    sys_users = SystemUsers.objects(agent=agent).first()

    if sys_users:
        # UPDATE If System Information data already exist
        try:
            # Create SystemUsers object to Compare
            new_users_obj = SystemUsers(**data)
            new_users_obj.agent = agent

            # Find deleted, new, and updated users
            new_users, deleted_users, updated_users = sys_users.compare_users(new_users_obj)
            
            changes = {}

            if deleted_users:
                changes["deleted_users"] = deleted_users
            if new_users:
                changes["new_users"] = new_users
            if updated_users:
                changes["updated_users"] = updated_users

            # If any changes happens
            if changes:
                # Apply updates
                data["updated"] = datetime.utcnow
                sys_users.update(**data)

                # Create a new ChangeLog entry
                change_log_entry = ChangeLogSystemUsers(
                    sys_users = sys_users.id,
                    changes = changes
                )
                change_log_entry.save()
            else:
                # Apply only updated time
                sys_users.update(updated=datetime.utcnow)
                return jsonify({"message":"Nothing changed"})

        except Exception as e:
            return jsonify({'error': e}), 500
        
    else:
        # CREATE If System Information not exist 
        try:
            sys_users = SystemUsers(**data)
            sys_users.agent = agent
            sys_users.save()
        except Exception as e:
            return jsonify({'error': e}), 500
    
    sys_users_data = json.loads(sys_users.to_json())

    return jsonify(
        {
            'message': 'System users registered successfully.',
            'sys_users': sys_users_data,
        }
    ), 200

##############################################################################
