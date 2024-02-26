#!/usr/bin/python3
"""Index module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review


@app_views.route('/status')
def status():
    """Status of the api"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count():
    """Length of the api object"""
    return jsonify({
        'amenities': storage.count(Amenity),
        'states': storage.count(State),
        'reviews': storage.count(Review),
        'users': storage.count(User),
        'cities': storage.count(City),
        'places': storage.count(Place)
    })
