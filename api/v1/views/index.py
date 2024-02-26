#!/usr/bin/python3
"""
Index module
Stats and status
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review


classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User,
}


@app_views.route('/status')
def status():
    """Status of the api"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """Retrieve the number of each objects by type"""
    statistics = {}

    for key, value in classes.items():
        statistics[key] = storage.count(value)
    return jsonify(statistics)
