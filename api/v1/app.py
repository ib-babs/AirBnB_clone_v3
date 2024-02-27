#!/usr/bin/python3
"""
It’s time to start your API!
Your first endpoint (route) will be to return the status of your API
This is the main app for running all the api endpoints
All endpoints are prefixed with /api/v1
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins=["0.0.0.0"])
app.register_blueprint(app_views)
host = getenv("HBNB_API_HOST", "0.0.0.0")
port = getenv("HBNB_API_PORT", "5000")


@app.teardown_appcontext
def close(error):
    """Close session"""
    storage.close()


@app.errorhandler(404)
def error(error):
    """Handling json error"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    app.run(host, port, threaded=True)
