import requests


def test_reserve_scooter(create_user, create_scooter, base_url):
    user_id = create_user()
    scooter_id = create_scooter()

    response = requests.post(f"{base_url}/scooters/{scooter_id}/reserve", json={"user_id": user_id})
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    data = response.json()
    assert data["status"] == "reserved", f"Expected status 'reserved' but got {data['status']}"


def test_start_ride(create_user, create_scooter, base_url):
    user_id = create_user()
    scooter_id = create_scooter()

    # Reserve the scooter first
    requests.post(f"{base_url}/scooters/{scooter_id}/reserve", json={"user_id": user_id})

    response = requests.post(f"{base_url}/scooters/{scooter_id}/start", json={"user_id": user_id})
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    data = response.json()
    assert data["status"] == "in_use", f"Expected status 'in_use' but got {data['status']}"


def test_end_ride(create_user, create_scooter, base_url):
    user_id = create_user()
    scooter_id = create_scooter()

    # Reserve and start the scooter first
    requests.post(f"{base_url}/scooters/{scooter_id}/reserve", json={"user_id": user_id})
    requests.post(f"{base_url}/scooters/{scooter_id}/start", json={"user_id": user_id})

    response = requests.post(f"{base_url}/scooters/{scooter_id}/end", json={"user_id": user_id})
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    data = response.json()
    assert data["status"] == "available", f"Expected status 'available' but got {data['status']}"
    assert "duration" in data, "Response JSON does not contain 'duration'"


def test_user_ride_history(create_user, create_scooter, base_url):
    user_id = create_user()
    scooter_id = create_scooter()

    # Reserve, start, and end the scooter ride first
    requests.post(f"{base_url}/scooters/{scooter_id}/reserve", json={"user_id": user_id})
    requests.post(f"{base_url}/scooters/{scooter_id}/start", json={"user_id": user_id})
    requests.post(f"{base_url}/scooters/{scooter_id}/end", json={"user_id": user_id})

    response = requests.get(f"{base_url}/users/{user_id}/history")
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Response JSON is not a list"
    assert len(data) > 0, "Expected at least one ride in the history"
    assert "start_time" in data[0], "Response JSON does not contain 'start_time'"
    assert "end_time" in data[0], "Response JSON does not contain 'end_time'"
    assert "duration" in data[0], "Response JSON does not contain 'duration'"
