import streamlit as st
import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import scipy.io as sio
import os

# FastAPI endpoint URLs
FASTAPI_PREDICT_URL = "http://app:8000/predict"
FASTAPI_EVALUATE_URL = "http://app:8000/evaluate"

# Streamlit title and description
st.title("ECG Model Inference Dashboard")
st.write("Select an ECG file to predict heart rate and QRS complexes.")

# Token input field
token = st.text_input("Enter your API token:", "")

# Dropdown to select files available in the data folder
data_folder = "./data/"  # Update with your data folder path
available_files = [f for f in os.listdir(data_folder) if f.endswith(".mat")]
sorted_files = sorted(available_files)

qrs_complexes = []

# Dropdown for selecting files with search and default selection as None
selected_file = st.selectbox("Select an ECG file:", ["None"] + sorted_files, index=0)


# Function to create headers with token
def create_headers(token):
    return {"Authorization": f"Bearer {token}"} if token else {}


# Button to trigger evaluation
if st.button("Evaluate Model (takes ~2-3 mins)"):
    # Send a POST request to FastAPI for evaluation
    evaluate_response = requests.get(
        FASTAPI_EVALUATE_URL, headers=create_headers(token)
    )

    if evaluate_response.status_code == 200:
        evaluation_result = evaluate_response.json()
        st.subheader("Model Evaluation Results")
        st.write("Total File Number:", evaluation_result["tot_file_number"])
        st.write("R Detection Accuracy:", evaluation_result["rec_acc"])
        st.write("Heart Rate Detection Accuracy:", evaluation_result["hr_acc"])

if selected_file != "None":
    # Create a request payload for FastAPI
    payload = {
        "data_path": data_folder,
        "ecg_file": selected_file,
    }

    # Send a POST request to FastAPI
    response = requests.post(
        FASTAPI_PREDICT_URL, headers=create_headers(token), json=payload
    )

    if response.status_code == 200:
        result = response.json()
        heart_rate = result["hr"]
        qrs_complexes = result["qrs"]

        # Load the ECG data from the selected file
        ecg_data = np.transpose(
            sio.loadmat(os.path.join(data_folder, selected_file))["ecg"]
        )[0]

        # Calculate time values (in seconds) based on the sampling rate of 500 Hz
        time_values = np.arange(len(ecg_data)) / 500.0  # 500 Hz sampling rate

        # Display the ECG signal with axes and title
        st.subheader("ECG Signal")
        fig_ecg, ax_ecg = plt.subplots(figsize=(10, 4))
        ax_ecg.plot(time_values, ecg_data)
        ax_ecg.set_xlabel("Time (s)")
        ax_ecg.set_ylabel("Amplitude (mV)")
        ax_ecg.set_title(f"ECG Signal from {selected_file}")
        ax_ecg.set_xlim(left=0, right=10)  # Set x-axis limits
        # Set x-axis ticks to be every second
        ax_ecg.xaxis.set_major_locator(ticker.MultipleLocator(1))

        st.pyplot(fig_ecg)

        # # Convert QRS complex times from milliseconds to seconds and add the starting time
        # qrs_seconds = [5.5 + qrs / 1000.0 for qrs in qrs_complexes]

        # # Find the y-axis position for the dots: a bit below the maximum amplitude
        # y_max = max(ecg_data)
        # dot_y_position = y_max * 0.60  # 90% of the maximum to be slightly below the top

        # # Plot the QRS complexes on the ECG signal
        # ax_ecg.plot(
        #     qrs_seconds, [dot_y_position] * len(qrs_seconds), "ro"
        # )  # 'ro' for red dots

        # Display results
        st.subheader("Predictions from ECG")
        st.write("Heart Rate:", heart_rate)
        st.write("QRS Complexes:", qrs_complexes)
