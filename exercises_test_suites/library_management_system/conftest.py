import pytest
import requests

BASE_URL = "http://api:5000"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="module")
def create_user(base_url):
    def _create_user(name, email, membership_type):
        response = requests.post(f"{base_url}/users", json={
            "name": name,
            "email": email,
            "membership_type": membership_type
        })
        return response.json()
    return _create_user


@pytest.fixture(scope="module")
def create_item(base_url):
    def _create_item(name, type):
        response = requests.post(f"{base_url}/items", json={
            "name": name,
            "type": type
        })
        return response.json()
    return _create_item
