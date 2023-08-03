#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
import uuid
import json
from .models import Agent
##############################################################################

# Blueprint
##############################################################################
agnt_bp = Blueprint('agent_blueprint', __name__)
##############################################################################


# Routes
##############################################################################

# Get All Agents
@agnt_bp.route('/', methods=['GET'])
def get_agents():
    try:
        agents = Agent.objects().to_json()
        return json.loads(agents)
    except Exception as e:
        return jsonify({"error":str(e)}), 500


# Register
@agnt_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    agent_type = data.get('type')

    if not agent_type:
        return jsonify({'message': 'Agent type is required.'}), 400

    # Generate a token for the agent
    token = str(uuid.uuid4())

    agent = Agent(type=agent_type, token=token)
    agent.save()
    
    agent_data = json.loads(agent.to_json())
    print(agent_data)

    return jsonify(
        {
            'message': 'Agent registered successfully.',
            'token': token,
            'agent':agent_data
        }
    ), 201

##############################################################################
