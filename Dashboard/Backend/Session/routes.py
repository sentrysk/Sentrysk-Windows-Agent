#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, jsonify

from Shared.validators import auth_token_required
##############################################################################

# Blueprint
##############################################################################
session_bp = Blueprint('session_blueprint', __name__)
##############################################################################


# Routes
##############################################################################

# Session Check
@session_bp.route('/check', methods=['GET'])
@auth_token_required
def check_session():
    return jsonify({"message":"Session active"}),200

##############################################################################
