# api/v1/views/cities.py
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import State, City

@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id):
    """
    Retrieves the list of all City objects of a State.

    Args:
        state_id (str): The ID of the State.

    Returns:
        JSON response with the list of City objects belonging to the specified State.
        Raises a 404 error if the State ID is not linked to any State object.
    """
    state = State.query.get(state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """
    Retrieves a City object.

    Args:
        city_id (str): The ID of the City.

    Returns:
        JSON response with the City object.
        Raises a 404 error if the City ID is not linked to any City object.
    """
    city = City.query.get(city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """
    Deletes a City object.

    Args:
        city_id (str): The ID of the City.

    Returns:
        Empty dictionary with status code 200 upon successful deletion.
        Raises a 404 error if the City ID is not linked to any City object.
    """
    city = City.query.get(city_id)
    if city is None:
        abort(404)
    city.delete()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """
    Creates a new City object.

    Args:
        state_id (str): The ID of the State to which the City belongs.

    Returns:
        JSON response with the new City object upon successful creation.
        Raises a 404 error if the State ID is not linked to any State object.
        Raises a 400 error if the request body is not a valid JSON or if the name is missing.
    """
    state = State.query.get(state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    city = City(**data)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """
    Updates a City object.

    Args:
        city_id (str): The ID of the City to update.

    Returns:
        JSON response with the updated City object upon successful update.
        Raises a 404 error if the City ID is not linked to any City object.
        Raises a 400 error if the request body is not a valid JSON.
    """
    city = City.query.get(city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200

