"""
Module: places_reviews.py
Contains routes for handling Review objects in the API.

Endpoints:
1. GET /api/v1/places/<place_id>/reviews
   Retrieves the list of all Review objects of a Place.

2. GET /api/v1/reviews/<review_id>
   Retrieves a Review object.

3. DELETE /api/v1/reviews/<review_id>
   Deletes a Review object.

4. POST /api/v1/places/<place_id>/reviews
   Creates a Review object.

5. PUT /api/v1/reviews/<review_id>
   Updates a Review object.
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import Review, Place, User

@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
    """
    Retrieves the list of all Review objects of a Place.

    Args:
        place_id (str): The ID of the Place.

    Returns:
        JSON response: List of Review objects in JSON format.
    """
    place = Place.query.get(place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """
    Retrieves a Review object by its ID.

    Args:
        review_id (str): The ID of the Review.

    Returns:
        JSON response: Review object in JSON format.
    """
    review = Review.query.get(review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Deletes a Review object by its ID.

    Args:
        review_id (str): The ID of the Review.

    Returns:
        JSON response: Empty dictionary with status code 200.
    """
    review = Review.query.get(review_id)
    if review is None:
        abort(404)
    review.delete()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """
    Creates a new Review object for a specific Place.

    Args:
        place_id (str): The ID of the Place.

    Returns:
        JSON response: New Review object in JSON format with status code 201.
    """
    place = Place.query.get(place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')
    user_id = data['user_id']
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    review = Review(**data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Updates a Review object by its ID.

    Args:
        review_id (str): The ID of the Review.

    Returns:
        JSON response: Updated Review object in JSON format with status code 200.
    """
    review = Review.query.get(review_id)
    if review is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200

