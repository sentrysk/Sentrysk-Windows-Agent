#!/usr/bin/env python3

# Libraries
#################################################################sys_appsapp#############
from flask import Blueprint, request, jsonify
from datetime import datetime

from .models import SystemInstalledApps
from Shared.validators import agent_token_required, auth_token_required

from Agents.helper_funcs import get_id_by_token
from Agents.models import Agent
##############################################################################

# Blueprint
##############################################################################
sys_apps_bp = Blueprint('sys_apps_blueprint', __name__)
##############################################################################


# Routes
##############################################################################

# Register
@sys_apps_bp.route('/', methods=['POST'])
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
    if 'apps' not in data:
        return jsonify({'error': 'Invalid JSON data'}), 400
        
    # Get if record already exist
    sys_apps = SystemInstalledApps.objects(agent=agent).first()

    if sys_apps:
        # UPDATE If System Information data already exist
        try:
            # Create SystemInstalledApps object to Compare
            new_apps_obj = SystemInstalledApps(**data)
            new_apps_obj.agent = agent

            # Find deleted, new, and updated apps
            new_apps, deleted_apps, updated_apps = sys_apps.compare_apps(new_apps_obj)
            
            changes = {}

            if deleted_apps:
                changes["deleted_apps"] = deleted_apps
            if new_apps:
                changes["new_apps"] = new_apps
            if updated_apps:
                changes["updated_apps"] = updated_apps

            # If any changes happens
            if changes:
                # Apply updates
                data["updated"] = datetime.utcnow
                sys_apps.update(**data)
            else:
                # Apply only updated time
                sys_apps.update(updated=datetime.utcnow)
                return jsonify({"message":"Nothing changed"})

        except Exception as e:
            return jsonify({'error': e}), 500
        
    else:
        # CREATE If System Installed Apps not exist 
        try:
            sys_apps = SystemInstalledApps(**data)
            sys_apps.agent = agent
            sys_apps.save()
        except Exception as e:
            return jsonify({'error': e}), 500

    return jsonify(
        {
            'message': 'System apps registered successfully.',
        }
    ), 200

##############################################################################
