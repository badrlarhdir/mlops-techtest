FROM python:3.9-slim

WORKDIR /cpsc2019
COPY ./ .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Run the uvicorn app:app --reload command by default when the container starts.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"] 
