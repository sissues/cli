import requests


def test_borrowing_history(base_url, create_user, create_item):
    user = create_user("Alex Smith", "alex.smith@example.com", "premium")
    item = create_item("1984", "book")

    requests.post(f"{base_url}/items/{item['item_id']}/borrow", json={
        "user_id": user["user_id"],
        "item_type": "book"
    })

    requests.post(f"{base_url}/items/{item['item_id']}/return", json={
        "user_id": user["user_id"]
    })

    response = requests.get(f"{base_url}/users/{user['user_id']}/history")
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    data = response.json()
    assert len(data) > 0, "Expected at least one borrowing history record"
    assert "borrowed_date" in data[0], "Borrowing history record does not contain 'borrowed_date'"
    assert "returned_date" in data[0], "Borrowing history record does not contain 'returned_date'"


def test_borrowing_history_no_history(base_url, create_user):
    user = create_user("History Test User", "history.test.user@example.com", "basic")

    response = requests.get(f"{base_url}/users/{user['user_id']}/history")
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    data = response.json()
    assert len(data) == 0, "Expected no borrowing history but found some records"


def test_borrowing_history_invalid_user(base_url):
    response = requests.get(f"{base_url}/users/invalid_user_id/history")
    assert response.status_code == 404, f"Expected status code 404 for invalid user but got {response.status_code}"
