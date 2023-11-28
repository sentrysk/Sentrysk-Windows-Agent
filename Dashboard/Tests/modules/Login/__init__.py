#!/usr/bin/env python3

# Libraries
##############################################################################
import requests
import json

from Modules.Register import test_register_success
##############################################################################

# Config
##############################################################################
BASE_URL = "http://localhost:5000"
LOGIN_EP = "/user/login"
LOGIN_URL = BASE_URL + LOGIN_EP
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
    print(response.text)

    assert "Login successful." in response.text

    return True
##############################################################################