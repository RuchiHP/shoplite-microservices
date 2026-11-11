# importing Flask and jsonify from the flask module
# Flask is the tool we use to create our web application, and jsonify is used to convert Python dictionaries into JSON format for API responses.
from flask import Flask, jsonify

# creating an instance of the Flask class
app = Flask(__name__)

# defining a route for the root URL ("/") of the web application
@app.route("/health", methods=["GET"])
def health():
    # returning a JSON response indicating that the service is healthy
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    # running the Flask application on host
    app.run(host="0.0.0.0", port=5000)