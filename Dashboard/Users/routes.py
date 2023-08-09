#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
import bcrypt

from .models import User
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
##############################################################################