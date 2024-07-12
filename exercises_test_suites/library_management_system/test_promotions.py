import requests


def test_promotion_eligibility(base_url, create_user, create_item):
    user = create_user("Chris Lee", "chris.lee@example.com", "student")

    for _ in range(15):
        item = create_item("Book {}".format(_), "book")
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
    assert len(data) >= 15, "Expected at least 15 borrowing records to be eligible for promotion"

    # Simulate checking the eligibility for promotion
    eligible = len([entry for entry in data if entry["item_type"] == "book"]) >= 15
    assert eligible is True, "User should be eligible for promotion but was not"


def test_promotion_ineligibility(base_url, create_user, create_item):
    user = create_user("Promotion Test User", "promotion.test.user@example.com", "basic")

    for _ in range(10):
        item = create_item("Book {}".format(_), "book")
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
    assert len(data) < 15, "Expected fewer than 15 borrowing records, but found more"

    # Simulate checking the eligibility for promotion
    eligible = len([entry for entry in data if entry["item_type"] == "book"]) >= 15
    assert eligible is False, "User should not be eligible for promotion but was"


def test_promotion_invalid_user(base_url):
    response = requests.get(f"{base_url}/users/invalid_user_id/promotion")
    assert response.status_code == 404, f"Expected status code 404 for invalid user but got {response.status_code}"
