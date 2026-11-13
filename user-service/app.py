# importing Flask and jsonify from the flask module
# Flask is the tool we use to create our web application
# jsonify is used to convert Python dictionaries into JSON format for API responses
# request is used to handle incoming HTTP requests in our Flask application
from flask import Flask, jsonify, request

# importing generate_password_hash from werkzeug.security
from werkzeug.security import generate_password_hash

# importing psycopg2, the Python library for connecting to PostgreSQL databases
import psycopg2  

# creating an instance of the Flask class
app = Flask(__name__)

def get_connection():
    # establishing a connection to the PostgreSQL database
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="usersdb",
        user="shopuser",
        password="shoppass"
    )

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

    if not username or not email or not password:
        # returning an error response if any of the required fields are missing
        return jsonify({"error": "Missing required fields"}), 400


    #hashing the password before storing it
    hashed_password = generate_password_hash(password)

    conn = get_connection()  # getting a connection to the database
    cur = conn.cursor()  # creating a cursor to execute SQL commands
    cur.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s) RETURNING id",
        (username, email, hashed_password)
    )
    user_id = cur.fetchone()[0]  # getting the ID of the newly created user
    conn.commit()  # committing the changes to the database
    cur.close()  # closing the cursor
    conn.close()  # closing the database connection

    return jsonify({"id": user_id, "username": username, "email": email}), 201

if __name__ == "__main__":
    # running the Flask application on host
    app.run(host="0.0.0.0", port=5000)