#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
import uuid

from .models import Agent
##############################################################################

# Blueprint
##############################################################################
agnt_bp = Blueprint('agent_blueprint', __name__)
##############################################################################


# Routes
##############################################################################
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

    return jsonify({'message': 'Agent registered successfully.', 'token': token}), 201
##############################################################################
