# Base image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements_be.txt ./requirements.txt

# install git
RUN apt-get update && apt-get install -y git ffmpeg libsm6 libxext6

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 4000

# Start the server
CMD ["python", "backend.py"]
