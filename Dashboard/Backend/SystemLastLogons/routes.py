#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
import json
from datetime import datetime
from marshmallow import ValidationError

from .models import SystemLastLogons
from .schema import LastLogonSchema
from Shared.validators import agent_token_required, auth_token_required

from Agents.helper_funcs import get_id_by_token
from Agents.models import Agent
##############################################################################

# Blueprint
##############################################################################
sys_last_logons_bp = Blueprint('sys_last_logons_blueprint', __name__)
##############################################################################

# Register
@sys_last_logons_bp.route('/', methods=['POST'])
@agent_token_required
def register():
    # Get Agent Token by Authorization Header
    agent_token = request.headers.get('Authorization')
    # Get Agent ID by Token
    agent_id = get_id_by_token(agent_token)
    # Get Agent by Agent ID
    agent = Agent.objects(id=agent_id).first()

    try:
        # Load and validate the JSON request using the schema
        data = LastLogonSchema().load(request.json)
    except ValidationError as e:
        # Return validation errors as a JSON response with a 400 status code
        return jsonify({'error': e.messages}), 400
        
    # Get if record already exist
    last_logons = SystemLastLogons.objects(agent=agent).first()

    if last_logons:
        # UPDATE If Last Logons data already exist
        try:
            # Compare 2 list
            # Save
            # Apply only updated time
            last_logons.update(updated=datetime.utcnow)

        except Exception as e:
            return jsonify({'error': e}), 500
        
    else:
        # CREATE If System Information not exist 
        try:
            last_logons = SystemLastLogons(**data)
            last_logons.agent = agent
            last_logons.save()
        except Exception as e:
            return jsonify({'error': e}), 500
    
    return jsonify(
        {
            'message': 'Last Logons data registered successfully.',
        }
    ), 200