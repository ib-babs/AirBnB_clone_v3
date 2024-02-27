#!/usr/bin/python3

"""New view for City objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import abort, request, jsonify


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id=None):
    """Retrieve all cities objects based on state_id"""
    a_state = storage.all(State).get(f'State.{state_id}')
    if a_state is None:
        abort(404)
    return jsonify(([st.to_dict() for st in storage.all(City).values()
                     if state_id == st.to_dict()['state_id']]))


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    '''Get city object'''
    a_city = storage.all(City).get(f'City.{city_id}')
    if a_city is None:
        abort(404)
    return jsonify(a_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id=None):
    '''Delete city object by id'''
    a_city = storage.all(City).get(f'City.{city_id}')
    if a_city is None:
        abort(404)
    storage.delete(a_city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_to_city(state_id=None):
    """Add new city object"""
    a_state = storage.all(State).get(f'State.{state_id}')
    if a_state is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'400': 'Not a JSON'}), 400
    if 'name' not in request.json:
        return jsonify({'400': 'Missing name'}), 400
    new_object = City(name=data.get('name'), state_id=state_id)
    storage.new(new_object)
    storage.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id=None):
    '''Update city object'''
    a_city = storage.all(City).get(f'City.{city_id}')
    if a_city is None:
        abort(404)

    # Try parsing incoming data to json
    try:
        data = request.get_json()
    except Exception as e:
        # If parsing failed
        return jsonify({'400': 'Not a JSON'}), 400

    for key, val in a_city.to_dict().items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(a_city, key, request.json.get(key, val))
    storage.save()
    return jsonify(a_city.to_dict()), 200
