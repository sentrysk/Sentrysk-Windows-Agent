#!/usr/bin/env python3

# Libraries
##############################################################################
import requests
import json

from Modules.Config import Urls,Endpoints
from Modules.Register import test_register_success
##############################################################################


# Config
##############################################################################
LOGIN_URL = Urls.base_url + Endpoints.login_ep
##############################################################################


# Functions
##############################################################################
def test_login_success():
    user_data = test_register_success()

    headers = {
        'Content-Type': 'application/json'
    }

    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    
    response = requests.request(
        "POST",
        LOGIN_URL,
        data=json.dumps(login_data),
        headers=headers
    )

    assert "Login successful." in response.text

    return True
##############################################################################
