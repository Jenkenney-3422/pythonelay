FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create the data file if it doesn't exist and set permissions
# This ensures the app doesn't crash on the first run
RUN touch tasks.json && chmod 666 tasks.json

# Render provides a $PORT environment variable automatically. 
# We use shell form for CMD to allow variable expansion.
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}