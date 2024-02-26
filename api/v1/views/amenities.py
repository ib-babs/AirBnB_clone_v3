#!/usr/bin/python3

"""New view for Amenity objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import abort, request, jsonify


@app_views.route('/amenities', methods=['GET'])
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenities_or_amenity(amenity_id=None):
    """Retrieve all amenity objects  or <amenity_id> object
    if specified and exists"""
    if amenity_id is None:
        return jsonify(([(st.to_dict())
                         for st in storage.all(Amenity).values()]))
    amenity = storage.all(Amenity).get(f'Amenity.{amenity_id}')
    if amenity is None:
        abort(404)
    return jsonify((amenity.to_dict()))


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id=None):
    '''Delete amenity object by id'''
    amenity = storage.all(Amenity).get(f'Amenity.{amenity_id}')
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def post_to_amenities():
    """Add new amenity object"""
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'400': 'Not a JSON'}), 400
    if 'name' not in request.json:
        return jsonify({'400': 'Missing name'}), 400
    new_object = Amenity(name=data.get('name'))
    storage.new(new_object)
    storage.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id=None):
    '''Update amenity object'''
    amenity = storage.all(Amenity).get(f'Amenity.{amenity_id}')
    if amenity is None:
        abort(404)

    # Try parsing incoming data to json
    try:
        data = request.get_json()
    except Exception as e:
        # If parsing failed
        return jsonify({'400': 'Not a JSON'}), 400

    for key, val in amenity.to_dict().items():
        if key not in ['id', 'created_at', 'updated_at', '__class__']:
            setattr(amenity, key, request.json.get(key, val))
    storage.save()
    return jsonify(amenity.to_dict()), 200
