#!/usr/bin/python3
"""It’s time to start your API!
Your first endpoint (route) will be to return the status of your API
"""

from flask import Flask, jsonify, make_response
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
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if host is None:
        host = '0.0.0.0'
    if port is None:
        port = 5000
    app.run(host, port, threaded=True)
