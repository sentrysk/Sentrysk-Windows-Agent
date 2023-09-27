#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
import json
from marshmallow import ValidationError

from .models import SystemInfo
from .schema import RegisterSchema
from Shared.validators import agent_token_required

from Agents.helper_funcs import get_id_by_token
from Agents.models import Agent
##############################################################################

# Blueprint
##############################################################################
sys_info_bp = Blueprint('sys_info_blueprint', __name__)
##############################################################################


# Routes
##############################################################################

# Register
@sys_info_bp.route('/', methods=['POST'])
@agent_token_required
def register():
    try:
        # Load and validate the JSON request using the schema
        data = RegisterSchema().load(request.json)
    except ValidationError as e:
        # Return validation errors as a JSON response with a 400 status code
        return jsonify({'error': e.messages}), 400
    
    os                  = data.get('os')
    domain              = data.get('domain')
    cpu                 = data.get('cpu')
    memory              = data.get('memory')
    disks               = data.get('disks')
    network_interfaces  = data.get('network_interfaces')

    # Get Agent Token by Authorization Header
    agent_token = request.headers.get('Authorization')
    # Get Agent ID by Token
    agent_id = get_id_by_token(agent_token)
    # Get Agent by Agent ID
    agent = Agent.objects(id=agent_id).first()

    # Register System Info to DB
    sys_info = SystemInfo(
        agent = agent,
        os = os, 
        domain=domain,
        cpu = cpu,
        memory = memory,
        disks = disks,
        network_interfaces = network_interfaces
    )
    sys_info.save()
    
    sys_info_data = json.loads(sys_info.to_json())

    return jsonify(
        {
            'message': 'System info registered successfully.',
            'sys_info': sys_info_data,
        }
    ), 201

##############################################################################
