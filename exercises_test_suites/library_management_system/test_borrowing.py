import requests


def test_borrow_item(base_url, create_user, create_item):
    user = create_user("John Doe", "john.doe@example.com", "student")
    item = create_item("Harry Potter", "book")

    response = requests.post(f"{base_url}/items/{item['item_id']}/borrow", json={
        "user_id": user["user_id"],
        "item_type": "book"
    })
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    data = response.json()
    assert data["status"] == "borrowed", f"Expected item status 'borrowed' but got {data['status']}"
    assert "borrowed_date" in data, "Response JSON does not contain 'borrowed_date'"


def test_borrow_item_exceeds_limit(base_url, create_user, create_item):
    user = create_user("Student User", "student@example.com", "student")
    for i in range(5):
        item = create_item(f"Book {i}", "book")
        requests.post(f"{base_url}/items/{item['item_id']}/borrow", json={
            "user_id": user["user_id"],
            "item_type": "book"
        })

    # Try to borrow one more book, should fail
    extra_item = create_item("Extra Book", "book")
    response = requests.post(f"{base_url}/items/{extra_item['item_id']}/borrow", json={
        "user_id": user["user_id"],
        "item_type": "book"
    })
    assert response.status_code == 400, f"Expected status code 400 for exceeding borrow limit but got {response.status_code}"


def test_borrow_nonexistent_item(base_url, create_user):
    user = create_user("Test User", "test.user@example.com", "basic")
    response = requests.post(f"{base_url}/items/nonexistent/borrow", json={
        "user_id": user["user_id"],
        "item_type": "book"
    })
    assert response.status_code == 404, f"Expected status code 404 for nonexistent item but got {response.status_code}"


def test_borrow_item_already_borrowed(base_url, create_user, create_item):
    user = create_user("User One", "user.one@example.com", "basic")
    item = create_item("Already Borrowed Book", "book")

    # Borrow the item once
    requests.post(f"{base_url}/items/{item['item_id']}/borrow", json={
        "user_id": user["user_id"],
        "item_type": "book"
    })

    # Try to borrow the same item again
    response = requests.post(f"{base_url}/items/{item['item_id']}/borrow", json={
        "user_id": user["user_id"],
        "item_type": "book"
    })
    assert response.status_code == 400, f"Expected status code 400 for already borrowed item but got {response.status_code}"


def test_borrow_item_invalid_user(base_url, create_item):
    item = create_item("Invalid User Borrow", "book")
    response = requests.post(f"{base_url}/items/{item['item_id']}/borrow", json={
        "user_id": "invalid_user_id",
        "item_type": "book"
    })
    assert response.status_code == 404, f"Expected status code 404 for invalid user but got {response.status_code}"
