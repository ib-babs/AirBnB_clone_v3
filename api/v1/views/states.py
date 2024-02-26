#!/usr/bin/python3

"""New view for State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import abort, request, jsonify


@app_views.route('/states', methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'])
def get_states(state_id=None):
    """Retrieve all state objects or state_id object if specified and exists"""
    if state_id is None:
        return jsonify([(st.to_dict()) for st in storage.all(State).values()])
    a_state = storage.all(State).get(f'State.{state_id}')
    if a_state is None:
        abort(404)
    return jsonify(a_state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id=None):
    '''Delete state object by id'''
    a_state = storage.all(State).get(f'State.{state_id}')
    if a_state is None:
        abort(404)
    storage.delete(a_state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def post_to_state():
    """Add new state object"""
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'400': 'Not a JSON'}), 400
    if not 'name' in request.json:
        return jsonify({'400': 'Missing name'}), 400
    new_object = State(name=data.get('name'))
    storage.new(new_object)
    storage.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id=None):
    '''Update state object'''
    a_state = storage.all(State).get(f'State.{state_id}')
    if a_state is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'400': 'Not a JSON'}), 400
    for key, val in a_state.to_dict().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(a_state, key, request.json.get(key, val))
    storage.save()
    return a_state.to_dict(), 200
