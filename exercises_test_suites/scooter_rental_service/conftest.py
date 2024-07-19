import pytest
import requests

BASE_URL = "http://localhost:5000"  # Replace with the actual base URL of your API

@pytest.fixture(scope="module")
def base_url():
    return BASE_URL

@pytest.fixture
def create_user(base_url):
    def _create_user(name="John Doe", email="john.doe@example.com", membership_type="basic"):
        payload = {
            "name": name,
            "email": email,
            "membership_type": membership_type
        }
        response = requests.post(f"{base_url}/users", json=payload)
        return response.json()["user_id"]
    return _create_user

@pytest.fixture
def create_scooter(base_url):
    def _create_scooter(location="Downtown", status="available"):
        payload = {
            "location": location,
            "status": status
        }
        response = requests.post(f"{base_url}/scooters", json=payload)
        return response.json()["scooter_id"]
    return _create_scooter
