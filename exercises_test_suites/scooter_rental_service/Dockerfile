# Use the official Python image from the Docker Hub
FROM python:3.8

# Install pip and pytest
RUN apt-get update && apt-get install -y python3-pip
RUN pip install pytest requests

# Set the working directory
WORKDIR /scooter_rental_service