#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
import pymongo
from datetime import datetime

from Shared.configs import DB_NAME,DB_HOST,DB_PORT,DB_USERNAME,DB_PASSWORD
from Shared.validators import agent_token_required
from Agents.helper_funcs import get_id_by_token
##############################################################################

# Blueprint
##############################################################################
sys_data_bp = Blueprint('system_data_blueprint', __name__)
##############################################################################

# Mongo Configs
##############################################################################
# Replace these values with your MongoDB connection details
mongo_client = pymongo.MongoClient(
    f"mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
)
db = mongo_client[DB_NAME]
system_data_collection  = db["system_data"]
changelog_collection    = db["changelog"]
##############################################################################


# Routes
##############################################################################

# Save Data
@sys_data_bp.route('/', methods=['POST'])
@agent_token_required
def register():
    # Extract the agent_token from the Authorization header
    agent_token = request.headers.get("Authorization")

    # Get Agent ID by token
    agent_id = get_id_by_token(agent_token)

    # Get Data from Request
    data = request.get_json()

    # Define the unique identifier using the agent_id
    unique_identifier = {"agent_id": agent_id}

    # Find existing document with the same identifier
    existing_document = system_data_collection.find_one(unique_identifier)

    if existing_document:
        # Document with the same identifier exists, check for changes
        changes = {}
        for key, value in data.items():
            if key not in existing_document or existing_document[key] != value:
                changes[key] = value
                existing_document[key] = value

        # Update the existing document with changes
        system_data_collection.update_one(unique_identifier, {"$set": existing_document})

        # Log changes to the changelog collection
        if changes:
            changelog_entry = {
                "timestamp": datetime.now(),
                "agent_id": agent_id,
                "changes": changes
            }
            changelog_collection.insert_one(changelog_entry)
    else:
        # Document with the unique identifier doesn't exist, insert the new document
        # Insert the System Data into the System Data Collection
        data["agent_id"] = agent_id
        system_data_collection.insert_one(data)
    
    return jsonify(
        {
            'message': 'Data registered successfully.',
        }
    ), 201
##############################################################################