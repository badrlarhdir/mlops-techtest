import os
from fastapi import FastAPI, Response, Depends, HTTPException

from auth import AuthHandler
from schemas import AuthDetails, RequestModel

import numpy as np
import scipy.io as sio

from CPSC2019_challenge import *

from eval import perform_model_evaluation


# Initialize the FastAPI application
app = FastAPI()

auth_handler = AuthHandler()
users = []


# Define the root endpoint
# This endpoint is used to check if the API is running
@app.get("/")
def index() -> Response:
    return Response("Welcome to the ECG Model Inference API!")


@app.post("/register")
def register(auth_details: AuthDetails) -> Response:
    """
    Register a new user.

    This endpoint takes an AuthDetails object as input, which includes the username and password for the new user.
    It checks if the username already exists in the users list. If the username is taken, it raises an HTTPException with status code 400.
    If the username is not taken, it hashes the password and appends the new user to the users list.

    Args:
        auth_details (AuthDetails): An AuthDetails object containing the username and password.

    Raises:
        HTTPException: If the username is already taken.
    """
    if any(x["username"] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail="Username is taken")
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({"username": auth_details.username, "password": hashed_password})
    return Response(f"Successfully registered {auth_details.username}.")


@app.post("/login")
def login(auth_details: AuthDetails) -> dict:
    """
    Login a user.

    This endpoint takes an AuthDetails object as input, which includes the username and password for the user.
    It checks if the user with the provided username exists in the users list and if the provided password matches the stored password.
    If the user is not found or the password does not match, it raises an HTTPException with status code 401.
    If the user is found and the password matches, it generates a token for the user and returns it in a JSON response.

    Args:
        auth_details (AuthDetails): An AuthDetails object containing the username and password.

    Returns:
        dict: A JSON response containing the token for the user.

    Raises:
        HTTPException: If the user is not found or the password does not match.
    """
    user = None
    for x in users:
        if x["username"] == auth_details.username:
            user = x
            break

    if (user is None) or (
        not auth_handler.verify_password(auth_details.password, user["password"])
    ):
        raise HTTPException(status_code=401, detail="Invalid username and/or password")
    token = auth_handler.encode_token(user["username"])
    return {"token": token}


# Define the predict endpoint
@app.post("/predict")
def predict(
    request: RequestModel,
    username=Depends(auth_handler.auth_wrapper),
    summary="Predict Heart Rate and QRS Complexes",
    description="This endpoint processes an ECG file and returns the heart rate and QRS complexes. You need to provide the path to the ECG file and the file name.",
) -> dict:
    """
    Predict heart rate and QRS complexes from an ECG file.

    This endpoint takes a RequestModel object as input, which includes the path to
    an ECG file to be processed. It loads the ECG data from the provided file,
    processes it using the CPSC2019_challenge function, and returns the heart rate
    and QRS complexes as a JSON response.

    Args:
        request (RequestModel): A RequestModel object containing the data path and file name.

    Returns:
        dict: A JSON response containing predicted heart rate and QRS complexes.
    """
    # Construct the full path to the ECG file
    ecg_path = os.path.join(request.data_path, request.ecg_file)

    # Load the ECG data from the .mat file
    ecg_data = np.transpose(sio.loadmat(ecg_path)["ecg"])[0]

    # Use the CPSC2019_challenge function to process the ECG data
    hr, qrs = CPSC2019_challenge(ecg_data)

    # Return the heart rate and QRS complexes as a JSON response
    return {"hr": hr.tolist(), "qrs": qrs.tolist()}


# Endpoint for model evaluation
@app.get("/evaluate")
def evaluate_model(username=Depends(auth_handler.auth_wrapper)) -> dict:
    """
    Get the model evaluation results.

    This endpoint calls the perform_model_evaluation function to
    obtain the model evaluation results and returns them as a JSON response.

    Returns:
        dict: A JSON response containing model evaluation results.
    """
    # Call the function to perform model evaluation
    evaluation_results = perform_model_evaluation()

    return evaluation_results
