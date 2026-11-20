# importing Flask and jsonify from the flask module
# Flask is the tool we use to create our web application
# jsonify is used to convert Python dictionaries into JSON format for API responses
# request is used to handle incoming HTTP requests in our Flask application
from flask import Flask, jsonify, request

# importing generate_password_hash and check_password_hash from werkzeug.security
from werkzeug.security import generate_password_hash, check_password_hash

# importing psycopg2, the Python library for connecting to PostgreSQL databases
import psycopg2  

# importing the os module to access environment variables
import os  

# importing the errors module from psycopg2 to handle database errors
from psycopg2 import errors

# creating an instance of the Flask class
app = Flask(__name__)

def get_connection():
    # establishing a connection to the PostgreSQL database
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", 5433),
        dbname=os.getenv("DB_NAME", "usersdb"),
        user=os.getenv("DB_USER", "shopuser"),
        password=os.getenv("DB_PASSWORD", "shoppass")
    )

# defining a route for the root URL ("/") of the web application
@app.route("/health", methods=["GET"])
def health():
    # returning a JSON response indicating that the service is healthy
    return jsonify({"status": "healthy"})

# defining a route for user registration
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
    cur = conn.cursor()  # creating a cursor object to execute SQL queries
    try:
        # executing an SQL query to insert the new user into the users table
        cur.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id",
            (username, email, hashed_password),
        )
        user_id = cur.fetchone()[0]  # fetching the ID of the newly created user
        conn.commit()  # committing the changes to the database
    except errors.UniqueViolation:
        # returning an error response if the email is already registered
        conn.rollback()  # rolling back the transaction in case of an error
        cur.close()  # closing the cursor
        conn.close()  # closing the database connection
        return jsonify({"error": "Email already registered"}), 409

    conn.commit()  # committing the changes to the database
    cur.close()  # closing the cursor
    conn.close()  # closing the database connection

    return jsonify({"id": user_id, "username": username, "email": email}), 201

# defining a route for user login
@app.route("/users/login", methods=["POST"])
def login_user():
    # getting the JSON data from the incoming request
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # checking if both email and password are provided in the request
    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    # checking if the user exists and if the provided password matches the stored hashed password
    if user is None or not check_password_hash(user[2], password):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"message": "login successful", "id": user[0], "username": user[1]}), 200

# defining a route to get user details by user ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
   conn = get_connection()
   cur = conn.cursor()
   cur.execute(
         "SELECT id, username, email, created_at FROM users WHERE id = %s", (user_id,)
   )
   user = cur.fetchone()
   cur.close()
   conn.close()

   # checking if the user exists in the database; if not, returning a 404 error
   if user is None:
       return jsonify({"error": "User not found"}), 404

   return jsonify({"id": user[0], "username": user[1], "email": user[2]}), 200

if __name__ == "__main__":
    # running the Flask application on host
    # 0.0.0.0 and port 5000, making it accessible from any network interface
    app.run(host="0.0.0.0", port=5000)