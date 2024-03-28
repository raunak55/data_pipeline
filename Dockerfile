# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the Python files into the container
COPY data_pipeline/* .

# Expose any ports your app needs
EXPOSE 8000

# Command to run the Python script
CMD ["python", "app.py"]
