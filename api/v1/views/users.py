#!/usr/bin/python3
"""New view for User object that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import abort, request, jsonify
from hashlib import md5


@app_views.route('/users', methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'])
def get_users_or_user(user_id=None):
    """Retrieve all user objects  or <user_id> object
    if specified and exists"""
    if user_id is None:
        return ([(st.to_dict()) for st in storage.all(User).values()])
    user = storage.all(User).get(f'User.{user_id}')
    if user is None:
        abort(404)
    return jsonify((user.to_dict()))


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id=None):
    '''Delete User object by id'''
    user = storage.all(User).get(f'User.{user_id}')
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def post_to_users():
    """Add new user object"""
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'400': 'Not a JSON'}), 400
    if 'email' not in request.json:
        return jsonify({'400': 'Missing email'}), 400
    if 'password' not in request.json:
        return jsonify({'400': 'Missing password'}), 400
    new_object = User(email=data.get('email'),
                      password=data.get('password'))
    storage.new(new_object)
    storage.save()
    return jsonify(new_object.to_dict()), 201 


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id=None):
    '''Update user object'''
    user = storage.all(User).get(f'User.{user_id}')
    if user is None:
        abort(404)

    # Try parsing incoming data to json
    try:
        data = request.get_json()
    except Exception as e:
        # If parsing failed
        return jsonify({'400': 'Not a JSON'}), 400

    for key, val in user.to_dict().items():
        if key not in ['id', 'created_at', 'updated_at', 'email', '__class__']:
            setattr(user, key, request.json.get(key, val))

    # Hash password
    if 'password' in data:
        setattr(user, 'password', md5(
            data.get('password').encode()).hexdigest())
    storage.save()
    return jsonify(user.to_dict()), 200
