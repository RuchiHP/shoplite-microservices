# This is a test file for the user service application. 
# It uses the pytest framework to run tests on the Flask application defined in app.py.
# The tests are designed to check the functionality of the user registration, login, and retrieval endpoints.
from app import app

def test_health():
    # creating a test client for the Flask application
    client = app.test_client()
    # sending a GET request to the /health endpoint
    response = client.get("/health")
    # asserting that the response status code is 200 (OK)
    assert response.status_code == 200
    # asserting that the response JSON data indicates that the service is healthy
    assert response.get_json()["status"] == "healthy"


def test_register_missing_field():
    # creating a test client for the Flask application
    client = app.test_client()
    # sending a POST request to the /users/register endpoint with missing fields
    response = client.post("/users/register", json={"username": "testuser"})
    # asserting that the response status code is 400 (Bad Request)
    assert response.status_code == 400
 


def test_login_missing_field():
    # creating a test client for the Flask application
    client = app.test_client()
    # sending a POST request to the /users/login endpoint with missing fields
    response = client.post("/users/login", json={"email": "a@test.com"})
    # asserting that the response status code is 400 (Bad Request)
    assert response.status_code == 400