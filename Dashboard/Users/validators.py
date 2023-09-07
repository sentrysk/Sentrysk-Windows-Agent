#!/usr/bin/env python3

# Libraries
##############################################################################
from functools import wraps
from flask import request, jsonify
import jwt
from configparser import ConfigParser

from Session.models import Session
##############################################################################

# Config
##############################################################################
CONFIG_FILE = 'config.ini'
config = ConfigParser()
config.read(CONFIG_FILE)

SECRET_KEY = config.get('app','secret_key')

JWT_ALG = 'HS256' # JWT Algorithm
##############################################################################

# Decorators
##############################################################################
def auth_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify(
                {
                    'message':'Token is missing'
                }
            ),499

        try:
            token = Session.objects(token=auth_header).first()
            if token.is_expired == False:
                token = jwt.decode(
                    auth_header,
                    SECRET_KEY,
                    algorithms=[JWT_ALG]
                )
            else:
                return jsonify(
                    {
                        'message':'Token is invalid'
                    }
                ),498
        except Exception as e:
            return jsonify(
                {
                    'message':'Token is invalid'
                }
            ),498
        
        return f(*args, **kwargs)
    return decorated
##############################################################################
