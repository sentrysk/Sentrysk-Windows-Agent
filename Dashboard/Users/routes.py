#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
import bcrypt
import uuid
from datetime import datetime,timedelta

from .models import User
from Session.models import Session
##############################################################################

# Blueprint
##############################################################################
users_bp = Blueprint('users_blueprint', __name__)
##############################################################################


# Routes
##############################################################################
@users_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400

    existing_user = User.objects(email=email).first()
    if existing_user:
        return jsonify({'message': 'Email already registered.'}), 409

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user = User(email=email, password=hashed_password)
    user.save()

    return jsonify({'message': 'User registered successfully.'}), 201

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400

    user = User.objects(email=email).first()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        # Expire previous session
        prev_session = Session.objects(email=email).first()
        prev_session.is_expired = True
        prev_session.expire_date = datetime.now()
        prev_session.save()

        # Generate a token for the user session
        token = str(uuid.uuid4())

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
def logout():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing.'}), 401

    # Get Session if is not expired
    session = Session.objects(token=token, is_expired=False).first()

    if session:
        session.is_expired = True
        session.save()
        return jsonify({'message': 'Logout successful.'}), 200

    return jsonify({'message': 'Invalid token.'}), 401
##############################################################################