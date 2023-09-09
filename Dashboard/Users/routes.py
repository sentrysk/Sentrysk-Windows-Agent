#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
import bcrypt
import jwt
from datetime import datetime,timedelta
from configparser import ConfigParser
from marshmallow import  ValidationError

from .models import User
from Session.models import Session
from .validators import auth_token_required
from .schema import RegisterSchema,LoginSchema
##############################################################################

# Blueprint
##############################################################################
users_bp = Blueprint('users_blueprint', __name__)
##############################################################################

# Configs
##############################################################################
CONFIG_FILE = 'config.ini'
config = ConfigParser()
config.read(CONFIG_FILE)

SECRET_KEY = config.get('app','secret_key')

JWT_ALG = 'HS256' # JWT Algorithm
##############################################################################

# Routes
##############################################################################
@users_bp.route('/register', methods=['POST'])
def register_user():
    try:
        # Load and validate the JSON request using the schema
        data = RegisterSchema().load(request.json)
    except ValidationError as e:
        # Return validation errors as a JSON response with a 400 status code
        return jsonify({'error': e.messages}), 400

    # Get Email & Password from request data
    name        = data.get('name')
    lastname    = data.get('lastname')
    email       = data.get('email')
    password    = data.get('password')

    # Check if User already exist
    existing_user = User.objects(email=email).first()
    if existing_user:
        return jsonify({'message': 'Email already registered.'}), 409

    # Generate password hash
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Register User
    user = User(
        name     = name,
        lastname = lastname,
        email    = email, 
        password = hashed_password
    )
    user.save()

    return jsonify({
        'message': 'User registered successfully.',
        'user': user.safe_serialize()
    }), 201

@users_bp.route('/login', methods=['POST'])
def login():
    try:
        # Load and validate the JSON request using the schema
        data = LoginSchema().load(request.json)
    except ValidationError as e:
        # Return validation errors as a JSON response with a 400 status code
        return jsonify({'error': e.messages}), 400

    # Get Email & Password from request data
    email = data.get('email')
    password = data.get('password')

    # Find user by email
    user = User.objects(email=email).first()

    # If User exist & Password matches
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        # Expire previous session
        prev_session = Session.objects(email=email,is_expired=False).first()
        # If Previous session exist -> Expire
        if prev_session:
            prev_session.is_expired = True
            prev_session.expire_date = datetime.now()
            prev_session.save()

        # Generate a token for the user session
        token = jwt.encode(
            {
                'email': email,
                'exp': datetime.now() + timedelta(hours=24)
            },
            SECRET_KEY,     # Secret Key
            JWT_ALG         # JWT Algorithm
        )

        # Create a Session for this User
        session = Session(
            email=email, 
            token=token
        )
        session.save()

        return jsonify(
            {
                'message': 'Login successful.',
                'token': token,
                'token_expiry_date': datetime.now() + timedelta(hours=24)
            }
        ), 200

    return jsonify({'message': 'Invalid credentials.'}), 401

@users_bp.route('/logout', methods=['POST'])
@auth_token_required
def logout():
    # Get Session if is not expired
    session = Session.objects(
        token       =  request.headers.get('Authorization'), 
        is_expired  =  False
    ).first()

    if session:
        session.is_expired = True
        session.save()
        return jsonify({'message': 'Logout successful.'}), 200
    
    return jsonify({'message': 'Token is invalid'}), 498

# Get User by ID
@users_bp.route('/<id>', methods=['GET'])
@auth_token_required
def get_agent_by_id(id):
    try:
        agent = User.objects(id=id).first().safe_serialize()
        return jsonify(agent)
    except Exception as e:
        return jsonify({"error":str(e)}), 500
##############################################################################