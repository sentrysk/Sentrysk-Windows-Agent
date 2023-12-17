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

    return response.json()["agent"]
##############################################################################


# Test Agent Register Wrong Agent Type
##############################################################################
def test_register_wrong_agent_types(token):
    agent_types = [
        'WinDowS',
        'LiNuX',
        'MaCos',
        '',
        'Test',
        'Test Space'
    ]
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    for agent_type in agent_types:
        reg_data = {
            'type': agent_type
        }

        response = requests.request(
            "POST",
            AGENT_REG_URL,
            data=json.dumps(reg_data),
            headers=headers
        )

        assert response.status_code == 400

    return True
##############################################################################


# Test Agent Register Double Agent Type
##############################################################################
def test_register_double_agent_type(token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    reg_data = {
        'type': 'Test',
        'type': 'Test2'
    }

    response = requests.request(
        "POST",
        AGENT_REG_URL,
        data=json.dumps(reg_data),
        headers=headers
    )
    print(response.text)
    assert response.status_code == 400

    return True
##############################################################################