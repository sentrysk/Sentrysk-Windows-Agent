#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, jsonify

from .functions import (
    get_sys_user_counts_by_agent_id
)
##############################################################################

# Blueprint
##############################################################################
inf_data_bp = Blueprint('informational_data', __name__)
##############################################################################


# Routes 
##############################################################################
@inf_data_bp.route('/user_counts/<agent_id>', methods=['GET'])
def sys_user_count_by_agent_id(agent_id):
    sys_user_count = get_sys_user_counts_by_agent_id(agent_id)
    
    return jsonify({
        "user_count": str(sys_user_count)
    })
##############################################################################