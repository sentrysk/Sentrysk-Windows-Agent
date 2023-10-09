#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
import json
from marshmallow import ValidationError

from .models import SystemUsers
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

    # Get if record already exist
    sys_users = SystemUsers.objects(agent=agent).first()

    if sys_users:
        # UPDATE If System Information data already exist 
        
        try:
            data = request.get_json()
            sys_users.update(**data)
        except Exception as e:
            return jsonify({'error': e.messages}), 400
        
    else:
        # CREATE If System Information not exist 
        
        try:
            data = request.get_json()
            sys_users = SystemUsers(**data)
            sys_users.agent = agent
            sys_users.save()
            
            sys_users_data = json.loads(sys_users.to_json())

            return jsonify(
                {
                    'message': 'System users registered successfully.',
                    'sys_users': sys_users_data,
                }
            ), 200

        except ValidationError as e:
            return jsonify({'error': e.messages}), 400
    


##############################################################################
