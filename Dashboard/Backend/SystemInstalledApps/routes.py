#!/usr/bin/env python3

# Libraries
##############################################################################
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


##############################################################################
