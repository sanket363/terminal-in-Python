# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /terminal-app

# Copy the local requirements.txt file to the container
COPY . .

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r app/requirements.txt

WORKDIR /terminal-app/app

# Set the default command to run your Python script (replace 'script.py' with your actual script name)
CMD ["python", "app/main.py"]

