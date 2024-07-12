import requests


def test_add_item(base_url):
    response = requests.post(f"{base_url}/items", json={
        "name": "Madagascar",
        "type": "dvd"
    })
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    data = response.json()
    assert "item_id" in data, "Response JSON does not contain 'item_id'"
    assert data["name"] == "Madagascar", f"Expected name 'Madagascar' but got {data['name']}"
    assert data["type"] == "dvd", f"Expected type 'dvd' but got {data['type']}"


def test_add_item_invalid_type(base_url):
    response = requests.post(f"{base_url}/items", json={
        "name": "Unknown Item",
        "type": "unknown_type"
    })
    assert response.status_code == 400, f"Expected status code 400 for invalid item type but got {response.status_code}"


def test_add_item_duplicate_name(base_url, create_item):
    item = create_item("Harry Potter", "book")
    response = requests.post(f"{base_url}/items", json={
        "name": "Harry Potter",
        "type": "book"
    })
    assert response.status_code == 400, f"Expected status code 400 for duplicate item name but got {response.status_code}"


def test_add_item_missing_fields(base_url):
    response = requests.post(f"{base_url}/items", json={
        "name": "Incomplete Item"
        # Missing type
    })
    assert response.status_code == 400, f"Expected status code 400 for missing fields but got {response.status_code}"
    assert 'type' in response.json().get('errors', {}), "Expected error message for missing type"
