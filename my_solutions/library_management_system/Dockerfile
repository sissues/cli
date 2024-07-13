# Use the official Python image from the Docker Hub
FROM python:3.8

# Set the working directory
WORKDIR /library_management_system

RUN pip install flask

# Copy the rest of the application code into the container
COPY src/ .

EXPOSE 5000

# Run the Flask app
# CMD ["flask", "run"]
CMD ["python", "app.py"]