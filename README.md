# ECG Model Inference System for the CPSC2019 challenge

This project is an MLOps system designed for ECG (Electrocardiography) signal analysis, leveraging a machine learning model to predict heart rate and QRS complexes from ECG data. It consists of two main components: a FastAPI backend for model inference and a Streamlit frontend for interactive data visualization and analysis.

## Todo List:

- [x] Deployment (Mandatory): Configure the repository to enable model deployment in
      an environment-agnostic manner. This may involve providing a Dockerfile or Docker
      Compose file and amending the documentation.

- [x] Model Evaluation: Develop code for evaluating model performance using appropriate
      metrics or data visualization techniques.

- [x] API Development: Create a Flask or FastAPI application to expose the machine
      learning model as an API endpoint.
- [x] API Documentation: Generate Swagger documentation for the API.
- [x] Input Validation: Implement input validation for the API endpoint.
- [x] Dashboard: Develop a simple web-based dashboard to display the results of model
      inferences.
- [x] Testing: Write tests to ensure the robustness and reliability of your deployed model.
- [x] Authentication: Implement a method of authentication for accessing the deployed
      model.

## System Overview

- **FastAPI Backend**: Serves as the core API for handling ECG data processing, user authentication, model predictions, and evaluations.
- **Streamlit Frontend**: Provides a user-friendly interface for users to interact with the ECG model, submit ECG files for prediction, and view model evaluation results.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

Ensure Docker and Docker Compose are installed on your system to build and run the application containers.

### Project Structure

```plaintext
project_root/
│
├── app.py                   # FastAPI application
├── Dockerfile               # Dockerfile for FastAPI application
├── docker-compose.yml       # Docker Compose for running the application
├── docker-compose.test.yml  # Docker Compose for running tests
├── test_docker.sh           # Script to execute Docker Compose tests
│
├── streamlit/               # Streamlit application directory
│   ├── Dockerfile           # Dockerfile for Streamlit application
│   │ ...
│   └── ecg_dashboard.py     # Streamlit dashboard application
│ ...
├── data/                    # Directory for ECG data files
├── ref/                    # Directory for Ref data files
└── requirements.txt         # Python dependencies for FastAPI application
```

### Installation & Running

1. **Clone the repository:**

   ```bash
   git clone https://github.com/badrlarhdir/mlops-techtest.git
   cd mlops-techtest
   ```

2. **Build and run the services using Docker Compose:**

   ```bash
   docker-compose up --build
   ```

   This command builds the FastAPI and Streamlit containers and starts them. The FastAPI application will be available at `http://localhost:8000` and the Streamlit dashboard at `http://localhost:8501`.

3. **Running Tests:**

   Execute the `test_docker.sh` script to run the test suite:

   ```bash
   ./test_docker.sh
   ```

   This script uses `docker-compose.test.yml` to run the tests in a containerized environment.

### Usage

- **FastAPI Application**:

  - **Authentication**: Use the `/register` endpoint to create a new user and `/login` to obtain a JWT token.
  - **Prediction**: Submit an ECG file using the `/predict` endpoint for heart rate and QRS complex predictions.
  - **Evaluation**: Access the `/evaluate` endpoint to receive model performance metrics.
  - **Swagger Documentation**: The API documentation, including comprehensive details on endpoints, parameters, and expected responses, is readily accessible through the `http://localhost:8000/docs` endpoint of the API. This Swagger documentation provides an interactive interface for exploring the API's capabilities, facilitating both understanding and integration for developers.

- **Streamlit Dashboard**:
  - Access the dashboard through your web browser at `http://localhost:8501`.
  - Enter your API token (obtained from the FastAPI application).
  - Select an ECG file from the dropdown menu to visualize its data and the model's predictions.

## Streamlit Dashboard:

For a user planning to utilize the ECG Model Inference Dashboard via the web interface, the process is designed to be intuitive and straightforward, focusing on user interaction with the Streamlit dashboard, which is connected to a FastAPI backend for data processing and model inference. Here's a high-level overview tailored for a non-technical audience:

### Getting Started

#### 1. **User Registration and Login:**

- **First-Time Users:** If you're new to the application, you'll begin by registering for an account. This involves providing a username and password, which you'll use for all future logins. This step is necessary for securing access and ensuring that your data and interactions remain private.
- **Returning Users:** If you've already registered, you'll simply log in using your existing credentials. Upon successful login, you'll receive a unique **API token**. Think of this token as a digital key that grants you access to use the application's features.

The process of registering and logging in order to use the ECG Model Inference Dashboard with your token is accomplished through API calls to the FastAPI backend, you can visit the swagger page to do so `http://localhost:8000/docs`

#### 2. **Navigating the Dashboard:**

Here's what you can do:

### Using the Dashboard

#### 1. **Enter Your API Token:**

- At the top of the dashboard, you'll find a field to enter the API token you received when you logged in. This step is crucial as it verifies your identity and authorizes you to request predictions and evaluations from the system.

#### 2. **ECG File Selection for Prediction:**

- The dashboard allows you to analyze ECG signals to predict heart rates and QRS complexes. You'll see a dropdown menu listing available ECG files. These files are part of the application's database and represent different ECG recordings you can analyze.
- Select an ECG file from the dropdown menu to proceed with the analysis.

#### 3. **Model Evaluation (Optional):**

- If you're interested in understanding how well the underlying ECG model performs, there's an option to evaluate the model. This process assesses the model's accuracy and reliability in detecting heart rates and QRS complexes from ECG signals.
- This evaluation can take a few minutes (2-3 minutes), as the system thoroughly checks the model's performance against a set of test data.

### Interacting with Features

#### 1. **Making Predictions:**

- After selecting an ECG file, you can initiate the prediction process. The system will analyze the selected ECG signal and provide you with the predicted heart rate and the detected QRS complexes.
- These predictions are displayed visually, allowing you to see the ECG signal graph and the points where QRS complexes are detected.

#### 2. **Viewing Model Evaluation Results:**

- Should you choose to evaluate the model, the dashboard will display key metrics such as the total number of files analyzed, the accuracy of R-wave detection, and the accuracy of heart rate predictions.
- These results give you insights into the model's performance and reliability.

### Final Notes

- **Privacy and Security:** Remember, your API token is unique to you.
- **Ease of Use:** The dashboard is designed to be user-friendly. Whether you're a medical professional, a researcher, or simply curious about ECG analysis, you can navigate the dashboard and use its features without needing a technical background.

This high-level overview is intended to guide you through the process of using the ECG Model Inference Dashboard, from registration to making predictions and evaluating the model, ensuring a smooth and informative user experience.
