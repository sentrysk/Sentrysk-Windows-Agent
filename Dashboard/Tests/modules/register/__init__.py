#!/usr/bin/env python3

# Libraries
##############################################################################
import requests
import json
from faker import Faker
##############################################################################

# Config
##############################################################################
fake = Faker()

BASE_URL = "http://localhost:5000"
REG_EP = "/user/register"
REG_URL = BASE_URL + REG_EP
##############################################################################


##############################################################################
def generate_user_data():
    user_data = {}
    user_data["name"] = str(fake.unique.first_name())
    user_data["lastname"] = str(fake.unique.first_name())
    user_data["email"] =user_data["name"].lower()\
        +"."+user_data["lastname"].lower()\
        +"@"+str(fake.free_email_domain())
    user_data["password"] = "1234"
    
    return user_data
##############################################################################

# Tests
##############################################################################
def test_register_success():
    user_data = generate_user_data()

    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request(
        "POST",
        REG_URL,
        data=json.dumps(user_data),
        headers=headers
    )

    assert "User registered successfully." in response.text
    assert response.status_code == 201
    
    print("[SUCCESS]\ttest_register_success")
##############################################################################

# Tests
##############################################################################
def test_register_invalid_name():
    testing_user_data = [
        123423,
        "!'.abcc-",
        "'ab123asdf",
        "||",
        "space  test   third",
        "",
        "space test third",
        "kerem oruc"
    ]

    headers = {
        'Content-Type': 'application/json'
    }
    
    for t_data in testing_user_data:
        user_data = generate_user_data()
        user_data["name"] = t_data

        response = requests.request(
            "POST",
            REG_URL,
            data=json.dumps(user_data),
            headers=headers
        )

        assert "error" in response.text
        assert response.status_code == 400
    
    return True
##############################################################################