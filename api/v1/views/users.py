from flask import jsonify, request, abort
from api.v1.views import app_views
from models import User

@app_views.route('/users', methods=['GET'])
def get_users():
    """
    Retrieves the list of all User objects.

    Returns:
        JSON response with the list of User objects.
    """
    users = [user.to_dict() for user in User.query.all()]
    return jsonify(users)

@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieves a User object.

    Args:
        user_id: The ID of the User object to retrieve.

    Returns:
        JSON response with the User object.
    """
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a User object.

    Args:
        user_id: The ID of the User object to delete.

    Returns:
        Empty JSON response with status code 200.
    """
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    user.delete()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'])
def create_user():
    """
    Creates a User object.

    Returns:
        JSON response with the new User object.
    """
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates a User object.

    Args:
        user_id: The ID of the User object to update.

    Returns:
        JSON response with the updated User object.
    """
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200

