from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/stats', methods=['GET'])
def get_stats():
    """
    Retrieves the number of each object by type
    """
    stats = {}
    for cls in storage.classes():
        stats[cls.__name__] = storage.count(cls)
    return jsonify(stats)


