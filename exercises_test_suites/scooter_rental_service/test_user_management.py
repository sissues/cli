import requests


def test_add_user(base_url):
    response = requests.post(f"{base_url}/users", json={
        "name": "John Doe",
        "email": "john.doe@example.com",
        "membership_type": "basic"
    })
    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"
    data = response.json()
    assert "user_id" in data, "Response JSON does not contain 'user_id'"
    assert data["name"] == "John Doe", f"Expected name 'John Doe' but got {data['name']}"
    assert data["email"] == "john.doe@example.com", f"Expected email 'john.doe@example.com' but got {data['email']}"
    assert data["membership_type"] == "basic", f"Expected membership type 'basic' but got {data['membership_type']}"


def test_add_user_invalid_membership(base_url):
    response = requests.post(f"{base_url}/users", json={
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "membership_type": "invalid_type"
    })
    assert response.status_code == 400, f"Expected status code 400 for invalid membership type but got {response.status_code}"


def test_add_user_duplicate_email(base_url, create_user):
    user_id = create_user("Alice", "alice@example.com", "basic")
    response = requests.post(f"{base_url}/users", json={
        "name": "Alice Clone",
        "email": "alice@example.com",
        "membership_type": "basic"
    })
    assert response.status_code == 400, f"Expected status code 400 for duplicate email but got {response.status_code}"


def test_add_user_missing_fields(base_url):
    response = requests.post(f"{base_url}/users", json={
        "name": "Incomplete User"
        # Missing email and membership_type
    })
    assert response.status_code == 400, f"Expected status code 400 for missing"