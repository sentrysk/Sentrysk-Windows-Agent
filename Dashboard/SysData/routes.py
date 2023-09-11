#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
import pymongo

from Shared.configs import DB_NAME,DB_HOST,DB_PORT,DB_USERNAME,DB_PASSWORD
from Shared.validators import agent_token_required
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
collection = mongo_client[DB_NAME]["system_data"]
##############################################################################


# Routes
##############################################################################

# Save Data
@sys_data_bp.route('/', methods=['POST'])
@agent_token_required
def register():

    data = request.get_json()

    # Insert the System Data into the System Data Collection
    collection.insert_one(data)
    
    return jsonify(
        {
            'message': 'Data registered successfully.',
        }
    ), 201
##############################################################################