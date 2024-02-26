#!/usr/bin/python3

"""New view for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models import storage
from flask import abort, request, jsonify


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id=None):
    """Retrieve all Place objects based on city_id"""
    city = storage.all(City).get(f'City.{city_id}')
    if city is None:
        abort(404)
    return jsonify([st.to_dict() for st in storage.all(Place).values()
                    if city_id == st.to_dict()['city_id']])


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    '''Get place object'''
    place = storage.all(Place).get(f'Place.{place_id}')
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id=None):
    '''Delete place object by id'''
    place = storage.all(Place).get(f'Place.{place_id}')
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_to_place(city_id=None):
    """Add new city object"""
    a_city = storage.all(City).get(f'City.{city_id}')
    if a_city is None:
        abort(404)

    # Try parsing incoming data to json
    try:
        data = request.get_json()
    except Exception as e:
        # If parsing failed
        return jsonify({'400': 'Not a JSON'}), 400

    if 'user_id' not in request.json:
        return jsonify({'400': 'Missing user_id'}), 400
    a_user = storage.all(User).get(f'User.{data.get("user_id")}')
    if a_user is None:
        abort(404)

    if 'name' not in request.json:
        return jsonify({'400': 'Missing name'}), 400

    new_object = Place(name=data.get('name'), user_id=data.get('user_id'),
                       city_id=data.get('city_id'))
    storage.new(new_object)
    storage.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id=None):
    '''Update Place object'''
    a_place = storage.all(Place).get(f'Place.{place_id}')
    if a_place is None:
        abort(404)

    # Try parsing incoming data to json
    try:
        data = request.get_json()
    except Exception as e:
        # If parsing failed
        return jsonify({'400': 'Not a JSON'}), 400

    for key, val in a_place.to_dict().items():
        if key not in ['id', 'created_at', 'updated_at',
                       'city_id', 'user_id', '__class__']:
            setattr(a_place, key, request.json.get(key, val))
    storage.save()
    return jsonify(a_place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"])
def search():
    # If the HTTP request body is not valid JSON
    guide = request.get_json()
    if not guide:
        abort(400, "Not a JSON")

    state_ids = guide.get("states")
    city_ids = guide.get("cities")
    amenity_ids = guide.get("amenities")
    result = []

    # If the JSON body is empty or each list of all keys are empty:
    # retrieve all Place objects
    if not guide and not state_ids and not city_ids:
        result = storage.all(Place)

    # If states list is not empty, results should
    # include all Place objects for each State id listed
    if state_ids:
        for state_id in state_ids:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        result.append(place)

    # If cities list is not empty, results should
    # include all Place objects for each City id listed
    if city_ids:
        for city_id in city_ids:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    if place not in result:
                        result.append(place)

    # If amenities list is not empty, limit search results to
    # only Place objects having all Amenity ids listed
    if amenity_ids:
        for place in result:
            if place.amenities:
                place_amenity_ids = [amenity.id for amenity in place.amenities]
                for amenity_id in amenity_ids:
                    if amenity_id not in place_amenity_ids:
                        result.remove(place)
                        break

    # serialize to json
    result = [storage.get(Place, place.id).to_dict() for place in result]
    # remove relationship keys with list comprehension and
    # dictionary comprehension
    keys_to_remove = ["amenities", "reviews", "amenity_ids"]
    result = [
        {k: v for k, v in place_dict.items() if k not in keys_to_remove}
        for place_dict in result
    ]

    return jsonify(result)
