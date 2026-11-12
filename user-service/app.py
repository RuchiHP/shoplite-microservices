# importing Flask and jsonify from the flask module
# Flask is the tool we use to create our web application
# jsonify is used to convert Python dictionaries into JSON format for API responses
# request is used to handle incoming HTTP requests in our Flask application
from flask import Flask, jsonify, request

# importing generate_password_hash from werkzeug.security
from werkzeug.security import generate_password_hash

# creating an instance of the Flask class
app = Flask(__name__)

# defining a route for the root URL ("/") of the web application
@app.route("/health", methods=["GET"])
def health():
    # returning a JSON response indicating that the service is healthy
    return jsonify({"status": "healthy"})

@app.route("/users/register", methods=["POST"])
def register_user():
    # getting the JSON data from the incoming request
    data = request.get_json()
    # extracting the user information from the JSON data
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    #hashing the password before storing it
    hashed_password = generate_password_hash(password)

    return jsonify({"username": username, "email": email , "password": hashed_password}), 201

if __name__ == "__main__":
    # running the Flask application on host
    app.run(host="0.0.0.0", port=5000)