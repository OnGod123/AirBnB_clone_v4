from flask import jsonify, request, abort
from models import State
from api.v1.views import app_views

@app_views.route('/states', methods=['GET'])
def get_states():
    """
    Retrieves a list of all State objects

    Returns:
        JSON response containing a list of State objects
    """
    states = [state.to_dict() for state in State.query.all()]
    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """
    Retrieves a specific State object by its ID

    Args:
        state_id (int): The ID of the State object to retrieve

    Returns:
        JSON response containing the State object
    """
    state = State.query.get(state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes a specific State object by its ID

    Args:
        state_id (int): The ID of the State object to delete

    Returns:
        JSON response with empty dictionary and status code 200 if successful,
        otherwise aborts with status code 404 if State object not found
    """
    state = State.query.get(state_id)
    if state:
        state.delete()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/states', methods=['POST'])
def create_state():
    """
    Creates a new State object

    Request Body (JSON):
        {
            "name": "string"  # Name of the state
        }

    Returns:
        JSON response containing the newly created State object and status code 201,
        otherwise aborts with status code 400 if request body is invalid or missing name
    """
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """
    Updates a specific State object by its ID

    Args:
        state_id (int): The ID of the State object to update

    Request Body (JSON):
        Any key-value pairs to update the State object

    Returns:
        JSON response containing the updated State object and status code 200,
        otherwise aborts with status code 404 if State object not found
    """
    state = State.query.get(state_id)
    if state:
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
OBOBOB        return jsonify(state.to_dict()), 200
    else:
        abort(404)

