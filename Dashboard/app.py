#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Flask
from mongoengine import connect
from configparser import ConfigParser

from Agents.routes import agnt_bp
from Users.routes import users_bp
##############################################################################

# Configs
##############################################################################

# Config File
CONFIG_FILE = 'config.ini'
config = ConfigParser()
config.read(CONFIG_FILE)

# App Config
HOST = '0.0.0.0'
PORT = 5000
app = Flask(__name__)
app.config['SECRET_KEY'] = config.get('app','secret_key')

# DB Config
db = connect(
    host     = config.get('database','host'),
    db       = config.get('database','db'),
    username = config.get('database','username'), 
    password = config.get('database','password')
)

##############################################################################


# Blueprints
##############################################################################
app.register_blueprint(agnt_bp, url_prefix='/agent')
app.register_blueprint(users_bp, url_prefix='/user')
##############################################################################


# Functions
##############################################################################
def test_mongodb():
    try:
        db = connect(
            host     = config.get('database','host'),
            db       = config.get('database','db'),
            username = config.get('database','username'), 
            password = config.get('database','password')
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
    app.run(host=HOST, port=PORT, debug=True)
##############################################################################