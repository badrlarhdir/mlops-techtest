# Import the necessary modules
import pytest
import uuid
from fastapi.testclient import TestClient
from app import app

# Create a test client using the FastAPI application
client = TestClient(app)


@pytest.fixture(scope="module")
def auth_token():
    """
    This fixture generates a unique username and password, registers and logs in the user,
    and returns the authentication token for the session. This token is used in other tests
    that require authentication.
    """
    unique_username = f"testuser_{uuid.uuid4()}"  # Generates a unique username
    register_response = client.post(
        "/register", json={"username": unique_username, "password": "testpass"}
    )
    assert register_response.status_code in [
        200,
        201,
    ], f"Registration failed: {register_response.text}"

    login_response = client.post(
        "/login", json={"username": unique_username, "password": "testpass"}
    )
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    token = login_response.json()["token"]
    assert token is not None, "Authentication token was not provided"

    return token


# Define a test function for the index (root) endpoint
def test_index_endpoint():
    """
    This function tests the index (root) endpoint of the FastAPI application.
    It sends a GET request to the / endpoint and checks the response status code and content.
    """
    # Send a GET request to the / endpoint
    response = client.get("/")

    assert response.status_code == 200

    # Assert that the response content contains the expected message
    assert "Welcome to the ECG Model Inference API!" in response.text


def test_register():
    """
    This function tests the registration endpoint of the FastAPI application.
    It sends a POST request to the /register endpoint with a JSON payload containing a username and password.
    It then checks the response status code and the response text.
    """
    response = client.post(
        "register", json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "Successfully registered testuser." in response.text


def test_login():
    """
    This function tests the login endpoint of the FastAPI application.
    It sends a POST request to the /login endpoint with a JSON payload containing a username and password.
    It then checks the response status code and the presence of the token in the response.
    """
    response = client.post(
        "login", json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    token = response.json()["token"]
    assert token is not None


# Test the predict endpoint
def test_predict_endpoint(auth_token):
    """
    This function tests the predict endpoint of the FastAPI application.
    It sends a POST request to the /predict endpoint with a JSON payload containing the path to the ECG file and the file name.
    It then checks the response status code and the keys in the JSON response.
    """
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Send a POST request to the /predict endpoint
    response = client.post(
        "/predict",
        json={
            "data_path": "./data/",
            "ecg_file": "data_00001.mat",
        },
        headers=headers,
    )

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Parse the JSON response
    data = response.json()

    # Assert that the keys 'hr' and 'qrs' are in the JSON response
    assert "hr" in data
    assert "qrs" in data


# Define a test function for the evaluate endpoint
def test_evaluate_endpoint(auth_token):
    """
    This function tests the evaluate endpoint of the FastAPI application.
    It sends a GET request to the /evaluate endpoint and checks the response status code and keys in the JSON response.
    """

    headers = {"Authorization": f"Bearer {auth_token}"}
    # Send a GET request to the /evaluate endpoint
    response = client.get("/evaluate", headers=headers)

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Parse the JSON response
    data = response.json()

    # Assert that the keys 'tot_file_number', 'rec_acc', and 'hr_acc' are in the JSON response
    assert "tot_file_number" in data
    assert "rec_acc" in data
    assert "hr_acc" in data
