import requests


def test_return_item(base_url, create_user, create_item):
    user = create_user("Jane Doe", "jane.doe@example.com", "basic")
    item = create_item("The Hobbit", "book")

    requests.post(f"{base_url}/items/{item['item_id']}/borrow", json={
        "user_id": user["user_id"],
        "item_type": "book"
    })

    response = requests.post(f"{base_url}/items/{item['item_id']}/return", json={
        "user_id": user["user_id"]
    })
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    data = response.json()
    assert data["status"] == "available", f"Expected item status 'available' but got {data['status']}"
    assert "return_date" in data, "Response JSON does not contain 'return_date'"


def test_return_item_not_borrowed(base_url, create_user, create_item):
    user = create_user("Test User", "test.user@example.com", "basic")
    item = create_item("Unused Book", "book")

    response = requests.post(f"{base_url}/items/{item['item_id']}/return", json={
        "user_id": user["user_id"]
    })
    assert response.status_code == 400, f"Expected status code 400 for returning not borrowed item but got {response.status_code}"


def test_return_item_invalid_user(base_url, create_item):
    item = create_item("Invalid User Return", "book")

    response = requests.post(f"{base_url}/items/{item['item_id']}/return", json={
        "user_id": "invalid_user_id"
    })
    assert response.status_code == 404, f"Expected status code 404 for invalid user but got {response.status_code}"
