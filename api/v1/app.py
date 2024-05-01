from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)

# Define the 404 error handler
@app.errorhandler(404)
def not_found(error):
    """
    Handler for 404 errors.

    Returns:
        JSON response with a 404 status code and content "error": "Not found".
    """
    return jsonify({"error": "Not found"}), 404

# Teardown appcontext to close storage
@app.teardown_appcontext
def teardown(exception):
    storage.close()

if __name__ == "__main__":
    # Get host and port from environment variables or use default values
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))

    # Run the Flask application
    app.run(host=host, port=port, threaded=True, debug=True)

