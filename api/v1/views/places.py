from flask import jsonify, request, abort
from api.v1.views import app_views
from models import City, Place, User

@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    """
    Retrieves the list of all Place objects of a City.

    Args:
        city_id: The ID of the City object.

    Returns:
        JSON response with the list of Place objects.
    """
    city = City.query.get(city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """
    Retrieves a Place object.

    Args:
        place_id: The ID of the Place object to retrieve.

    Returns:
        JSON response with the Place object.
    """
    place = Place.query.get(place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes a Place object.

    Args:
        place_id: The ID of the Place object to delete.

    Returns:
        Empty JSON response with status code 200.
    """
    place = Place.query.get(place_id)
    if place is None:
        abort(404)
    place.delete()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """
    Creates a Place object.

    Args:
        city_id: The ID of the City object.

    Returns:
        JSON response with the new Place object.
    """
    city = City.query.get(city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = User.query.get(data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    place = Place(**data)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """
    Updates a Place object.

    Args:
        place_id: The ID of the Place object to update.

    Returns:
        JSON response with the updated Place object.
    """
    place = Place.query.get(place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

