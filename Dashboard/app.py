#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Flask
from mongoengine import connect

from Shared.configs import (
    SECRET_KEY,APP_HOST,APP_PORT,
    DB_HOST,DB_NAME,DB_USERNAME,DB_PASSWORD
)
from Agents.routes import agnt_bp
from Users.routes import users_bp
from SysData.routes import sys_data_bp
##############################################################################

# Configs
##############################################################################

# App Config
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# DB Config
db = connect(
    host     = DB_HOST,
    db       = DB_NAME,
    username = DB_USERNAME, 
    password = DB_PASSWORD
)

##############################################################################


# Blueprints
##############################################################################
app.register_blueprint(agnt_bp, url_prefix='/agent')
app.register_blueprint(users_bp, url_prefix='/user')
app.register_blueprint(sys_data_bp, url_prefix='/data')
##############################################################################


# Functions
##############################################################################
def test_mongodb():
    try:
        db = connect(
            host     = DB_HOST,
            db       = DB_NAME,
            username = DB_USERNAME, 
            password = DB_PASSWORD
        )
        db.server_info() # This will raise an exception if the connection fail
        print('MongoDB connection successful!')
    except Exception as e:
        print(f'MongoDB connection failed: {e}')
##############################################################################


# Main
##############################################################################
if __name__ == '__main__':
    test_mongodb()
    app.run(host=APP_HOST, port=APP_PORT, debug=True)
##############################################################################