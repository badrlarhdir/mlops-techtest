# Use an official Python image as a parent image
FROM python:3.9-slim

# Set the working directory to /streamlit
WORKDIR /streamlit
COPY ./streamlit .
COPY data ./data

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8501 for Streamlit
EXPOSE 8501

# Define the command to run your Streamlit app
CMD ["streamlit", "run", "ecg_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
