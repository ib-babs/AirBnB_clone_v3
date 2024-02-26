#!/usr/bin/python3

"""New view for Review objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from flask import abort, request, jsonify


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_places_reviews(place_id=None):
    """Retrieve all Place objects based on place_id"""
    place = storage.all(Place).get(f'Place.{place_id}')
    if place is None:
        abort(404)
    return jsonify(([st.to_dict() for st in storage.all(Review).values()
                     if place_id == st.to_dict()['place_id']]))


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_place_review(review_id):
    '''Get place review object'''
    review = storage.all(Review).get(f'Review.{review_id}')
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_place_review(review_id=None):
    '''Delete review object by id'''
    review = storage.all(Review).get(f'Review.{review_id}')
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_place_review(place_id=None):
    """Add new review object"""
    place = storage.all(Place).get(f'Place.{place_id}')
    if place is None:
        abort(404)

    # Try parsing incoming data to json
    try:
        data = request.get_json()
    except Exception as e:
        # If parsing failed
        return jsonify({'400': 'Not a JSON'}), 400

    if not 'user_id' in request.json:
        return jsonify({'400': 'Missing user_id'}), 400
    a_user = storage.all(User).get(f'User.{data.get("user_id")}')
    if a_user is None:
        abort(404)

    if not 'text' in request.json:
        return jsonify({'400': 'Missing text'}), 400

    new_object = Review(text=data.get('text'), user_id=data.get('user_id'),
                        place_id=data.get('place_id'))
    storage.new(new_object)
    storage.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_place_review(review_id=None):
    '''Update Review object'''
    review = storage.all(Review).get(f'Review.{review_id}')
    if review is None:
        abort(404)

    # Try parsing incoming data to json
    try:
        data = request.get_json()
    except Exception as e:
        # If parsing failed
        return jsonify({'400': 'Not a JSON'}), 400

    for key, val in review.to_dict().items():
        if key not in ['id', 'created_at', 'updated_at',
                       'place_id', 'user_id', '__class__']:
            setattr(review, key, request.json.get(key, val))
    storage.save()
    return jsonify(review.to_dict()), 200
