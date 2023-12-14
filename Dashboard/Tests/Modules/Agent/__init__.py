#!/usr/bin/env python3

# Libraries
##############################################################################
import requests
import json
import random

from Modules.Config import Urls,Endpoints
##############################################################################

# Config
##############################################################################
AGENT_REG_URL = Urls.base_url + Endpoints.agents_reg_ep
##############################################################################


# Test Agent Register Success
##############################################################################
def test_register_agent_success(token):
    agent_types = [
        'windows',
        'linux',
        'macos'
    ]
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    reg_data = {
        'type': random.choice(agent_types)
    }

    response = requests.request(
        "POST",
        AGENT_REG_URL,
        data=json.dumps(reg_data),
        headers=headers
    )

    assert "Agent registered successfully." in response.text
    assert response.status_code == 201

    return True
##############################################################################