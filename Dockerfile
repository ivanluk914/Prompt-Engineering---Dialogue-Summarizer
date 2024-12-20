FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./templates ./templates

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY ./app.py .

# Expose the port that Flask runs on
EXPOSE 5001

# Start the Gunicorn server
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "--timeout", "120", "app:app"]